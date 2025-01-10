import typing as tp
from collections import defaultdict
from datetime import datetime
from decimal import Decimal

from .exceptions import SplitViseException
from .models import User, Expense, Trip, Debt, Event, Summary
from .models.base import Session

MoneyType = Decimal


def create_user(
        username: str,
        *,
        session: Session
) -> User:
    """
    Create new User; validate user exists
    :param username: username to create
    :param session: active session to perform operations with
    :return: orm User object
    :exception: username already taken
    """

    if session.query(User).filter(User.username == username).first():
        raise SplitViseException("username already taken")

    user = User(username=username)

    session.add(user)
    session.commit()

    return user


def create_event(
        trip_id: int,
        people_debt: tp.Mapping[int, MoneyType],
        people_payment: tp.Mapping[int, MoneyType],
        title: str,
        *,
        session: Session
) -> Event:
    """
    Create Event in database, automatically creates Debts and Expenses; validates sum
    :param trip_id: Trip.trip_id from the database
    :param people_debt: mapping of User.user_id to theirs debt in that event
    :param people_payment: mapping of User.user_id to theirs payments in that event
    :param title: title of the event
    :param session: active session to perform operations with
    :return: orm Event object
    :exception: Trip not found by id, Can not create debt for user not in trip,
                Can not create payment for user not in trip, Sum of debts and sum of payments are not equal
    """

    trip = session.get(Trip, trip_id)

    if not trip:
        raise SplitViseException("Trip not found by id")

    user_ids = set([user.user_id for user in trip.users])
    missing_debt_users = set(people_debt.keys()) - user_ids
    missing_payment_users = set(people_payment.keys()) - user_ids

    if missing_debt_users:
        raise SplitViseException(f"Can not create debt for users not in trip: {missing_debt_users}")
    if missing_payment_users:
        raise SplitViseException(f"Can not create payment for users not in trip: {missing_payment_users}")
    if sum(people_debt.values()) != sum(people_payment.values()):
        raise SplitViseException("Sum of debts and sum of payments are not equal")

    event = Event(trip_id=trip_id, title=title, happened_datetime=datetime.now())
    session.add(event)
    session.commit()

    for (payer_id, pay_value) in people_payment.items():
        payment = Expense(event_id=event.event_id, payer_id=payer_id, value=pay_value)
        session.add(payment)
        session.commit()

    for (debtor_id, debt_value) in people_debt.items():
        debt = Debt(event_id=event.event_id, debtor_id=debtor_id, value=debt_value)
        session.add(debt)
        session.commit()

    return event


def create_trip(
        creator_id: int,
        title: str,
        description: str,
        *,
        session: Session
) -> Trip:
    """
    Create Trip. Automatically add creator to the trip. Validate input: the title should not be empty and the creator
    should exist in the users table
    :param creator_id: User.user_id from the database to create trip by
    :param title: Title of the trip
    :param description: Long (or not so long) description of the trip
    :param session: active session to perform operations with
    :return: orm Trip object
    :exception: Title of a trip should not be empty, User not found by id
    """
    if not title:
        raise SplitViseException("Title is empty")
    if not session.get(User, creator_id):
        raise SplitViseException("Creator not found")

    trip = Trip(title=title, description=description, created_timestamp=datetime.now())
    session.add(trip)
    session.commit()
    add_user_to_trip(guest_id=creator_id, trip_id=trip.trip_id, session=session)

    return trip


def add_user_to_trip(
        guest_id: int,
        trip_id: int,
        *,
        session: Session
) -> None:
    """
    Mark that the user with guest_id takes part in the trip. Check that the user and the trip do exist and the user has
    not been added to the trip yet.
    :param guest_id: User.user_id from the database to add to the trip
    :param trip_id: Trip.trip_id from the database
    :param session: active session to perform operations with
    :return: None
    :exception: Trip not found by id, User already in trip
    """

    guest = session.get(User, guest_id)
    trip = session.get(Trip, trip_id)

    if not guest:
        raise SplitViseException("User does not exist")
    if not trip:
        raise SplitViseException("Trip does not exist")

    user_ids = set([user.user_id for user in trip.users])

    if guest_id in user_ids:
        raise SplitViseException("User already in trip")

    trip.users.append(guest)
    session.commit()


def get_trip_users(
        trip_id: int,
        *,
        session: Session
) -> list[User]:
    """
    Get Users from Trip; validate Trip exists
    :param trip_id: Trip.trip_id from the database
    :param session: active session to perform operations with
    :return: list of orm User objects
    :exception: Trip not found by id
    """
    trip = session.get(Trip, trip_id)

    if not trip:
        raise SplitViseException("Trip does not exist")

    return trip.users


def make_summary(
        trip_id: int,
        *,
        session: Session
) -> None:
    """
    Make trip summary. Mark all the events of the trip as settled up. Validate at least the existence of the trip
    being calculated
    :param trip_id: Trip.trip_id from the database
    :param session: active session to perform operations with
    :return: None
    :exception: Trip not found by id
    """

    if not session.get(Trip, trip_id):
        raise SplitViseException("Trip does not exist")

    sum_stats: tp.Mapping[int, MoneyType] = defaultdict(MoneyType)

    for event in session.query(Event).filter(Event.trip_id == trip_id).all():
        event.settled_up = True
        expenses = session.query(Expense).filter(Expense.event_id == event.event_id)
        debts = session.query(Debt).filter(Debt.event_id == event.event_id)
        for expense in expenses:
            sum_stats[expense.payer_id] += expense.value
        for debt in debts:
            sum_stats[debt.debtor_id] -= debt.value

    if sum(sum_stats.values()) != 0:
        raise SplitViseException("The summary does not add up")

    total_stats: tp.List[tuple[MoneyType, int]] = [(user_sum[1], user_sum[0]) for user_sum in sum_stats.items() if
                                                   user_sum[1] != 0]
    total_stats.sort()

    left = 0
    right = len(total_stats) - 1
    while left < right:
        (debt_value, debtor_id) = total_stats[left]
        (pay_value, payer_id) = total_stats[right]
        transfer_sum = max(-pay_value, debt_value)
        session.add(Summary(trip_id=trip_id, user_from_id=debtor_id, user_to_id=payer_id, value=transfer_sum))
        if pay_value + transfer_sum == 0:
            right -= 1
        else:
            left += 1
    session.commit()

from sqlalchemy import Column, Integer, ForeignKey, Numeric

from .base import Base


class Expense(Base):  # type: ignore
    __tablename__ = 'expenses'

    expense_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('trips.trip_id'))
    payer_id = Column(Integer, ForeignKey('users.user_id'))
    value = Column(Numeric)

    def __repr__(self) -> str:
        return f'<Event expense_id={self.expense_id}, payer_id={self.payer_id}, value={self.value}>'

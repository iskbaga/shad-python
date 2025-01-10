from queue import Queue
from abc import ABC, abstractmethod
from typing import Generator, Any
from math import inf


class SystemCall(ABC):
    """SystemCall yielded by Task to handle with Scheduler"""

    @abstractmethod
    def handle(self, scheduler: 'Scheduler', task: 'Task') -> bool:
        """
        :param scheduler: link to scheduler to manipulate with active tasks
        :param task: task which requested the system call
        :return: an indication that the task must be scheduled again
        """


Coroutine = Generator[SystemCall | None, Any, None]


class Task:
    def __init__(self, task_id: int, target: Coroutine) -> None:
        """
        :param task_id: id of the task
        :param target: coroutine to run. Coroutine can produce system calls.
        System calls are being executed by scheduler and the result sends back to coroutine.
        """
        self.id: int = task_id
        self.wait: bool = False
        self.target: Coroutine = target
        self._last: Any = None

    def set_syscall_result(self, result: Any) -> None:
        """
        Saves result of the last system call
        """
        self._last = result

    def step(self) -> SystemCall | None:
        """
        Performs one step of coroutine, i.e. sends result of last system call
        to coroutine (generator), gets yielded value and returns it.
        """
        return self.target.send(self._last)


class Scheduler:
    """Scheduler to manipulate with tasks"""

    def __init__(self) -> None:
        self.task_id = 0
        self.task_queue: Queue[Task] = Queue()
        self.task_map: dict[int, Task] = {}  # task_id -> task
        self.wait_map: dict[int, list[Task]] = {}  # task_id -> list of waiting tasks

    def _schedule_task(self, task: Task) -> None:
        """
        Add task into task queue
        :param task: task to schedule for execution
        """
        self.task_queue.put(task)

    def new(self, target: Coroutine) -> int:
        """
        Create and schedule new task
        :param target: coroutine to wrap in task
        :return: id of newly created task
        """
        self.task_id += 1
        new: 'Task' = Task(self.task_id, target)

        self.task_map[self.task_id] = new
        self._schedule_task(new)
        return self.task_id

    def exit_task(self, task_id: int) -> bool:
        """
        PRIVATE API: can be used only from scheduler itself or system calls
        Hint: do not forget to reschedule waiting tasks
        :param task_id: task to remove from scheduler
        :return: true if task id is valid
        """
        if task_id not in self.task_map.keys():
            return False

        self.task_map[task_id].target.close()
        del self.task_map[task_id]

        if task_id in self.wait_map.keys():
            for waiting in self.wait_map[task_id]:
                self._schedule_task(waiting)
                waiting.wait = False
            del self.wait_map[task_id]

        return True

    def wait_task(self, task_id: int, wait_id: int) -> bool:
        """
        PRIVATE API: can be used only from scheduler itself or system calls
        :param task_id: task to hold on until another task is finished
        :param wait_id: id of the other task to wait for
        :return: true if task and wait ids are valid task ids
        """
        if task_id and wait_id in self.task_map.keys():
            self.wait_map[wait_id] = [self.task_map[task_id]]
            return True
        return False

    @staticmethod
    def _range_for_none(maxx: int | float) -> Generator[int, Any, None]:
        n = 0
        while n < maxx:
            yield n
            n += 1

    def run(self, ticks: int | None = None) -> None:
        """
        Executes tasks consequently, gets yielded system calls,
        handles them and reschedules task if needed
        :param ticks: number of iterations (task steps), infinite if not passed
        """

        try:
            for _ in self._range_for_none(ticks if ticks is not None else +inf):
                task: 'Task' = self.task_queue.get()
                if not task.wait:
                    try:
                        call = task.step()
                        if call is not None:
                            call.handle(self, task)
                    except StopIteration:
                        self.exit_task(task.id)
                    self.task_queue.put(task)
        except KeyboardInterrupt:
            return

    def empty(self) -> bool:
        """Checks if there are some scheduled tasks"""
        return not bool(self.task_map)


class GetTid(SystemCall):
    """System call to get current task id"""

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        task.set_syscall_result(task.id)
        return True


class NewTask(SystemCall):
    """System call to create new task from target coroutine"""

    def __init__(self, target: Coroutine) -> None:
        self.target = target

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        task.set_syscall_result(scheduler.new(self.target))
        return True


class KillTask(SystemCall):
    """System call to kill task with particular task id"""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        scheduler.exit_task(self.task_id)
        return True


class WaitTask(SystemCall):
    """System call to wait task with particular task id"""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        # Note: One shouldn't reschedule task which is waiting for another one.
        # But one must reschedule task if task id to wait for is invalid.
        if scheduler.wait_task(task.id, self.task_id):
            task.set_syscall_result(True)
            task.wait = True
        return task.wait

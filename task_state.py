from aiogram.dispatcher.filters.state import StatesGroup, State


class TaskState(StatesGroup):
    task = State()

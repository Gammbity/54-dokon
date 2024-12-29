from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    login = State()
    phone = State()
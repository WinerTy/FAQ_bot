from aiogram.fsm.state import State, StatesGroup


class MenuState(StatesGroup):
    in_main_menu = State()
    in_submenu = State()

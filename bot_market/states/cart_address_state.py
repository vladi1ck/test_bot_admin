from aiogram.fsm.state import StatesGroup, State


class AddressState(StatesGroup):
    waiting_for_city = State()
    waiting_for_street = State()
    waiting_for_house = State()
    waiting_for_apartment = State()
    waiting_for_confirm = State()

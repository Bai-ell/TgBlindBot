from aiogram.filters.callback_data import CallbackData

class MyCallbackData(CallbackData, prefix='action'):
    action: str
    value: int


class GiftCallbackData(CallbackData, prefix='gift'):
    gift_id: int
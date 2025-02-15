from delivery.delivery_strategy import DeliveryStrategy
from delivery.telegram_delivery_strategy import TelegramDeliveryStrategy
from delivery.dummy_delivery_strategy import DummyDeliveryStrategy


class DeliveryStrategyFactory:
    @staticmethod
    def create_delivery_strategy(delivery_type: str, chat_id: str) -> DeliveryStrategy:
        if delivery_type == "telegram":
            return TelegramDeliveryStrategy(chat_id)
        elif delivery_type == "dummy":
            return DummyDeliveryStrategy()
        else:
            raise Exception(f"Delivery type {delivery_type} not supported")

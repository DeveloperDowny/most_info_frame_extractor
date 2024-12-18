from delivery.delivery_strategy import DeliveryStrategy
from delivery.telegram_delivery_strategy import TelegramDeliveryStrategy


class DeliveryStrategyFactory:
    @staticmethod
    def create_delivery_strategy(delivery_type: str, chat_id: str) -> DeliveryStrategy:
        if delivery_type == "telegram":
            return TelegramDeliveryStrategy(chat_id)
        else:
            raise Exception(f"Delivery type {delivery_type} not supported")

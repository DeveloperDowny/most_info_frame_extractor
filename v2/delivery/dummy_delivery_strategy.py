from delivery.delivery_strategy import DeliveryStrategy

class DummyDeliveryStrategy(DeliveryStrategy):
    def __init__(self):
        pass

    def deliver(self, pdf_url: str, caption: str) -> None:
        print(f"Delivering to {pdf_url} with caption {caption}")
        pass
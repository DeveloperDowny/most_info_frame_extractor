from typing import Any

from ytvideo2pdf.extraction_strategy.base_extraction_strategy import (
    BaseExtractionStrategy,
)
from ytvideo2pdf.extraction_strategy.k_transactions_extraction_strategy import (
    KTransactionsExtractionStrategy,
)
from ytvideo2pdf.extraction_strategy.key_moments_extraction_strategy import (
    KeyMomentsExtractionStrategy,
)
from ytvideo2pdf.extraction_strategy.prominent_peak_extraction_strategy import (
    ProminentPeakExtractionStrategy,
)
from ytvideo2pdf.extraction_strategy.timestamp_extraction_strategy import (
    TimestampExtractionStrategy,
)


class ExtractionStrategyFactory:
    """Factory class for creating extraction strategy objects."""

    STRATEGIES = {
        "k_transactions": KTransactionsExtractionStrategy,
        "key_moments": KeyMomentsExtractionStrategy,
        "timestamps": TimestampExtractionStrategy,
        "prominent_peaks": ProminentPeakExtractionStrategy,
    }

    @classmethod
    def create_extraction_strategy(
            cls, extraction_type: str, **kwargs: Any
    ) -> BaseExtractionStrategy:
        """
        Create an extraction strategy based on the specified type and parameters.

        Args:
            extraction_type: The type of extraction strategy to create
            **kwargs: Additional parameters for the extraction strategy

        Returns:
            An instance of the requested extraction strategy

        Raises:
            ValueError: If the extraction type is invalid
        """
        if extraction_type not in cls.STRATEGIES:
            valid_types = ", ".join(cls.STRATEGIES.keys())
            raise ValueError(
                f"Invalid extraction type: '{extraction_type}'. "
                f"Valid types are: {valid_types}"
            )

        strategy_class = cls.STRATEGIES[extraction_type]

        # Handle the special case for TimestampExtractionStrategy
        if extraction_type == "timestamps":
            timestamps = kwargs.get("timestamps")
            if timestamps is None:
                raise ValueError(
                    "Timestamps must be provided for timestamp extraction strategy"
                )
            return strategy_class(timestamps)

        return strategy_class()

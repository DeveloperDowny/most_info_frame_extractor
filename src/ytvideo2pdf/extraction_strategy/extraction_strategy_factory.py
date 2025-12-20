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
from ytvideo2pdf.extraction_strategy.rate_change_threshold_strategy import (
    RateChangeThresholdStrategy,
)
from ytvideo2pdf.enums import ExtractionType


class ExtractionStrategyFactory:
    """Factory class for creating extraction strategy objects."""

    STRATEGIES = {
        ExtractionType.K_TRANSACTIONS: KTransactionsExtractionStrategy,
        ExtractionType.KEY_MOMENTS: KeyMomentsExtractionStrategy,
        ExtractionType.TIMESTAMPS: TimestampExtractionStrategy,
        ExtractionType.PROMINENT_PEAKS: ProminentPeakExtractionStrategy,
        ExtractionType.RATE_CHANGE_THRESHOLD: RateChangeThresholdStrategy,
    }

    @classmethod
    def create_extraction_strategy(
        cls, extraction_type: str | ExtractionType, **kwargs: Any
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
        try:
            extraction_type = ExtractionType(extraction_type)
        except ValueError:
            possible_types = [et.value for et in ExtractionType]
            raise ValueError(
                f"Invalid extraction type: '{extraction_type}'. "
                f"Valid types are: {', '.join(possible_types)}"
            )

        if extraction_type not in cls.STRATEGIES:
            valid_types = ", ".join(cls.STRATEGIES.keys())
            raise ValueError(
                f"Invalid extraction type: '{extraction_type}'. "
                f"Valid types are: {valid_types}"
            )

        strategy_class = cls.STRATEGIES[extraction_type]
        return strategy_class(**kwargs)

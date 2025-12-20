from ytvideo2pdf.enums import OCRApprovalType
from ytvideo2pdf.ocr_approval.approve_all import ApproveAllApprovalStrategy
from ytvideo2pdf.ocr_approval.base import OCRApprovalStrategy
from ytvideo2pdf.ocr_approval.phash import PHash
from ytvideo2pdf.ocr_approval.pixel_comparison import (
    PixelComparison,
)
from ytvideo2pdf.ocr_approval.reject_all import RejectAllApprovalStrategy


class OCRApprovalStrategyFactory:
    @staticmethod
    def create_strategy(approval_type: str | OCRApprovalType) -> OCRApprovalStrategy:
        approval_type = OCRApprovalType(approval_type)
        creators = {
            OCRApprovalType.PIXEL_COMPARISON: PixelComparison,
            OCRApprovalType.APPROVE_ALL: ApproveAllApprovalStrategy,
            OCRApprovalType.REJECT_ALL: RejectAllApprovalStrategy,
            OCRApprovalType.PHASH: PHash,
        }
        if approval_type in creators:
            return creators[approval_type]()
        else:
            raise ValueError(f"Invalid OCR approval strategy: {approval_type}")

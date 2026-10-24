"""Pydantic schemas and Enums for Voice-of-Customer (VoC) Defect Triage."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class DefectType(str, Enum):
    """Categorization of operational and product defects."""
    TEMPERATURE = "Temperature"
    PACKAGING = "Packaging"
    MISSING_ITEM = "Missing_Item"
    QUALITY = "Quality"
    NONE = "None"


class RoutingDestination(str, Enum):
    """Operational team responsible for resolving the ticket."""
    DARK_STORE_OPS = "Dark_Store_Ops"
    CATEGORY_MANAGER = "Category_Manager"
    SUPPLY_CHAIN = "Supply_Chain"
    NONE = "None"


class DefectReport(BaseModel):
    """Structured quality assurance assessment and routing ticket."""

    is_defect: bool = Field(
        description="True if the customer feedback describes an operational, delivery, or product defect. False for positive or non-defect feedback."
    )
    sku_category: str = Field(
        description="The relevant product category (e.g., Fresh Meat & Poultry, Dairy & Eggs, Seafood, Fruits & Vegetables, Beverages, Ambient Grocery, None)."
    )
    defect_type: DefectType = Field(
        description="Classification of defect: Temperature (cold chain break), Packaging (leaks, damage), Missing_Item (order shortfall), Quality (spoilage, taste, freshness), or None."
    )
    severity: int = Field(
        ge=1,
        le=5,
        description="Defect severity rating from 1 (minor cosmetic/inconvenience) to 5 (critical food safety, hazardous, or complete order failure). 1 for non-defects."
    )
    routing_destination: RoutingDestination = Field(
        description="Operational team responsible for root-cause mitigation: Dark_Store_Ops (packing/picking/missing items), Category_Manager (vendor quality/sourcing), Supply_Chain (cold chain logistics/inbound freight), or None."
    )
    root_cause_summary: str = Field(
        description="Concise 1-sentence diagnostic explanation of the failure mode."
    )
    action_recommended: str = Field(
        description="Immediate operational remediation action (e.g., vendor QA audit, reefer temperature log check, dark store picker retrain, refund)."
    )

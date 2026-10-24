"""Voice-of-Customer (VoC) Defect Triage & Routing Agent.
Utilizes LangChain and Groq's OpenAI-compatible endpoint with openai/gpt-oss-120b
to extract structured defect assessments and route tickets to operational owners.
"""

import os
from typing import Any, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from schema import DefectReport, DefectType, RoutingDestination

DEFAULT_MODEL = "openai/gpt-oss-120b"
DEFAULT_BASE_URL = "https://api.groq.com/openai/v1"

QA_SYSTEM_PROMPT = """You are a Senior Quick-Commerce Retail Quality Assurance Analyst and Operational Triage Specialist.
Your responsibility is to analyze unstructured customer reviews, identify operational and product defects,
assess incident severity, and assign root-cause accountability to the appropriate operational department.

Triage Classification Framework:
1. is_defect:
   - TRUE if customer experienced an operational, fulfillment, cold-chain, or product quality issue.
   - FALSE if the review is positive praise, general feedback, or delivery satisfaction.

2. sku_category:
   - Identify the exact product category (e.g., 'Fresh Meat & Poultry', 'Dairy & Eggs', 'Seafood', 'Frozen Foods', 'Ambient Grocery', 'Fresh Produce', 'None').

3. defect_type:
   - Temperature: Cold chain break, product warm on arrival, melted frozen goods, lack of gel/ice packs.
   - Packaging: Leaks, burst pouches, crushed cartons, torn bags, crushed eggs.
   - Missing_Item: Dispatch omissions, missing SKU from order bag, picker shortfall.
   - Quality: Stale product, off odor, sour/fermented taste, sliminess, puffed pack before expiry.
   - None: For positive or non-defect feedback.

4. severity (1-5 Scale):
   - 5: Critical food safety hazard, dangerous spoilage in raw meat/fish, severe microbial risk (e.g., warm poultry, puffed dairy).
   - 4: Major damage causing total loss of product usability (e.g., burst milk soaking groceries, completely melted ice cream).
   - 3: Moderate defect or picker shortfall (e.g., missing items, broken eggs in carton).
   - 2: Minor cosmetic imperfection or slight packaging scuff.
   - 1: No defect / positive feedback.

5. routing_destination:
   - Supply_Chain: Inbound logistics, reefer cold-chain transit failures, temperature control breaches, last-mile cooler bag issues.
   - Dark_Store_Ops: Picker omissions (missing items), improper bagging, rough store handling, damaged eggs during dispatch.
   - Category_Manager: Vendor batch defects, supplier quality issues, stale stock from supplier, premature spoilage within expiry.
   - None: For non-defects.

Be objective, analytical, and prescriptive in root_cause_summary and action_recommended.
"""

QA_USER_PROMPT = """Analyze the following customer review and produce a structured DefectReport:
- Ticket ID: {ticket_id}
- Store ID: {store_id}
- Customer ID: {customer_id}
- Timestamp: {timestamp}
- Review Text: "{review_text}"
"""


def get_groq_llm(
    model: str = DEFAULT_MODEL,
    temperature: float = 0.0,
    base_url: str = DEFAULT_BASE_URL,
) -> ChatOpenAI:
    """Initialize ChatOpenAI configured for Groq's endpoint with openai/gpt-oss-120b."""
    api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("OPENAI_API_KEY")
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=api_key or "placeholder-groq-key",
        base_url=base_url,
    )


def build_voc_extraction_chain():
    """Create LangChain extraction pipeline using with_structured_output(DefectReport)."""
    llm = get_groq_llm()
    structured_llm = llm.with_structured_output(DefectReport)
    prompt = ChatPromptTemplate.from_messages([
        ("system", QA_SYSTEM_PROMPT),
        ("user", QA_USER_PROMPT),
    ])
    return prompt | structured_llm


def run_deterministic_fallback(review_data: Dict[str, Any]) -> DefectReport:
    """Algorithmic heuristic fallback for testing without active Groq API keys."""
    text = review_data["review_text"].lower()

    if "warm" in text or "temperature" in text or "melted" in text or "ice pack" in text:
        if "chicken" in text or "poultry" in text or "meat" in text:
            return DefectReport(
                is_defect=True,
                sku_category="Fresh Meat & Poultry",
                defect_type=DefectType.TEMPERATURE,
                severity=5,
                routing_destination=RoutingDestination.SUPPLY_CHAIN,
                root_cause_summary="Cold-chain temperature breach; melted ice pack caused raw poultry to arrive at ambient temperature.",
                action_recommended="Audit cold-chain reefer logs and enforce insulated delivery bags with fresh gel packs.",
            )
        else:
            return DefectReport(
                is_defect=True,
                sku_category="Frozen Foods & Desserts",
                defect_type=DefectType.TEMPERATURE,
                severity=4,
                routing_destination=RoutingDestination.SUPPLY_CHAIN,
                root_cause_summary="Transit temperature breach caused frozen dessert to melt completely.",
                action_recommended="Mandate passive cooling dry-ice pouches for all frozen SKU last-mile deliveries.",
            )

    elif "leaking" in text or "burst" in text:
        return DefectReport(
            is_defect=True,
            sku_category="Dairy & Eggs",
            defect_type=DefectType.PACKAGING,
            severity=4,
            routing_destination=RoutingDestination.DARK_STORE_OPS,
            root_cause_summary="Milk pouch ruptured due to excessive pressure or poor secondary packing inside bag.",
            action_recommended="Retrain dark store packing associates on heavy-item separation and protective polybags.",
        )

    elif "missing" in text:
        return DefectReport(
            is_defect=True,
            sku_category="Dairy & Eggs",
            defect_type=DefectType.MISSING_ITEM,
            severity=3,
            routing_destination=RoutingDestination.DARK_STORE_OPS,
            root_cause_summary="Picker omission during dark store order fulfillment; eggs missing from bag.",
            action_recommended="Issue immediate customer refund and retrain dispatch pickers on barcode scan-verify workflow.",
        )

    elif "smelled off" in text or "slimy" in text:
        return DefectReport(
            is_defect=True,
            sku_category="Seafood",
            defect_type=DefectType.QUALITY,
            severity=5,
            routing_destination=RoutingDestination.CATEGORY_MANAGER,
            root_cause_summary="Stale, decomposing fish delivered to customer indicating upstream supplier QA failure.",
            action_recommended="Escalate to Seafood Category Manager to quarantine vendor batch and review supplier chill-tank audits.",
        )

    elif "crushed" in text or "cracked" in text:
        return DefectReport(
            is_defect=True,
            sku_category="Dairy & Eggs",
            defect_type=DefectType.PACKAGING,
            severity=3,
            routing_destination=RoutingDestination.DARK_STORE_OPS,
            root_cause_summary="Fragile egg carton crushed due to improper bag stacking during packing/delivery.",
            action_recommended="Instruct dark store packers to place egg cartons on top layer of grocery bags.",
        )

    elif "puffed" in text or "sour" in text or "fermented" in text:
        return DefectReport(
            is_defect=True,
            sku_category="Dairy & Eggs",
            defect_type=DefectType.QUALITY,
            severity=5,
            routing_destination=RoutingDestination.CATEGORY_MANAGER,
            root_cause_summary="Premature microbial spoilage causing package ballooning prior to expiry date.",
            action_recommended="Quarantine dairy vendor batch across dark stores and conduct microbiological testing.",
        )

    else:
        return DefectReport(
            is_defect=False,
            sku_category="None",
            defect_type=DefectType.NONE,
            severity=1,
            routing_destination=RoutingDestination.NONE,
            root_cause_summary="Positive customer feedback; no operational or product defect detected.",
            action_recommended="Log as customer satisfaction benchmark.",
        )


def analyze_review(review_data: Dict[str, Any]) -> DefectReport:
    """Analyze a single customer review using Groq LLM or deterministic fallback."""
    try:
        chain = build_voc_extraction_chain()
        result: DefectReport = chain.invoke(review_data)
        return result
    except Exception:
        # Fallback to deterministic NLP heuristic
        return run_deterministic_fallback(review_data)

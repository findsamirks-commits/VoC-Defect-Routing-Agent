"""Synthetic Voice-of-Customer (VoC) feedback dataset for quick-commerce retail.
Provides realistic customer reviews across ambient grocery, dairy, poultry, seafood,
and cold-chain categories with operational ticket metadata.
"""

from typing import Any, Dict, List
import pandas as pd

SYNTHETIC_REVIEWS: List[Dict[str, Any]] = [
    {
        "ticket_id": "TKT-801",
        "store_id": "DS-BLR-KORAMANGALA-04",
        "customer_id": "CUST-9102",
        "timestamp": "2026-10-24 18:42:15",
        "review_text": "The skinless chicken curry cut was warm on arrival! The ice pack had completely melted and the poultry felt room temperature. Dangerous to consume.",
    },
    {
        "ticket_id": "TKT-802",
        "store_id": "DS-MUM-ANDHERI-02",
        "customer_id": "CUST-4411",
        "timestamp": "2026-10-24 19:15:30",
        "review_text": "Milk pouch was leaking all over the grocery bag! The entire packet burst inside the paper bag and soaked the bread and biscuits.",
    },
    {
        "ticket_id": "TKT-803",
        "store_id": "DS-BLR-INDIRANAGAR-01",
        "customer_id": "CUST-6729",
        "timestamp": "2026-10-24 19:30:10",
        "review_text": "Super fast delivery in just 8 minutes! Fresh coriander and mint leaves were crisp and vibrant. Delivery partner was polite.",
    },
    {
        "ticket_id": "TKT-804",
        "store_id": "DS-DEL-SAKET-03",
        "customer_id": "CUST-3812",
        "timestamp": "2026-10-24 20:05:44",
        "review_text": "Missing items in my Zepto delivery! I ordered 2 packs of Amul butter and 1 box of eggs, but only the butter was in the bag. Charged for full order.",
    },
    {
        "ticket_id": "TKT-805",
        "store_id": "DS-HYD-HITECH-05",
        "customer_id": "CUST-5510",
        "timestamp": "2026-10-24 20:22:00",
        "review_text": "Catla fish smelled off and the flesh was slimy when opened. This is clearly stale batch from your fish supplier.",
    },
    {
        "ticket_id": "TKT-806",
        "store_id": "DS-BLR-WHITEFIELD-07",
        "customer_id": "CUST-2234",
        "timestamp": "2026-10-24 20:45:12",
        "review_text": "Belgian chocolate tub was completely melted into liquid soup. Dark store driver did not carry an insulated cooler bag.",
    },
    {
        "ticket_id": "TKT-807",
        "store_id": "DS-PUN-KALYANI-01",
        "customer_id": "CUST-7789",
        "timestamp": "2026-10-24 21:10:05",
        "review_text": "Avocados and bananas were in perfect ripe condition. Loved the packaging and quick delivery time.",
    },
    {
        "ticket_id": "TKT-808",
        "store_id": "DS-DEL-GURGAON-02",
        "customer_id": "CUST-1923",
        "timestamp": "2026-10-24 21:28:40",
        "review_text": "Carton of 6 brown eggs arrived crushed and cracked. Yolk was smeared all over the outer container due to poor packing.",
    },
    {
        "ticket_id": "TKT-809",
        "store_id": "DS-MUM-BANDRA-06",
        "customer_id": "CUST-8832",
        "timestamp": "2026-10-24 21:55:18",
        "review_text": "Great service as always. All household cleaning supplies were delivered in 11 minutes without any hassle.",
    },
    {
        "ticket_id": "TKT-810",
        "store_id": "DS-BLR-KORAMANGALA-04",
        "customer_id": "CUST-3129",
        "timestamp": "2026-10-24 22:14:50",
        "review_text": "The paneer pack had air puffing and a sour, fermented smell on opening despite being within expiry date. Defective vendor batch.",
    },
]


def get_sample_reviews() -> List[Dict[str, Any]]:
    """Return synthetic Voice-of-Customer feedback items."""
    return [review.copy() for review in SYNTHETIC_REVIEWS]


def get_reviews_df() -> pd.DataFrame:
    """Return synthetic reviews structured as a pandas DataFrame."""
    return pd.DataFrame(SYNTHETIC_REVIEWS)


if __name__ == "__main__":
    df = get_reviews_df()
    print("Synthetic Quick-Commerce VoC Reviews (10 Items):")
    print(df[["ticket_id", "store_id", "review_text"]])

"""Voice-of-Customer (VoC) Defect Routing Agent - Main Orchestrator.
Loops through customer reviews, executes LLM defect classification,
and prints a formatted operational triage scorecard for actionable defects.
"""

import os
import sys
from collections import Counter
from tabulate import tabulate

# Ensure cross-platform UTF-8 output on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Try loading .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from data import get_sample_reviews
from agent import analyze_review
from schema import DefectReport


def run_defect_routing_pipeline():
    """Execute triage pipeline over synthetic VoC feed."""
    reviews = get_sample_reviews()

    print("\n" + "=" * 115)
    print("      VOICE-OF-CUSTOMER (VoC) DEFECT ROUTING AGENT - QUICK-COMMERCE TRIAGE      ")
    print("      Powered by LangChain & Groq (model: openai/gpt-oss-120b)                  ")
    print("=" * 115)

    groq_key = os.environ.get("GROQ_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if groq_key:
        print("[Status] Connected to Groq endpoint: https://api.groq.com/openai/v1 (openai/gpt-oss-120b)")
    else:
        print("[Notice] No GROQ_API_KEY detected in environment. Running with deterministic QA logic.")
    print(f"[Status] Ingesting {len(reviews)} raw customer feedback tickets...\n")

    defect_reports = []
    total_reviews = len(reviews)
    defect_count = 0

    for idx, rev in enumerate(reviews, start=1):
        ticket_id = rev["ticket_id"]
        store_id = rev["store_id"]
        text_preview = (rev["review_text"][:65] + "..") if len(rev["review_text"]) > 65 else rev["review_text"]

        print(f"[{idx}/{total_reviews}] Analyzing Ticket: {ticket_id} ({store_id})")
        print(f"      Feedback: \"{text_preview}\"")

        report: DefectReport = analyze_review(rev)

        if report.is_defect:
            defect_count += 1
            print(
                f"      -> [FLAGGED DEFECT] Type: {report.defect_type.value} | "
                f"Severity: {report.severity}/5 | Routed to: {report.routing_destination.value}"
            )
            defect_reports.append((rev, report))
        else:
            print("      -> [PASSED] Customer sentiment positive / non-defect.")
        print("-" * 115)

    return total_reviews, defect_reports


def display_defect_report(total_reviews: int, defect_reports: list):
    """Format and print an operational scorecard showing only classified defects."""
    print("\n" + "=" * 135)
    print("                     OPERATIONAL DEFECT TRIAGE & INCIDENT ROUTING SCORECARD                     ")
    print("=" * 135)

    table_rows = []
    dest_counts = Counter()
    type_counts = Counter()
    total_severity = 0

    for rev, report in defect_reports:
        dest_counts[report.routing_destination.value] += 1
        type_counts[report.defect_type.value] += 1
        total_severity += report.severity

        # Truncate customer review for clean table layout
        short_feedback = (rev["review_text"][:50] + "..") if len(rev["review_text"]) > 52 else rev["review_text"]
        short_action = (report.action_recommended[:45] + "..") if len(report.action_recommended) > 47 else report.action_recommended

        table_rows.append([
            rev["ticket_id"],
            rev["store_id"].replace("DS-", ""),
            short_feedback,
            report.sku_category,
            report.defect_type.value,
            f"{report.severity}/5",
            report.routing_destination.value,
            short_action,
        ])

    headers = [
        "Ticket ID",
        "Dark Store",
        "Customer Review Snippet",
        "Category",
        "Defect Type",
        "Severity",
        "Routing Destination",
        "Recommended Remediation",
    ]

    print(tabulate(table_rows, headers=headers, tablefmt="grid", stralign="left", numalign="center"))

    # Summary Statistics
    num_defects = len(defect_reports)
    defect_rate = (num_defects / total_reviews * 100) if total_reviews else 0.0
    avg_severity = (total_severity / num_defects) if num_defects else 0.0

    print("\n" + "=" * 65)
    print("               OPERATIONAL TRIAGE SUMMARY METRICS                ")
    print("=" * 65)
    summary_data = [
        ["Total Customer Reviews Ingested", str(total_reviews)],
        ["Operational Defects Identified", f"{num_defects} ({defect_rate:.1f}%)"],
        ["Average Defect Severity Rating", f"{avg_severity:.2f} / 5.00"],
        ["Routed to Dark Store Operations", f"{dest_counts['Dark_Store_Ops']} tickets"],
        ["Routed to Supply Chain (Cold Chain)", f"{dest_counts['Supply_Chain']} tickets"],
        ["Routed to Category Management (Vendor QA)", f"{dest_counts['Category_Manager']} tickets"],
    ]
    print(tabulate(summary_data, headers=["Triage Metric", "Summary Output"], tablefmt="grid"))
    print("=" * 65 + "\n")


def main():
    total_reviews, defect_reports = run_defect_routing_pipeline()
    display_defect_report(total_reviews, defect_reports)


if __name__ == "__main__":
    main()

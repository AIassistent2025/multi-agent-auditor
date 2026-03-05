import sys
import types

# ChromaDB bypass for Python 3.13 silent crash on macOS ARM64
try:
    import chromadb
except (ImportError, RuntimeError, Exception):
    sys.modules['chromadb'] = types.ModuleType('chromadb')

import os
from dotenv import load_dotenv
from crewai import Crew, Task, Process
from src.agents import get_agents

load_dotenv()

def run_audit(company_name: str, ticker: str):
    print(f"[*] Initializing Audit for {company_name} ({ticker})...")

    researcher, analyst, writer = get_agents()

    research_task = Task(
        description=f"Search for the latest 10-K report and recent financial news for {company_name} (Ticker: {ticker}). Extract key balance sheet and income statement figures.",
        expected_output="A detailed summary of raw financial data and links to source documents.",
        agent=researcher
    )

    analysis_task = Task(
        description=f"Based on the research for {company_name}, calculate P/E ratio, debt-to-equity, and identify any discrepancies between reported earnings and cash flow.",
        expected_output="A technical assessment of the company's financial health and any potential red flags.",
        agent=analyst,
        context=[research_task]
    )

    writing_task = Task(
        description=f"Generate a final audit report for {company_name}. Include an Executive Summary, Financial Performance section, and a Risk Assessment.",
        expected_output=f'A professional markdown report titled "Financial Audit Report: {company_name}".',
        agent=writer,
        context=[research_task, analysis_task]
    )

    audit_crew = Crew(
        agents=[researcher, analyst, writer],
        tasks=[research_task, analysis_task, writing_task],
        process=Process.sequential,
        verbose=True
    )

    result = audit_crew.kickoff()
    return result

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("[ERROR] OPENAI_API_KEY is missing from environment variables.")
        sys.exit(1)
    try:
        output = run_audit("NVIDIA", "NVDA")
        print("\n=== FINAL AUDIT REPORT ===\n")
        print(output.raw)
    except Exception as e:
        print(f"[ERROR] Execution failed: {e}")

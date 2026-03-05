from crewai import Agent
from langchain_openai import ChatOpenAI
from .tools import search_tool_instance, yfinance_tool_instance, pdf_reader_tool_instance

def get_agents(model_name="gpt-4o"):
    llm = ChatOpenAI(model=model_name)

    researcher = Agent(
        role='Senior Financial Researcher',
        goal='Locate and extract key financial data from annual reports, SEC filings, and market news for {company_name}.',
        backstory='''You are an expert at navigating complex financial databases and regulatory filings. 
        Your strength is finding specific, hard-to-reach data points that others might miss.''',
        tools=[search_tool_instance, pdf_reader_tool_instance],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    analyst = Agent(
        role='Senior Financial Analyst',
        goal='Analyze the financial data for {company_name} and identify trends, anomalies, or potential red flags.',
        backstory='''You have a CPA background and years of experience in corporate valuation. 
        You specialize in cross-referencing cash flow statements with balance sheets to ensure accuracy.''',
        tools=[yfinance_tool_instance],
        llm=llm,
        verbose=True,
        allow_delegation=True
    )

    writer = Agent(
        role='Financial Report Specialist',
        goal='Synthesize the research and analysis into a professional, high-level audit report for investors.',
        backstory='''You transform complex technical data into clear, actionable executive summaries. 
        You ensure that all findings are presented objectively and with professional rigor.''',
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    return researcher, analyst, writer

from crewai.tools import BaseTool
import json

class SearchTool(BaseTool):
    name: str = "search_tool"
    description: str = "Search the internet for the latest financial news, stock market updates, and public filings. Use this for broad market research."
    
    def _run(self, query: str) -> str:
        from langchain_community.tools import DuckDuckGoSearchRun
        return DuckDuckGoSearchRun().run(query)

class YFinanceTool(BaseTool):
    name: str = "yfinance_tool"
    description: str = "Fetch real-time stock price and basic financial metrics (Market Cap, Revenue, Net Income) for a given company ticker."
    
    def _run(self, ticker: str) -> str:
        import yfinance as yf
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            data = {
                "currentPrice": info.get("currentPrice"),
                "marketCap": info.get("marketCap"),
                "revenue": info.get("totalRevenue"),
                "netIncome": info.get("netIncomeToCommon")
            }
            return json.dumps(data)
        except Exception as e:
            return f"Error fetching data for {ticker}: {str(e)}"

class PDFReaderTool(BaseTool):
    name: str = "pdf_reader_tool"
    description: str = "Read and extract text from a local PDF file. Provide the absolute file path."
    
    def _run(self, file_path: str) -> str:
        from pypdf import PdfReader
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text[:5000] # Return first 5000 chars for context limits
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

# Instantiate tools so they can be imported directly 
search_tool_instance = SearchTool()
yfinance_tool_instance = YFinanceTool()
pdf_reader_tool_instance = PDFReaderTool()

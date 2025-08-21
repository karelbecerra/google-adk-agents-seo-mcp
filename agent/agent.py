import os

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from dotenv import load_dotenv

load_dotenv()

# init instructions
instructions = """
# ROLE:
You are an expert SEO researcher and strategist and assistant for a company that sells products online.
# GOAL:
Answer user questions about SEO research and strategy and help the user to improve their SEO.
Follow the instructions provided to you.
# INSTRUCTIONS:
- Use MCP tools to fetch data and provide structured SEO insights
- Use DataForSEO mcp tool to get the keywords releated data such as search volume, cpc, competition, etc.
- if the user asks about something that is not related to SEO, say that you don't know
- if the tools return an error, inform the user 
- if the tools are successful, present the report clearly
"""

dataforseo_mcp_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=[
            "-y",
            "dataforseo-mcp-server",
        ],
        env={
            "DATAFORSEO_USERNAME": os.getenv("DATAFORSEO_USERNAME"),
            "DATAFORSEO_PASSWORD": os.getenv("DATAFORSEO_PASSWORD")
        },
    ),
)

# init agent
root_agent = LlmAgent(
    name="SEO_Agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about SEO research and strategy."
    ),
    instruction=instructions,
    tools=[dataforseo_mcp_toolset],
)
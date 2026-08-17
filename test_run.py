import os
import sys

# Load env variables from root
from dotenv import load_dotenv
load_dotenv('.env')

# Add apps/api/src to path so we can import ares
sys.path.append(os.path.join(os.path.dirname(__file__), "apps/api/src"))

import logging
logging.basicConfig(level=logging.INFO)

from ares.agents.agents import ResearchPlanner, ResearchDiscovery, SourceAnalyst
from ares.agents.schemas import ResearchPlannerInput, ResearchDiscoveryInput, SourceAnalystInput
from ares.agents.tools.research_tools import search_sources, retrieve_source

def run():
    print("=== 1. PLANNING STAGE (LangChain + Gemini) ===")
    planner = ResearchPlanner()
    planner_input = ResearchPlannerInput(
        objective="Find the latest scientific consensus on the LK-99 room temperature superconductor claims."
    )
    plan = planner.execute(planner_input)
    print("Plan Output:")
    print(plan.model_dump_json(indent=2))

    print("\n=== 2. DISCOVERY STAGE ===")
    discovery = ResearchDiscovery()
    # Take the first task from the planner
    task = plan.tasks[0] if plan.tasks else "Search for LK-99 papers"
    discovery_input = ResearchDiscoveryInput(
        task=task,
        queries=["LK-99 replication studies 2024", "LK-99 scientific consensus"]
    )
    discovery_output = discovery.execute(discovery_input)
    print("Discovery Output:")
    print(discovery_output.model_dump_json(indent=2))

    print("\n=== 3. ACTUAL TOOL INVOCATION: DuckDuckGo Search ===")
    query = discovery_input.queries[0]
    print(f"Searching for: {query}")
    results = search_sources(query, max_results=2)
    for r in results:
        print(f" -> Found: {r['title']} ({r['url']})")

    if results:
        print("\n=== 4. ACTUAL TOOL INVOCATION: BeautifulSoup Scraping ===")
        url_to_scrape = results[0]['url']
        print(f"Scraping URL: {url_to_scrape}")
        content = retrieve_source(url_to_scrape)
        print(f" -> Successfully scraped {len(content)} characters of text content.")
        print(f" -> Snippet: {content[:200]}...")
        
        print("\n=== 5. ANALYSIS STAGE ===")
        analyst = SourceAnalyst()
        # In a fully wired AgentExecutor, the agent would call `retrieve_source` itself.
        # Here we just prove the LLM can generate the structured extraction based on the objective.
        analyst_input = SourceAnalystInput(
            source_url=url_to_scrape, 
            extraction_goal="Extract the main claims about replication success or failure."
        )
        try:
            analyst_output = analyst.execute(analyst_input)
            print("Analysis Output:")
            print(analyst_output.model_dump_json(indent=2))
        except Exception as e:
            print(f"Analysis failed (possibly due to API limits or parsing): {e}")
    
    print("\n=== PIPELINE TEST COMPLETE ===")

if __name__ == "__main__":
    run()

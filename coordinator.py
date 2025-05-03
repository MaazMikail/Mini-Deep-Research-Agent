import time
from agents import trace, Runner
from models import SearchResult
from research_agents.search_agent import search_agent
from research_agents.query_agent import QueryResponse, query_agent
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from duckduckgo_search import DDGS


console = Console()

class ResearchCoordinator:

    def __init__(self, query:str):
        self.query = query
        self.search_results = []


    async def research(self) -> str:
        with trace("Deep Research Workflow"):
            query_response = await self.generate_queries()
            return "dummy report"


    async def generate_queries(self) -> QueryResponse:

        with console.status("[bold cyan]Analyzing Query...[/bold cyan]") as status:
            
            result = await Runner.run(query_agent, input=self.query)

            console.print(Panel(f"[bold cyan]Query Analysis[/bold cyan]"))
            console.print(f"[yellow]Thoughts:[/yellow] {result.final_output.thoughts}")
            console.print("\n[yellow]Generated Search Queries:[/yellow]")
            for i, query in enumerate(result.final_output.queries, 1):
                console.print(f"  {i}. {query}")

            return result.final_output
        

    def duckduckgo_search(query: str):
        try:
            results = DDGS().text(query, region='us-en', safesearch='on', timelimit='y', max_results=1)
        except Exception as ex:
            return []
            console.print(f"[bold red]Search Error:[/bold red]")
        return results


    async def perform_research_for_queries(self, queries: list[str]) -> None:
        all_search_results = {}
        for query in queries:
            search_results = self.duckduckgo_search(query)
            all_search_results[query] = search_results

        for query in queries:
            console.print(f"\n[bold cyan]Searching for:[/bold cyan] {query}")

            for result in all_search_results[query]:

                console.print(f" [green]Result:[/green] {result['title']}")
                console.print(f" [dim]Result:[/dim] {result['href']}")
                console.print(f" [cyan]Analyzing content...[/cyan]")

                start_analysis_time = time.time()
                search_input = f"Title: {result['title']}\nURL: {result['href']}"
                agent_result = await Runner.run(search_agent, input=search_input)
                analysis_time = time.time() - start_analysis_time


                search_result = SearchResult(
                    title=result['title'],
                    url=result['href'],
                    summary=agent_result.final_output
                )

                self.search_results.append(search_result)

                summary_preview = agent_result.final_output[:100] + ("..." if len(agent_result.final_output)>100 else "")

                console.print(f" [green]Summary:[/green] {summary_preview}")
                console.print(f" [dim]Analysis Completed in {analysis_time}s[/dim]")

        console.print(f"\n[bold green]✓ Research round complete![/bold green] Found {len(all_search_results)} sources across {len(queries)} queries.")
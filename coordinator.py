from agents import trace, Runner
from research_agents.query_agent import QueryResponse, query_agent
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown


console = Console()

class ResearchCoordinator:

    def __init__(self, query:str):
        self.query = query


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
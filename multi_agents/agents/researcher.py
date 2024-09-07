from gpt_researcher import GPTResearcher
from colorama import Fore, Style
from .utils.views import print_agent_output
from ..output import Output


class ResearchAgent:
    def __init__(self, websocket=None, stream_output=None, tone=None, lang='zh', headers=None):
        self.websocket = websocket
        self.stream_output = stream_output
        self.headers = headers or {}
        self.tone = tone
        self.lang = lang
        self.output = Output(self.lang)

    async def research(self, query: str, research_report: str = "research_report",
                       parent_query: str = "", verbose=True, source="web", tone=None, lang='zh', headers=None):
        # Initialize the researcher
        researcher = GPTResearcher(query=query, report_type=research_report, parent_query=parent_query,
                                   verbose=verbose, report_source=source, tone=tone, lang=lang, websocket=self.websocket, headers=self.headers)
        # Conduct research on the given query
        await researcher.conduct_research()
        # Write the report
        report = await researcher.write_report()

        return report

    async def run_subtopic_research(self, parent_query: str, subtopic: str, verbose: bool = True, source="web", headers=None):
        try:
            report = await self.research(parent_query=parent_query, query=subtopic,
                                         research_report="subtopic_report", verbose=verbose, source=source, tone=self.tone, lang=self.lang, headers=None)
        except Exception as e:
            print(f"{Fore.RED}Error in researching topic {subtopic}: {e}{Style.RESET_ALL}")
            report = None
        return {subtopic: report}

    async def run_initial_research(self, research_state: dict):
        task = research_state.get("task")
        query = task.get("query")
        source = task.get("source", "web")

        if self.websocket and self.stream_output:
            await self.stream_output("logs",
                                     "initial_research",
                                     self.output.get_output(
                                         'INITIAL_RESEARCH', query=query),
                                     self.websocket
                                     )
        else:
            print_agent_output(
                self.output.get_output('RESEARCHER_RUNNING', query=query),
                agent="RESEARCHER")
        return {"task": task, "initial_research": await self.research(query=query, verbose=task.get("verbose"),
                                                                      source=source, tone=self.tone, lang=self.lang, headers=self.headers)}

    async def run_depth_research(self, draft_state: dict):
        task = draft_state.get("task")
        topic = draft_state.get("topic")
        parent_query = task.get("query")
        source = task.get("source", "web")
        verbose = task.get("verbose")
        if self.websocket and self.stream_output:
            await self.stream_output("logs", "depth_research",
                                     self.output.get_output(
                                         'DEPTH_RESEARCH', topic=topic),
                                     self.websocket
                                     )
        else:
            print_agent_output(self.output.get_output(
                'DEPTH_RESEARCH', topic=topic), agent="RESEARCHER")
        research_draft = await self.run_subtopic_research(parent_query=parent_query, subtopic=topic,
                                                          verbose=verbose, source=source, headers=self.headers)
        return {"draft": research_draft}

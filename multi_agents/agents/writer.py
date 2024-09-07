from datetime import datetime
import json5 as json
from .utils.views import print_agent_output
from .utils.llms import call_model
from ..prompts.writer_prompts import WriterPrompts
from ..output import Output


class WriterAgent:
    def __init__(self, websocket=None, stream_output=None, lang='zh', headers=None):
        self.websocket = websocket
        self.stream_output = stream_output
        self.lang = lang
        self.headers = headers
        self.output = Output(self.lang)

    async def write_sections(self, research_state: dict):
        query = research_state.get("title")
        data = research_state.get("research_data")
        task = research_state.get("task")
        follow_guidelines = task.get("follow_guidelines")
        guidelines = task.get("guidelines")

        prompts = WriterPrompts.get_prompts(
            self.lang, query, data, task, follow_guidelines, guidelines)

        response = await call_model(
            prompts,
            task.get("model"),
            response_format="json",
        )
        return response

    async def revise_headers(self, task: dict, headers: dict):
        prompts = WriterPrompts.get_revise_headers_prompt(
            self.lang, task, headers)

        response = await call_model(
            prompts,
            task.get("model"),
            response_format="json",
        )
        return {"headers": response}

    async def run(self, research_state: dict):
        if self.websocket and self.stream_output:
            await self.stream_output(
                "logs",
                "writing_report",
                self.output.get_output('WRITING_REPORT'),
                self.websocket,
            )
        else:
            print_agent_output(
                self.output.get_output('WRITING_REPORT'),
                agent="WRITER",
            )

        research_layout_content = await self.write_sections(research_state)

        if research_state.get("task").get("verbose"):
            if self.websocket and self.stream_output:
                research_layout_content_str = json.dumps(
                    research_layout_content, indent=2
                )
                await self.stream_output(
                    "logs",
                    "research_layout_content",
                    research_layout_content_str,
                    self.websocket,
                )
            else:
                print_agent_output(research_layout_content, agent="WRITER")

        headers = WriterPrompts.get_headers(self.lang, research_state)
        if research_state.get("task").get("follow_guidelines"):
            if self.websocket and self.stream_output:
                await self.stream_output(
                    "logs",
                    "rewriting_layout",
                    self.output.get_output('REWRITING_LAYOUT'),
                    self.websocket,
                )
            else:
                print_agent_output(
                    self.output.get_output('REWRITING_LAYOUT'),
                    agent="WRITER"
                )
            headers = await self.revise_headers(
                task=research_state.get("task"), headers=headers
            )
            headers = headers.get("headers")

        return {**research_layout_content, "headers": headers}

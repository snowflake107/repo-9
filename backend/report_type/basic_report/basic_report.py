from fastapi import WebSocket

from typing import Literal
from gpt_researcher.master.agent import GPTResearcher
from gpt_researcher.utils.enum import Tone


class BasicReport:
    def __init__(
        self,
        query: str,
        report_type: str,
        report_source: str,
        source_urls,
        tone: Tone,
        lang: Literal['en', 'zh'],
        config_path: str,
        websocket: WebSocket,
        headers=None
    ):
        self.query = query
        self.report_type = report_type
        self.report_source = report_source
        self.source_urls = source_urls
        self.tone = tone
        self.lang = lang
        self.config_path = config_path
        self.websocket = websocket
        self.headers = headers or {}

    async def run(self):
        # Initialize researcher
        researcher = GPTResearcher(
            query=self.query,
            report_type=self.report_type,
            report_source=self.report_source,
            source_urls=self.source_urls,
            tone=self.tone,
            lang=self.lang,
            config_path=self.config_path,
            websocket=self.websocket,
            headers=self.headers
        )

        await researcher.conduct_research()
        report = await researcher.write_report()
        return report

import json
from ..output import Output


class HumanAgent:
    def __init__(self, websocket=None, stream_output=None, lang='zh', headers=None):
        self.websocket = websocket
        self.stream_output = stream_output
        self.lang = lang
        self.headers = headers or {}
        self.output = Output(self.lang)

    async def review_plan(self, research_state: dict):
        print(f"HumanAgent websocket: {self.websocket}")
        print(f"HumanAgent stream_output: {self.stream_output}")
        task = research_state.get("task")
        layout = research_state.get("sections")

        user_feedback = None

        if task.get("include_human_feedback"):
            # Stream response to the user if a websocket is provided (such as from web app)
            if self.websocket and self.stream_output:
                try:
                    await self.stream_output(
                        "human_feedback",
                        "request",
                        self.output.get_output(
                            'HUMAN_FEEDBACK_REQUEST', layout=layout),
                        self.websocket,
                    )
                    response = await self.websocket.receive_text()
                    print(f"Received response: {response}", flush=True)
                    response_data = json.loads(response)
                    if response_data.get("type") == "human_feedback":
                        user_feedback = response_data.get("content")
                    else:
                        print(
                            f"Unexpected response type: {response_data.get('type')}",
                            flush=True,
                        )
                except Exception as e:
                    print(f"Error receiving human feedback: {e}", flush=True)
            # Otherwise, prompt the user for feedback in the console
            else:
                user_feedback = input(
                    self.output.get_output(
                        'HUMAN_FEEDBACK_REQUEST', layout=layout)
                )

        if user_feedback and "no" in user_feedback.strip().lower():
            user_feedback = None

        print(f"User feedback before return: {user_feedback}")

        return {"human_feedback": user_feedback}

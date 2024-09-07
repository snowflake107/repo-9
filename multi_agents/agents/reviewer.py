from .utils.views import print_agent_output
from .utils.llms import call_model
from ..prompts.reviewer_prompts import ReviewerPrompts
from ..output import Output


class ReviewerAgent:
    def __init__(self, websocket=None, stream_output=None, lang='zh', headers=None):
        self.websocket = websocket
        self.stream_output = stream_output
        self.lang = lang
        self.headers = headers or {}
        self.output = Output(self.lang)

    async def review_draft(self, draft_state: dict):
        """
        Review a draft article
        :param draft_state:
        :return:
        """
        task = draft_state.get("task")
        guidelines = "- ".join(guideline for guideline in task.get("guidelines"))
        revision_notes = draft_state.get("revision_notes")

        review_prompt = ReviewerPrompts.get_review_prompt(
            guidelines, draft_state, revision_notes, self.lang)

        prompt = [
            {"role": "system",
                "content": ReviewerPrompts.get_template(self.lang)},
            {"role": "user", "content": review_prompt},
        ]

        response = await call_model(prompt, model=task.get("model"))

        if task.get("verbose"):
            if self.websocket and self.stream_output:
                await self.stream_output(
                    "logs",
                    "review_feedback",
                    self.output.get_output(
                        'REVIEW_FEEDBACK', response=response),
                    self.websocket,
                )
            else:
                print_agent_output(
                    self.output.get_output('REVIEW_FEEDBACK', response=response), agent="REVIEWER"
                )

        if "None" in response:
            return None
        return response

    async def run(self, draft_state: dict):
        task = draft_state.get("task")
        guidelines = task.get("guidelines")
        to_follow_guidelines = task.get("follow_guidelines")
        review = None
        if to_follow_guidelines:
            print_agent_output(self.output.get_output(
                'REVIEW_DRAFT'), agent="REVIEWER")

            if task.get("verbose"):
                print_agent_output(
                    self.output.get_output('REVIEW_GUIDELINES', guidelines=guidelines), agent="REVIEWER"
                )

            review = await self.review_draft(draft_state, self.lang)
        else:
            print_agent_output(f"Ignoring guidelines...", agent="REVIEWER")
        return {"review": review}

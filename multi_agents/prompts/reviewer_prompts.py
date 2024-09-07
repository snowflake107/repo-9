
class ReviewerPrompts:
    @staticmethod
    def get_template(lang="zh"):
        if lang == "zh":
            return "你是一名研究文章审稿专家。你的目标是根据特定的指南审查研究草稿并向修订者提供反馈。\n"
        else:  # Default to English
            return "You are an expert research article reviewer. Your goal is to review research drafts and provide feedback to the reviser only based on specific guidelines.\n"

    @staticmethod
    def get_review_prompt(guidelines, draft_state, revision_notes=None, lang="zh"):
        if lang == "zh":
            revise_prompt = f"""修订者已经根据你之前的审查意见对草稿进行了修订，反馈如下：
{revision_notes}\n
请仅在关键情况下提供额外反馈，因为修订者已经根据你之前的反馈进行了更改。
如果你认为文章已经足够好或者只需要非关键性的修订，请尽量返回 None。
"""
            review_prompt = f"""你被要求审查一篇由非专家根据特定指南撰写的草稿。
如果草稿足够好可以发表，请接受草稿，或者发送修订意见以指导修订。
如果没有满足所有的指南标准，你应该发送适当的修订意见。
如果草稿符合所有指南，请返回 None。
{revise_prompt if revision_notes else ""}

指南: {guidelines}\n草稿: {draft_state.get("draft")}\n
"""
        else:  # Default to English
            revise_prompt = f"""The reviser has already revised the draft based on your previous review notes with the following feedback:
{revision_notes}\n
Please provide additional feedback ONLY if critical since the reviser has already made changes based on your previous feedback.
If you think the article is sufficient or that non critical revisions are required, please aim to return None.
"""
            review_prompt = f"""You have been tasked with reviewing the draft which was written by a non-expert based on specific guidelines.
Please accept the draft if it is good enough to publish, or send it for revision, along with your notes to guide the revision.
If not all of the guideline criteria are met, you should send appropriate revision notes.
If the draft meets all the guidelines, please return None.
{revise_prompt if revision_notes else ""}

Guidelines: {guidelines}\nDraft: {draft_state.get("draft")}\n
"""
        return review_prompt

from datetime import datetime

class WriterPrompts:
    @staticmethod
    def get_headers(lang, research_state):
        headers = {
            'en': {
                "title": research_state.get("title"),
                "date": "Date",
                "introduction": "Introduction",
                "table_of_contents": "Table of Contents",
                "conclusion": "Conclusion",
                "references": "References",
            },
            'zh': {
                "title": research_state.get("title"),
                "date": "日期",
                "introduction": "介绍",
                "table_of_contents": "目录",
                "conclusion": "结论",
                "references": "参考文献",
            }
        }
        return headers.get(lang, headers['zh'])

    @staticmethod
    def get_sample_json(lang):
        sample_json = {
            'en': """
            {
              "table_of_contents": A table of contents in markdown syntax (using '-') based on the research headers and subheaders,
              "introduction": An indepth introduction to the topic in markdown syntax and hyperlink references to relevant sources,
              "conclusion": A conclusion to the entire research based on all research data in markdown syntax and hyperlink references to relevant sources,
              "sources": A list with strings of all used source links in the entire research data in markdown syntax and apa citation format. For example: ['-  Title, year, Author [source url](source)', ...]
            }
            """,
            'zh': """
            {
              "目录": 基于研究标题和副标题的markdown语法目录（使用'-'），
              "介绍": 对主题的深入介绍，使用markdown语法和超链接引用相关来源，
              "结论": 基于所有研究数据的整个研究的结论，使用markdown语法和超链接引用相关来源，
              "来源": 一个包含所有使用的来源链接的字符串列表，使用markdown语法和APA引用格式。例如：['-  标题, 年份, 作者 [来源网址](来源)', ...]
            }
            """
        }
        return sample_json.get(lang, sample_json['zh'])

    @staticmethod
    def get_prompts(lang, query, data, task, follow_guidelines, guidelines):
        prompts = {
            'en': [
                {
                    "role": "system",
                    "content": "You are a research writer. Your sole purpose is to write a well-written research report about a topic based on research findings and information.\n",
                },
                {
                    "role": "user",
                    "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n."
                               f"Query or Topic: {query}\n"
                               f"Research data: {str(data)}\n"
                               f"Your task is to write an in depth, well written and detailed "
                               f"introduction and conclusion to the research report based on the provided research data. "
                               f"Do not include headers in the results.\n"
                               f"You MUST include any relevant sources to the introduction and conclusion as markdown hyperlinks -"
                               f"For example: 'This is a sample text. ([url website](url))'\n\n"
                               f"{f'You must follow the guidelines provided: {guidelines}' if follow_guidelines else ''}\n"
                               f"You MUST return nothing but a JSON in the following format (without json markdown):\n"
                               f"{WriterPrompts.get_sample_json(lang)}\n\n",
                },
            ],
            'zh': [
                {
                    "role": "system",
                    "content": "你是一名研究写作者。你的唯一目的是根据研究结果和信息撰写一份写得很好的研究报告。\n",
                },
                {
                    "role": "user",
                    "content": f"今天的日期是 {datetime.now().strftime('%d/%m/%Y')}\n."
                               f"查询或主题: {query}\n"
                               f"研究数据: {str(data)}\n"
                               f"你的任务是根据提供的研究数据撰写一份深入、写得很好且详细的研究报告的介绍和结论。"
                               f"不要在结果中包含标题。\n"
                               f"你必须将任何相关来源作为markdown超链接包含在介绍和结论中 -"
                               f"例如：'这是一个示例文本。 ([网址](url))'\n\n"
                               f"{f'你必须遵循提供的指南: {guidelines}' if follow_guidelines else ''}\n"
                               f"你必须只返回以下格式的JSON（不带json markdown）：\n"
                               f"{WriterPrompts.get_sample_json(lang)}\n\n",
                },
            ]
        }
        return prompts.get(lang, prompts['zh'])

    @staticmethod
    def get_revise_headers_prompt(lang, task, headers):
        prompts = {
            'en': [
                {
                    "role": "system",
                    "content": """You are a research writer. 
    Your sole purpose is to revise the headers data based on the given guidelines.""",
                },
                {
                    "role": "user",
                    "content": f"""Your task is to revise the given headers JSON based on the guidelines given.
    You are to follow the guidelines but the values should be in simple strings, ignoring all markdown syntax.
    You must return nothing but a JSON in the same format as given in headers data.
    Guidelines: {task.get("guidelines")}\n
    Headers Data: {headers}\n
    """,
                },
            ],
            'zh': [
                {
                    "role": "system",
                    "content": "你是一名研究写作者。你的唯一目的是根据给定的指南修改标题数据。",
                },
                {
                    "role": "user",
                    "content": f"""你的任务是根据给定的指南修改给定的标题JSON。
    你必须遵循指南，但值应为简单字符串，忽略所有markdown语法。
    你必须只返回与标题数据中给出的格式相同的JSON。
    指南: {task.get("guidelines")}\n
    标题数据: {headers}\n
    """,
                },
            ]
        }
        return prompts.get(lang, prompts['zh'])

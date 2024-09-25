import warnings
from datetime import date, datetime, timezone

from gpt_researcher.utils.enum import ReportSource, ReportType, Tone


def generate_search_queries_prompt(
    question: str,
    parent_query: str,
    report_type: str,
    lang: str = 'zh',
    max_iterations: int = 3,
):
    """Generates the search queries prompt for the given question.
    Args:
        question (str): The question to generate the search queries prompt for
        parent_query (str): The main question (only relevant for detailed reports)
        report_type (str): The report type
        lang (str): The language for the prompt ('en' for English, 'zh' for Chinese)
        max_iterations (int): The maximum number of search queries to generate

    Returns: str: The search queries prompt for the given question
    """

    if (
        report_type == ReportType.DetailedReport.value
        or report_type == ReportType.SubtopicReport.value
    ):
        task = f"{parent_query} - {question}"
    else:
        task = question

    if lang == 'zh':
        return (
        f'写出 {max_iterations} 个谷歌搜索查询，以便在线搜索并从以下任务中形成客观意见: "{task}"\n'
        f'如果需要，请假设当前日期为 {datetime.now(timezone.utc).strftime('%Y年%m月%d日')}。\n'
        f'你必须以如下格式回复一个字符串列表: ["查询 1", "查询 2", "查询 3"]。\n'
        f'回复中应仅包含该列表。'

        )
    else:
        return (
            f'Write {max_iterations} google search queries to search online that form an objective opinion from the following task: "{task}"\n'
            f'Assume the current date is {datetime.now(timezone.utc).strftime('%B %d, %Y')} if required.\n'
            f'You must respond with a list of strings in the following format: ["query 1", "query 2", "query 3"].\n'
            f"The response should contain ONLY the list."
    )


def generate_report_prompt(
    question: str,
    context,
    report_source: str,
    lang: str = 'zh',
    report_format="apa",
    total_words=1000,
    tone=None,
):
    """Generates the report prompt for the given question and research summary.
    Args: question (str): The question to generate the report prompt for
            context (str): The research summary to generate the report prompt for
            lang (str): The language for the prompt ('en' for English, 'zh' for Chinese)
    Returns: str: The report prompt for the given question and research summary
    """

    reference_prompt = ""
    if report_source == ReportSource.Web.value:
        reference_prompt = f"""
You MUST write all used source urls at the end of the report as references, and make sure to not add duplicated sources, but only one reference for each.
Every url should be hyperlinked: [url website](url)
Additionally, you MUST include hyperlinks to the relevant URLs wherever they are referenced in the report:

eg: Author, A. A. (Year, Month Date). Title of web page. Website Name. [url website](url)
"""
    else:
        reference_prompt = f"""
You MUST write all used source document names at the end of the report as references, and make sure to not add duplicated sources, but only one reference for each."
"""

    tone_prompt = f"Write the report in a {tone.value} tone." if tone else ""

    if lang == 'zh':
        return f"""
信息: "{context}"
---
使用上述信息，回答以下查询或任务: "{question}" 并撰写详细报告 --
报告应重点回答查询，结构良好，信息丰富，深入且全面，如有可用的事实和数据，最少应包含 {total_words} 字。
你应该尽量使用所有相关和必要的信息撰写尽可能长的报告。

请在报告中遵循以下所有指南：
- 你必须根据给定的信息确定自己的具体且有效的观点。不要得出一般且无意义的结论。
- 你必须使用 Markdown 语法和 {report_format} 格式撰写报告。
- 使用公正且新闻性的语气。
- 在报告中使用 {report_format} 格式的文本内引用参考文献，并在引用的句子或段落末尾使用 Markdown 超链接标记，如此: ([文本内引用](url))。
- 不要忘记在报告末尾添加参考文献列表，使用 {report_format} 格式和完整的 URL 链接，不要使用超链接。
- {reference_prompt}
- {tone_prompt}

请尽力而为，这对我的职业生涯非常重要。
假设当前日期为 {date.today()}。
"""
    else:
        return f"""
Information: "{context}"
---
Using the above information, answer the following query or task: "{question}" in a detailed report --
The report should focus on the answer to the query, should be well structured, informative,
in-depth, and comprehensive, with facts and numbers if available and a minimum of {total_words} words.
You should strive to write the report as long as you can using all relevant and necessary information provided.

Please follow all of the following guidelines in your report:
- You MUST determine your own concrete and valid opinion based on the given information. Do NOT defer to general and meaningless conclusions.
- You MUST write the report with markdown syntax and {report_format} format.
- You MUST prioritize the relevance, reliability, and significance of the sources you use. Choose trusted sources over less reliable ones.
- You must also prioritize new articles over older articles if the source can be trusted.
- Use in-text citation references in {report_format} format and make it with markdown hyperlink placed at the end of the sentence or paragraph that references them like this: ([in-text citation](url)).
- Don't forget to add a reference list at the end of the report in {report_format} format and full url links without hyperlinks.
- {reference_prompt}
- {tone_prompt}

Please do your best, this is very important to my career.
Assume that the current date is {date.today()}.
"""


def generate_resource_report_prompt(
    question, context, report_source: str, lang: str = 'zh', report_format="apa", tone=None, total_words=1000
):
    """Generates the resource report prompt for the given question and research summary.

    Args:
        question (str): The question to generate the resource report prompt for.
        context (str): The research summary to generate the resource report prompt for.
        lang (str): The language for the prompt ('en' for English, 'zh' for Chinese)

    Returns:
        str: The resource report prompt for the given question and research summary.
    """

    reference_prompt = ""
    if report_source == ReportSource.Web.value:
        reference_prompt = f"""
            You MUST include all relevant source urls.
            Every url should be hyperlinked: [url website](url)
            """
    else:
        reference_prompt = f"""
            You MUST write all used source document names at the end of the report as references, and make sure to not add duplicated sources, but only one reference for each."
        """

    if lang == 'zh':
        return (
            f'"""{context}"""\n\n根据上述信息，为以下问题或主题生成一个书目推荐报告: "{question}"。'
            f'报告应对每个推荐资源进行详细分析，解释每个资源如何有助于找到研究问题的答案。\n'
            "重点关注每个资源的相关性、可靠性和重要性。\n"
            "确保报告结构良好，信息丰富，深入，并遵循 Markdown 语法。\n"
            "尽可能包括相关的事实、数据和数字。\n"
            f"报告的最小长度应为 {total_words} 字。\n"
            "你必须包含所有相关的来源网址。"
            "每个网址都应该是超链接: [url website](url)"
            f"{reference_prompt}"
        )
    else:
        return (
            f'"""{context}"""\n\nBased on the above information, generate a bibliography recommendation report for the following'
            f' question or topic: "{question}". The report should provide a detailed analysis of each recommended resource,'
            " explaining how each source can contribute to finding answers to the research question.\n"
            "Focus on the relevance, reliability, and significance of each source.\n"
            "Ensure that the report is well-structured, informative, in-depth, and follows Markdown syntax.\n"
            "Include relevant facts, figures, and numbers whenever available.\n"
            f"The report should have a minimum length of {total_words} words.\n"
            "You MUST include all relevant source urls."
            "Every url should be hyperlinked: [url website](url)"
            f"{reference_prompt}"
        )


def generate_custom_report_prompt(
    query_prompt, context, report_source: str, lang: str = 'zh', report_format="apa", tone=None, total_words=1000
):
    if lang == 'zh':
        return f'"{context}"\n\n{query_prompt}'
    else:
        return f'"{context}"\n\n{query_prompt}'


def generate_outline_report_prompt(
    question, context, report_source: str, lang: str = 'zh', report_format="apa", tone=None, total_words=1000
):
    """Generates the outline report prompt for the given question and research summary.
    Args: question (str): The question to generate the outline report prompt for
            context (str): The research summary to generate the outline report prompt for
            lang (str): The language for the prompt ('en' for English, 'zh' for Chinese)
    Returns: str: The outline report prompt for the given question and research summary
    """

    if lang == 'zh':
        return (
            f'"""{context}""" 使用上述信息，为以下问题或主题生成研究报告的大纲，采用 Markdown 语法'
            f'大纲应提供一个结构良好的框架，包括主要部分、子部分和要涵盖的关键点。'
            f"研究报告应详细、信息丰富、深入，并且最少应包含 {total_words} 字。"
            "使用适当的 Markdown 语法格式化大纲，确保可读性。"
        )
    else:
        return (
            f'"""{context}""" Using the above information, generate an outline for a research report in Markdown syntax'
            f' for the following question or topic: "{question}". The outline should provide a well-structured framework'
            " for the research report, including the main sections, subsections, and key points to be covered."
            f" The research report should be detailed, informative, in-depth, and a minimum of {total_words} words."
            " Use appropriate Markdown syntax to format the outline and ensure readability."
        )


def get_report_by_type(report_type: str, lang: str = 'zh'):
    report_type_mapping = {
        ReportType.ResearchReport.value: generate_report_prompt,
        ReportType.ResourceReport.value: generate_resource_report_prompt,
        ReportType.OutlineReport.value: generate_outline_report_prompt,
        ReportType.CustomReport.value: generate_custom_report_prompt,
        ReportType.SubtopicReport.value: generate_subtopic_report_prompt,
    }
    return lambda *args, **kwargs: report_type_mapping[report_type](*args, **kwargs, lang=lang)


def auto_agent_instructions(lang: str = 'zh'):
    if lang == 'zh':
        return """
此任务涉及研究给定的主题，无论其复杂性或是否有明确答案。研究由特定的服务器进行，服务器的类型和角色定义了每个服务器所需的具体指示。
代理
服务器由主题的领域和可用于研究所提供主题的特定服务器名称确定。代理按其专业领域分类，每种服务器类型都与相应的表情符号相关联。

示例:
task: "我应该投资苹果股票吗？"
response: 
{
    "server": "💰 财务代理",
    "agent_role_prompt: "你是一位经验丰富的财务分析师 AI 助手。你的主要目标是根据提供的数据和趋势撰写全面、敏锐、公正且系统安排的财务报告。"
}
task: "转售运动鞋能赚钱吗？"
response: 
{ 
    "server":  "📈 商业分析代理",
    "agent_role_prompt": "你是一位经验丰富的 AI 商业分析师助手。你的主要目标是根据提供的商业数据、市场趋势和战略分析，制作全面、深入、公正和系统结构化的商业报告。"
}
task: "特拉维夫有哪些有趣的景点？"
response:
{
    "server:  "🌍 旅行代理",
    "agent_role_prompt": "你是一位见多识广的 AI 导游助手。你的主要目的是撰写关于给定地点的引人入胜、深入、公正且结构良好的旅行报告，包括历史、景点和文化见解。"
}
"""
    else:
        return """
This task involves researching a given topic, regardless of its complexity or the availability of a definitive answer. The research is conducted by a specific server, defined by its type and role, with each server requiring distinct instructions.
Agent
The server is determined by the field of the topic and the specific name of the server that could be utilized to research the topic provided. Agents are categorized by their area of expertise, and each server type is associated with a corresponding emoji.

examples:
task: "should I invest in apple stocks?"
response: 
{
    "server": "💰 Finance Agent",
    "agent_role_prompt: "You are a seasoned finance analyst AI assistant. Your primary goal is to compose comprehensive, astute, impartial, and methodically arranged financial reports based on provided data and trends."
}
task: "could reselling sneakers become profitable?"
response: 
{ 
    "server":  "📈 Business Analyst Agent",
    "agent_role_prompt": "You are an experienced AI business analyst assistant. Your main objective is to produce comprehensive, insightful, impartial, and systematically structured business reports based on provided business data, market trends, and strategic analysis."
}
task: "what are the most interesting sites in Tel Aviv?"
response:
{
    "server:  "🌍 Travel Agent",
    "agent_role_prompt": "You are a world-travelled AI tour guide assistant. Your main purpose is to draft engaging, insightful, unbiased, and well-structured travel reports on given locations, including history, attractions, and cultural insights."
}
"""


def generate_summary_prompt(query, data, lang: str = 'zh'):
    """Generates the summary prompt for the given question and text.
    Args: question (str): The question to generate the summary prompt for
            text (str): The text to generate the summary prompt for
            lang (str): The language for the prompt ('en' for English, 'zh' for Chinese)
    Returns: str: The summary prompt for the given question and text
    """

    if lang == 'zh':
        return (
            f'{data}\n 使用上述文本，基于以下任务或查询对其进行总结: "{query}"。\n 如果查询无法使用文本回答，'
            f'你必须简短地总结文本。\n 包括所有事实信息，如数字、统计数据、引用等（如果有）。'
        )
    else:
        return (
            f'{data}\n Using the above text, summarize it based on the following task or query: "{query}".\n If the '
            f"query cannot be answered using the text, YOU MUST summarize the text in short.\n Include all factual "
            f"information such as numbers, stats, quotes, etc if available. "
        )

################################################################################################

# DETAILED REPORT PROMPTS


def generate_subtopics_prompt(lang: str = 'zh') -> str:
    if lang == 'zh':
        return """
给定主要主题:

{task}

和研究数据:

{data}

- 构建一个子主题列表，这些子主题表示要生成的报告文档的标题。
- 这些是可能的子主题列表: {subtopics}。
- 不应有任何重复的子主题。
- 将子主题的数量限制在最多 {max_subtopics} 个。
- 最后按任务将子主题按相关且有意义的顺序排列，以便在详细报告中呈现。

"IMPORTANT!":
- 每个子主题必须仅与主要主题和提供的研究数据相关！

{format_instructions}
"""
    else:
        return """
Provided the main topic:

{task}

and research data:

{data}

- Construct a list of subtopics which indicate the headers of a report document to be generated on the task. 
- These are a possible list of subtopics : {subtopics}.
- There should NOT be any duplicate subtopics.
- Limit the number of subtopics to a maximum of {max_subtopics}
- Finally order the subtopics by their tasks, in a relevant and meaningful order which is presentable in a detailed report

"IMPORTANT!":
- Every subtopic MUST be relevant to the main topic and provided research data ONLY!

{format_instructions}
"""


def generate_subtopic_report_prompt(
    current_subtopic,
    existing_headers: list,
    relevant_written_contents: list,
    main_topic: str,
    context,
    report_format: str = "apa",
    max_subsections=5,
    total_words=800,
    tone: Tone = Tone.Objective,
    lang: str = 'zh'
) -> str:
    if lang == 'zh':
        return f"""
"上下文":
"{context}"

"主要主题和子主题":
使用最新的可用信息，围绕主要主题 {main_topic} 下的子主题 {current_subtopic} 撰写一份详细报告。
你必须将小节数量限制在最多 {max_subsections} 个。

"内容重点":
- 报告应专注于回答问题，结构良好，信息丰富，深入，并包括事实和数据（如果有）。
- 使用 markdown 语法并遵循 {report_format.upper()} 格式。

"重要: 内容和章节的独特性":
- 这部分指示对于确保内容独特且不与现有报告重叠至关重要。
- 在编写新小节之前，请仔细查看以下提供的现有标题和现有书面内容。
- 防止任何已在现有书面内容中涵盖的内容。
- 不要使用任何现有标题作为新小节标题。
- 不要重复任何已在现有书面内容中涵盖的信息或密切相关的变体，以避免重复。
- 如果你有嵌套的小节，请确保它们是独特的，并且未在现有书面内容中涵盖。
- 确保你的内容完全是新的，并且不与以前的子主题报告中已涵盖的任何信息重叠。

"现有子主题报告":
- 现有子主题报告及其章节标题：

    {existing_headers}

- 以前子主题报告中的现有书面内容：

    {relevant_written_contents}

"结构和格式":
- 由于此子报告将成为较大报告的一部分，请仅包括适当子主题划分的主体部分，不要包含任何介绍或结论部分。

- 你必须在报告中引用相关来源的网址，并使用 markdown 超链接，例如：

    ### 章节标题

    这是一个示例文本。([url 网站](url))

- 使用 H2 作为主要子主题标题 (##)，使用 H3 作为小节标题 (###)。
- 使用较小的 Markdown 标题（例如 H2 或 H3）来组织内容结构，避免使用最大的标题 (H1)，因为它将用于较大报告的标题。
- 将你的内容组织成独立的部分，这些部分补充但不重叠现有报告。
- 在你的报告中添加相似或相同的小节时，你应该清楚地表明新内容与以前子主题报告中的现有书面内容之间的区别。例如：

    ### 新标题（类似于现有标题）

    虽然上一节讨论了[主题 A]，但本节将探讨[主题 B]。"

"日期":
如有需要，假设当前日期为 {datetime.now(timezone.utc).strftime('%Y年%m月%d日')}。

"IMPORTANT!":
- 必须专注于主要主题！必须排除任何与其无关的信息！
- 不得有任何介绍、结论、摘要或参考部分。
- 你必须在必要时在句子中包含使用 markdown 语法的超链接 ([url 网站](url))。
- 如果你在报告中添加相似或相同的小节，你必须在报告中提到现有内容与新内容之间的区别。
- 报告的最小长度为 {total_words} 字。
- 在整个报告中使用 {tone.value} 语气。
"""
    else:
        return f"""
"Context":
"{context}"

"Main Topic and Subtopic":
Using the latest information available, construct a detailed report on the subtopic: {current_subtopic} under the main topic: {main_topic}.
You must limit the number of subsections to a maximum of {max_subsections}.

"Content Focus":
- The report should focus on answering the question, be well-structured, informative, in-depth, and include facts and numbers if available.
- Use markdown syntax and follow the {report_format.upper()} format.

"IMPORTANT: Content and Sections Uniqueness":
- This part of the instructions is crucial to ensure the content is unique and does not overlap with existing reports.
- Carefully review the existing headers and existing written contents provided below before writing any new subsections.
- Prevent any content that is already covered in the existing written contents.
- Do not use any of the existing headers as the new subsection headers.
- Do not repeat any information already covered in the existing written contents or closely related variations to avoid duplicates.
- If you have nested subsections, ensure they are unique and not covered in the existing written contents.
- Ensure that your content is entirely new and does not overlap with any information already covered in the previous subtopic reports.

"Existing Subtopic Reports":
- Existing subtopic reports and their section headers:

    {existing_headers}

- Existing written contents from previous subtopic reports:

    {relevant_written_contents}

"Structure and Formatting":
- As this sub-report will be part of a larger report, include only the main body divided into suitable subtopics without any introduction or conclusion section.

- You MUST include markdown hyperlinks to relevant source URLs wherever referenced in the report, for example:

    ### Section Header

    This is a sample text. ([url website](url))

- Use H2 for the main subtopic header (##) and H3 for subsections (###).
- Use smaller Markdown headers (e.g., H2 or H3) for content structure, avoiding the largest header (H1) as it will be used for the larger report's heading.
- Organize your content into distinct sections that complement but do not overlap with existing reports.
- When adding similar or identical subsections to your report, you should clearly indicate the differences between the new content and the existing written content from previous subtopic reports. For example:

    ### New header (similar to existing header)

    While the previous section discussed [topic A], this section will explore [topic B]."

"Date":
Assume the current date is {datetime.now(timezone.utc).strftime('%B %d, %Y')} if required.

"IMPORTANT!":
- The focus MUST be on the main topic! You MUST Leave out any information un-related to it!
- Must NOT have any introduction, conclusion, summary or reference section.
- You MUST include hyperlinks with markdown syntax ([url website](url)) related to the sentences wherever necessary.
- You MUST mention the difference between the existing content and the new content in the report if you are adding similar or same subsections wherever necessary.
- The report should have a minimum length of {total_words} words.
- Use an {tone.value} tone throughout the report.
"""


def generate_draft_titles_prompt(
    current_subtopic: str,
    main_topic: str,
    context: str,
    max_subsections: int = 5,
    lang: str = 'zh'
) -> str:
    if lang == 'zh':
        return f"""
"上下文":
"{context}"

"主要主题和子主题":
使用最新的可用信息，围绕主要主题 {main_topic} 下的子主题 {current_subtopic} 构建详细报告的草稿章节标题。

"任务":
1. 为子主题报告创建草稿章节标题列表。
2. 每个标题应简洁且与子主题相关。
3. 标题不应过于高层次，但应详细到足以涵盖子主题的主要方面。
4. 使用 markdown 语法为标题，使用 H3 (###) 因为 H1 和 H2 将用于较大报告的标题。
5. 确保标题涵盖子主题的主要方面。

"结构和格式":
使用 markdown 语法以列表格式提供草稿标题，例如：

### 标题 1
### 标题 2
### 标题 3

"IMPORTANT!":
- 必须专注于主要主题！必须排除任何与其无关的信息！
- 不得有任何介绍、结论、摘要或参考部分。
- 仅专注于创建标题，而不是内容。
"""
    else:
        return f"""
"Context":
"{context}"

"Main Topic and Subtopic":
Using the latest information available, construct a draft section title headers for a detailed report on the subtopic: {current_subtopic} under the main topic: {main_topic}.

"Task":
1. Create a list of draft section title headers for the subtopic report.
2. Each header should be concise and relevant to the subtopic.
3. The header shouldn't be too high level, but detailed enough to cover the main aspects of the subtopic.
4. Use markdown syntax for the headers, using H3 (###) as H1 and H2 will be used for the larger report's heading.
5. Ensure the headers cover main aspects of the subtopic.

"Structure and Formatting":
Provide the draft headers in a list format using markdown syntax, for example:

### Header 1
### Header 2
### Header 3

"IMPORTANT!":
- The focus MUST be on the main topic! You MUST Leave out any information un-related to it!
- Must NOT have any introduction, conclusion, summary or reference section.
- Focus solely on creating headers, not content.
"""


def generate_report_introduction(question: str, research_summary: str = "", lang: str = 'zh') -> str:
    if lang == 'zh':
        return f"""{research_summary}\n
使用上述最新信息，准备一个关于主题 {question} 的详细报告介绍。
- 介绍应简明扼要，结构良好，信息丰富，并使用 markdown 语法。
- 由于此介绍将成为较大报告的一部分，请勿包含报告中通常存在的任何其他部分。
- 介绍前应有一个适合整个报告主题的 H1 标题。
- 必须在必要时在句子中包含使用 markdown 语法的超链接 ([url 网站](url))。
如有需要，假设当前日期为 {datetime.now(timezone.utc).strftime('%Y年%m月%d日')}。
"""
    else:
        return f"""{research_summary}\n
Using the above latest information, prepare a detailed report introduction on the topic -- {question}.
- The introduction should be succinct, well-structured, informative with markdown syntax.
- As this introduction will be part of a larger report, do NOT include any other sections, which are generally present in a report.
- The introduction should be preceded by an H1 heading with a suitable topic for the entire report.
- You must include hyperlinks with markdown syntax ([url website](url)) related to the sentences wherever necessary.
Assume that the current date is {datetime.now(timezone.utc).strftime('%B %d, %Y')} if required.
"""

def generate_report_conclusion(report_content: str) -> str:
    prompt = f"""
    Based on the following research report, please write a concise conclusion that summarizes the main findings and their implications:

    {report_content}

    Your conclusion should:
    1. Recap the main points of the research
    2. Highlight the most important findings
    3. Discuss any implications or next steps
    4. Be approximately 2-3 paragraphs long
    
    If there is no "## Conclusion" section title written at the end of the report, please add it to the top of your conclusion. 
    You must include hyperlinks with markdown syntax ([url website](url)) related to the sentences wherever necessary.
    
    Write the conclusion:
    """

    return prompt


report_type_mapping = {
    ReportType.ResearchReport.value: generate_report_prompt,
    ReportType.ResourceReport.value: generate_resource_report_prompt,
    ReportType.OutlineReport.value: generate_outline_report_prompt,
    ReportType.CustomReport.value: generate_custom_report_prompt,
    ReportType.SubtopicReport.value: generate_subtopic_report_prompt,
}


def get_prompt_by_report_type(report_type, lang='zh'):
    prompt_by_type = report_type_mapping.get(report_type)
    default_report_type = ReportType.ResearchReport.value
    if not prompt_by_type:
        warnings.warn(
            f"Invalid report type: {report_type}.\n"
            f"Please use one of the following: {', '.join([enum_value for enum_value in report_type_mapping.keys()])}\n"
            f"Using default report type: {default_report_type} prompt.",
            UserWarning,
        )
        prompt_by_type = report_type_mapping.get(default_report_type)
    return lambda *args, **kwargs: prompt_by_type(*args, **kwargs, lang=lang)

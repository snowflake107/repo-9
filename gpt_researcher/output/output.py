# 定义一个函数来生成多语言字典
def create_multilang_dict(zh_text, en_text):
    return {'zh': zh_text, 'en': en_text}

# 定义一个类来管理多语言字符串


class Output:
    def __init__(self, lang):
        self.lang = lang
        self.strings = {
            'STARTING_RESEARCH': create_multilang_dict(
                "🔎 开始研究任务 '{query}'...",
                "🔎 Starting the research task for '{query}'..."
            ),
            'CONTEXT': create_multilang_dict(
                "上下文来自本地文档: {docs_context}\n\n上下文来自网络资源: {web_context}",
                "Context from local documents: {docs_context}\n\nContext from web sources: {web_context}"
            ),
            'ADDED_SOURCE_URL': create_multilang_dict(
                "✅ 已将来源网址添加到研究中: {url}\n",
                "✅ Added source url to research: {url}\n"
            ),
            'SOURCE_URLS': create_multilang_dict(
                "🗂️ 我将根据以下网址进行研究：{new_search_urls}……",
                "🗂️ I will conduct my research based on the following urls: {new_search_urls}..."
            ),
            'SUBQUERIES': create_multilang_dict(
                "🗂️ 我将基于以下查询进行研究：{sub_queries}",
                "🗂️ I will conduct my research based on the following queries: {sub_queries}..."
            ),
            'FETCHING_QUERY_CONTENT': create_multilang_dict(
                "📚 正在根据查询获取相关内容: {query}...",
                "📚 Getting relevant content based on query: {query}..."
            ),
            'RUNNING_SUBQUERY_RESEARCH': create_multilang_dict(
                "\n🔍 正在为 '{sub_query}' 进行研究...",
                "\n🔍 Running research for '{sub_query}'..."
            ),
            'SUBQUERY_CONTEXT_NOT_FOUND': create_multilang_dict(
                "🤷 未找到 '{sub_query}' 的相关内容……",
                "🤷 No content found for '{sub_query}'..."
            ),
            'RUNNING_SUBQUERY_WITH_VECTORSTORE_RESEARCH': create_multilang_dict(
                "\n🔍 正在为 '{sub_query}' 进行研究...",
                "\n🔍 Running research for '{sub_query}'..."
            ),
            'RESEARCH_STEP_FINALIZED': create_multilang_dict(
                "研究步骤已完成。\n💸 研究总消耗：: {costs}",
                "Finalized research step.\n💸 Total Research Costs: {costs}"
            ),
            'TASK_SUMMARY_COMING_UP': create_multilang_dict(
                "✍️ 正在为研究任务撰写摘要：{query}（这可能需要几分钟时间）...",
                "✍️ Writing summary for research task: {query} (this may take a few minutes)..."
            ),
            'RESEARCHING': create_multilang_dict(
                "🤔 正在通过多个来源查找相关信息...\n",
                "🤔 Researching for relevant information across multiple sources...\n"
            ),
            'SUBTOPICS': create_multilang_dict(
                "📋子主题: {subtopics}",
                "📋Subtopics: {subtopics}"
            ),
            'GENERATING_SUBTOPICS': create_multilang_dict(
                "🤔 正在生成子主题...",
                "🤔 Generating subtopics..."
            ),
            'TASK_SUMMARY_COMING_UP': create_multilang_dict(
                "✍️ 正在撰写研究任务的草稿章节标题: {query}...",
                "✍️ Writing draft section titles for research task: {query}..."
            ),
            'FETCHING_RELEVANT_WRITTEN_CONTENT': create_multilang_dict(
                "🔎 正在根据查询获取相关书面内容: {query}...",
                "🔎 Getting relevant written content based on query: {query}..."
            )
        }

    def get_output(self, key, **kwargs):
        template = self.strings[key][self.lang]
        return template.format(**kwargs)

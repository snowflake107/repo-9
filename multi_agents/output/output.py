# 定义一个函数来生成多语言字典
def create_multilang_dict(zh_text, en_text):
    return {'zh': zh_text, 'en': en_text}

# 定义一个类来管理多语言字符串


class Output:
    def __init__(self, lang='zh'):
        self.lang = lang
        self.strings = {
            'STARTING_RESEARCH': create_multilang_dict(
                "开始对查询 “{query}” 进行研究...",
                "Starting the research process for query '{query}'..."
            ),
            'WRITING_REPORT': create_multilang_dict(
                "根据研究数据撰写最终研究报告...",
                "Writing final research report based on research data..."
            ),
            'REWRITING_LAYOUT': create_multilang_dict(
                "根据指南重新排版布局...",
                "Rewriting layout based on guidelines..."
            ),
            'EDITOR_AGENT_PLANNING': create_multilang_dict(
                "根据初步研究规划大纲布局...",
                "Planning an outline layout based on initial research..."
            ),
            'EDITOR_AGENT_RUNNING': create_multilang_dict(
                "正在并行进行以下研究任务: {queries}...",
                "Running the following research tasks in parallel: {queries}..."
            ),
            'RESEARCHER_RUNNING': create_multilang_dict(
                "正在对以下查询进行初步研究: {queries}...",
                "Running initial research on the following query: {query}"
            ),
            'PARALLEL_RESEARCH': create_multilang_dict(
                "进行以下查询的并行研究: {queries}",
                "Running parallel research for the following queries: {queries}"
            ),
            'INITIAL_RESEARCH': create_multilang_dict(
                "正在对以下查询进行初步研究: {queries}",
                "Running initial research on the following query: {query}"
            ),
            'DEPTH_RESEARCH': create_multilang_dict(
                "正在对以下报告主题进行深入研究: {topic}",
                "Running in depth research on the following report topic: {topic}"
            ),
            'PUBLISHING': create_multilang_dict(
                "基于检索到的数据，正在发布最终研究报告...",
                "Publishing final research report based on retrieved data..."
            ),
            'HUMAN_FEEDBACK_REQUEST': create_multilang_dict(
                "对这个研究主题计划（{layout}）有任何反馈吗? 如果没有，请回复“没有”。\n>> ",
                "Any feedback on this plan of topics to research? {layout}? If not, please reply with 'no'.\n>> "
            ),
            'REVIEW_FEEDBACK': create_multilang_dict(
                "审查反馈为: {response}...",
                "Review feedback is: {response}..."
            ),
            'REVIEW_DRAFT': create_multilang_dict(
                "正在审查草稿...",
                "Reviewing draft..."
            ),
            'REVIEW_GUIDELINES': create_multilang_dict(
                "遵循以下指南 {guidelines}...",
                "Following guidelines {guidelines}..."
            ),
        }

    def get_output(self, key, **kwargs):
        template = self.strings[key][self.lang]
        return template.format(**kwargs)

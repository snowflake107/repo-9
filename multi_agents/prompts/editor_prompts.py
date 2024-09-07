from datetime import datetime

class EditorPrompts:
    @staticmethod
    def get_plan_research_prompt(initial_research, task, human_feedback, lang="zh"):
        include_human_feedback = task.get("include_human_feedback")
        max_sections = task.get("max_sections")
        date_str = datetime.now().strftime('%d/%m/%Y')

        if lang == "zh":
            prompt = [
                {
                    "role": "system",
                    "content": "你是一名研究编辑。你的目标是监督研究项目从开始到完成。你的主要任务是根据初步研究总结来规划文章的章节布局。\n",
                },
                {
                    "role": "user",
                    "content": f"""今天的日期是 {date_str}
                                  研究总结报告: '{initial_research}'
                                  {f'用户反馈: {human_feedback}。你必须根据用户反馈来规划章节。'
            if include_human_feedback and human_feedback and human_feedback != 'no' else ''}
                                  \n你的任务是根据上述研究总结报告生成研究项目的章节标题大纲。
                                  你最多可以生成 {max_sections} 个章节标题。
                                  你必须只专注于相关的研究主题作为子标题，不要包括引言、结论和参考文献。
                                  你必须只返回一个 JSON，其中包含字段 'title'（字符串）和 
                                  'sections'（最多 {max_sections} 个章节标题），结构如下：
                                  '{{title: string 研究标题, date: 今天的日期, 
                                  sections: ['章节标题 1', '章节标题 2', '章节标题 3' ...]}}.""",
                },
            ]
        else:  # Default to English
            prompt = [
                {
                    "role": "system",
                    "content": "You are a research editor. Your goal is to oversee the research project"
                               " from inception to completion. Your main task is to plan the article section "
                               "layout based on an initial research summary.\n ",
                },
                {
                    "role": "user",
                    "content": f"""Today's date is {date_str}
                                      Research summary report: '{initial_research}'
                                      {f'Human feedback: {human_feedback}. You must plan the sections based on the human feedback.'
                if include_human_feedback and human_feedback and human_feedback != 'no' else ''}
                                      \nYour task is to generate an outline of sections headers for the research project
                                      based on the research summary report above.
                                      You must generate a maximum of {max_sections} section headers.
                                      You must focus ONLY on related research topics for subheaders and do NOT include introduction, conclusion and references.
                                      You must return nothing but a JSON with the fields 'title' (str) and 
                                      'sections' (maximum {max_sections} section headers) with the following structure:
                                      '{{title: string research title, date: today's date, 
                                      sections: ['section header 1', 'section header 2', 'section header 3' ...]}}.""",
                },
            ]
        return prompt

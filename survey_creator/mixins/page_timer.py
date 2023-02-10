class PageTimerQuestionMixin:
    def __init__(self, *args, **kwargs):
        self.page_timer_num: int = 1
        super().__init__(*args, **kwargs)

    def add_page_timer_question(self) -> None:
        desc = f'page_timer_{self.page_timer_num}'
        self.page_timer_num += 1

        body = {
            'Choices': {'1': {'Display': 'First Click'},
            '2': {'Display': 'Last Click'},
            '3': {'Display': 'Page Submit'},
            '4': {'Display': 'Click Count'}},
            'Configuration': {'MaxSeconds': '0',
            'MinSeconds': '0',
            'QuestionDescriptionOption': 'UseText'},
            'DataExportTag': desc,
            'DefaultChoices': False,
            'Language': [],
            'QuestionDescription': desc,
            'QuestionText': 'Timing',
            'QuestionText_Unsafe': 'Timing',
            'QuestionType': 'Timing',
            'Selector': 'PageTimer'
            }

        resp = self._make_qualtrics_request(
                    method='post', 
                    endpoint=self.question_url, 
                    json_dump=body,
                    querystring={'blockId': self.last_created_block.block_id}
                )

        self.question_list.append(resp['result']['QuestionID'])
        return resp    
 
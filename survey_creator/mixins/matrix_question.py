class MatrixQuestionMixin:
    def add_matrix_question(self, question_text: str, desc: str) -> None:
        body = self._text_description_question(
                        qtext=question_text,
                        data_export_tag=desc, 
                        question_desc=desc, 
                    )
        
        resp = self._make_qualtrics_request(
                    method='post', 
                    endpoint=self.question_url, 
                    json_dump=body,
                    querystring={'blockId': self.last_created_block.block_id}
                )

        self.question_list.append(resp['result']['QuestionID'])

    @staticmethod
    def _create_matrix_body(qtext: str, data_export_tag: str, question_desc: str) -> dict:
        return {
            'QuestionText': qtext,
            'DefaultChoices': False,
            'DataExportTag': data_export_tag,
            'QuestionType': 'Matrix',
            'Selector': 'Likert',
            'SubSelector': 'SingleAnswer',
            'DataVisibility': {
                'Private': False,
                'Hidden': False
                },
            'Configuration': {
                'QuestionDescriptionOption': 'UseText',
                'TextPosition': 'inline',
                'ChoiceColumnWidth': 25,
                'RepeatHeaders': 'none',
                'WhiteSpace': 'OFF',
                'MobileFirst': True
                },
            'QuestionDescription': question_desc,
            'Choices': {
                '2': {
                    'Display': 'likable'
                    },
                '3': {
                    'Display': 'friendly'
                    },
                '4': {
                    'Display': 'someone you would enjoy chatting with'
                    },
                '5': {
                    'Display': 'someone you would like to be friends with'
                    }
                },
            'ChoiceOrder': ['2', '3', '4', '5'],
            'Validation': {
                'Settings': {
                    'ForceResponse': 'ON',
                    'ForceResponseType': 'ON',
                    'Type': 'None'
                    }
                },
            'Language': [],
            'QuestionID': 'QID469',
            'QuestionText_Unsafe': qtext
        }
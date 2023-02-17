from typing import Callable


class MatrixTemplate:
    """Log matrix bodies"""

    def __init__(self):
        self.template: dict[str, Callable] = {}

    def __getitem__(self, item):
        return self.template[item]

    def add(self, opt):
        def decorator(f):
            self.template[opt] = f
            return f
        return decorator 


class MatrixQuestionMixin:

    matrix_template = MatrixTemplate()

    def add_matrix_question(self, template: int, question_text: str, desc: str, randomization: bool = False) -> dict:
        matrix_func = self.matrix_template[template]

        body = matrix_func(text=question_text, desc=desc, data_export_tag=desc)
        if randomization: body['randomization'] = { "type": "all"}

        resp = self._make_qualtrics_request(
                    method='post', 
                    endpoint=self.question_url, 
                    json_dump=body,
                    querystring={'blockId': self.last_created_block.block_id}
                )

        self.question_list.append(resp['result']['QuestionID'])
        return resp 

    @staticmethod
    @matrix_template.add(1)
    def matrix_question_1(text: str, desc: str, data_export_tag: str) -> dict:
        """
        "choices" are the vertical options (on the left)
        "answers" are the horizontal options (on top)
        """
        return {"Answers":{
                    "1": {
                        "Display": '1-Not At All'
                    },
                    "2": {
                        "Display": '2'
                    },
                    "3": {
                        "Display": '3'
                    },
                    "4": {
                        "Display": '4'
                    },
                    "5": {
                        "Display": '5'
                    },
                    "6": {
                        "Display": '6'
                    },
                    "7": {
                        "Display": '7-Extremely'
                    }
                },
                "AnswerOrder":[
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8
                ],
                "ChoiceDataExportTags": False,
                "ChoiceOrder":[
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8
                ],
                "Choices":{
                    "1": {
                        "Display": 'Happy'
                    },
                    "2": {
                        "Display": 'Friendly'
                    },
                    "3": { 
                        "Display": 'Someone you would enjoy chatting with'
                    },
                    "4": {
                        "Display": 'Calm'
                    },
                    "5": {
                        "Display": 'someone you would like to be friends with'
                    },
                    "6": {
                        "Display": 'Likeable'
                    },
                    "7": {
                        "Display": 'Sad'
                    },
                    "8": {
                        "Display": 'Excited'
                    }
                },
                "Configuration":{
                    "QuestionDescriptionOption":"UseText",
                    "TextPosition":"inline",
                    "ChoiceColumnWidth": 25,
                    "RepeatHeaders":"none",
                    "WhiteSpace":"OFF",
                    "MobileFirst":True,
                    "ChoiceColumnWidthPixels":392
                    },
                "DefaultChoices":False,
                "Language":[],
                "QuestionDescription":desc,
                "QuestionText":text,
                "QuestionType":"Matrix",
                "Selector":"Likert",
                "SubSelector":"SingleAnswer",
                "Validation": {
                    "Settings": {
                        "ForceResponse":"ON",
                        "ForceResponseType":"ON",
                        "Type":"None"
                        }
                    },
                "DataExportTag": data_export_tag
                }
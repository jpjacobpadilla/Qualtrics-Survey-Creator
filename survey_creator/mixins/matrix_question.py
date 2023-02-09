class MatrixQuestionMixin:
    def add_matrix_question() -> None:
        pass

    @staticmethod
    def _create_matrix_body() -> dict:
        return {
            'QuestionText': 'On a scale of 1-7, to what extent is Person 1 ________?',
            'DefaultChoices': False,
            'DataExportTag': '51_conv_like_p1',
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
            'QuestionDescription': 'On a scale of 1-7, to what extent is Person 1 ________?',
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
            'QuestionText_Unsafe': 'On a scale of 1-7, to what extent is Person 1 ________?'
        }
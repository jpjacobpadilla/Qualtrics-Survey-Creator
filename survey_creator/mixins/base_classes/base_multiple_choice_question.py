from typing import Union


class BaseMultipleChoiceQuestion:
    """
    Methods that all multiple choice based question mixins need.

    Currently this is only a staticmethod, but I made it a parent class 
    so that I can easily add more features in the future to multiple 
    choice questions.
    """
    @staticmethod
    def _multiple_choice_question(qtext: str, direction: Union['vertical', 'horizontal'], 
            choices: list[str], desc: str) -> dict:

        f_direction = {'vertical': 'SAVR', 'horizontal': 'SAHR'}
        
        base =  {
            'ChoiceOrder': [],
            'Choices': {},
            'Configuration': {
                'QuestionDescriptionOption': 'UseText'
                },
            'DataExportTag': desc,
            'DataVisibility': {
                'Hidden': False, 
                'Private': False
                },
            'DefaultChoices': False,
            'Language': [],
            'QuestionDescription': desc,
            'QuestionText': qtext,
            'QuestionText_Unsafe': qtext,
            'QuestionType': 'MC',
            'Selector': f_direction[direction],
            'SubSelector': 'TX',
            'Validation': {
                'Settings': {
                    'ForceResponse': 'ON',
                    'ForceResponseType': 'ON',
                    'Type': 'None'
                }
            }
        }

        for index, item in enumerate(choices):
            base['ChoiceOrder'].append(index + 1)
            base['Choices'].append({index + 1: {'Display': item}})

        return base
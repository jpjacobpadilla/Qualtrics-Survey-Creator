import random
from typing import Union
from .base_classes.base_multiple_choice_question import BaseMultipleChoiceQuestion


class AttentionCheckQuestionMixin(BaseMultipleChoiceQuestion):
    
    ac_generic_1 = 'To verify that you are still following along with these questions, please pick "Somewhat disagree" from the list of responses provided below.'
    ac_generic_choices_1 = ['Strongly disagree', 'Somewhat disagree', 'Neither agree nor disagree', 'Somewhat agree', 'Strongly agree']
    ac_generic_2 = '<div>To be sure you are still reading the content of these questions, please select "🌹" from the list of responses below.&nbsp;</div>'
    ac_generic_choices_2 = ['🐔', '👀', '🌹', '👍', '🌻']
    ac_generic_3 = 'To confirm that you are still paying attention to the questions, we kindly ask that you choose "Neither agree nor disagree" from the list of options below.'
    ac_generic_choices_3 = ['Strongly disagree', 'Somewhat disagree', 'Neither agree nor disagree', 'Somewhat agree', 'Strongly agree']
    ac_generic_4 = 'To be sure you are still reading the content of these questions, please select "Somewhat agree" from the list of responses below.'
    ac_generic_choices_4 = ['Strongly disagree', 'Somewhat disagree', 'Neither agree nor disagree', 'Somewhat agree', 'Strongly agree']

    default_ac = {
        1: (ac_generic_1, ac_generic_choices_1),
        2: (ac_generic_2, ac_generic_choices_2),
        3: (ac_generic_3, ac_generic_choices_3),
        4: (ac_generic_4, ac_generic_choices_4)
    }

    def __init__(self, *args, **kwargs):
        self.attention_check_num: int = 1
        super().__init__(*args, **kwargs)
   
    def add_attention_check(self, question_text: str, choices: list, type: str) -> dict:
        """
        Add a multiple choice style attention check.

        The TYPE (str) parameter is used to specify the attention check "Type". 
        This is helpful in determining the answers to the attention checks when 
        once you have collected the data.
        """
        desc = f'attention_check_{self.attention_check_num}_[type_{type}]'
        self.attention_check_num += 1

        body = self._multiple_choice_question(
                qtext=question_text,
                direction = random.choice(('vertical', 'horizontal')),
                choices=choices,
                desc=desc
            )
            
        resp = self._make_qualtrics_request(
                    method='post', 
                    endpoint=self.question_url, 
                    json_dump=body,
                    querystring={'blockId': self.last_created_block.block_id}
                )

        self.question_list.append(resp['result']['QuestionID'])
        return resp  
    
    def add_generic_attention_check(self, opt: Union[1,2,3,4] = None) -> dict:
        """
        Add a multiple choice style attention check.

        You can either specify no arguments, and a random question will be selected 
        from self.default_ac (dict), or you can use the OPT param to specify which default
        option you want.
        """
        if opt is None:
            opt = random.randint(1, 4)

        desc = f'attention_check_{self.attention_check_num}_[type_{opt}g]'
        self.attention_check_num += 1

        body = self._multiple_choice_question(
                qtext=self.default_ac[opt][0],
                direction = random.choice(('vertical', 'horizontal')),
                choices=self.default_ac[opt][1],
                desc=desc
            )
            
        resp = self._make_qualtrics_request(
                    method='post', 
                    endpoint=self.question_url, 
                    json_dump=body,
                    querystring={'blockId': self.last_created_block.block_id}
                )

        self.question_list.append(resp['result']['QuestionID'])
        return resp   
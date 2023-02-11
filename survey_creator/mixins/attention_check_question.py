import random
from .base_classes.base_multiple_choice_question import BaseMultipleChoiceQuestion


class AttentionCheckQuestionMixin(BaseMultipleChoiceQuestion):
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
        desc = f'AC_{self.attention_check_num}_TYPE_{type}'
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
        
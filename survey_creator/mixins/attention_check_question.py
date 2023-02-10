import random
from .base_classes.base_multiple_choice_question import BaseMultipleChoiceQuestion


class AttentionCheckQuestionMixin(BaseMultipleChoiceQuestion):
    def __init__(self, *args, **kwargs):
        self.attention_check_num: int = 1
        super().__init__(*args, **kwargs)
   
    def add_attention_check(self, question_text: str, desc: str, choices: list) -> dict:
        desc = f'Attention_check_{self.attention_check_num}'
        self.attention_check_num += 1

        body = self._multiple_choice_question(
                qtext=question_text,
                direction = random.choice(('vertical', 'horizontal')),
                choices=choices,
                desc=desc
            )
        
from .base_classes.base_multiple_choice_question import BaseMultipleChoiceQuestion


class MultipleChoiceQuestionMixin(BaseMultipleChoiceQuestion):
    def add_mc_question(self, question_text: str, desc: str, 
            choices: list, direction:str) -> dict:
        body = self._multiple_choice_question(
                qtext=question_text,
                direction = direction,
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
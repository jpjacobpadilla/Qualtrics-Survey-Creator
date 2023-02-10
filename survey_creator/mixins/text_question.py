from .base_classes.base_text_question import BaseTextQuestion


class TextQuestionMixin(BaseTextQuestion):
    def add_text_question(self, question_text: str, desc: str) -> None:
        """
        Creates a Qualtrics "text/Graphic" question.
        """
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
        return resp  
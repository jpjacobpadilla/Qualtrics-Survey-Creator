class TextQuestionMixin:
    def add_text_question(self, question_text: str, desc: str) -> None:
        """
        Creates a Qualtrics "text/Graphic" question.
        """
        body = self._text_description_question(
                        qtext=question_text,
                        data_export_tag=desc, 
                        question_desc=desc, 
                        querystring={'blockId': self.last_created_block.block_id}
                    )
        
        resp = self._make_qualtrics_request(
                    method='post', 
                    endpoint=self.question_url, 
                    json_dump=body
                )

        self.question_list.append(resp['result']['QuestionID'])
       
    @staticmethod
    def _text_description_question(qtext: str, data_export_tag: str, question_desc: str) -> dict:
        """Text Description Question definition"""
        return {
            "Configuration": {
                "QuestionDescriptionOption":"UseText"
            },
            "DataExportTag": data_export_tag,
            "Language": [],
            "QuestionDescription": question_desc,
            "QuestionText": qtext,
            "DefaultChoices": False,
            "QuestionType":"DB",
            "Selector":"TB",
            "Validation": {
            "Settings": {
                "ForceResponse": "ON",
                "ForceResponseType": "ON",
                "Type": "None"
                }
            }
        }

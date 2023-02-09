from sqlalchemy import text
from .base_classes.base_text_question import BaseTextQuestion

class ECArticleQuestionMixin(BaseTextQuestion):
    def add_ec_article_text_question(self, question_text: str, desc: str) -> None:
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

    
    @staticmethod
    def _empathic_conversation_article_text_question(self, db):
        query = text('''
        select ai.title, ai.text 
        from article_info as ai
        inner join conversations as c on ai.article_id=c.article_id
        where c.conversation_id = :conv_id
        limit 1;
        ''')
    
        with db.connect() as conn:
            title, article_body = conn.execute(query, {'conv_id': conversation_id}).first()

        formatted_article = article_formatter(number_of_sentences=7, text=article_body)

        resp = requester('post',
                        question_url.format(survey_id_placeholder=survey_id), 
                        text_description_question(
                            qtext=article_text(title, formatted_article),
                            data_export_tag=f'{conversation_id}_article', 
                            question_desc=f'{conversation_id}_article'), 
                        querystring={'blockId': block_id})
        
        q_list.append(resp['result']['QuestionID'])

    


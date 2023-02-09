from sqlalchemy import text
from .base_classes.base_text_question import BaseTextQuestion
from sqlalchemy.engine.base import Engine


class ECArticleQuestionMixin(BaseTextQuestion):
    def add_ec_article_text_question(self, db: Engine, conversation_id: int, desc: str) -> None:
        """
        Creates a Qualtrics "text/Graphic" question.
        """
        query = text('''
        select ai.title, ai.text 
        from article_info as ai
        inner join conversations as c on ai.article_id=c.article_id
        where c.conversation_id = :conv_id
        limit 1;
        ''')
    
        with db.connect() as conn:
            title, article_body = conn.execute(query, {'conv_id': conversation_id}).first()

        formatted_article = self._article_formatter(number_of_sentences=7, text=article_body)

        body = self._text_description_question(
                        qtext=self._article_text(title, formatted_article),
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
    def _article_text(title, body) -> str:
        return f'''<h1 style="line-height: 60px; color: black;"><strong>{title}</strong></h1>&nbsp;<p >{body}</p>'''
    
    @staticmethod
    def _article_formatter(text: str, number_of_sentences: int = 5) -> str:
        """Takes article and returns x number of sentences from top of article"""
        punctuation = ['.', '?', '!']
        new_text = ''
        count = 0
        letter_check = False

        for letter in text.strip():
            new_text += letter

            if letter_check and letter == ' ':
                count += 1

            letter_check = False
            if letter in punctuation:
                letter_check = True

            if count >= number_of_sentences:
                break

        return new_text

    


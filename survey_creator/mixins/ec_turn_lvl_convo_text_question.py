from sqlalchemy import text
from sqlalchemy.engine.base import Engine
import pandas as pd
from pretty_html_table import build_table
from .base_classes.base_text_question import BaseTextQuestion


class ECTurnLVLConvoQuestionMixin(BaseTextQuestion):
    def add_ec_turn_lvl_convo(self, db: Engine, conversation_id: int, desc: str) -> None:
        """
        Creates a Qualtrics "text/Graphic" question.
        """
        sql_query = text('''
        select case speaker
                    when 'Person 2' then 'Person 2'
                    when 'Person 1' then 'Person 1'
               end as Speaker,
               text as Utterance
        from conversations
        where conversation_id = :conv_id
        order by turn_id;
        ''')

        with db.connect() as conn:
            df = pd.read_sql(sql_query, conn, params={'conv_id': conversation_id})

        # https://pypi.org/project/pretty-html-table/
        text_content = build_table(df, 'blue_light', width_dict=['85px','auto'], padding='10px', even_color='black', even_bg_color='white')
        
        for index in range(len(text_content)):
            if index + 2 <= len(text_content) and  text_content[index] == '\\' and text_content[index + 1] != 'n':
                text_content = text_content[:index] + text_content[index + 1:]
                text_content = text_content[:index] + "'" + text_content[index:] 

        body = self._text_description_question(
                        qtext=text_content,
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
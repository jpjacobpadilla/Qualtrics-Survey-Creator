import sys
from sqlalchemy import create_engine
from utils import mod_ten_conversation_id_list
from survey_creator import Creator
from secret import (
    jacob_key, db_pass, 
    db_host, db_schema, 
    db_user
)
from question_text import (
    question_one_text, question_two_P1_text, 
    question_two_P2_text
)


# SQLAlchemy engine for research MySQL server
conn_string = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset:{encoding}'.format(
    user=db_user, 
    password=db_pass, 
    host=db_host, 
    port=3306, 
    db=db_schema,
    encoding = 'utf-8'
)
engine = create_engine(conn_string)

api_key = jacob_key
data_center_id = 'ca1'

# List of survey id's
list_of_survey_ids = ['SURVEY_IDS']

for survey_index, survey_id in enumerate(list_of_survey_ids):
    # This is for the SQL queries to get the correct conversations
    conversation_id_queue = mod_ten_conversation_id_list(survey_index + 1)
    
    sc = Creator(survey_id=survey_id, data_center_id=data_center_id, api_key=api_key)

    # 50 blocks per survey * 10 surveys = 500 blocks (1 per conversation)
    for index in range(1, 51):
        # Get the conversation id for the block
        if not conversation_id_queue.empty():
            conversation_id = conversation_id_queue.get()
            print(f'Conversation ID: {conversation_id}')
        else: 
            print("No more conversation ID's in queue!")
            sys.exit()

        # Create block
        sc.create_block(desc=f'block_{conversation_id}')
        sc.add_text_question(question_text=question_one_text, desc=f'{conversation_id}_intro')
        sc.add_ec_article_text_question(db=engine, conversation_id=conversation_id, desc=f'{conversation_id}_article')
        sc.add_ec_turn_lvl_convo(db=engine, conversation_id=conversation_id, desc=f'{conversation_id}_turn_lvl_convo')
        sc.add_matrix_question(template=1, question_text=question_two_P1_text, desc=f'{conversation_id}_conv_like_p1')
        sc.add_page_timer_question()
        sc.add_page_break_questions()
        sc.add_matrix_question(template=1, question_text=question_two_P1_text, desc=f'{conversation_id}_conv_like_p1')
        sc.add_page_timer_question()
        sc.add_page_break_questions()
        sc.add_matrix_question(template=1, question_text=question_two_P2_text, desc=f'{conversation_id}_conv_like_p2')
        sc.add_page_timer_question()
        break       

print('done!')

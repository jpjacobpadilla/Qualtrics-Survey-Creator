import sys
import concurrent.futures
from sqlalchemy import create_engine
from utils import mod_ten_conversation_id_list
from survey_creator import Creator
from secret import (
    jacob_key, db_pass, 
    db_host, db_schema, 
    db_user
)
from question_text import (
    QUESTION_TWO_PERSON_1_TEXT, 
    QUESTION_TWO_PERSON_2_TEXT,
    AC_2_CHOICES, AC_1_CHOICES,
    AC_2_TEXT, AC_1_TEXT,
    MC_1_TEXT_CHOICES, MC_1_TEXT
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
survey_ids = ['SURVEY_ID','SURVEY_ID','SURVEY_ID']


def create_survey(survey_index):
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
        sc.add_matrix_question(template=1, question_text=QUESTION_TWO_PERSON_1_TEXT, desc=f'{conversation_id}_conv_like_p1')
        if sc.block_counter == 2: sc.add_attention_check(question_text=AC_1_TEXT, choices=AC_1_CHOICES) 
        sc.add_page_timer_question()
        sc.add_page_break_questions()

        if sc.block_counter == 4: sc.add_attention_check(question_text=AC_2_TEXT, choices=AC_2_CHOICES) 
        sc.add_matrix_question(template=1, question_text=QUESTION_TWO_PERSON_2_TEXT, desc=f'{conversation_id}_conv_like_p2')
        if sc.block_counter == 5: sc.add_attention_check(question_text=AC_2_TEXT, choices=AC_2_CHOICES) 
        sc.add_mc_question(question_text=MC_1_TEXT, choices=MC_1_TEXT_CHOICES, direction='horizontal', desc=f'{conversation_id}_mc_1')
        sc.add_page_timer_question()

    sc.apply_generic_flow()


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(create_survey, id) for id in survey_ids]

    # Wait for all futures to finish
    concurrent.futures.wait(futures)

print('done!')

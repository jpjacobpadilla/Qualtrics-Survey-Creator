import concurrent.futures
from sqlalchemy import create_engine
from examples.utils import mod_ten_conversation_id_list
from survey_creator import Creator
from secret import (
    jacob_key, db_pass, 
    db_host, db_schema, 
    db_user
)
from question_text import (
    QUESTION_ONE_TEXT, QUESTION_TWO_PERSON_1_TEXT, 
    QUESTION_TWO_PERSON_2_TEXT
)


def create_survey(survey_info) -> None:
    survey_index = survey_info[0]
    survey_id = survey_info[1]

    # This is for the SQL queries to get the correct conversations
    conversation_id_queue = mod_ten_conversation_id_list(survey_index + 1)
    
    sc = Creator(survey_id=survey_id, data_center_id=data_center_id, api_key=api_key)

    # 50 blocks per survey * 10 surveys = 500 blocks (1 per conversation)
    for _ in range(1, 11):
        # Get the conversation id for the block
        if not conversation_id_queue.empty():
            conversation_id = conversation_id_queue.get()
            print(f'Conversation ID: {conversation_id}')
        else: 
            print("No more conversation ID's in queue!")
            break 

        sc.create_block(desc=f'{conversation_id}_block')
        sc.add_text_question(question_text=QUESTION_ONE_TEXT, desc=f'{conversation_id}_intro')
        sc.add_page_timer_question()
        sc.add_page_break_questions()
        
        sc.add_ec_article_text_question(db=engine, conversation_id=conversation_id, desc=f'{conversation_id}_article')
        sc.add_ec_turn_lvl_convo(db=engine, conversation_id=conversation_id, desc=f'{conversation_id}_turn_lvl_convo')
        sc.add_matrix_question(template=1, question_text=QUESTION_TWO_PERSON_1_TEXT, desc=f'{conversation_id}_conv_like_p1')
        if sc.block_counter == 5: sc.add_generic_attention_check(opt=4) 
        if sc.block_counter == 3: sc.add_generic_attention_check(opt=3) 
        sc.add_matrix_question(template=1, question_text=QUESTION_TWO_PERSON_2_TEXT, desc=f'{conversation_id}_conv_like_p2')
        if sc.block_counter == 2: sc.add_generic_attention_check(opt=2) 
        if sc.block_counter in (1, 4): sc.add_generic_attention_check(opt=1) 
        sc.add_page_timer_question()

    sc.apply_flow_with_template()


# SQLAlchemy engine for research MySQL server
conn_string = 'mysql://{user}:{password}@{host}:{port}/{db}?charset:{encoding}'.format(
    user=db_user, 
    password=db_pass, 
    host=db_host, 
    port=3306, 
    db=db_schema,
    encoding = 'utf-8')
engine = create_engine(conn_string)

api_key = jacob_key
data_center_id = 'ca1'

# List of survey ids
survey_ids = ['SURVEY_ID','SURVEY_ID','SURVEY_ID']

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(create_survey, (index, id)) for index, id in enumerate(survey_ids)]

    # Wait for all futures to finish
    concurrent.futures.wait(futures)

print('done!')

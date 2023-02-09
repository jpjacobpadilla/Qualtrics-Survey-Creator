from survey_creator import Creator
from secret import (
    jacob_key, db_pass, 
    db_host, db_schema, 
    db_user
)
from sqlalchemy import create_engine

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
list_of_survey_ids = []

# for survey_index, survey_id in enumerate(list_of_survey_ids):
#     sc = creator(survey_id=survey_id)

#     # range(50) becuase 50 blocks are made per survey. 
#     # 50 blocks per survey * 10 surveys = 500 blocks (1 per convo)
#     for _ in range(50):
#         # Create block
#         sc.create_block()

#         # Add questions to the last_created_block
#         sc.add_question()
#         sc.add_question()
#         sc.add_question()
#         sc.add_question()

#         # Update block to add page breaks AND move timing questions to the correct place
#         sc.compile_block()

#     sc.apply_flow()

# print('done!')

sc = Creator(
    survey_id='SV_cFODjwlDXy7fybc',
    data_center_id=data_center_id,
    api_key=api_key
    )
sc.create_block(desc='BLOCK_test')
print(sc.blocks)
print(sc.block_counter)
print(sc.last_created_block)
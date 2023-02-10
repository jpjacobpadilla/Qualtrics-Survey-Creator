import json
import requests
from collections import namedtuple

from .exceptions import RequestFailed

from .mixins.create_block import CreateBlockMixin
from .mixins.text_question import TextQuestionMixin
from .mixins.matrix_question import MatrixQuestionMixin
from .mixins.attention_check_question import AttentionCheckQuestionMixin
from .mixins.page_timer import PageTimerQuestionMixin
from .mixins.page_break import PageBreakQuestionMixin
from .mixins.multiple_choice_question import MultipleChoiceQuestionMixin
from .mixins.ec_article_question import ECArticleQuestionMixin
from .mixins.ec_turn_lvl_convo_text_question import ECTurnLVLConvoQuestionMixin
from .mixins.apply_flow import ApplyFlowMixin

class Creator(
    CreateBlockMixin,
    TextQuestionMixin,
    ECArticleQuestionMixin,
    ECTurnLVLConvoQuestionMixin,
    MatrixQuestionMixin,
    AttentionCheckQuestionMixin,
    PageTimerQuestionMixin,
    PageBreakQuestionMixin,
    MultipleChoiceQuestionMixin,
    ApplyFlowMixin
    ):
    """
    This object handles the creation of single survey

    The first method called should be create_block(). This will
    then allow you to create questions, which will be added to the block.
    
    When you create a block, it is added to self.block, which is 
    essentially a way to sort the blocks into 5 buckets. When you apply flow to the blocks,
    the idea is that there will be 5 "randomizer flow blocks" in Qualtrics, and thus a worker will see
    one random block from each of the 5 blocks. This allows you to easily control where attention checks are shown.


    Instance Attributes:
        survey_id: 
            The Qualtrics survey id (used to send requests to Qualtrics).
        base_url: 
            Qualtrics base url for requests.
        api_key: 
            Qualtrics api key.
        headers: 
            Headers for the Qualtrics API.

        ** Created in mixin classes **

        blocks: 
            Each Qualtrics block is put into a "bucket" so that the blocks can 
            be given flow in the flow function later
            A worker will see one question from block 1, then block 2, etc...
            The 50 Qualtrics blocks are chunked into 5 sections so that some 
            sections can have attention checks in them.
        block_counter: 
            This keeps track of what block the creator is on. 
            This is used to then know which block bucket to 
            put the Qualtrics block into.
        last_created_block: 
            when create_block() is called, last_created_block 
            will be set to that block.
        last_block_desc:
            The last block description
        question_list:
            When a new block is created, the question_list is reset. When you 
            add a question, the question id is added to this list.
        page_timer_num:
            All page time questions have a incrementing description.
        page_break_num:
            All page break questions have a incrementing description.
        attention_check_num:
            All attention check questions have a incrementing description.


    Class Attributes:
        blocks_url: 
            A Qualtrics endpoint. Use to create blocks.
        question_url: 
            A Qualtrics endpoint. Use to create questions.
        flow_url:
            A Qualtrics endpoint. Use to apply flow.

        ** Created in mixin classes **

        matrix_func:
            You can't make a dynamic matrix question request body because there 
            are a lot of different options. matrix_func is a instance of the MatrixTemplate class.
            You can register new matrix body options via this object. You can then retrieve the callable
            body functions via: self.matrix_template[template_number]
    """

    # Qualtrics endpoints
    blocks_url = 'survey-definitions/{survey_id_placeholder}/blocks'
    question_url = 'survey-definitions/{survey_id_placeholder}/questions'
    flow_url = 'survey-definitions/{survey_id_placeholder}/flow'

    def __init__(
            self, 
            survey_id: str, 
            data_center_id: str, 
            api_key: str, 
            *args,
            **kwargs
            ):
        self.survey_id: str = survey_id

        # Qualtrics base url
        self.base_url = f'https://{data_center_id}.qualtrics.com/API/v3/'

        # Qualtrics common headers
        self.headers = {
            'X-API-TOKEN': api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        super().__init__(*args, **kwargs)
    
    def _make_qualtrics_request(self, method: str, endpoint: str, json_dump, **kwargs):
        """
        Makes a request to Qualtrics

        Params:
            method: 
                HTTP request method
            endpoint: 
                One of the two class vars. This method will automatically
                add the current survey_id
            json_dump: 
                Data to be turned into json
            
            **kwargs: 
                querystring: 
                    This is usually the block_id 
        """
        assert method.lower() in ['post', 'put', 'get', 'delete'], 'Invalid request method.'

        endpoint = endpoint.format(survey_id_placeholder=self.survey_id)

        response = requests.request(
                method.lower(),
                self.base_url + endpoint + kwargs.get('extra_endpoint', ''), 
                data = json.dumps(json_dump), 
                headers = self.headers, 
                params = kwargs.get('querystring', None),
            )

        print(response.text)

        if response.status_code == 200:
            return response.json()
            
        else:
            raise RequestFailed 
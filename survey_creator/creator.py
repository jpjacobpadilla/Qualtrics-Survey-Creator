import json
import threading
from collections import namedtuple
import requests
from .exceptions import RequestFailed
from .mixins.create_block import CreateBlockMixin
from .mixins.multiple_choice_question import MultipleChoiceQuestionMixin
from .mixins.text_question import TextQuestionMixin
from .mixins.likart_question import LikartQuestionMixin


class Creator(
    CreateBlockMixin,
    MultipleChoiceQuestionMixin,
    TextQuestionMixin,
    LikartQuestionMixin,
    threading.Thread
    ):
    """
    This object handles the creation of single survey

    The general steps for creating one survey:
        1. Create 50 blocks per survey 
        2. Add questions to block
        3. Apply randomized flow

    This class inherits from the threading class, so that
    multiple surveys can be made at the same time.

    The first method called should be create_block(). This will
    then allow you to create questions, which will be added to the block.

    Instance Attributes:
        survey_id: the Qualtrics survey id (used to send requests to Qualtrics)
        blocks: Each Qualtrics block is put into a "bucket" so that the blocks can 
                be given flow in the flow function later
                A worker will see one question from block 1, then block 2, etc...
                The 50 Qualtrics blocks are chunked into 5 sections so that some 
                sections can have attention checks in them.
        block_counter: This keeps track of what block the creator is on. 
                       This is used to then know which block bucket to 
                       put the Qualtrics block into.
        last_created_block: when create_block() is called, last_created_block 
                            will be set to that block.
        base_url: Qualtrics base url for requests
        api_key: Qualtrics api key
        logger: A logging object that works.
        request_session: request.Session()

    Class Attributes:
        blocks_url: A Qualtrics endpoint. Use to create blocks.
        question_url: a Qualtrics endpoint. Use to create questions
    """

    # Qualtrics endpoints
    blocks_url = 'survey-definitions/{survey_id_placeholder}/blocks'
    question_url = 'survey-definitions/{survey_id_placeholder}/questions'

    def __init__(
            self, 
            survey_id: str, 
            data_center_id: str, 
            api_key: str, 
            *args,
            **kwargs
            ):
        self.survey_id: str = survey_id

        # Block stuff
        self.blocks: dict = {
            1: [], 
            2: [], 
            3: [], 
            4: [], 
            5: []
        }
        self.block_counter: int = 1
        self.last_created_block: str = None
        
        # question list for each block
        self.question_list = []

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
            method: HTTP request method
            endpoint: One of the two class vars. This method will automatically
                      add the current survey_id
            json_dump: data to be turned into json
            
            **kwargs: 
                querystring: This is usually the block_id 
        """
        assert method.lower() in ['post', 'put', 'get', 'delete'], 'Invalid request method.'

        endpoint = endpoint.format(survey_id_placeholder=self.survey_id)

        response = requests.request(
                method.lower(),
                self.base_url + endpoint, 
                data = json.dumps(json_dump), 
                headers = self.headers, 
                params = kwargs.get('querystring', None),
            )

        print(response.text)

        if response.status_code == 200:
            return response.json()
            
        else:
            raise RequestFailed 
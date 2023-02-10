from survey_creator.utils import block_info


class CreateBlockMixin:
    def __init__(self, *args, **kwargs):
        self.last_block_desc = None
        self.question_list = None
        self.blocks: dict = {1: [], 2: [], 3: [], 4: [], 5: []}
        self.block_counter: int = 0
        self.last_created_block: str = None

        super().__init__(*args, **kwargs)
        
    def create_block(self, desc: str) -> dict:
        self.last_block_desc = desc

        """
        Creates a Qualtrics block and assigns self.last_created_block to the 
        block just created, increments block_counter, 
        and adds block to self.blocks
        """
        resp = self._make_qualtrics_request(
                    method='post', 
                    endpoint=self.blocks_url, 
                    json_dump=self._block_body(desc=desc)
                )
        block_id = resp['result']['BlockID']
        flow_id = 'FL_' + str(int(resp['result']['FlowID'].split('_')[-1]) + 101)

        temp_block_info = block_info(block_id, flow_id)
        
        self.block_counter = self.block_counter % 5 + 1
        self.blocks[self.block_counter].append(temp_block_info)
        self.last_created_block = temp_block_info

        self.question_list = []

        return resp 

    @staticmethod
    def _block_body(desc) -> dict:
        return {
            "Type": "Standard",
            "Description": desc
            }

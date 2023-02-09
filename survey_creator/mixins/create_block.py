from survey_creator.utils import block_info


class CreateBlockMixin:
    def create_block(self, desc: str) -> None:
        """
        Creates a Qualtrics block and assigns self.last_created_block to the 
        block just created, incraments block_counter, 
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
        self.blocks[self.block_counter] = temp_block_info
        self.block_counter = self.block_counter % 5 + 1
        self.last_created_block = temp_block_info

    @staticmethod
    def _block_body(desc) -> dict:
        return {
            "Type": "Standard",
            "Description": desc
            }

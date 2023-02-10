from survey_creator.utils import block_info


class ApplyFlowMixin:
    """
    Qualtrics "flow" is how the flow of questions in the survey is controlled.

    By apply flow to the 5 block buckets, we can make sure that
    a survey taker will only see one question from each block.
    """

    def apply_generic_flow(self) -> dict:
        body = self.flow_request_body()

        resp = self._make_qualtrics_request(
                    method='put', 
                    endpoint=self.flow_url, 
                    json_dump=body
                )

        return resp

    def flow_request_body(self):
        
        return {'Flow': [{'Autofill': [],
            'FlowID': 'FL_1',
            'ID': 'BL_2gARGw3jgJSAMSO',
            'Type': 'Standard'},
        {'EvenPresentation': True,
            'FlowID': 'FL_2',
            'Flow': self._add_flow_elements(self.blocks[1]),
            'SubSet': 1,
            'Type': 'BlockRandomizer'},
        {'EvenPresentation': True,
            'FlowID': 'FL_3',
            'Flow': self._add_flow_elements(self.blocks[2]),
            'SubSet': 1,
            'Type': 'BlockRandomizer'},
        {'EvenPresentation': True,
            'FlowID': 'FL_4',
            'Flow': self._add_flow_elements(self.blocks[3]),
            'SubSet': 1,
            'Type': 'BlockRandomizer'},
        {'EvenPresentation': True,
            'FlowID': 'FL_5',
            'Flow': self._add_flow_elements(self.blocks[4]),
            'SubSet': 1,
            'Type': 'BlockRandomizer'},
            {'EvenPresentation': True,
            'FlowID': 'FL_6',
            'Flow': self._add_flow_elements(self.blocks[5]),
            'SubSet': 1,
            'Type': 'BlockRandomizer'},
        {'Autofill': [],
            'FlowID': 'FL_7',
            'ID': 'BL_cYITtIPjSaPzbWm',
            'Type': 'Standard'},
        {'Autofill': [],
            'FlowID': 'FL_8',
            'ID': 'BL_dmuTtZcIWxMqM3s',
            'Type': 'Standard'},
        {'EmbeddedData': [{'AnalyzeText': False,
            'DataVisibility': [],
            'Description': 'MTurkCode',
            'Field': 'MTurkCode',
            'Type': 'Custom',
            'Value': '${rand://int/0:999999999}',
            'VariableType': 'String'}],
            'FlowID': 'FL_9',
            'Type': 'EmbeddedData'},
        {'EmbeddedData': [{'AnalyzeText': False,
            'DataVisibility': [],
            'Description': 'workerId',
            'Field': 'workerId',
            'Type': 'Recipient',
            'VariableType': 'String'},
            {'AnalyzeText': False,
            'DataVisibility': [],
            'Description': 'assignmentId',
            'Field': 'assignmentId',
            'Type': 'Recipient',
            'VariableType': 'String'},
            {'AnalyzeText': False,
            'DataVisibility': [],
            'Description': 'hitId',
            'Field': 'hitId',
            'Type': 'Recipient',
            'VariableType': 'String'}],
            'FlowID': 'FL_10',
            'Type': 'EmbeddedData'}],
        'FlowID': 'FL_1',
        'Properties': {'Count': 19, 'RemovedFieldsets': []},
        'Type': 'Root'}

    @staticmethod
    def _add_flow_elements(elements: list[block_info]) -> list:
        _placeholder = []

        for elem in elements:
            block_id, flow_id = elem
            _placeholder.append({
                "Type":"Standard",
                "Autofill": [],
                "ID": block_id,
                "FlowID": flow_id
            })
            
        return _placeholder
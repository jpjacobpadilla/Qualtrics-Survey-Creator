from survey_creator.utils import block_info


class ApplyFlowMixin:
    """
    Qualtrics "flow" is how the flow of questions in the survey is controlled.

    By apply flow to the 5 block buckets, we can make sure that
    a survey taker will only see one question from each block.
    """

    def apply_generic_flow(self) -> dict:
        resp = self._make_qualtrics_request(
                    method='put', 
                    endpoint=self.flow_url, 
                    json_dump=self.flow_request_body()
                )
        return resp

    def apply_flow_with_template(self) -> dict:
        """
        This is to apply flow to a Qualtrics survey with the template that we
        have been using. It includes the starting and ending questions.
        """
        resp = self._make_qualtrics_request(
                    method='put', 
                    endpoint=self.flow_url, 
                    json_dump=self.flow_request_body_with_template()
                )
        return resp

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

    @staticmethod
    def flow_request_body_with_template(self) -> dict:
        return {
        'Flow': [
        {'Autofill': [],
            'FlowID': 'FL_1',
            'Type': 'Standard'
        },
        {
            "Type": "Branch",
            "FlowID": "FL_2",
            "Description": "New Branch",
            "BranchLogic": {
                "0": {
                    "0": {
                        "LogicType": "Question",
                        "QuestionID": "QID60",
                        "QuestionIsInLoop": "no",
                        "ChoiceLocator": "q://QID60/SelectableChoice/2",
                        "Operator": "Selected",
                        "QuestionIDFromLocator": "QID60",
                        "LeftOperand": "q://QID60/SelectableChoice/2",
                        "Type": "Expression",
                        "Description": "<span class=\"ConjDesc\">If</span> <span class=\"QuestionDesc\">Empathy and Well-Being Study &nbsp; Study Contacts: Study Contact:&nbsp;Jo\u00e3o Sedoc; 215-746-5085; joao@upen...</span> <span class=\"LeftOpDesc\">I do not agree to participate in this research.</span> <span class=\"OpDesc\">Is Selected</span> "
                    },
                    "Type": "If"
                },
                "Type": "BooleanExpression"
            },
            "Flow": [
                {
                    "Type": "EndSurvey",
                    "FlowID": "FL_3",
                    "EndingType": "Advanced",
                    "Options": {
                        "Advanced": "true",
                        "SurveyTermination": "DisplayMessage",
                        "EOSMessageLibrary": "UR_1NCwWqyejOMbZgG",
                        "EOSMessage": "MS_bjgIpXolXlCpqn4"
                    }
                }
            ]
        },
        {'EvenPresentation': True,
            'FlowID': 'FL_4',
            'Flow': self._add_flow_elements(self.blocks[1]),
            'SubSet': 1,
            'Type': 'BlockRandomizer'},
        {'EvenPresentation': True,
            'FlowID': 'FL_5',
            'Flow': self._add_flow_elements(self.blocks[2]),
            'SubSet': 1,
            'Type': 'BlockRandomizer'},
        {'EvenPresentation': True,
            'FlowID': 'FL_6',
            'Flow': self._add_flow_elements(self.blocks[3]),
            'SubSet': 1,
            'Type': 'BlockRandomizer'},
        {'EvenPresentation': True,
            'FlowID': 'FL_7',
            'Flow': self._add_flow_elements(self.blocks[4]),
            'SubSet': 1,
            'Type': 'BlockRandomizer'},
        {'EvenPresentation': True,
            'FlowID': 'FL_8',
            'Flow': self._add_flow_elements(self.blocks[5]),
            'SubSet': 1,
            'Type': 'BlockRandomizer'},
        {'Autofill': [],
            'FlowID': 'FL_9',
            'ID': 'BL_cYITtIPjSaPzbWm',
            'Type': 'Standard'},
        {'Autofill': [],
            'FlowID': 'FL_10',
            'ID': 'BL_dmuTtZcIWxMqM3s',
            'Type': 'Standard'},
        {'EmbeddedData': [
            {'AnalyzeText': False,
            'DataVisibility': [],
            'Description': 'MTurkCode',
            'Field': 'MTurkCode',
            'Type': 'Custom',
            'Value': '${rand://int/0:999999999}',
            'VariableType': 'String'
            }],
            'FlowID': 'FL_11',
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
            'FlowID': 'FL_12',
            'Type': 'EmbeddedData'}],
        'FlowID': 'FL_1',
        'Type': 'Root'}

    @staticmethod
    def flow_request_body(self) -> dict:
        return {
        'Flow': [
            {
                'EvenPresentation': True,
                'FlowID': 'FL_2',
                'Flow': self._add_flow_elements(self.blocks[1]),
                'SubSet': 1,
                'Type': 'BlockRandomizer'},
            {
                'EvenPresentation': True,
                'FlowID': 'FL_3',
                'Flow': self._add_flow_elements(self.blocks[2]),
                'SubSet': 1,
                'Type': 'BlockRandomizer'},
            {
                'EvenPresentation': True,
                'FlowID': 'FL_4',
                'Flow': self._add_flow_elements(self.blocks[3]),
                'SubSet': 1,
                'Type': 'BlockRandomizer'},
            {
                'EvenPresentation': True,
                'FlowID': 'FL_5',
                'Flow': self._add_flow_elements(self.blocks[4]),
                'SubSet': 1,
                'Type': 'BlockRandomizer'},
            {
                'EvenPresentation': True,
                'FlowID': 'FL_6',
                'Flow': self._add_flow_elements(self.blocks[5]),
                'SubSet': 1,
                'Type': 'BlockRandomizer'}
        ],
        'FlowID': 'FL_1',
        'Type': 'Root'
        }

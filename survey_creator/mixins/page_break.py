class PageBreak:
    def __init__(self, *args, **kwargs):
        self.page_break_num: int = 1
        super().__init__(*args, **kwargs)

    def add_page_break(self):

        base = {'Type':'Standard',
                "Description": self.last_block_desc,
                "BlockElements": [],
                'Options': {
                'BlockLocking': 'false',
                'BlockVisibility': 'Collapsed'
                }
                }

        for question in self.question_list:
            question_dict = {"Type": "Question", "QuestionID": question}
            base['BlockElements'].append(question_dict)
        
        base['BlockElements'].append({"Type": "Page Break"})

        import json
        print(json.dumps(base, indent=4))

        resp = self._make_qualtrics_request(
            method='put', 
            endpoint=self.blocks_url, 
            json_dump=base,
            extra_endpoint=f'/{self.last_created_block.block_id}'
            )

        return resp 


    def block_compiler(desc, q_list, block_counter):
        base = {'Type':'Standard',
                "Description": desc,
                "BlockElements": [
                {"Type": "Question", "QuestionID": q_list[0]},
                {"Type": "Question", "QuestionID": q_list[8]}, # Timing
                {"Type": "Page Break"},                        # Page break
                {"Type": "Question", "QuestionID": q_list[1]},
                {"Type": "Question", "QuestionID": q_list[2]},
                {"Type": "Question", "QuestionID": q_list[3]},
                {"Type": "Question", "QuestionID": q_list[4]},
                {"Type": "Question", "QuestionID": q_list[9]}, # Timing
                {"Type": "Page Break"},                        # Page break
                {"Type": "Question", "QuestionID": q_list[5]},
                {"Type": "Question", "QuestionID": q_list[6]},
                {"Type": "Question", "QuestionID": q_list[7]},
                {"Type": "Question", "QuestionID": q_list[10]}, # Timing
                ],
                'Options': {
                'BlockLocking': 'false',
                'BlockVisibility': 'Collapsed',
                'Randomization': {
                    'Advanced': {
                    'FixedOrder': 
                    [q_list[0],
                        q_list[8],
                        q_list[1],
                        q_list[2],
                        '{~Randomized~}',
                        '{~Randomized~}',
                        q_list[9],
                        q_list[5],
                        q_list[6],
                        q_list[7],
                        q_list[10]],
                    'QuestionsPerPage': 0,
                    'RandomSubSet': [],
                    'RandomizeAll': [q_list[3], q_list[4]],
                    'TotalRandSubset': 0,
                    'Undisplayed': []},
                    'EvenPresentation': False
                    },
                'RandomizeQuestions': 'Advanced'}
                }
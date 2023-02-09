class BaseTextQuestion:
    """methods that all text based question mixins need"""
    
    @staticmethod
    def _text_description_question(qtext: str, data_export_tag: str, question_desc: str) -> dict:
        """Text Description Question definition"""
        return {
            "Configuration": {
                "QuestionDescriptionOption":"UseText"
            },
            "DataExportTag": data_export_tag,
            "Language": [],
            "QuestionDescription": question_desc,
            "QuestionText": qtext,
            "DefaultChoices": False,
            "QuestionType":"DB",
            "Selector":"TB",
            "Validation": {
            "Settings": {
                "ForceResponse": "ON",
                "ForceResponseType": "ON",
                "Type": "None"
                }
            }
        }
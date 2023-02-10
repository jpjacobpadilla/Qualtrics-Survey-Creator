class BaseTextQuestion:
    """
    Methods that all text based question mixins need.
    
    Currently this is only a staticmethod, but I made it a parent class 
    so that I can easily add more features in the future to text
    based questions.
    """
    
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
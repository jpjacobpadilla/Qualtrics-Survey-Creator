# **Qualtrics Survey Creator**

### **Mixin Classes**
1. CreateBlockMixin
2. TextQuestionMixin
3. ECArticleQuestionMixin
4. ECTurnLVLConvoQuestionMixin
5. MatrixQuestionMixin
6. AttentionCheckQuestionMixin
7. PageTimerQuestionMixin
8. PageBreakQuestionMixin
9. MultipleChoiceQuestionMixin
10. ApplyFlowMixin

### Mixin Parent Classes
1. BaseMultipleChoiceQuestion
2. BaseTextQuestion

### Installation & Instructions

Download the code:
```bash
git clone https://github.com/jpjacobpadilla/Qualtrics-Survey-Creator.git
```

Navigate to the Repository Directory:
```
cd Qualtrics-Survey-Creator
```

Make some sort of environment:
```bash
python -m venv venv
source venv/bin/activate
```

Install the package in editable mode so that you can make changes to it:
```bash
pip install -e .
```

### Missing files

```secret.py``` - Program secrets - Keeps the Qualtrics API key and database credentials.

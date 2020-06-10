from django import forms
from .models import Question, Answer

class PostQuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        
        exclude = ['created_date', 'user']

class PostAnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['answer_desc']
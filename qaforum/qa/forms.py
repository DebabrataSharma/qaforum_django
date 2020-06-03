from django import forms
from .models import Question, Answer

class PostQuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        
        exclude = ['date_of_add', 'user']

class PostAnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['answer_desc']
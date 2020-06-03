from django.shortcuts import render
from qa.models import Question
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    question = Question.objects.all()
    paginator = Paginator(question, 3)
    page = request.GET.get('page')
    question = paginator.get_page(page)
    context = {'question':question}
    return render(request,'home.html', context)
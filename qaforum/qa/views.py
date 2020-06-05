from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sessions.models import Session
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Question, Answer
from .forms import PostQuestionForm, PostAnswerForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import date
from django.urls import reverse
from django.views import View
from django.contrib.auth import get_user_model
from taggit.models import Tag
from algoliasearch_django import raw_search
from django.http import HttpResponse
import json
from .tasks import celery_task
from django.views.decorators.csrf import csrf_exempt




User = get_user_model()
index_name = 'qa'

@login_required(login_url="/user/login/")
def post_question(request):
    """
    Url for post question.

    :http relative-url: /qa/question/add
    :http-method : POST
    """
    if request.method=='POST':
        form = PostQuestionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.date_of_add = date.today()
            post.save()
            form.save_m2m()
            return redirect('home:home')
    
    form = PostQuestionForm()
    templates = 'add_question.html'
    context = {'form':form }

    return render(request, templates, context)


@login_required(login_url="/user/login/")
def my_questions(request):
    """
    Url for user's question.

    :http relative-url: /qa/my_questions
    :http-method : GET
    """
    questions = Question.objects.filter(user=request.user)        
    context = {'question': questions}
    return render(request, 'my_questions.html', context)

def tag_result(request, slug):
    """
    Url for tag-sort.

    :http relative-url: /qa/question/tag/<tag-slug>
    :http-method : GET
    """
    tag = get_object_or_404(Tag, slug=slug)
    question = Question.objects.filter(tags=tag)
    context = {'tags':  tag, 'question': question}
    return render(request, 'tag_result.html', context)


@login_required(login_url="/user/login/")   
def update_question(request, id):
    """
    Url for user's question update.

    :http relative-url: /qa/questions/<q_id>/edit
    :http-method : POST
    """
    ques_obj = get_object_or_404(Question, id=id)

    if request.user == ques_obj.user:
        form = PostQuestionForm(request.POST or None, instance=ques_obj)

        if request.method=="POST":
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.date_of_add = date.today()
                post.save()
                form.save_m2m()
                return redirect('qa:my_questions')
        
        context = {'form':form}
        return render(request, 'edit_question.html', context)
    else:
        return redirect('home:home')


@login_required(login_url="/user/login/")   
def delete_question(request, id):
    """
    Url for user's question delete.

    :http relative-url: /qa/questions/<q_id>/delete
    :http-method : POST
    """
    question = Question.objects.get(id=id)
    if request.user==question.user:
        question.delete()
        return redirect('qa:my_questions')
    else:
        return redirect('home:home')


def get_answers(request, id):
    """
    Url for get answers to a question.

    :http relative-url: /qa/questions/<q_id>/answers
    :http-method : GET
    """
    question = Question.objects.get(id=id)
    answer = Answer.objects.filter(ques=question)
    context = {'question': question, 'answers':answer}
    return render(request, 'answers.html', context )

@login_required(login_url="/user/login/")   
def post_answer(request, id):
    """
    Url for post answer to a question.

    :http relative-url: /qa/questions/<q_id>/answers
    :http-method : POST
    """
    question = Question.objects.get(id=id)
    if request.method=='POST':
        form = PostAnswerForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.ques = question
            post.date_of_add = date.today()
            post.save()
            return redirect('home:home')
    form = PostAnswerForm()
    context = {'form':form, 'question':question}
    return render(request, 'add_answer.html',context)

@login_required(login_url="/user/login/")   
def my_answers(request):
    """
    Url for user's answers.

    :http relative-url: /qa/my_answers
    :http-method : GET
    """
    answers = Answer.objects.filter(user=request.user)        
    context = {'answer': answers}
    return render(request, 'my_answers.html', context)

@login_required(login_url="/user/login/")   
def update_answer(request, id):
    """
    Url for user's answers update.

    :http relative-url: /qa/answer/<id>/edit
    :http-method : POST
    """
    ans_obj = get_object_or_404(Answer, id=id)
    if request.user == ans_obj.user:
        
        form = PostAnswerForm(request.POST or None, instance=ans_obj)

        if request.method=="POST":
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.ques = ans_obj.ques
                post.date_of_add = date.today()
                post.save()
                return redirect('qa:my_answers')
        
        context = {'form':form, 'answer':ans_obj}
        return render(request, 'edit_answer.html', context)
    else:
        return redirect('home:home')

        
@login_required(login_url="/user/login/")   
def delete_answer(request, id):
    """
    Url for user's answers delete.

    :http relative-url: /qa/answer/<id>/delete
    :http-method : POST
    """
    answer = Answer.objects.get(id=id)
    if request.user==answer.user:
        answer.delete()
        return redirect('qa:my_answers')
    else:
        return redirect('home:home')

def search(request):
    """
    Url for search.

    :http relative-url: /qa/search
    :http-method : GET
    """
    query = request.GET.get('q')
    params = { "hitsPerPage": 5 }
    response = raw_search(Question, query, params)    
    context = {'result': response}
    return render(request, 'search_result.html', context)


def download_json_data(request):
    """
    Url to download user's data.

    :http relative-url: /qa/download_json_data
    :http-method : POST
    """
    user = request.user
    task = celery_task.delay(user.id, 1)
    return HttpResponse(task.task_id)    


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
from .tasks import long_task
from django.views.decorators.csrf import csrf_exempt



User = get_user_model()
index_name = 'qa'

# search part

@login_required(login_url="/user/login/")
def post_question(request):

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
    questions = Question.objects.filter(user=request.user)        
    context = {'question': questions}
    # print(questions)
    return render(request, 'my_questions.html', context)

def tag_result(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    question = Question.objects.filter(tags=tag)
    context = {'tags':  tag, 'question': question}
    # print(tag)
    # print('\n\n', question)
    return render(request, 'tag_result.html', context)


@login_required(login_url="/user/login/")   
def update_question(request, id):
    ques_obj = get_object_or_404(Question, id=id)
    # print("qqqqqqqqq", ques_obj)
    # print (request.user, type(request.user))
    # print(ques_obj.user, type(ques_obj.user))
    # question = Question.objects.filter(id=q_id)
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
    question = Question.objects.get(id=id)
    if request.user==question.user:
        question.delete()
        return redirect('qa:my_questions')
    else:
        return redirect('home:home')


def get_answers(request, id):
    question = Question.objects.get(id=id)
    answer = Answer.objects.filter(ques=question)
    context = {'question': question, 'answers':answer}
    return render(request, 'answers.html', context )

@login_required(login_url="/user/login/")   
def post_answer(request, id):
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
    answers = Answer.objects.filter(user=request.user)        
    context = {'answer': answers}
    return render(request, 'my_answers.html', context)

@login_required(login_url="/user/login/")   
def update_answer(request, id):
    ans_obj = get_object_or_404(Answer, id=id)
    # print("qqqqqqqqq", ans_obj)
    # print (request.user, type(request.user))
    # print(ans_obj.user, type(ans_obj.user))
    # question = Question.objects.filter(id=q_id)
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
    answer = Answer.objects.get(id=id)
    if request.user==answer.user:
        answer.delete()
        return redirect('qa:my_answers')
    else:
        return redirect('home:home')

def search(request):
    query = request.GET.get('q')
    print(query)
    params = { "hitsPerPage": 5 }
    response = raw_search(Question, query, params)
    print(response)
      
    context = {'result': response}
    return render(request, 'search_result.html', context)


# def taskstatus(task_id):
#     task = long_task.AsyncResult(task_id)
#     if task.state == 'PENDING':
#         # job did not start yet
#         response = {
#             'state': task.state,
#             'current': 0,
#             'total': 1,
#             'status': 'Pending...'
#         }
#     elif task.state != 'FAILURE':
#         response = {
#             'state': task.state,
#             'current': task.info.get('current', 0),
#             'total': task.info.get('total', 1),
#             'status': task.info.get('status', '')
#         }
#         if 'result' in task.info:
#             response['result'] = task.info['result']
#     else:
#         # something went wrong in the background job
#         response = {
#             'state': task.state,
#             'current': 1,
#             'total': 1,
#             'status': str(task.info),  # this is the exception raised
#         }
#     print("asdasd", response)
#     return response

def download_json_data(request):
    
    user = request.user
    task = long_task.delay(user.id)
    # print("............",task,task.id)
    # location = taskstatus(task.id)
    # print(location)
    # print("yeiiiiiii")    
    return redirect('home:home') 
    


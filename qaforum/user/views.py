from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from qa.models import Question, Answer
from django.contrib.auth.decorators import login_required




# Create your views here.
def signup_view(request):
    """
    Url to user's sign up page.

    :http relative-url: /user/signup
    :http-method : POST, GET
    """
    if request.method== "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('user:login_view')

    else:
        form = UserCreationForm()
        title = 'Sign Up'
        context = {'form':form, 'title': title}
        return render(request, 'signup.html',context)


def login_view(request):

    """
    Url to user's login page.

    :http relative-url: /user/login
    :http-method : POST, GET
    """
    if request.user.is_authenticated:
        return redirect('home:home')

    else:
    
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('home:home')
        else:
            form = AuthenticationForm()
            context = {'form':form, 'title':'login' }

        return render(request, 'login.html', context)

def logout_view(request):
    """
    Url to user's logout.

    :http relative-url: /user/logout
    :http-method : GET
    """
    logout(request)
    return redirect('home:home')

@login_required(login_url="/user/login/")
def user_details(request, username):
    """
    Url to user's details.

    :http relative-url: /user/user_details
    :http-method : GET
    """
    user = request.user
    question = Question.objects.filter(user=user)
    question_count = question.count()
    answers = Answer.objects.filter(user=user)
    answers_count = answers.count()
    context = {'user':user, 'question_count':question_count, 'answer_count':answers_count}
    return render(request, 'user_details.html', context)

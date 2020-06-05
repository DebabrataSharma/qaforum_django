"""Celery task"""
import celery,time
from celery import Celery, shared_task, task, current_task
from time import sleep
import random
from .models import Question, Answer
import json
from django.core import serializers
from django.contrib.auth.models import User
from celery_progress.backend import ProgressRecorder

@shared_task(bind=True)
def celery_task(self, user, duration):
    progress_recorder = ProgressRecorder(self)
    user_obj = User.objects.get(id=user)
    question = serializers.serialize("json", Question.objects.filter(user=user_obj))
    path = '/home/debabrata/mountblue/project-7/' + user_obj.username + '.json'
    file1 = open(path,"w", encoding='utf-8')
    json.dump(question, file1, ensure_ascii=False)
    time.sleep(1)
    progress_recorder.set_progress(1, 1, description='my progress description')
    return "Done"
    
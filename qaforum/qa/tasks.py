import celery
from celery import Celery, shared_task
from time import sleep
import random
from .models import Question, Answer
import json
from celery.decorators import task
from django.core import serializers
from django.contrib.auth.models import User


@celery.task
def long_task(user):
    """Background task that runs a long function with progress reports."""
    # verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    # adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    # noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    # message = ''
    # total = random.randint(10, 50)
    # for i in range(total):
    #     if not message or random.random() < 0.25:
    #         message = '{0} {1} {2}...'.format(random.choice(verb),
    #                                           random.choice(adjective),
    #                                           random.choice(noun))
    #     self.update_state(state='PROGRESS',
    #                       meta={'current': i, 'total': total,
    #                             'status': message})
        # sleep(1)
    user_obj = User.objects.get(id=user)
    question = serializers.serialize("json", Question.objects.filter(user=user_obj))
    json_question = json.dumps(question)
    path = '/home/debabrata/mountblue/project-7/' + user_obj.username + '.json'
    file1 = open(path,"w", encoding='utf-8')
    json.dump(question, file1, ensure_ascii=False)

    return None
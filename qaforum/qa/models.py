from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager


User = get_user_model()


# Create your models here.


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateField()
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
         return self.title

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question= models.ForeignKey(Question, on_delete=models.CASCADE, related_name='ans')
    answer_desc = models.TextField()
    created_date = models.DateField()

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
         return self.answer_desc
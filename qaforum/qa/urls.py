from django.urls import path
from . import views

app_name = 'qa'

urlpatterns = [
    path('questions/add', views.post_question, name='post_question'),
    path('my_questions', views.my_questions, name='my_questions'),
    path('questions/<int:id>/edit', views.update_question, name='update_question'),
    path('questions/<int:id>/delete', views.delete_question, name='delete_question'),
    path('questions/<int:id>/answers', views.get_answers, name='get_answers'),
    path('questions/<int:id>/answers/add', views.post_answer, name='post_answer'),
    path('my_answers', views.my_answers, name='my_answers'),
    path('answers/<int:id>/edit', views.update_answer, name='update_answer'),
    path('answers/<int:id>/delete', views.delete_answer, name='delete_answer'),
    path('question/tag/<slug>', views.tag_result, name='tag_result'),
    path('search', views.search, name='search'),
    path('download_json_data', views.download_json_data, name='download_json_data'),

]

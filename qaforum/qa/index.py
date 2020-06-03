from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Question

@register(Question)
class QaModelIndex(AlgoliaIndex):
    fields = ('id','title', 'description','user', 'date_of_add')
    settings = {'searchableAttributes': ['title', 'description']}
    index_name = 'qa'

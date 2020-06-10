"""Register at alogia search"""

from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Question

@register(Question)
class QaModelIndex(AlgoliaIndex):
    fields = ('id','title', 'description','user', 'created_date')
    settings = {'searchableAttributes': ['title', 'description']}
    index_name = 'qa'

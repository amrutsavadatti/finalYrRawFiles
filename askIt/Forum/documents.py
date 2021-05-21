from django_elasticsearch_dsl import (
    Document ,
    fields,
    Index,
)
from .models import *

ANSWER_INDEX = Index('ans_index')
ANSWER_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)



@ANSWER_INDEX.doc_type
class AnsDocument(Document):
    id = fields.IntegerField(attr='id')
    ansTo = fields.ObjectField(properties={
        'id':fields.IntegerField(),
        'question': fields.TextField(
            
        ),

    })
    answer = fields.TextField(
        fields={
            'raw':{
                'type': 'keyword',
            }
            
        }
    )

    class Django:
        model = Answers
        related_models = [Questions]  # Optional: to ensure the Car will be re-saved when Manufacturer or Ad is updated

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(AnsDocument, self).get_queryset().select_related(
            'ansTo'
        )

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, Questions):
            return related_instance.answers_set.all()
        


Q_INDEX = Index('question_index')
Q_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0
)



@Q_INDEX.doc_type
class QuestionDocument(Document):
    id = fields.IntegerField(attr='id')
    userWhoAsked = fields.ObjectField(properties={
        'id':fields.IntegerField(),
        'username': fields.TextField(
            
        ),

    })
    question = fields.TextField(
        fields={
            'raw':{
                'type': 'keyword',
            }
            
        }
    )

    class Django:
        model = Questions
        related_models = [User]  # Optional: to ensure the Car will be re-saved when Manufacturer or Ad is updated

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(QuestionDocument, self).get_queryset().select_related(
            'userWhoAsked'
        )

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, User):
            return related_instance.questions_set.all()
        
        



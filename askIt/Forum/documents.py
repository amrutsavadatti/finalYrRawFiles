from django_elasticsearch_dsl import (
    Document ,
    fields,
    Index,
)
from .models import *


# @ANSWER_INDEX.doc_type
# class AnsDocument(Document):
    
#     id = fields.IntegerField(attr='id')
#     fielddata=True
#     answer = fields.TextField(
#         fields={
#             'raw':{
#                 'type': 'keyword',
#             }
            
#         }
#     )
   
#     class Django(object):
#         model = Answers


ANSWER_INDEX = Index('ans_index')
ANSWER_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)



@ANSWER_INDEX.doc_type
class AnsDocument(Document):
    id = fields.IntegerField(attr='id')
    ansTo = fields.ObjectField(properties={
        'question': fields.TextField()
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

    # def get_instances_from_related(self, related_instance):
    #     """If related_models is set, define how to retrieve the Car instance(s) from the related model.
    #     The related_models option should be used with caution because it can lead in the index
    #     to the updating of a lot of items.
    #     """
    #     if isinstance(related_instance, Questions):
    #         return related_instance.car_set.all()
    #     elif isinstance(related_instance, Ad):
    #         return related_instance.car


QUESTION_INDEX = Index('question_index')
QUESTION_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


@QUESTION_INDEX.doc_type
class QuestionsDocument(Document):
    id = fields.IntegerField(attr='id')
    userWhoAsked = fields.ObjectField(properties={
        'email': fields.TextField()
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
        related_models = [UserCred]  # Optional: to ensure the Car will be re-saved when Manufacturer or Ad is updated

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(QuestionsDocument, self).get_queryset().select_related(
            'userWhoAsked'
        )
    # def get_instances_from_related(self, related_instance):
    #     """If related_models is set, define how to retrieve the Car instance(s) from the related model.
    #     The related_models option should be used with caution because it can lead in the index
    #     to the updating of a lot of items.
    #     """
    #     if isinstance(related_instance, UserCred):
    #         return related_instance.car_set.all()
        # elif isinstance(related_instance, Ad):
        #     return related_instance.car
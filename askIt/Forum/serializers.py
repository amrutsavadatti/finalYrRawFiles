from .models import *
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import *



class AnsDocumentSerializer(DocumentSerializer):
    class Meta:
        model = Answers
        document = AnsDocument

        fields = (
            'answer',
            'upvotes',
            'downVotes',
            'ansTo'
            )

        def get_location(self, obj):
            try:
                return obj.location.to_dict()
            except:
                return{}

class QuestionDocumentSerializer(DocumentSerializer):
    class Meta:
        model = Questions
        document = QuestionDocument

        fields = (
            'id',
            'question',
            'userWhoAskeds'
            
            )

        def get_location(self, obj):
            try:
                return obj.location.to_dict()
            except:
                return{}




from .models import *
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import *
from .docTest import *



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

class QuestionsDocumentSerializer(DocumentSerializer):
    class Meta:
        model = Questions
        document = QuestionsDocument

        fields = (
            'queston',
            'upVotes',
            'downVotes',
            'userWhoAsked'
            )

        def get_location(self, obj):
            try:
                return obj.location.to_dict()
            except:
                return{}


# FOR TEST                

class CarDocumentSerializer(DocumentSerializer):
    class Meta:
        model = Car
        document = CarDocument

        fields = (
            'name',
            'color',
            'manufacturer'
            )

        def get_location(self, obj):
            try:
                return obj.location.to_dict()
            except:
                return{}

# class ManufacturerDocumentSerializer(DocumentSerializer):
#     class Meta:
#         model = Manufacturer
#         document = ManufacturerDocument

#         fields = (
#             'name',
#             'country_code',
#             'created'
#             )

#         def get_location(self, obj):
#             try:
#                 return obj.location.to_dict()
#             except:
#                 return{}


# class AdDocumentSerializer(DocumentSerializer):
#     class Meta:
#         model = Ad
#         document = AdDocument

#         fields = (
#             'title',
#             'description',
#             'created',
#             'modified',
#             'url',
#             'car'
#             )

#         def get_location(self, obj):
#             try:
#                 return obj.location.to_dict()
#             except:
#                 return{}
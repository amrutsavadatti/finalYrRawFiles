from .models import ElasticDemo
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import *



class NewsDocumentSerializer(DocumentSerializer):
    class Meta:
        model = ElasticDemo
        document = NewsDocument

        fields = ('title','content')

        def get_location(self, obj):
            try:
                return obj.location.to_dict()
            except:
                return{}
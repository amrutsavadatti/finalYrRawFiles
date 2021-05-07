from django_elasticsearch_dsl import (
    Document ,
    fields,
    Index,
)
from .models import Car, Manufacturer, Ad


CAR_INDEX = Index('car_index')
CAR_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

@CAR_INDEX.doc_type
class CarDocument(Document):
    manufacturer = fields.ObjectField(properties={
        'id':fields.IntegerField(),
        'name': fields.TextField(
            fields={
            'raw':{
                'type': 'keyword',
            }
            
        }
        ),
        'country_code': fields.TextField(
            fields={
            'raw':{
                'type': 'keyword',
            }
            
        }
        ),
    })
    ads = fields.ObjectField(properties={
        'description': fields.TextField(
            fields={
            'raw':{
                'type': 'keyword',
            }
            
        }
        ),
        'title': fields.TextField(
            fields={
            'raw':{
                'type': 'keyword',
            }
            
        }
        ),
        'pk': fields.IntegerField(),
    })


    class Django:
        model = Car
        fields = [
            'name',
            'color',
        ]
        related_models = [Manufacturer, Ad]  # Optional: to ensure the Car will be re-saved when Manufacturer or Ad is updated

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(CarDocument, self).get_queryset().select_related(
            'manufacturer'
        )

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, Manufacturer):
            return related_instance.car_set.all()
        elif isinstance(related_instance, Ad):
            return related_instance.car
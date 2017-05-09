from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField

from app.models import Institution, Admissions, Tuition, Completions, CIP, AliasTitle


class DynamicDepthSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes in an additional field to control the depth
    of nested serialization
    
    Adapted from http://stackoverflow.com/a/37572944/214892
    """

    def __init__(self, *args, **kwargs):
        nest = kwargs.pop('nest', None)

        if nest and nest == True:
            self.Meta.depth = 1

        super().__init__(*args, **kwargs)


class TuitionSerializer(serializers.ModelSerializer):


    class Meta:
        model = Tuition
        fields = '__all__'
        depth = 1

class CIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = CIP
        fields = '__all__'

class CompletionsSerializer(serializers.ModelSerializer):
    cip = CIPSerializer()

    class Meta:
        model = Completions
        fields = '__all__'

class AdmissionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admissions
        fields = '__all__'


class InstitutionSerializer(serializers.ModelSerializer):
    location_region = serializers.CharField(source = 'get_location_region_display')
    sector = serializers.CharField(source = 'get_sector_display')
    level = serializers.CharField(source = 'get_level_display')
    control = serializers.CharField(source = 'get_control_display')
    highest_award = serializers.CharField(source = 'get_highest_award_display')
    locale = serializers.CharField(source = 'get_locale_display')
    system_type = serializers.CharField(source = 'get_system_type_display')
    location = PointField()
    web_address = serializers.URLField()
    admission_url = serializers.URLField()
    financial_aid_url = serializers.URLField()
    application_url = serializers.URLField()
    net_price_url = serializers.URLField()
    tuitions = TuitionSerializer(many = True)
    admissions = AdmissionsSerializer()
    completions = CompletionsSerializer(many = True)


    class Meta:
        model = Institution
        fields = '__all__'
        depth = 1







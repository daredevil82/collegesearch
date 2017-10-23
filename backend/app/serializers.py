from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField


from app.models import Institution, Admission, Tuition, Completion, Crosswalk


class TuitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tuition
        fields = '__all__'
        depth = 1


class CrosswalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crosswalk
        fields = '__all__'


class CompletionSerializer(serializers.ModelSerializer):
    crosswalk = CrosswalkSerializer()

    class Meta:
        model = Completion
        fields = '__all__'


class AdmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admission
        fields = '__all__'


class InstitutionGeoSerializer(serializers.ModelSerializer):
    location_region = serializers.CharField(source = 'get_location_region_display')
    locale = serializers.CharField(source = 'get_locale_display')
    location = PointField()

    class Meta:
        model = Institution
        fields = ('pk', 'location_region', 'locale', 'location')
        depth = 0

class BaseInstitutionSerializer(InstitutionGeoSerializer):

    sector = serializers.CharField(source = 'get_sector_display')
    level = serializers.CharField(source = 'get_level_display')
    control = serializers.CharField(source = 'get_control_display')
    highest_award = serializers.CharField(source = 'get_highest_award_display')
    system_type = serializers.CharField(source = 'get_system_type_display')
    web_address = serializers.URLField()
    admission_url = serializers.URLField()
    financial_aid_url = serializers.URLField()
    application_url = serializers.URLField()
    net_price_url = serializers.URLField()

    class Meta(InstitutionGeoSerializer.Meta):
        model = Institution
        fields = '__all__'
        depth = 1


class InstitutionSerializer(BaseInstitutionSerializer):
    tuitions = TuitionSerializer(many = True)
    admission = AdmissionSerializer()
    completions = CompletionSerializer(many = True)


class InstitutionPKSerializer(BaseInstitutionSerializer):
    tuitions = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    admission = serializers.PrimaryKeyRelatedField(read_only = True)
    completions = serializers.PrimaryKeyRelatedField(many = True, read_only = True)

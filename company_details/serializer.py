from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer class for the Company Model
    """
    class Meta:
        model = Company
        fields = ('name', 'profile_id', 'created_at', 'updated_at',
                  'founded_at', 'description', 'funding_amount', 'funding_date',
                  'investor', 'funding_stage', 'website', 'social_info', 'logo_url')


from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer class for the Company Model
    """
    class Meta:
        model = Company
        fields = ('name', 'founded_at', 'description', 'funding_amount', 'funding_date',
                  'investor', 'funding_stage', 'website', 'social_info', 'profile_id')


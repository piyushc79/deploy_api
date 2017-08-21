import datetime
import re
import uuid

from django.db import models
from jsonfield import JSONField

from .app_settings import COMPANY_KEYS, DATE_FORMATS, STAGES, WEBSITE_REGEX


class Company(models.Model):
    objects = models.Manager()
    id = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(
        max_length=200, unique=True)
    founded_at = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    funding_amount = models.FloatField(max_length=10, null=True, blank=True)
    funding_date = models.DateTimeField()
    investor = models.OneToOneField("Company", null=True, blank=True)
    funding_stage = models.CharField(
        max_length=20, null=True, blank=True,
        choices=zip(STAGES, STAGES),
        help_text='Funding Stage')
    website = models.CharField(
        max_length=500, null=True, blank=True)
    logo_url = models.CharField(
        max_length=500, null=True, blank=True)
    social_info = JSONField(null=True, blank=True, default='{}')
    profile_id = models.CharField(max_length=200, unique=True)

    def save(self, *args, **kwargs):

        if not self.profile_id:
            self.profile_id = 'cms::profile::{}'.format(str(uuid.uuid1()))

        super(Company, self).save(*args, **kwargs)

    @staticmethod
    def create_from_api(payload):
        """
        Static method for creating company
        """
        invalid_keys = []
        for key in payload.keys():
            if key not in COMPANY_KEYS:
                invalid_keys.append(key)

        if invalid_keys:
            return False, 'Extra Keys in payload {}'.format(', '.join(invalid_keys)), {}

        if not payload.get('name'):
            return False, 'Cannot create company without name.', {}

        investor = None
        if payload.get('investor'):
            try:
                investor = Company.objects.get(name=payload.get('investor'))
            except Company.DoesNotExist:
                return False, 'No investor found with the name {}'.\
                    format(payload.get('investor')), {}

        if investor:
            payload['investor'] = investor
        else:
            payload['investor'] = None

        for dt in ['founded_at', 'funding_date']:
            if payload.get(dt):
                if not isinstance(payload.get('funding_date'), datetime.datetime):
                    date = None
                    for df in DATE_FORMATS:
                        try:
                            date = datetime.datetime.strptime(
                                payload.get(dt), df)
                            break
                        except:
                            continue
                    if date:
                        payload[dt] = date
            else:
                payload[dt] = None

        if payload.get('funding_amount'):
            try:
                funding_amount = float(payload.get('funding_amount'))
            except ValueError:
                return False, 'Incorrect funding_amount.'.format(payload.get('funding_amount')), {}
        else:
            funding_amount = 0.0
        payload['funding_amount'] = funding_amount

        if payload.get('funding_stage') and payload.get('funding_stage') not in STAGES:
            return False, 'Incorrect Funding Stage.'.format(payload.get('funding_stage')), {}
        else:
            payload['funding_stage'] = None

        if payload.get('website'):
            web_pattern = re.compile(WEBSITE_REGEX)
            if not web_pattern.match(payload.get('website')):
                return False, 'Incorrect website.'.format(payload.get('website')), {}
        else:
            payload['website'] = None

        if payload.get('social_info') and not isinstance(payload.get('social_info'), dict):
            return False, 'Incorrect social_info format.'.format(payload.get('social_info')), {}
        else:
            payload['social_info'] = {}

        payload['profile_id'] = 'cms::profile::{}'.format(str(uuid.uuid1()))

        try:
            created_object = Company(**payload)
            created_object.save()
        except Exception as e:
            return False, 'Error while company creation: {}'.format(e), {}

        # Cyclic import
        from .serializer import CompanySerializer
        serialized_obj = CompanySerializer(created_object)

        return True, '', serialized_obj.data

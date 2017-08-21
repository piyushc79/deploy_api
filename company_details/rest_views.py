from django.core.exceptions import MultipleObjectsReturned
from rest_framework import status, viewsets
from rest_framework.response import Response


from .models import Company
from .serializer import CompanySerializer


class ManageCompany(viewsets.ViewSet):
    """
    Class for managing company creation and fetch
    """
    def create_company(self, request, format=None):
        """
        API for creating a center
        """
        response = {'success': True, 'error': None, 'data': {}}
        st = status.HTTP_200_OK
        success, error, data = Company.create_from_api(request.data)

        # if created 200, else 400
        if not success:
            response['success'] = False
            response['error'] = error
            st = status.HTTP_400_BAD_REQUEST
        else:
            response['data'] = data

        return Response(data=response, status=st)

    def fetch_company(self, request, profile_id):
        """
        API for fetching a center
        """
        response = {'success': True, 'error': None, 'data': {}}
        try:
            company = Company.objects.get(profile_id=profile_id)
        except Company.DoesNotExist:
            response['error'] = 'Company does not exists for  given profile_id.'
            response['success'] = False
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        except MultipleObjectsReturned:
            response['error'] = 'Multiple companies exists for  given profile_id.'
            response['success'] = False
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        try:
            serialized_obj = CompanySerializer(company)
            response['data'] = serialized_obj.data
        except Exception as e:
            response['error'] = 'Error: {}'.format(e)
            response['success'] = False
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=response, status=status.HTTP_200_OK)

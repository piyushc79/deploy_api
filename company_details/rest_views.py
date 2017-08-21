from rest_framework import status, viewsets
from rest_framework.response import Response


from .models import Company


class ManageCompany(viewsets.ViewSet):
    """
    Class for managing company creation and fetch
    """
    def create_company(self, request, format=None):
        """
        View for creating a center
        """
        response = {'success': True, 'error': None, 'data': {}}
        st = status.HTTP_200_OK
        success, error, data = Company.create_from_api(request.DATA)

        # if created 200, else 400
        if not success:
            response['success'] = False
            response['error'] = error
            st = status.HTTP_400_BAD_REQUEST

        return Response(data=response, status=st)

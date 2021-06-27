from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import pagination

from .scrapers import CovidDataSraper
from .serializers import CovidCountrySerializer

class CovidCountryViewSet(viewsets.ViewSet):
    
    serializer_class = CovidCountrySerializer
    pagination_class = pagination.LimitOffsetPagination

    def list(self, request):
        summary = CovidDataSraper().fetch_summary_data()
        
        if summary["status"] == status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(summary, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = CovidCountrySerializer(
            instance=summary["data"], many=True)
        return Response(serializer.data)


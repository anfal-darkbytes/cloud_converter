from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import  BlogModel
from ..serializers import BlogSerializer

class Blog(APIView):
    def get(self, request):
        blogs = BlogModel.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
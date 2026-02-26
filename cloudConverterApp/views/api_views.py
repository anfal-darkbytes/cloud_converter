from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.core.files.base import ContentFile
from ..models import ConvertModel, UploadMultiFileModel, ConvertedMultiFileModel
from ..serializers import ConverterSerializer
from ..utils import execute_conversion, get_filename

class Convert(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        to_format = request.data.get('to_format', 'png').lower()
        from_format = request.data.get('from_format', 'auto').lower()

        convert_instance = ConvertModel.objects.create(
            ipaddr = request.META.get('REMOTE_ADDR'),
            from_format=from_format,
            to_format=to_format
        )

        files = request.FILES.getlist('files')
        if not files:
            return Response({"success":True, "error": "No files provided"}, status=status.HTTP_400_BAD_REQUEST)

        for file_obj in files:
            UploadMultiFileModel.objects.create(
                file = file_obj,
                convert=convert_instance
            )

            try:
                file_obj.seek(0)
                file_bytes = file_obj.read()

                params = {
                    'width': int(request.data.get('width', 800)),
                    'height': int(request.data.get('height', 600)),
                    'quality': int(request.data.get('quality', 90)),
                    'remove_bg': request.data.get('remove_bg', False)
                }

                converted_bytes = execute_conversion(file_bytes, to_format, params)

                new_filename = f'{get_filename(file_obj)}.{to_format}'
                converted_file = ContentFile(converted_bytes, new_filename)

                ConvertedMultiFileModel.objects.create(
                    file = converted_file,
                    convert = convert_instance
                )

            except Exception as e:
                return Response({'success': False, 'error': f'Failed to process the {file_obj.name} as error is {str(e)
                }'})
        serializer = ConverterSerializer(convert_instance)
        response_data = serializer.data
        response_data['converted_files'] =[request.build_absolute_uri(f.file.url) for f in
                                           convert_instance.converted_files.all()]


        return Response({'success' : True, 'data': response_data})




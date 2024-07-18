from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

class TemporaryFileUpload(ModelViewSet):
    def create(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"message": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 指定文件保存的路径
        file_path = f'/tmp/{file.name}'

        # 保存文件到指定路径
        try:
            with open(file_path, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            return Response({"message": "File uploaded successfully", "path": file_path}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "File upload failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
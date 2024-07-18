from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

import os

base_path = 'media/picture/'
base_url = 'https://s1.v100.vip:5728/api/media/picture/'

class SystemBackgroundPicture(ModelViewSet):
    def list(self, request):
        '''
        获取背景视频文件
        '''
        data = []
        exclude_dir = 'custom'  # 排除的目录名称
        for category in os.listdir(base_path):
            if category == exclude_dir or not os.path.isdir(os.path.join(base_path, category)):
                continue

            files_list = []
            category_path = os.path.join(base_path, category)
            for file_name in os.listdir(category_path):
                if os.path.isfile(os.path.join(category_path, file_name)):
                    files_list.append({
                        "fileName": file_name,
                        "url": f"{base_url}{category}/{file_name}"
                    })

            data.append({
                "description": category,
                "list": files_list
            })

        return Response({
            "data": data,
            "message": "success",
            "statusCode": 0
        })

class CustomBackgroundPicture(ModelViewSet):
    def upload(self, request):
        user_name = request.data.get('user_name')
        video_file = request.FILES.get('file')

        if not user_name or not video_file:
            return Response({
                "message": "user_name and file are required",
                "statusCode": 400
            }, status=status.HTTP_400_BAD_REQUEST)

        # 确定文件保存路径
        save_dir = os.path.join(base_path, 'custom', user_name)
        os.makedirs(save_dir, exist_ok=True)  # 如果目录不存在，则创建它

        # 构建文件的完整路径
        file_path = os.path.join(save_dir, video_file.name)
        print(file_path)

        try:
            # 打开文件进行写入
            with open(file_path, 'wb+') as f:
                for chunk in video_file.chunks():  # 处理大文件上传
                    f.write(chunk)

            return Response({
                "message": "File uploaded successfully",
                "file_url": f"{base_url}custom/{user_name}/{video_file.name}",
                "statusCode": 200
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": "Error saving file",
                "error": str(e),
                "statusCode": 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        # 从请求中获取 user_name
        user_name = request.query_params.get('user_name', None)
        if not user_name:
            return Response({
                "data": [],
                "message": "user_name is required",
                "statusCode": 400
            })

        # 构建目标目录的完整路径
        target_path = os.path.join(base_path, 'custom', user_name)
        
        # 检查目录是否存在并且是一个文件夹
        if not os.path.exists(target_path) or not os.path.isdir(target_path):
            return Response({
                "data": [],
                "message": "Directory does not exist",
                "statusCode": 404
            })

        data = []
        files_list = []
        
        # 遍历目录中的文件
        for file_name in os.listdir(target_path):
            if os.path.isfile(os.path.join(target_path, file_name)):
                files_list.append({
                    "fileName": file_name,
                    "url": f"{base_url}custom/{user_name}/{file_name}"
                })

        data.append({
            "description": user_name,  # 使用 user_name 作为描述
            "list": files_list
        })

        return Response({
            "data": data,
            "message": "success",
            "statusCode": 200
        })
    
    def delete_video(self, request):
        user_name = request.query_params.get('user_name')
        file_name = request.query_params.get('file_name')

        if not user_name or not file_name:
            return Response({
                "message": "Both user_name and file_name are required",
                "statusCode": 400
            }, status=status.HTTP_400_BAD_REQUEST)

        # 构建文件的完整路径
        file_path = os.path.join(base_path, 'custom', user_name, file_name)

        # 检查文件是否存在
        if not os.path.isfile(file_path):
            return Response({
                "message": "File not found",
                "statusCode": 404
            }, status=status.HTTP_404_NOT_FOUND)

        # 尝试删除文件
        try:
            os.remove(file_path)
            return Response({
                "message": "File deleted successfully",
                "statusCode": 200
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": "Error deleting the file",
                "statusCode": 500,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
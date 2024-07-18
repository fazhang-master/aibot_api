from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from moviepy.editor import VideoFileClip
import cv2
import numpy as np
from django.http import FileResponse
import os

class RemoveVideoGreenScreen(ModelViewSet):
    def retrieve(self, request, pk=None):
        input_file_path = request.GET.get('file_path')
        if not input_file_path:
            return Response({"message": "File path parameter 'file_path' is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not os.path.exists(input_file_path) or not os.path.isfile(input_file_path):
            return Response({"message": "File does not exist at the provided path"}, status=status.HTTP_404_NOT_FOUND)

        # 构造输出文件路径
        clean_file_name = os.path.basename(input_file_path)
        output_file_name = f"{os.path.splitext(clean_file_name)[0]}_nobg.mp4"
        output_file_path = f'/tmp/{output_file_name}'

        # 处理视频移除绿幕
        try:
            video_clip = VideoFileClip(input_file_path)

            def process_frame(frame):
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_no_green = remove_green_background(frame_rgb)
                return cv2.cvtColor(frame_no_green, cv2.COLOR_RGB2BGR)

            new_video_clip = video_clip.fl_image(process_frame)
            new_video_clip.write_videofile(output_file_path, codec='libx264')
        except Exception as e:
            return Response({"message": "Video processing failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 返回处理后的视频文件
        try:
            return FileResponse(open(output_file_path, 'rb'), as_attachment=True, filename=output_file_name)
        except Exception as e:
            return Response({"message": "Error sending the file", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def remove_green_background(frame):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Define the green screen color range
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])
    # Create a mask to detect the green color
    mask = cv2.inRange(hsv, lower_green, upper_green)
    # Invert the mask
    mask_inv = cv2.bitwise_not(mask)
    # Keep only the parts of the image without green color
    frame_no_green = cv2.bitwise_and(frame, frame, mask=mask_inv)
    return frame_no_green
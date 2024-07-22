import subprocess
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
import os
import shutil

class RelaunchVDP(ModelViewSet):
    def create(self, request):
        video_path = request.data.get('video_path')
        audio_path = request.data.get('audio_path')
        prompt_text = request.data.get('prompt_text')

        def kill_python_process(port):
            command = f"lsof -i:{port}"
            ps = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = ps.communicate()
            for line in output.splitlines():
                if b'python' in line:
                    pid = int(line.split()[1])
                    os.kill(pid, 9)

        def run_command(command):
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            while True:
                output_line = process.stdout.readline()
                if not output_line:
                    break
                print(output_line.strip())
                if "start inference" in output_line:
                    process.kill()
                    return "重启成功"
            return "重启失败"

        try:
            kill_python_process(8010)
            avatar_path = "/mnt/data/zf/metahuman-stream/data/avatars/wav2lip_avatar1"

            # 检查并删除已存在的文件夹
            if video_path and os.path.exists(avatar_path):
                shutil.rmtree(avatar_path)

            command_relaunch = None

            if video_path and audio_path and prompt_text:
                command_clipvideo = f"/home/vipuser/anaconda3/envs/nerfstream/bin/python /mnt/data/zf/metahuman-stream/wav2lip/genavatar.py --video_path {video_path}"
                run_command(command_clipvideo)
                command_relaunch = f"/home/vipuser/anaconda3/envs/nerfstream/bin/python /mnt/data/zf/metahuman-stream/app.py --tts gpt-sovits --TTS_SERVER http://127.0.0.1:9880 --REF_FILE {audio_path} --REF_TEXT \"{prompt_text}\" --model wav2lip --avatar_id wav2lip_avatar1 --batch_size 8 --transport webrtc"
            elif audio_path and prompt_text:
                command_relaunch = f"/home/vipuser/anaconda3/envs/nerfstream/bin/python /mnt/data/zf/metahuman-stream/app.py --tts gpt-sovits --TTS_SERVER http://127.0.0.1:9880 --REF_FILE {audio_path} --REF_TEXT \"{prompt_text}\" --model wav2lip --avatar_id wav2lip_avatar1_15fps --batch_size 8 --transport webrtc"
            elif video_path:
                command_relaunch = f"/home/vipuser/anaconda3/envs/nerfstream/bin/python /mnt/data/zf/metahuman-stream/wav2lip/genavatar.py --video_path {video_path}"

            output = run_command(command_relaunch)
            if output == "重启成功":
                return Response({"message": "重启成功"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": output}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        output_line = process.stdout.readline()
        if not output_line:
            break
        print(output_line.strip())  # 打印输出供调试使用
        if "start inference" in output_line:
            return "重启成功"
    return_code = process.wait()  # 等待进程自然结束
    return "重启失败" if return_code != 0 else "重启成功"
import subprocess
import os
import platform

def find_musescore_executable():
    system = platform.system()
    if system == "Windows":
        # 默认 Windows 安装路径
        return r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe"
    elif system == "Darwin":
        # macOS 默认路径
        default_path = "/Applications/MuseScore 4.app/Contents/MacOS/mscore"
        return default_path if os.path.exists(default_path) else "mscore"
    else:
        # Linux / Unix
        return "mscore"

def split_midi(input_file, output_file, musescore_path=None):
    if not os.path.isfile(input_file):
        print(f"❌ 输入文件不存在: {input_file}")
        return

    mscore = musescore_path or find_musescore_executable()

    # 加引号防止路径中有空格
    cmd = [
        f'"{mscore}"',
        "-o", f'"{output_file}"',
        f'"{input_file}"'
    ]

    # 拼成字符串执行（因为我们加了引号）
    full_cmd = ' '.join(cmd)

    try:
        print(f"▶ 正在运行：{full_cmd}")
        subprocess.run(full_cmd, shell=True, check=True)
        print(f"✅ 导出成功：{output_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ MuseScore 导出失败，错误码 {e.returncode}")

# ✅ 修改这里的路径来使用
if __name__ == "__main__":
    input_midi = r"input.mid"
    output_midi = r"output_split.mid"
    musescore_exe = r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe"

    split_midi(input_midi, output_midi, musescore_exe)

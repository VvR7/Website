# MIDI文件转换工具

这是一个简单的网页应用，用于将MIDI文件转换为分割后的MIDI文件。该工具使用MuseScore来处理MIDI文件。

## 功能特点

- 美观的用户界面
- 支持上传本地MIDI文件
- 可手动输入输出路径
- 使用MuseScore进行MIDI文件处理

## 安装要求

- Python 3.6+
- Flask
- MuseScore 4

## 安装步骤

1. 克隆或下载此仓库
2. 安装所需的Python依赖项：

```bash
pip install -r requirements.txt
```

3. 确保已安装MuseScore 4，并且可以在系统中找到MuseScore可执行文件

## 使用方法

1. 运行服务器：

```bash
python server.py
```

2. 在浏览器中打开 http://localhost:5000
3. 点击"选择MIDI文件"按钮，选择要转换的MIDI文件
4. 在输出路径输入框中输入保存文件的目录路径（例如：D:\Music\Output）
5. 点击"转换文件"按钮开始转换
6. 转换完成后，将在状态区域显示结果

## 注意事项

- 确保MuseScore已正确安装，并且可以在系统中找到MuseScore可执行文件
- 默认情况下，程序会在Windows系统中查找 `C:\Program Files\MuseScore 4\bin\MuseScore4.exe`
- 如果MuseScore安装在不同位置，请修改 `transform.py` 文件中的 `musescore_exe` 变量
- 确保指定的输出路径存在或有权限创建该路径

## 文件结构

- `code.html` - 网页界面
- `server.py` - Flask服务器
- `transform.py` - MIDI文件处理逻辑
- `requirements.txt` - Python依赖项列表 
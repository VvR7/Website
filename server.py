import os
import tempfile
from flask import Flask, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
import transform

app = Flask(__name__, static_folder='.')

# 配置上传文件的最大大小（16MB）
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'mid', 'midi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_midi_file(file_path):
    """检查文件是否为有效的MIDI文件"""
    try:
        with open(file_path, 'rb') as f:
            # 读取文件头
            header = f.read(4)
            # MIDI文件头应该是 "MThd"
            return header == b'MThd'
    except Exception:
        return False

def ensure_directory_exists(directory):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            return True
        except Exception as e:
            return False
    return True

@app.route('/')
def index():
    return send_from_directory('.', 'code.html')

@app.route('/api/convert-midi', methods=['POST'])
def convert_midi():
    # 检查是否有文件
    if 'midiFile' not in request.files:
        return jsonify({'success': False, 'error': '没有上传文件'}), 400
    
    file = request.files['midiFile']
    
    # 检查文件名是否为空
    if file.filename == '':
        return jsonify({'success': False, 'error': '没有选择文件'}), 400
    
    # 检查文件类型
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': '不支持的文件类型，请上传MIDI文件（.mid或.midi格式）'}), 400
    
    try:
        # 创建临时文件保存上传的MIDI文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mid') as temp_input:
            file.save(temp_input.name)
            input_file = temp_input.name
        
        # 验证文件是否为有效的MIDI文件
        if not is_valid_midi_file(input_file):
            os.unlink(input_file)  # 删除无效文件
            return jsonify({'success': False, 'error': '无效的MIDI文件格式'}), 400
        
        # 创建临时文件用于输出
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mid').name
        
        # 调用transform.py中的split_midi函数
        transform.split_midi(input_file, output_file)
        
        # 删除输入临时文件
        os.unlink(input_file)
        
        # 发送转换后的文件
        return send_file(
            output_file,
            as_attachment=True,
            download_name=secure_filename(file.filename).replace('.mid', '_split.mid').replace('.midi', '_split.mid'),
            mimetype='audio/midi'
        )
    
    except Exception as e:
        # 确保清理临时文件
        if 'input_file' in locals():
            try:
                os.unlink(input_file)
            except:
                pass
        if 'output_file' in locals():
            try:
                os.unlink(output_file)
            except:
                pass
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
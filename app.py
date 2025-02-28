from flask import Flask, render_template, jsonify, request
from werkzeug.utils import safe_join
import socket
import subprocess
import psutil
import platform
import GPUtil
import os

Port = 80
Build = 201
Version = "2.0.1"
app = Flask(__name__, template_folder='Assets')
pc_name = socket.gethostname()
info = "Version : " + Version + " Build : " + str(Build)

@app.route('/files')
@app.route('/files/<path:filepath>')
def file_manager(filepath=None):
    # 获取所有驱动器的函数应定义在内部
    def get_drives():
        import string
        from ctypes import windll
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(f"{letter}:\\")
            bitmask >>= 1
        return drives

    # 处理路径转换的函数定义在内部
    def convert_path(url_path):
        if url_path and ':/' not in url_path and url_path.endswith(':'):
            return url_path + '\\'
        return url_path.replace('/', '\\').strip('\\') if url_path else ""

    # 逻辑修正开始
    if not filepath:  # 当访问 /files 时显示驱动器
        return render_template('files.html',
                            pc_name=pc_name,
                            info=info,
                            drives=get_drives(),
                            current_path="")

    # 处理带路径的情况
    try:
        # 转换路径
        if filepath.endswith(':'):
            current_path = filepath + '\\'
        else:
            base_path = '\\'
            current_path = safe_join(base_path, convert_path(filepath))

        if not os.path.exists(current_path):
            return "路径不存在", 404

        # 获取目录内容
        entries = []
        for entry in os.listdir(current_path):
            full_path = os.path.join(current_path, entry)
            is_dir = os.path.isdir(full_path)
            entries.append({
                'name': entry,
                'is_dir': is_dir,
                'url_path': f"{filepath}/{entry}" if is_dir else None
            })

        parent_dir = os.path.dirname(filepath.rstrip('/')) if filepath else None

        return render_template('files.html',
                            pc_name=pc_name,
                            info=info,
                            entries=entries,
                            current_path=current_path,
                            parent_dir=parent_dir)

    except PermissionError:
        return "无权访问该目录", 403

# 获取本机 IP 地址
def get_ip_address():
    try:
        # 获取本机 IP 地址
        ip_address = socket.gethostbyname(pc_name)
        return ip_address
    except Exception as e:
        return "未知"

# 获取 CPU 信息
def get_cpu_info():
    try:
        return platform.processor()  # 获取 CPU 型号
    except Exception as e:
        return "未知"

# 获取磁盘信息
def get_disk_info():
    try:
        disk_count = 0
        total_disk_space = 0
        for partition in psutil.disk_partitions():
            if 'cdrom' in partition.opts or partition.fstype == '':
                continue
            disk_count += 1
            usage = psutil.disk_usage(partition.mountpoint)
            total_disk_space += usage.total
        return disk_count, total_disk_space // (1024 ** 3)  # 返回磁盘数量和总内存（GB）
    except Exception as e:
        return 0, 0

# 获取显卡信息
def get_gpu_info():
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            return gpus[0].name  # 返回第一个显卡的名称
        return "无显卡"
    except Exception as e:
        return "未知"

# 定义路由
@app.route('/')
def index():
    return render_template('control.html', pc_name=pc_name, info=info)

@app.route('/settings')
def settings():
    # 获取本机信息
    ip = get_ip_address()
    cpu_info = get_cpu_info()
    disk_count, total_disk_space = get_disk_info()
    gpu_info = get_gpu_info()

    return render_template(
        'settings.html',
        pc_name=pc_name,
        info=info,
        ip=ip,
        CPU_Info=cpu_info,
        disk_count=disk_count,
        total_disk_space=total_disk_space,
        gpu_info=gpu_info
    )

@app.route('/settings/stop')
def kill():
    os._exit(0)

# 处理命令执行的路由
@app.route('/execute', methods=['POST'])
def execute():
    data = request.json
    command = data.get('command')
    safe_mode = data.get('safe_mode', False)

    if safe_mode:
        command = f"start {command}"

    try:
        # 执行命令并获取输出
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout if result.returncode == 0 else result.stderr
        return jsonify({"success": True, "output": output})
    except Exception as e:
        return jsonify({"success": False, "output": str(e)})

# 运行应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Port)

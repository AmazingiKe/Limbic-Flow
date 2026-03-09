"""
Web Dashboard - 管理面板
"""

from flask import Flask, jsonify, request
import psutil
import time


app = Flask(__name__)


@app.route('/api/stats')
def stats():
    """系统统计"""
    return jsonify({
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "uptime": time.time() - start_time,
    })


@app.route('/api/config', methods=['GET', 'POST'])
def config():
    """配置管理"""
    if request.method == 'POST':
        # 保存配置
        return jsonify({"status": "ok"})
    
    # 读取配置
    return jsonify({})


@app.route('/api/plugins')
def plugins():
    """插件列表"""
    return jsonify([])


start_time = time.time()


if __name__ == '__main__':
    app.run(port=8002)

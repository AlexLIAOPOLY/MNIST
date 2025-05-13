#!/usr/bin/env python
"""
Flask端口绑定测试应用程序
此脚本创建一个最小化的Flask应用程序来验证Render部署中的端口绑定
"""

import os
import sys
import socket
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    """主页显示基本信息"""
    return f"""
    <html>
    <head>
        <title>Flask端口绑定测试</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #4285f4; }}
            .info {{ background: #f0f0f0; padding: 15px; border-radius: 5px; }}
            .success {{ color: green; }}
            .env-list {{ height: 300px; overflow-y: auto; }}
        </style>
    </head>
    <body>
        <h1>Flask端口绑定测试</h1>
        <div class="info">
            <h2 class="success">✅ 服务器运行成功!</h2>
            <p><strong>Python版本:</strong> {sys.version}</p>
            <p><strong>Flask版本:</strong> {Flask.__version__}</p>
            <p><strong>端口:</strong> {os.environ.get('PORT', '未设置')}</p>
            <p><strong>主机:</strong> {socket.gethostname()}</p>
        </div>
        
        <h2>环境变量:</h2>
        <div class="env-list">
            <ul>
                {"".join([f"<li><strong>{k}</strong>: {v}</li>" for k, v in os.environ.items()])}
            </ul>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    """健康检查接口"""
    return jsonify({
        "status": "healthy",
        "python_version": sys.version,
        "flask_version": Flask.__version__,
        "port": os.environ.get('PORT'),
        "host": socket.gethostname()
    })

if __name__ == '__main__':
    # 获取端口 - Render会设置PORT环境变量
    port = int(os.environ.get('PORT', 10000))
    
    print(f"启动Flask应用在 http://0.0.0.0:{port}")
    print(f"PORT环境变量: {os.environ.get('PORT', '未设置')}")
    print(f"Python版本: {sys.version}")
    
    # 启动Flask应用，绑定到所有网络接口(0.0.0.0)
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True) 
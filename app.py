#!/usr/bin/env python
"""
直接的Flask应用入口点
确保在Render部署时能正确绑定端口
"""

import os
import sys
import socket
import logging
from flask import Flask, jsonify

# 配置日志记录
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 初始化Flask应用
app = Flask(__name__)

@app.route('/')
def index():
    """主页显示基本信息"""
    port = os.environ.get('PORT', 'Not set')
    logger.info(f"访问了主页，当前PORT环境变量: {port}")
    return f"""
    <html>
    <head>
        <title>MNIST Web App - 部署测试</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #4285f4; }}
            .info {{ background: #f0f0f0; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            .success {{ color: green; }}
            .env-list {{ height: 200px; overflow-y: auto; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h1>MNIST Web App - 部署测试</h1>
        <div class="info">
            <h2 class="success">✅ 服务器运行成功!</h2>
            <p><strong>Python版本:</strong> {sys.version}</p>
            <p><strong>Flask版本:</strong> {Flask.__version__}</p>
            <p><strong>端口:</strong> {port}</p>
            <p><strong>主机:</strong> {socket.gethostname()}</p>
        </div>
        
        <p>这是一个临时的部署测试页面。一旦确认部署和端口绑定正常工作，将恢复完整的MNIST Web应用程序。</p>
        
        <h2>诊断信息:</h2>
        <div class="info">
            <p><strong>工作目录:</strong> {os.getcwd()}</p>
            <p><strong>Python路径:</strong> {sys.executable}</p>
            <p><strong>导入路径:</strong></p>
            <ul>
                {"".join([f"<li>{path}</li>" for path in sys.path])}
            </ul>
        </div>
        
        <h2>环境变量:</h2>
        <div class="env-list">
            <ul>
                {"".join([f"<li><strong>{k}</strong>: {v}</li>" for k, v in sorted(os.environ.items())])}
            </ul>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    """健康检查接口"""
    logger.info("健康检查被调用")
    return jsonify({
        "status": "healthy",
        "python_version": sys.version,
        "flask_version": Flask.__version__,
        "port": os.environ.get('PORT'),
        "host": socket.gethostname()
    })

# 确保应用正确绑定到PORT环境变量
def get_port():
    """获取应用应该绑定的端口"""
    # Render设置的PORT环境变量
    port_env = os.environ.get('PORT')
    if port_env:
        try:
            return int(port_env)
        except ValueError:
            logger.warning(f"无效的PORT环境变量值: {port_env}，使用默认值10000")
            return 10000
    # 默认端口
    return 10000

# 这部分代码只在直接运行脚本时执行
# 不会在使用Gunicorn时执行
if __name__ == '__main__':
    # 获取端口
    port = get_port()
    
    logger.info(f"启动Flask应用在 http://0.0.0.0:{port}")
    logger.info(f"PORT环境变量: {os.environ.get('PORT', '未设置')}")
    logger.info(f"Python版本: {sys.version}")
    
    # 启动Flask应用，绑定到所有网络接口(0.0.0.0)
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True) 
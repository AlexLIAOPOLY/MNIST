#!/usr/bin/env python
"""
端口绑定测试脚本 - 创建一个简单的HTTP服务器来响应请求
"""

import os
import sys
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        response = f"""
        <html>
        <head><title>端口绑定测试</title></head>
        <body>
            <h1>端口绑定测试成功!</h1>
            <p>服务器正在运行在: {self.server.server_address[0]}:{self.server.server_address[1]}</p>
            <p>环境变量 PORT: {os.environ.get('PORT', '未设置')}</p>
            <p>Python 版本: {sys.version}</p>
            <h2>环境变量:</h2>
            <ul>
                {"".join([f"<li>{k}: {v}</li>" for k, v in os.environ.items()])}
            </ul>
        </body>
        </html>
        """
        
        self.wfile.write(response.encode())
    
    def log_message(self, format, *args):
        print(f"[HTTP] {self.client_address[0]} - {format % args}")

def get_ip():
    """获取本机IP地址"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 不需要真正连接
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def run_server():
    # 获取PORT环境变量，默认为10000
    port = int(os.environ.get('PORT', 10000))
    
    # 输出所有环境变量
    print("环境变量:")
    for key, value in os.environ.items():
        print(f"  {key}: {value}")
    
    # 创建服务器
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, SimpleHandler)
    
    # 获取本机IP
    local_ip = get_ip()
    
    print(f"启动HTTP服务器在 http://{local_ip}:{port}")
    print(f"绑定地址: {server_address[0]}:{server_address[1]}")
    print("按Ctrl+C停止服务器")
    
    # 启动服务器
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("服务器已停止")

if __name__ == "__main__":
    run_server() 
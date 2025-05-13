#!/bin/bash
# Tensor2Tensor部署测试脚本

echo "===== Tensor2Tensor部署前测试 ====="

# 设置环境变量
export PORT=10000
export MNIST_PRELOAD_DATA=1
export PYTHONPATH=$(pwd)

# 创建虚拟环境
echo -e "\n===== 创建虚拟环境 ====="
python3 -m venv venv_test
source venv_test/bin/activate

# 安装依赖
echo -e "\n===== 安装依赖 ====="
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt

# 检查Python版本
echo -e "\n===== 检查Python版本 ====="
python --version

# 运行健康检查
echo -e "\n===== 运行健康检查 ====="
python health_check.py

# 测试应用启动
echo -e "\n===== 测试应用启动 ====="
python app.py &
APP_PID=$!

echo "应用启动中，等待5秒..."
sleep 5

# 发送请求测试应用
echo -e "\n===== 测试API ====="
curl -s http://localhost:$PORT/health || echo "无法连接到应用"

# 终止应用
echo -e "\n===== 结束测试 ====="
kill $APP_PID

# 测试Docker构建(如果有Docker)
if command -v docker &> /dev/null; then
    echo -e "\n===== 测试Docker构建 ====="
    docker build -t tensor2tensor-test . && echo "Docker构建成功" || echo "Docker构建失败"
    
    echo -e "\n===== 测试Docker运行 ====="
    docker run --rm -p $PORT:$PORT -e PORT=$PORT --name tensor2tensor-test-container -d tensor2tensor-test
    sleep 5
    curl -s http://localhost:$PORT/health || echo "无法连接到Docker容器中的应用"
    docker stop tensor2tensor-test-container
else
    echo -e "\n系统中未检测到Docker，跳过Docker测试"
fi

# 退出虚拟环境
deactivate
echo -e "\n===== 测试完成 ====="
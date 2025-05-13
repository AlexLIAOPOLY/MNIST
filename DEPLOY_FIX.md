# Tensor2Tensor 部署修复说明

本文档记录了为了使Tensor2Tensor项目成功部署到Render平台所做的修改。

## 更新内容

1. **依赖包更新**
   - 更新了`requirements.txt`文件中的依赖包版本
   - 移除了不必要的`--only-binary`标志
   - 升级了核心包的版本要求，以符合现代兼容性标准

2. **部署配置**
   - 更新了`render.yaml`配置文件
   - 将服务类型从`worker`改为`web`
   - 升级Python版本到3.11.11
   - 简化了构建命令

3. **Docker支持**
   - 新增了`Dockerfile`
   - 添加了`.dockerignore`文件
   - 优化了Docker镜像构建过程

4. **健康检查**
   - 更新了`health_check.py`脚本
   - 增加了对新依赖包的检查
   - 修改了Python版本要求

5. **部署测试**
   - 更新了`test_deploy.sh`测试脚本
   - 添加了Docker构建测试
   - 增加了API测试

6. **文档更新**
   - 更新了`README_DEPLOY.md`文档
   - 添加了更详细的部署步骤
   - 增加了Render平台部署说明

## 关键配置

### Python版本
升级到Python 3.11.11（Render当前支持的默认版本）

### 依赖版本
主要依赖包版本：
- Flask >= 2.0.0
- Werkzeug >= 2.0.0
- numpy >= 1.21.0
- scipy >= 1.7.0

### 端口配置
应用现在会自动使用环境变量`PORT`中指定的端口

### 健康检查
- 端点: `/health`
- 超时: 120秒

## 测试方法

可以通过以下方式测试部署配置：

1. 本地测试:
   ```bash
   ./test_deploy.sh
   ```

2. Docker测试:
   ```bash
   docker build -t tensor2tensor-app .
   docker run -p 10000:10000 -e PORT=10000 tensor2tensor-app
   ```

3. 健康检查:
   ```bash
   python health_check.py
   ```

## 注意事项

1. Render平台会自动设置`PORT`环境变量
2. 确保应用监听在`0.0.0.0`上而不是`127.0.0.1`
3. 健康检查必须返回2xx状态码才能被认为是健康的 
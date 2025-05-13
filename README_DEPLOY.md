# Tensor2Tensor Web Application

一个基于Tensor2Tensor库的Web应用程序，支持深度学习模型的训练、测试和可视化。

## 功能特性

- **模型训练**：使用可定制的超参数训练神经网络模型
- **模型测试**：上传数据并实时查看预测结果
- **数据集探索**：可视化和理解数据集
- **模型比较**：比较不同模型的性能并查看详细指标
- **可视化**：查看混淆矩阵、t-SNE可视化等

## 部署说明

### 系统要求

- Python 3.11+ (建议使用Python 3.11.11)
- 内存：至少2GB
- CPU：至少1核

### 本地安装

#### 先决条件

- Python 3.11或更高版本
- pip (Python包安装器)

#### 设置步骤

1. 克隆仓库:
   ```
   git clone https://github.com/yourusername/tensor2tensor.git
   cd tensor2tensor
   ```

2. 创建虚拟环境:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```

3. 安装依赖:
   ```
   pip install -r requirements.txt
   ```

### 本地运行

要在本地计算机上运行应用程序:

```
python app.py
```

默认情况下，应用程序将在 http://127.0.0.1:10000/ 上可用

### 命令行选项

应用程序支持以下环境变量:

- `PORT`: 服务器绑定的端口（默认：10000）
- `MNIST_PRELOAD_DATA`: 是否在启动时预加载数据集（1=是，0=否）

## 部署到Render平台

### 使用GitHub部署

1. Fork此存储库到您的GitHub账户
2. 在Render上创建一个Web Service
3. 链接您的GitHub仓库
4. Render将自动从`render.yaml`中检测配置
5. 点击"Create Web Service"开始部署

### 使用Docker部署

1. 构建Docker镜像：
   ```
   docker build -t tensor2tensor-app .
   ```

2. 在Render上创建一个新的Web Service，选择"Docker Registry"
3. 配置您的Docker镜像
4. Render将拉取并部署您的Docker镜像

### 环境变量配置

在Render仪表板上，为您的Web Service设置以下环境变量:

- `PYTHON_VERSION`: 3.11.11
- `MNIST_PRELOAD_DATA`: 1

### 健康检查

部署成功后，您可以通过访问 `/health` 端点来验证应用程序状态。它将返回包含应用程序详细信息的JSON响应。

## Project Structure

```
mnist-web-app/
├── mnist_web/
│   ├── static/         # Static assets (CSS, JS, images)
│   │   ├── css/        # Stylesheets
│   │   ├── js/         # JavaScript files
│   │   ├── img/        # Images
│   │   └── models/     # Saved models
│   ├── templates/      # HTML templates
│   └── app.py          # Flask application
├── run_mnist_web.py    # Script to run the web app
├── requirements.txt    # Python dependencies
├── Procfile            # For Heroku/Render deployment
└── README.md           # Project documentation
```

## Development

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Running Tests

```
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The MNIST dataset was created by Yann LeCun, Corinna Cortes, and Christopher J.C. Burges
- Built with Flask, scikit-learn, and Chart.js 
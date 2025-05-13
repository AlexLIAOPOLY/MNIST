#!/usr/bin/env python
# 测试训练好的MNIST模型
import numpy as np
import pickle
import os

# 检查模型文件是否存在
if not os.path.exists('mnist_model.pkl'):
    print("错误: 未找到模型文件 'mnist_model.pkl'")
    print("请先运行 mnist_example.py 训练模型")
    exit(1)

# 导入特定函数
from mnist_example import load_mnist, SimpleNeuralNetwork

def main():
    """主函数"""
    print("加载测试数据...")
    try:
        _, _, x_test, y_test = load_mnist()
    except Exception as e:
        print(f"加载测试数据时出错: {e}")
        return
    
    print("加载训练好的模型...")
    try:
        model = SimpleNeuralNetwork.load('mnist_model.pkl')
    except Exception as e:
        print(f"加载模型时出错: {e}")
        return
    
    print("评估模型性能...")
    accuracy = model.evaluate(x_test, y_test)
    print(f"测试集准确率: {accuracy:.4f}")
    
    # 随机选择10个样本进行预测
    print("\n随机样本预测:")
    indices = np.random.choice(len(x_test), 10, replace=False)
    for i, idx in enumerate(indices):
        x = x_test[idx]
        actual = y_test[idx]
        predicted = model.predict(x.reshape(1, -1))[0]
        print(f"样本 {i+1}: 预测 = {predicted}, 实际 = {actual}")
        
    print("\n模型结构:")
    print(f"输入尺寸: {model.input_size}")
    print(f"隐藏层尺寸: {model.hidden_size}")
    print(f"输出尺寸: {model.output_size}")

if __name__ == "__main__":
    main() 
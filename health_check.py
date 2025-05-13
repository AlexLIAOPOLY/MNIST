#!/usr/bin/env python
"""
Tensor2Tensor Web应用健康检查工具
检查应用运行所需的环境和依赖是否正确
"""

import sys
import os
import platform
import time
import json

def check_python_version():
    """检查Python版本"""
    required_version = (3, 11, 0)
    current_version = sys.version_info
    
    print(f"Python版本: {sys.version}")
    if current_version >= required_version:
        return True, f"Python版本: {'.'.join(map(str, current_version[:3]))} (满足要求)"
    else:
        return False, f"Python版本过低: {'.'.join(map(str, current_version[:3]))}, 需要 {'.'.join(map(str, required_version))}"

def check_dependencies():
    """检查必要的软件包是否已安装"""
    required_packages = [
        "numpy",
        "flask",
        "werkzeug",
        "jinja2",
        "pillow",
        "markupsafe",
        "itsdangerous",
        "click",
        "gunicorn",
        "scipy",
        "matplotlib",
        "requests"
    ]
    
    missing_packages = []
    version_info = {}
    
    for package in required_packages:
        try:
            module = __import__(package)
            version = getattr(module, "__version__", "Unknown")
            version_info[package] = version
            print(f"✓ {package} {version}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} - 未安装")
    
    if missing_packages:
        return False, f"缺少必要的软件包: {', '.join(missing_packages)}", version_info
    else:
        return True, "所有必要的软件包已安装", version_info

def check_data_access():
    """检查数据目录是否可访问"""
    data_dir = "data"
    if not os.path.exists(data_dir):
        try:
            os.makedirs(data_dir)
            print(f"✓ 已创建数据目录: {data_dir}")
            return True, f"已创建数据目录: {data_dir}"
        except OSError as e:
            print(f"✗ 无法创建数据目录: {e}")
            return False, f"无法创建数据目录: {e}"
    else:
        print(f"✓ 数据目录已存在: {data_dir}")
        return True, f"数据目录已存在: {data_dir}"

def check_environment():
    """检查环境变量"""
    required_vars = ["PYTHON_VERSION", "MNIST_PRELOAD_DATA"]
    missing_vars = [var for var in required_vars if var not in os.environ]
    
    env_info = {}
    for var in required_vars:
        value = os.environ.get(var, "未设置")
        env_info[var] = value
        if var in missing_vars:
            print(f"✗ {var} - 未设置")
        else:
            print(f"✓ {var} = {value}")
    
    if missing_vars:
        return False, f"缺少必要的环境变量: {', '.join(missing_vars)}", env_info
    else:
        return True, "所有必要的环境变量已设置", env_info

def check_import_paths():
    """检查导入路径是否正确"""
    import_paths = [
        os.path.abspath("."),
        os.path.abspath("tensor2tensor")
    ]
    
    all_exists = True
    results = {}
    
    for path in import_paths:
        exists = os.path.exists(path)
        results[path] = exists
        if exists:
            print(f"✓ 导入路径存在: {path}")
        else:
            print(f"✗ 导入路径不存在: {path}")
            all_exists = False
    
    # 检查sys.path
    print("\nPython搜索路径:")
    for i, path in enumerate(sys.path):
        print(f"  {i}: {path}")
    
    return all_exists, "所有导入路径检查完成", results

def run_health_check():
    """运行所有健康检查"""
    print("=== MNIST Web应用健康检查 ===")
    start_time = time.time()
    
    checks = [
        ("Python版本", check_python_version),
        ("软件依赖", check_dependencies),
        ("数据访问", check_data_access),
        ("环境变量", check_environment),
        ("导入路径", check_import_paths)
    ]
    
    results = {}
    all_passed = True
    
    for name, check_func in checks:
        print(f"\n--- 检查{name} ---")
        if name == "软件依赖" or name == "环境变量":
            status, message, details = check_func()
            results[name] = {"status": status, "message": message, "details": details}
        else:
            status, message = check_func()
            results[name] = {"status": status, "message": message}
        
        if not status:
            all_passed = False
    
    # 添加系统信息
    system_info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_path": sys.executable,
        "cwd": os.getcwd()
    }
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n=== 健康检查完成 ===")
    print(f"总用时: {duration:.2f}秒")
    
    if all_passed:
        print("✅ 所有检查均已通过，应用程序应该可以正常运行")
        exit_code = 0
    else:
        print("❌ 部分检查未通过，请查看详细结果")
        exit_code = 1
    
    # 生成健康报告
    report = {
        "timestamp": time.time(),
        "duration": duration,
        "all_passed": all_passed,
        "results": results,
        "system_info": system_info
    }
    
    try:
        with open("health_check_report.json", "w") as f:
            json.dump(report, f, indent=2)
        print(f"健康报告已保存至 health_check_report.json")
    except Exception as e:
        print(f"无法保存健康报告: {e}")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(run_health_check()) 
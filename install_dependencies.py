#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖安装脚本
自动检测并安装视频人脸检测项目所需的所有依赖

功能:
- 检测Python环境
- 安装Python依赖包
- 下载YuNet模型文件
- 验证安装结果
- 提供详细的安装日志
"""

import os
import sys
import subprocess
import urllib.request
import hashlib
from pathlib import Path

class DependencyInstaller:
    """依赖安装器类"""
    
    def __init__(self):
        """初始化安装器"""
        self.project_root = Path(__file__).parent
        self.models_dir = self.project_root / "models"
        self.requirements_file = self.project_root / "requirements.txt"
        
        # YuNet模型信息
        self.yunet_models = {
            "face_detection_yunet_2023mar.onnx": {
                "url": "https://github.com/opencv/opencv_zoo/raw/master/models/face_detection_yunet/face_detection_yunet_2023mar.onnx",
                "size": 1939328  # 约1.85MB
            },
            "face_detection_yunet_2023mar_int8.onnx": {
                "url": "https://github.com/opencv/opencv_zoo/raw/master/models/face_detection_yunet/face_detection_yunet_2023mar_int8.onnx",
                "size": 484864   # 约473KB
            }
        }
        
        # 必需的Python包
        self.required_packages = [
            "opencv-python>=4.8.0",
            "numpy>=1.21.0",
            "deepface>=0.0.79",
            "tensorflow>=2.12.0",
            "mtcnn>=0.1.1",
            "retina-face>=0.0.13"
        ]
    
    def print_header(self):
        """打印安装器标题"""
        print("="*60)
        print("🎯 视频人脸检测项目 - 依赖安装器")
        print("="*60)
        print(f"📁 项目路径: {self.project_root}")
        print(f"🐍 Python版本: {sys.version}")
        print("="*60)
    
    def check_python_version(self):
        """检查Python版本"""
        print("\n🔍 检查Python版本...")
        if sys.version_info < (3, 8):
            print("❌ 错误: 需要Python 3.8或更高版本")
            print(f"   当前版本: {sys.version}")
            return False
        print(f"✅ Python版本检查通过: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        return True
    
    def check_pip(self):
        """检查pip是否可用"""
        print("\n🔍 检查pip...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                         check=True, capture_output=True)
            print("✅ pip可用")
            return True
        except subprocess.CalledProcessError:
            print("❌ 错误: pip不可用")
            print("   请先安装pip: https://pip.pypa.io/en/stable/installation/")
            return False
    
    def create_models_directory(self):
        """创建模型文件目录"""
        print("\n📁 创建模型目录...")
        self.models_dir.mkdir(exist_ok=True)
        print(f"✅ 模型目录已创建: {self.models_dir}")
    
    def install_python_packages(self):
        """安装Python依赖包"""
        print("\n📦 安装Python依赖包...")
        
        # 首先尝试从requirements.txt安装
        if self.requirements_file.exists():
            print(f"📋 从 {self.requirements_file} 安装依赖...")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)
                ], check=True)
                print("✅ requirements.txt 依赖安装完成")
                return True
            except subprocess.CalledProcessError as e:
                print(f"⚠️  requirements.txt 安装失败: {e}")
                print("🔄 尝试逐个安装必需包...")
        
        # 逐个安装必需包
        failed_packages = []
        for package in self.required_packages:
            print(f"📦 安装 {package}...")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], check=True, capture_output=True)
                print(f"✅ {package} 安装成功")
            except subprocess.CalledProcessError as e:
                print(f"❌ {package} 安装失败")
                failed_packages.append(package)
        
        if failed_packages:
            print(f"\n⚠️  以下包安装失败: {', '.join(failed_packages)}")
            print("💡 建议手动安装这些包或检查网络连接")
            return False
        
        print("✅ 所有Python依赖包安装完成")
        return True
    
    def download_file(self, url, filepath, expected_size=None):
        """下载文件"""
        try:
            print(f"📥 下载 {filepath.name}...")
            
            # 检查文件是否已存在且大小正确
            if filepath.exists():
                if expected_size and filepath.stat().st_size == expected_size:
                    print(f"✅ {filepath.name} 已存在且大小正确，跳过下载")
                    return True
                else:
                    print(f"🔄 {filepath.name} 存在但大小不正确，重新下载")
            
            # 下载文件
            urllib.request.urlretrieve(url, filepath)
            
            # 验证文件大小
            if expected_size:
                actual_size = filepath.stat().st_size
                if actual_size != expected_size:
                    print(f"❌ 文件大小不匹配: 期望 {expected_size}, 实际 {actual_size}")
                    filepath.unlink()  # 删除损坏的文件
                    return False
            
            print(f"✅ {filepath.name} 下载完成 ({filepath.stat().st_size} bytes)")
            return True
            
        except Exception as e:
            print(f"❌ 下载 {filepath.name} 失败: {e}")
            if filepath.exists():
                filepath.unlink()  # 删除部分下载的文件
            return False
    
    def download_yunet_models(self):
        """下载YuNet模型文件"""
        print("\n🤖 下载YuNet模型文件...")
        
        success_count = 0
        for model_name, model_info in self.yunet_models.items():
            model_path = self.models_dir / model_name
            if self.download_file(model_info["url"], model_path, model_info["size"]):
                success_count += 1
        
        if success_count == 0:
            print("❌ 所有模型文件下载失败")
            print("💡 请检查网络连接或手动下载模型文件")
            return False
        elif success_count < len(self.yunet_models):
            print(f"⚠️  部分模型文件下载失败 ({success_count}/{len(self.yunet_models)})")
            print("💡 至少需要一个模型文件才能正常运行")
        else:
            print("✅ 所有YuNet模型文件下载完成")
        
        return True
    
    def verify_installation(self):
        """验证安装结果"""
        print("\n🔍 验证安装结果...")
        
        # 验证Python包
        failed_imports = []
        test_imports = [
            ("cv2", "OpenCV"),
            ("numpy", "NumPy"),
            ("deepface", "DeepFace"),
            ("tensorflow", "TensorFlow")
        ]
        
        for module, name in test_imports:
            try:
                __import__(module)
                print(f"✅ {name} 导入成功")
            except ImportError as e:
                print(f"❌ {name} 导入失败: {e}")
                failed_imports.append(name)
        
        # 验证模型文件
        model_count = 0
        for model_name in self.yunet_models.keys():
            model_path = self.models_dir / model_name
            if model_path.exists():
                model_count += 1
                print(f"✅ 模型文件存在: {model_name}")
            else:
                print(f"❌ 模型文件缺失: {model_name}")
        
        # 总结验证结果
        print("\n" + "="*60)
        if failed_imports:
            print(f"❌ 安装验证失败: {len(failed_imports)} 个包导入失败")
            print(f"   失败的包: {', '.join(failed_imports)}")
        elif model_count == 0:
            print("❌ 安装验证失败: 没有可用的模型文件")
        else:
            print("✅ 安装验证成功!")
            print(f"   📦 Python包: 全部导入成功")
            print(f"   🤖 模型文件: {model_count}/{len(self.yunet_models)} 个可用")
        
        return len(failed_imports) == 0 and model_count > 0
    
    def print_usage_guide(self):
        """打印使用指南"""
        print("\n" + "="*60)
        print("🚀 安装完成! 使用指南:")
        print("="*60)
        print("\n📖 基础使用:")
        print("   python main.py sample.mp4 --mosaic --preview")
        print("\n🔄 侧脸检测优化:")
        print("   python main.py sample.mp4 --detector deepface --deepface-backend mtcnn --mosaic")
        print("\n🔀 混合检测器 (推荐):")
        print("   python main.py sample.mp4 --detector hybrid --deepface-backend retinaface --mosaic")
        print("\n🎯 自定义延续打码:")
        print("   python main.py sample.mp4 --continuation-frames 10 --mosaic")
        print("\n📷 实时摄像头检测:")
        print("   python main.py 0 --detector yunet --mosaic --preview")
        print("\n📚 更多帮助:")
        print("   python main.py --help")
        print("   查看 README.md 获取详细文档")
        print("="*60)
    
    def run(self):
        """运行安装器"""
        self.print_header()
        
        # 检查基础环境
        if not self.check_python_version():
            return False
        
        if not self.check_pip():
            return False
        
        # 创建必要目录
        self.create_models_directory()
        
        # 安装依赖
        if not self.install_python_packages():
            print("\n❌ Python包安装失败，但继续尝试下载模型文件...")
        
        # 下载模型文件
        if not self.download_yunet_models():
            print("\n❌ 模型文件下载失败")
        
        # 验证安装
        success = self.verify_installation()
        
        if success:
            self.print_usage_guide()
        else:
            print("\n❌ 安装未完全成功，请检查上述错误信息")
            print("💡 建议:")
            print("   1. 检查网络连接")
            print("   2. 手动安装失败的包: pip install <package_name>")
            print("   3. 手动下载模型文件到 models/ 目录")
        
        return success

def main():
    """主函数"""
    installer = DependencyInstaller()
    success = installer.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
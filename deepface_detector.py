import cv2
import numpy as np
import os
from typing import List, Dict, Tuple, Optional, Union

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("警告: DeepFace未安装，相关功能将不可用")
    print("安装命令: pip install deepface")

class DeepFaceDetector:
    """
    基于DeepFace的人脸检测和分析器
    提供人脸检测、属性分析等高级功能
    """
    
    def __init__(self, detector_backend='opencv', model_name='VGG-Face'):
        """
        初始化DeepFace检测器
        
        Args:
            detector_backend (str): 检测后端 ('opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface')
            model_name (str): 人脸识别模型 ('VGG-Face', 'Facenet', 'OpenFace', 'DeepFace')
        """
        if not DEEPFACE_AVAILABLE:
            raise ImportError("DeepFace未安装，请先安装: pip install deepface")
            
        self.detector_backend = detector_backend
        self.model_name = model_name
        
        # 支持的检测后端
        self.supported_backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface']
        if detector_backend not in self.supported_backends:
            raise ValueError(f"不支持的检测后端: {detector_backend}")
            
        print(f"DeepFace检测器初始化完成 - 后端: {detector_backend}, 模型: {model_name}")
    
    def detect_faces_in_frame(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        在单帧图像中检测人脸
        
        Args:
            frame (numpy.ndarray): 输入的图像帧
            
        Returns:
            list: 检测到的人脸矩形框列表，每个元素为(x, y, w, h)
        """
        try:
            # 使用DeepFace检测人脸区域
            face_objs = DeepFace.extract_faces(
                img_path=frame,
                detector_backend=self.detector_backend,
                enforce_detection=False,
                align=False
            )
            
            # 获取人脸区域坐标
            face_boxes = []
            if face_objs:
                # DeepFace返回的是归一化的人脸区域，需要转换为像素坐标
                height, width = frame.shape[:2]
                
                # 使用DeepFace的函数获取精确坐标
                try:
                    from deepface.commons import functions
                    detected_faces = functions.extract_faces(
                        img=frame,
                        detector_backend=self.detector_backend,
                        grayscale=False,
                        enforce_detection=False,
                        align=False
                    )
                except ImportError:
                    # 如果导入失败，使用备用方法
                    detected_faces = DeepFace.extract_faces(
                        img_path=frame,
                        detector_backend=self.detector_backend,
                        grayscale=False,
                        enforce_detection=False,
                        align=False
                    )
                
                for face_data in detected_faces:
                    if 'facial_area' in face_data:
                        area = face_data['facial_area']
                        x, y, w, h = area['x'], area['y'], area['w'], area['h']
                        face_boxes.append((x, y, w, h))
            
            return face_boxes
            
        except Exception as e:
            print(f"DeepFace人脸检测错误: {e}")
            return []
    
    def analyze_faces_in_frame(self, frame: np.ndarray) -> List[Dict]:
        """
        分析帧中人脸的属性（年龄、性别、情绪、种族）
        
        Args:
            frame (numpy.ndarray): 输入的图像帧
            
        Returns:
            list: 人脸分析结果列表
        """
        try:
            # 分析人脸属性
            analysis_results = DeepFace.analyze(
                img_path=frame,
                actions=['age', 'gender', 'race', 'emotion'],
                detector_backend=self.detector_backend,
                enforce_detection=False,
                silent=True
            )
            
            # 确保返回列表格式
            if not isinstance(analysis_results, list):
                analysis_results = [analysis_results]
                
            return analysis_results
            
        except Exception as e:
            print(f"DeepFace人脸分析错误: {e}")
            return []
    
    def get_face_embeddings(self, frame: np.ndarray) -> List[np.ndarray]:
        """
        获取人脸特征向量
        
        Args:
            frame (numpy.ndarray): 输入的图像帧
            
        Returns:
            list: 人脸特征向量列表
        """
        try:
            # 获取人脸特征向量
            embeddings = DeepFace.represent(
                img_path=frame,
                model_name=self.model_name,
                detector_backend=self.detector_backend,
                enforce_detection=False
            )
            
            # 提取embedding向量
            embedding_vectors = []
            if isinstance(embeddings, list):
                for emb in embeddings:
                    if 'embedding' in emb:
                        embedding_vectors.append(np.array(emb['embedding']))
            
            return embedding_vectors
            
        except Exception as e:
            print(f"DeepFace特征提取错误: {e}")
            return []
    
    def compare_faces(self, face1: np.ndarray, face2: np.ndarray) -> Dict:
        """
        比较两个人脸的相似度
        
        Args:
            face1 (numpy.ndarray): 第一个人脸图像
            face2 (numpy.ndarray): 第二个人脸图像
            
        Returns:
            dict: 比较结果，包含verified和distance
        """
        try:
            result = DeepFace.verify(
                img1_path=face1,
                img2_path=face2,
                model_name=self.model_name,
                detector_backend=self.detector_backend,
                enforce_detection=False
            )
            return result
            
        except Exception as e:
            print(f"DeepFace人脸比较错误: {e}")
            return {'verified': False, 'distance': float('inf')}

# 导入VideoFaceDetector基类
from face_detector import VideoFaceDetector

class HybridFaceDetector(VideoFaceDetector):
    """
    混合人脸检测器
    结合YuNet的高性能检测和DeepFace的高级分析功能
    继承VideoFaceDetector以复用视频处理功能
    """
    
    def __init__(self, primary_backend='yunet', enable_deepface=False):
        """
        初始化混合检测器
        
        Args:
            primary_backend (str): 主要检测后端 ('yunet' 或 'deepface')
            enable_deepface (bool): 是否启用DeepFace高级功能
        """
        # 调用父类初始化方法
        super().__init__()
        
        self.primary_backend = primary_backend
        self.enable_deepface = enable_deepface and DEEPFACE_AVAILABLE
        
        # 初始化DeepFace检测器
        if self.enable_deepface:
            self.deepface_detector = DeepFaceDetector()
        
        print(f"混合检测器初始化完成 - 主后端: {primary_backend}, DeepFace: {self.enable_deepface}")
    
    def detect_faces(self, frame: np.ndarray) -> List[Dict]:
        """
        检测人脸并返回标准格式的结果
        
        Args:
            frame (numpy.ndarray): 输入的图像帧
            
        Returns:
            list: 检测到的人脸列表，每个元素包含bbox等信息
        """
        faces_coords = self.detect_faces_in_frame(frame)
        faces = []
        for x, y, w, h in faces_coords:
            faces.append({
                'bbox': (x, y, w, h),
                'confidence': 1.0  # 默认置信度
            })
        return faces
    
    def detect_faces_in_frame(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        检测人脸（使用主要后端）
        
        Args:
            frame (numpy.ndarray): 输入的图像帧
            
        Returns:
            list: 检测到的人脸矩形框列表
        """
        if self.primary_backend == 'yunet':
            # 使用父类的YuNet检测器
            return super().detect_faces_in_frame(frame)
        elif self.primary_backend == 'deepface' and self.enable_deepface:
            return self.deepface_detector.detect_faces_in_frame(frame)
        else:
            # 如果DeepFace不可用，回退到YuNet（父类方法）
            return super().detect_faces_in_frame(frame)
    
    def analyze_faces_with_attributes(self, frame: np.ndarray) -> Dict:
        """
        检测人脸并分析属性
        
        Args:
            frame (numpy.ndarray): 输入的图像帧
            
        Returns:
            dict: 包含检测结果和属性分析的完整信息
        """
        result = {
            'faces': [],
            'analysis': [],
            'has_deepface_analysis': False
        }
        
        # 使用主要后端检测人脸
        faces = self.detect_faces_in_frame(frame)
        result['faces'] = faces
        
        # 如果启用DeepFace，进行属性分析
        if self.enable_deepface and faces:
            analysis = self.deepface_detector.analyze_faces_in_frame(frame)
            result['analysis'] = analysis
            result['has_deepface_analysis'] = True
        
        return result
    
    def get_detector_info(self) -> Dict:
        """
        获取检测器信息
        
        Returns:
            dict: 检测器配置信息
        """
        return {
            'primary_backend': self.primary_backend,
            'deepface_enabled': self.enable_deepface,
            'deepface_available': DEEPFACE_AVAILABLE,
            'supported_features': {
                'face_detection': True,
                'face_tracking': self.primary_backend == 'yunet',
                'age_analysis': self.enable_deepface,
                'gender_analysis': self.enable_deepface,
                'emotion_analysis': self.enable_deepface,
                'race_analysis': self.enable_deepface,
                'face_comparison': self.enable_deepface
            }
        }

# 使用示例
if __name__ == "__main__":
    # 测试DeepFace可用性
    if DEEPFACE_AVAILABLE:
        print("DeepFace可用，可以使用高级功能")
        
        # 创建混合检测器
        detector = HybridFaceDetector(
            primary_backend='yunet',  # 使用YuNet作为主要检测器
            enable_deepface=True      # 启用DeepFace分析功能
        )
        
        # 显示检测器信息
        info = detector.get_detector_info()
        print("检测器配置:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    else:
        print("DeepFace不可用，仅使用YuNet检测功能")
        detector = HybridFaceDetector(primary_backend='yunet', enable_deepface=False)
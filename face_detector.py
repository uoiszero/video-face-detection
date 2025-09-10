import cv2
import numpy as np
import os
import time

class VideoFaceDetector:
    """
    视频人脸检测器类
    用于检测视频文件中的人脸并生成带标注的输出视频
    使用YuNet深度学习人脸检测模型，支持人脸跟踪以减少马赛克抖动
    """
    
    def __init__(self, model_path=None):
        """
        初始化人脸检测器
        
        Args:
            model_path (str): YuNet模型文件路径，如果为None则使用默认路径
        """
        if model_path is None:
            # 使用项目中的YuNet模型
            self.model_path = os.path.join(os.path.dirname(__file__), 'models', 'face_detection_yunet_2023mar_int8bq.onnx')
        else:
            self.model_path = model_path
            
        # 检查模型文件是否存在
        if not os.path.exists(self.model_path):
            raise ValueError(f"无法找到YuNet模型文件: {self.model_path}")
            
        # 初始化YuNet人脸检测器
        # 输入尺寸设为320x320，置信度阈值0.9，NMS阈值0.3
        self.detector = cv2.FaceDetectorYN.create(
            model=self.model_path,
            config="",
            input_size=(320, 320),
            score_threshold=0.9,
            nms_threshold=0.3,
            top_k=5000
        )
        
        # 人脸跟踪相关变量
        self.face_history = []  # 存储最近几帧的人脸位置
        self.history_length = 5  # 保持最近5帧的历史记录
        self.tracking_threshold = 50  # 人脸位置变化阈值
    
    def detect_faces_in_frame(self, frame):
        """
        在单帧图像中检测人脸
        
        Args:
            frame (numpy.ndarray): 输入的图像帧
            
        Returns:
            list: 检测到的人脸矩形框列表，每个元素为(x, y, w, h)
        """
        # 获取图像尺寸
        height, width = frame.shape[:2]
        
        # 设置检测器的输入尺寸为当前帧的尺寸
        self.detector.setInputSize((width, height))
        
        # 使用YuNet检测人脸
        _, faces = self.detector.detect(frame)
        
        # 转换检测结果格式
        face_boxes = []
        if faces is not None:
            for face in faces:
                # YuNet返回的格式: [x, y, w, h, x_re, y_re, x_le, y_le, x_nt, y_nt, x_rcm, y_rcm, x_lcm, y_lcm]
                # 我们只需要前4个值: x, y, w, h
                x, y, w, h = face[:4].astype(int)
                face_boxes.append((x, y, w, h))
        
        return face_boxes
    
    def track_faces_with_history(self, current_faces):
        """
        使用历史帧信息跟踪人脸，减少马赛克抖动
        
        Args:
            current_faces (list): 当前帧检测到的人脸列表
            
        Returns:
            list: 经过跟踪平滑处理的人脸列表
        """
        # 如果当前帧检测到人脸，直接使用并更新历史记录
        if len(current_faces) > 0:
            self.face_history.append(current_faces)
            # 保持历史记录长度
            if len(self.face_history) > self.history_length:
                self.face_history.pop(0)
            return current_faces
        
        # 如果当前帧没有检测到人脸，尝试使用历史信息
        if len(self.face_history) == 0:
            return []  # 没有历史记录，返回空列表
        
        # 使用最近一帧的人脸位置作为预测位置
        last_faces = self.face_history[-1]
        
        # 检查历史记录的一致性，如果最近几帧都有人脸，则继续使用
        recent_frames_with_faces = 0
        for hist_faces in self.face_history[-3:]:  # 检查最近3帧
            if len(hist_faces) > 0:
                recent_frames_with_faces += 1
        
        # 如果最近3帧中至少有2帧检测到人脸，则使用历史位置
        if recent_frames_with_faces >= 2:
            # 添加空的当前帧到历史记录（表示这一帧使用了预测位置）
            self.face_history.append([])
            if len(self.face_history) > self.history_length:
                self.face_history.pop(0)
            return last_faces
        else:
            # 历史记录不够一致，清空历史并返回空列表
            self.face_history.append([])
            if len(self.face_history) > self.history_length:
                self.face_history.pop(0)
            return []
    
    def draw_faces(self, frame, faces):
        """
        在图像帧上绘制人脸检测框
        
        Args:
            frame (numpy.ndarray): 输入的图像帧
            faces (list): 人脸矩形框列表
            
        Returns:
            numpy.ndarray: 绘制了检测框的图像帧
        """
        result_frame = frame.copy()
        
        for (x, y, w, h) in faces:
            # 绘制矩形框
            cv2.rectangle(result_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # 添加标签
            cv2.putText(result_frame, 'Face', (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        return result_frame
    
    def apply_mosaic_to_faces(self, frame, faces, mosaic_size=15):
        """
        对检测到的人脸区域应用椭圆形马赛克效果
        
        Args:
            frame (numpy.ndarray): 输入的图像帧
            faces (list): 人脸矩形框列表
            mosaic_size (int): 马赛克块的大小，值越小马赛克越细腻
            
        Returns:
            numpy.ndarray: 应用了椭圆形马赛克效果的图像帧
        """
        result_frame = frame.copy()
        
        for (x, y, w, h) in faces:
            # 确保坐标在图像范围内
            x = max(0, x)
            y = max(0, y)
            w = min(w, frame.shape[1] - x)
            h = min(h, frame.shape[0] - y)
            
            # 提取人脸区域
            face_region = result_frame[y:y+h, x:x+w]
            
            # 计算马赛克后的尺寸
            mosaic_h = max(1, h // mosaic_size)
            mosaic_w = max(1, w // mosaic_size)
            
            # 缩小图像
            small_face = cv2.resize(face_region, (mosaic_w, mosaic_h), interpolation=cv2.INTER_LINEAR)
            
            # 放大回原尺寸，使用最近邻插值产生马赛克效果
            mosaic_face = cv2.resize(small_face, (w, h), interpolation=cv2.INTER_NEAREST)
            
            # 创建椭圆形遮罩
            mask = np.zeros((h, w), dtype=np.uint8)
            
            # 计算椭圆中心和轴长
            center_x = w // 2
            center_y = h // 2
            # 椭圆的半轴长度，扩大10%以更好地遮挡面部
            axis_x = int(w * 0.50)  # 水平半轴（从45%增加到50%）
            axis_y = int(h * 0.66)  # 垂直半轴（从60%增加到66%），人脸通常是竖向的椭圆
            
            # 绘制填充的椭圆遮罩
            cv2.ellipse(mask, (center_x, center_y), (axis_x, axis_y), 0, 0, 360, 255, -1)
            
            # 将遮罩转换为3通道
            mask_3d = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
            
            # 应用椭圆形马赛克：只在椭圆区域内应用马赛克效果
            blended_region = face_region * (1 - mask_3d) + mosaic_face * mask_3d
            
            # 将处理后的区域放回原图
            result_frame[y:y+h, x:x+w] = blended_region.astype(np.uint8)
        
        return result_frame
    
    def process_video(self, input_path, output_path=None, show_preview=False, apply_mosaic=False, mosaic_size=15, progress_callback=None):
        """
        处理视频文件，检测其中的人脸
        
        Args:
            input_path (str): 输入视频文件路径
            output_path (str): 输出视频文件路径，如果为None则不保存
            show_preview (bool): 是否显示实时预览
            apply_mosaic (bool): 是否对人脸应用马赛克效果
            mosaic_size (int): 马赛克块大小，仅在apply_mosaic=True时有效
            progress_callback (callable): 进度回调函数，接收(当前帧数, 总帧数)参数，返回是否继续处理
            
        Returns:
            dict: 处理结果统计信息
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"输入视频文件不存在: {input_path}")
        
        # 打开视频文件
        cap = cv2.VideoCapture(input_path)
        
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {input_path}")
        
        # 获取视频属性
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # 获取输入视频的编码器信息
        input_fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        input_codec = "".join([chr((input_fourcc >> 8 * i) & 0xFF) for i in range(4)])
        
        print(f"视频信息: {width}x{height}, {fps}fps, 总帧数: {total_frames}")
        print(f"输入视频编码器: {input_codec}")
        
        # 设置输出视频编码器
        out = None
        if output_path:
            # 首先尝试使用与输入视频相同的编码器
            if input_fourcc != 0:  # 确保获取到了有效的编码器信息
                print(f"尝试使用输入视频的编码器: {input_codec}")
                out = cv2.VideoWriter(output_path, input_fourcc, fps, (width, height))
            
            # 如果输入编码器不可用或无效，尝试使用H.264编码器
            if not out or not out.isOpened():
                print("输入编码器不可用，尝试使用H.264编码器")
                fourcc = cv2.VideoWriter_fourcc(*'H264')
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            # 如果H.264不可用，尝试使用avc1编码器（H.264的另一种标识）
            if not out.isOpened():
                print("H.264编码器不可用，尝试使用avc1编码器")
                fourcc = cv2.VideoWriter_fourcc(*'avc1')
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            # 如果avc1不可用，回退到XVID编码器
            if not out.isOpened():
                print("avc1编码器不可用，尝试使用XVID编码器")
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                
            # 如果XVID也不可用，使用mp4v作为最后的选择
            if not out.isOpened():
                print("XVID编码器不可用，使用mp4v编码器")
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                
            # 检查编码器是否成功初始化
            if not out.isOpened():
                raise ValueError(f"无法初始化视频编码器，请检查输出路径: {output_path}")
            
            print(f"成功初始化视频编码器")
        
        # 统计信息
        processed_frames = 0
        frames_with_faces = 0
        total_faces_detected = 0
        
        # 记录开始时间
        start_time = time.time()
        
        print("开始处理视频...")
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # 检测人脸
                detected_faces = self.detect_faces_in_frame(frame)
                
                # 统一使用跟踪算法来保持两种模式的一致性
                faces = self.track_faces_with_history(detected_faces)
                
                if apply_mosaic:
                    # 马赛克模式
                    result_frame = self.apply_mosaic_to_faces(frame, faces, mosaic_size)
                else:
                    # 预览模式，绘制检测框
                    result_frame = self.draw_faces(frame, faces)
                
                # 更新统计信息（基于实际检测结果，不是跟踪结果）
                processed_frames += 1
                if len(detected_faces) > 0:
                    frames_with_faces += 1
                    total_faces_detected += len(detected_faces)
                
                # 保存到输出视频
                if out:
                    out.write(result_frame)
                
                # 显示预览
                if show_preview:
                    cv2.imshow('人脸检测', result_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("用户中断处理")
                        break
                
                # 调用进度回调
                if progress_callback:
                    should_continue = progress_callback(processed_frames, total_frames)
                    if not should_continue:
                        print("用户中断处理")
                        break
                
                # 显示进度
                if processed_frames % 30 == 0:
                    progress = (processed_frames / total_frames) * 100
                    print(f"处理进度: {progress:.1f}% ({processed_frames}/{total_frames})")
        
        finally:
            # 释放资源
            cap.release()
            if out:
                out.release()
            if show_preview:
                cv2.destroyAllWindows()
        
        # 计算处理时间和性能指标
        end_time = time.time()
        processing_time = end_time - start_time
        fps_processed = processed_frames / processing_time if processing_time > 0 else 0
        
        # 返回处理结果
        result = {
            'processed_frames': processed_frames,
            'frames_with_faces': frames_with_faces,
            'total_faces_detected': total_faces_detected,
            'detection_rate': frames_with_faces / processed_frames if processed_frames > 0 else 0,
            'processing_time': processing_time,
            'fps_processed': fps_processed
        }
        
        print(f"\n处理完成!")
        print(f"总处理帧数: {result['processed_frames']}")
        print(f"检测到人脸的帧数: {result['frames_with_faces']}")
        print(f"总检测人脸数: {result['total_faces_detected']}")
        print(f"人脸检测率: {result['detection_rate']:.2%}")
        print(f"处理时间: {result['processing_time']:.2f}秒")
        print(f"处理速度: {result['fps_processed']:.2f}帧/秒")
        
        return result
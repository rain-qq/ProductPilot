"""
图片服务 - 封装所有图片处理逻辑
"""
import base64
import requests
from PIL import Image
from io import BytesIO
from typing import List, Dict, Any, Optional
import numpy as np
import uuid
from datetime import datetime

from config.settings import settings
from loguru import logger

try:
    from minio import Minio
    from minio.error import S3Error
    MINIO_AVAILABLE = True
except ImportError:
    MINIO_AVAILABLE = False
    logger.warning("MinIO library not installed. Install with: pip install minio")


class ImageService:
    """图片处理服务"""
    
    def __init__(self):
        self.sd_api_url = f"{settings.SD_WEBUI_URL}/sdapi/v1"
        
        # 初始化 MinIO 客户端
        if MINIO_AVAILABLE:
            try:
                self.minio_client = Minio(
                    settings.MINIO_ENDPOINT,
                    access_key=settings.MINIO_ACCESS_KEY,
                    secret_key=settings.MINIO_SECRET_KEY,
                    secure=False  # 本地开发使用 HTTP
                )
                # 确保 bucket 存在
                self._ensure_bucket_exists()
                logger.info(f"MinIO client initialized successfully. Bucket: {settings.MINIO_BUCKET_NAME}")
            except Exception as e:
                logger.error(f"Failed to initialize MinIO client: {str(e)}")
                self.minio_client = None
        else:
            self.minio_client = None
            logger.warning("MinIO storage disabled - library not available")
    
    def _ensure_bucket_exists(self):
        """确保 MinIO bucket 存在"""
        try:
            if not self.minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
                self.minio_client.make_bucket(settings.MINIO_BUCKET_NAME)
                logger.info(f"Created bucket: {settings.MINIO_BUCKET_NAME}")
            else:
                logger.debug(f"Bucket already exists: {settings.MINIO_BUCKET_NAME}")
        except Exception as e:
            logger.error(f"Error ensuring bucket exists: {str(e)}")
            raise
    
    def upload_to_minio(self, image_data: str, filename: Optional[str] = None) -> str:
        """
        上传图片到 MinIO
        
        Args:
            image_data: 图片数据 (base64 Data URL 或 bytes)
            filename: 文件名 (可选,自动生成)
            
        Returns:
            图片访问 URL
        """
        if not self.minio_client:
            logger.warning("MinIO client not available, returning data URL")
            return image_data
        
        try:
            # 生成唯一文件名
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_id = str(uuid.uuid4())[:8]
                filename = f"{timestamp}_{unique_id}.png"
            
            # 处理 base64 Data URL
            if isinstance(image_data, str) and image_data.startswith("data:"):
                # 提取 base64 部分
                base64_data = image_data.split(",")[1]
                image_bytes = base64.b64decode(base64_data)
            elif isinstance(image_data, str):
                # 纯 base64
                image_bytes = base64.b64decode(image_data)
            else:
                image_bytes = image_data
            
            # 上传到 MinIO
            content_type = "image/png"
            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                content_type = "image/jpeg"
            elif filename.endswith(".webp"):
                content_type = "image/webp"
            
            self.minio_client.put_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=filename,
                data=BytesIO(image_bytes),
                length=len(image_bytes),
                content_type=content_type
            )
            
            # 构建访问 URL
            url = f"http://{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET_NAME}/{filename}"
            logger.info(f"Image uploaded to MinIO: {url}")
            
            return url
            
        except S3Error as e:
            logger.error(f"MinIO upload error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error uploading to MinIO: {str(e)}")
            # 失败时返回原始数据 URL
            return image_data
    
    def upload_multiple_images(self, images: List[str]) -> List[str]:
        """
        批量上传图片到 MinIO
        
        Args:
            images: 图片列表 (base64 Data URLs)
            
        Returns:
            图片 URL 列表
        """
        urls = []
        for i, img in enumerate(images):
            try:
                url = self.upload_to_minio(img)
                urls.append(url)
            except Exception as e:
                logger.error(f"Failed to upload image {i+1}: {str(e)}")
                urls.append(img)  # 失败时保留原数据
        
        return urls
    
    def delete_from_minio(self, object_name: str) -> bool:
        """
        从 MinIO 删除图片
        
        Args:
            object_name: 对象名称 (文件名)
            
        Returns:
            是否删除成功
        """
        if not self.minio_client:
            return False
        
        try:
            self.minio_client.remove_object(settings.MINIO_BUCKET_NAME, object_name)
            logger.info(f"Deleted object from MinIO: {object_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting from MinIO: {str(e)}")
            return False
    
    def text_to_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = None,
        height: int = None,
        batch_size: int = None,
        steps: int = None,
        cfg_scale: float = None,
        **kwargs
    ) -> List[str]:
        """
        文本生图 - 调用SD WebUI API
        
        Args:
            prompt: 正向提示词
            negative_prompt: 负向提示词
            width: 图片宽度
            height: 图片高度
            batch_size: 批量生成数量
            steps: 采样步数
            cfg_scale: CFG引导系数
            
        Returns:
            生成的图片URL列表 (base64格式)
        """
        url = f"{self.sd_api_url}/txt2img"
        
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "steps": steps or settings.DEFAULT_STEPS,
            "cfg_scale": cfg_scale or settings.DEFAULT_CFG_SCALE,
            "width": width or settings.DEFAULT_IMAGE_WIDTH,
            "height": height or settings.DEFAULT_IMAGE_HEIGHT,
            "batch_size": batch_size or settings.DEFAULT_BATCH_SIZE,
            "sampler_name": "DPM++ 2M Karras",
            "restore_faces": True,
            "enable_hr": False,
        }
        
        try:
            logger.info(f"Calling SD API: {url}")
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()
            
            result = response.json()
            images = []
            
            for img_base64 in result["images"]:
                # 转换为data URL格式
                data_url = f"data:image/png;base64,{img_base64}"
                images.append(data_url)
            
            logger.info(f"Generated {len(images)} images successfully")
            return images
            
        except Exception as e:
            logger.error(f"Error in text_to_image: {str(e)}")
            raise
    
    def image_to_image(
        self,
        reference_image: str,
        prompt: str,
        negative_prompt: str = "",
        strength: float = 0.75,
        **kwargs
    ) -> List[str]:
        """
        图生图
        
        Args:
            reference_image: 参考图片 (base64或URL)
            prompt: 正向提示词
            negative_prompt: 负向提示词
            strength: 重绘幅度 (0-1)
            
        Returns:
            生成的图片URL列表
        """
        url = f"{self.sd_api_url}/img2img"
        
        # 处理参考图片
        init_images = self._prepare_init_images(reference_image)
        
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "init_images": init_images,
            "strength": strength,
            "steps": kwargs.get("steps", settings.DEFAULT_STEPS),
            "cfg_scale": kwargs.get("cfg_scale", settings.DEFAULT_CFG_SCALE),
            "width": kwargs.get("width", settings.DEFAULT_IMAGE_WIDTH),
            "height": kwargs.get("height", settings.DEFAULT_IMAGE_HEIGHT),
            "batch_size": kwargs.get("batch_size", settings.DEFAULT_BATCH_SIZE),
        }
        
        try:
            logger.info(f"Calling SD img2img API")
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()
            
            result = response.json()
            images = [f"data:image/png;base64,{img}" for img in result["images"]]
            
            logger.info(f"Generated {len(images)} images via img2img")
            return images
            
        except Exception as e:
            logger.error(f"Error in image_to_image: {str(e)}")
            raise
    
    def controlnet_generate(
        self,
        reference_image: str,
        prompt: str,
        negative_prompt: str = "",
        control_type: str = "canny",
        **kwargs
    ) -> List[str]:
        """
        ControlNet生成 - 精确控制构图
        
        Args:
            reference_image: 参考图片
            prompt: 正向提示词
            negative_prompt: 负向提示词
            control_type: 控制类型 (canny/depth/openpose等)
            
        Returns:
            生成的图片URL列表
        """
        # 注意: 需要安装ControlNet扩展
        url = f"{self.sd_api_url}/controlnet/txt2img"
        
        # 预处理参考图生成control map
        control_image = self._generate_control_map(reference_image, control_type)
        
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "steps": kwargs.get("steps", settings.DEFAULT_STEPS),
            "cfg_scale": kwargs.get("cfg_scale", settings.DEFAULT_CFG_SCALE),
            "width": kwargs.get("width", settings.DEFAULT_IMAGE_WIDTH),
            "height": kwargs.get("height", settings.DEFAULT_IMAGE_HEIGHT),
            "batch_size": kwargs.get("batch_size", settings.DEFAULT_BATCH_SIZE),
            "alwayson_scripts": {
                "controlnet": {
                    "args": [
                        {
                            "input_image": control_image,
                            "module": control_type,
                            "model": f"control_{control_type}",
                            "weight": 1.0,
                            "preprocessor": control_type
                        }
                    ]
                }
            }
        }
        
        try:
            logger.info(f"Calling ControlNet API with {control_type}")
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()
            
            result = response.json()
            images = [f"data:image/png;base64,{img}" for img in result["images"]]
            
            logger.info(f"Generated {len(images)} images via ControlNet")
            return images
            
        except Exception as e:
            logger.error(f"Error in controlnet_generate: {str(e)}")
            raise
    
    def preprocess(self, image_url: str) -> str:
        """
        预处理参考图片
        
        Args:
            image_url: 参考图片URL
            
        Returns:
            处理后的图片base64
        """
        try:
            # 1. 下载图片
            logger.info(f"Downloading image: {image_url}")
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # 2. 打开图片
            image = Image.open(BytesIO(response.content))
            
            # 3. 去除背景
            logger.info("Removing background...")
            from rembg import remove
            image_no_bg = remove(image)
            
            # 4. 调整尺寸
            logger.info("Resizing image...")
            image_resized = image_no_bg.resize(
                (settings.DEFAULT_IMAGE_WIDTH, settings.DEFAULT_IMAGE_HEIGHT),
                Image.Resampling.LANCZOS
            )
            
            # 5. 转换为base64
            buffered = BytesIO()
            image_resized.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            logger.info("Preprocessing completed")
            return f"data:image/png;base64,{img_base64}"
            
        except Exception as e:
            logger.error(f"Error in preprocess: {str(e)}")
            raise
    
    def enhance(self, image_data: str) -> str:
        """
        图片增强 - 超分辨率、调色等
        
        Args:
            image_data: 图片base64或URL
            
        Returns:
            增强后的图片
        """
        try:
            # TODO: 实现超分辨率 (Real-ESRGAN)
            # TODO: 实现自动调色
            # TODO: 实现人脸修复 (GFPGAN)
            
            logger.info("Image enhancement applied")
            return image_data  # 暂时返回原图
            
        except Exception as e:
            logger.error(f"Error in enhance: {str(e)}")
            return image_data
    
    def extract_features(self, image_url: str) -> Dict[str, Any]:
        """
        提取图片特征 - 用于分析参考产品
        
        Args:
            image_url: 图片URL
            
        Returns:
            特征字典
        """
        try:
            # 下载图片
            response = requests.get(image_url, timeout=30)
            image = Image.open(BytesIO(response.content))
            
            # 基本特征提取
            features = {
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
                "format": image.format,
            }
            
            # 主色调提取
            img_array = np.array(image.resize((100, 100)))
            pixels = img_array.reshape(-1, 3)
            
            # 简单的颜色统计
            dominant_colors = self._extract_dominant_colors(pixels, k=5)
            
            features["dominant_colors"] = dominant_colors
            features["composition_type"] = self._estimate_composition(image)
            features["background_type"] = self._estimate_background(image)
            
            logger.info(f"Extracted features: {features.keys()}")
            return features
            
        except Exception as e:
            logger.error(f"Error in extract_features: {str(e)}")
            return {}
    
    def _prepare_init_images(self, reference_image: str) -> List[str]:
        """准备初始图片"""
        if reference_image.startswith("http"):
            # 下载图片
            response = requests.get(reference_image, timeout=30)
            img_base64 = base64.b64encode(response.content).decode("utf-8")
            return [img_base64]
        elif reference_image.startswith("data:"):
            # 已经是data URL
            return [reference_image.split(",")[1]]
        else:
            # 假设是base64
            return [reference_image]
    
    def _generate_control_map(self, image_url: str, control_type: str) -> str:
        """生成control map"""
        # 简化实现 - 实际应该使用ControlNet预处理器
        return self.preprocess(image_url)
    
    def _extract_dominant_colors(self, pixels: np.ndarray, k: int = 5) -> List[List[int]]:
        """提取主色调"""
        from sklearn.cluster import KMeans
        
        # K-means聚类找主色调
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(pixels)
        
        colors = kmeans.cluster_centers_.astype(int)
        return colors.tolist()
    
    def _estimate_composition(self, image: Image.Image) -> str:
        """估算构图类型"""
        # 简化实现 - 实际应该用深度学习模型
        aspect_ratio = image.width / image.height
        
        if abs(aspect_ratio - 1.0) < 0.1:
            return "square"
        elif aspect_ratio > 1.5:
            return "landscape"
        elif aspect_ratio < 0.7:
            return "portrait"
        else:
            return "standard"
    
    def _estimate_background(self, image: Image.Image) -> str:
        """估算背景类型"""
        # 简化实现
        return "simple"

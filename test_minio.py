"""
测试 MinIO 图片存储功能
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from services.image_service import ImageService
from loguru import logger


def test_minio_connection():
    """测试 MinIO 连接"""
    print("=" * 60)
    print("测试 1: MinIO 连接")
    print("=" * 60)
    
    service = ImageService()
    
    if service.minio_client:
        print("✅ MinIO 客户端初始化成功")
        
        # 检查 bucket
        try:
            from config.settings import settings
            exists = service.minio_client.bucket_exists(settings.MINIO_BUCKET_NAME)
            if exists:
                print(f"✅ Bucket '{settings.MINIO_BUCKET_NAME}' 已存在")
            else:
                print(f"❌ Bucket '{settings.MINIO_BUCKET_NAME}' 不存在")
        except Exception as e:
            print(f"❌ 检查 bucket 失败: {e}")
    else:
        print("❌ MinIO 客户端未初始化")
        print("   可能原因:")
        print("   1. minio 库未安装: pip install minio")
        print("   2. MinIO 服务未启动")
        print("   3. 配置错误 (endpoint/access_key/secret_key)")
    
    print()


def test_upload_image():
    """测试上传图片"""
    print("=" * 60)
    print("测试 2: 上传示例图片到 MinIO")
    print("=" * 60)
    
    service = ImageService()
    
    if not service.minio_client:
        print("⚠️  MinIO 不可用,跳过上传测试")
        print()
        return
    
    # 创建一个简单的测试图片
    try:
        from PIL import Image
        import base64
        from io import BytesIO
        
        # 创建 100x100 的红色图片
        img = Image.new('RGB', (100, 100), color='red')
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        data_url = f"data:image/png;base64,{img_base64}"
        
        print("📤 正在上传测试图片...")
        url = service.upload_to_minio(data_url, filename="test_image.png")
        
        print(f"✅ 上传成功!")
        print(f"   URL: {url}")
        print()
        
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        print()


def test_batch_upload():
    """测试批量上传"""
    print("=" * 60)
    print("测试 3: 批量上传图片")
    print("=" * 60)
    
    service = ImageService()
    
    if not service.minio_client:
        print("⚠️  MinIO 不可用,跳过批量上传测试")
        print()
        return
    
    try:
        from PIL import Image
        import base64
        from io import BytesIO
        
        # 创建多个测试图片
        images = []
        colors = ['red', 'green', 'blue']
        
        for i, color in enumerate(colors):
            img = Image.new('RGB', (100, 100), color=color)
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            data_url = f"data:image/png;base64,{img_base64}"
            images.append(data_url)
        
        print(f"📤 正在上传 {len(images)} 张测试图片...")
        urls = service.upload_multiple_images(images)
        
        print(f"✅ 批量上传成功!")
        for i, url in enumerate(urls):
            print(f"   图片 {i+1}: {url}")
        print()
        
    except Exception as e:
        print(f"❌ 批量上传失败: {e}")
        print()


def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "MinIO 存储功能测试" + " " * 23 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # 运行测试
    test_minio_connection()
    test_upload_image()
    test_batch_upload()
    
    print("=" * 60)
    print("测试完成!")
    print("=" * 60)
    print()
    print("💡 提示:")
    print("   - 如果 MinIO 连接失败,请检查:")
    print("     1. Docker 中的 MinIO 服务是否运行")
    print("     2. .env 文件中的配置是否正确")
    print("     3. 防火墙是否允许访问 9000 端口")
    print()
    print("   - 查看 MinIO 控制台:")
    print("     http://localhost:9001 (默认账号: minioadmin/minioadmin)")
    print()


if __name__ == "__main__":
    main()

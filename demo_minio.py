"""
MinIO 图片存储功能演示
展示如何上传图片到 MinIO 并获取访问 URL
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from services.image_service import ImageService
from PIL import Image
from io import BytesIO
import base64


def demo_upload():
    """演示上传单张图片"""
    print("=" * 70)
    print("📤 演示 1: 上传单张图片到 MinIO")
    print("=" * 70)
    
    # 创建服务实例
    service = ImageService()
    
    if not service.minio_client:
        print("❌ MinIO 不可用,请检查配置")
        return
    
    # 创建一个示例图片 (渐变色彩)
    print("\n🎨 创建示例图片...")
    img = Image.new('RGB', (512, 512))
    pixels = img.load()
    
    for i in range(img.width):
        for j in range(img.height):
            r = int(255 * i / img.width)
            g = int(255 * j / img.height)
            b = 128
            pixels[i, j] = (r, g, b)
    
    # 转换为 base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    data_url = f"data:image/png;base64,{img_base64}"
    
    print("✅ 示例图片创建完成 (512x512 渐变色)")
    
    # 上传到 MinIO
    print("\n📤 正在上传到 MinIO...")
    url = service.upload_to_minio(data_url, filename="demo_gradient.png")
    
    print(f"\n✅ 上传成功!")
    print(f"   📍 文件位置: ecommerce-images/demo_gradient.png")
    print(f"   🔗 访问 URL: {url}")
    print(f"\n💡 提示: 在浏览器中打开上述 URL 即可查看图片")
    print()


def demo_batch_upload():
    """演示批量上传"""
    print("=" * 70)
    print("📦 演示 2: 批量上传多张图片")
    print("=" * 70)
    
    service = ImageService()
    
    if not service.minio_client:
        print("❌ MinIO 不可用")
        return
    
    # 创建多张不同颜色的图片
    print("\n🎨 创建 5 张不同颜色的示例图片...")
    colors = [
        ('red', (255, 0, 0)),
        ('green', (0, 255, 0)),
        ('blue', (0, 0, 255)),
        ('yellow', (255, 255, 0)),
        ('purple', (128, 0, 128))
    ]
    
    images = []
    for color_name, color_rgb in colors:
        img = Image.new('RGB', (256, 256), color=color_rgb)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        data_url = f"data:image/png;base64,{img_base64}"
        images.append(data_url)
        print(f"   ✓ {color_name.capitalize()}")
    
    # 批量上传
    print(f"\n📤 正在批量上传 {len(images)} 张图片...")
    urls = service.upload_multiple_images(images)
    
    print(f"\n✅ 批量上传成功!")
    print(f"\n📋 生成的文件列表:")
    for i, url in enumerate(urls):
        filename = url.split('/')[-1]
        print(f"   {i+1}. {filename}")
        print(f"      URL: {url}")
    
    print(f"\n💡 所有图片已保存到 MinIO Bucket: ecommerce-images")
    print(f"   访问 MinIO 控制台查看: http://localhost:9001")
    print()


def demo_workflow_integration():
    """演示工作流集成"""
    print("=" * 70)
    print("🔄 演示 3: 工作流自动上传 (模拟)")
    print("=" * 70)
    
    print("\nℹ️  说明:")
    print("   在实际使用中,当你调用图片生成 API 时:")
    print()
    print("   1. SD WebUI 生成图片 (base64 格式)")
    print("   2. LangGraph 工作流进行质量检查")
    print("   3. ✅ 自动上传所有图片到 MinIO")
    print("   4. 返回 MinIO URL (而非 base64)")
    print()
    print("   示例 API 响应:")
    print("   {")
    print('     "success": true,')
    print('     "images": [')
    print('       "http://localhost:9000/ecommerce-images/20260412_190326_xxx.png",')
    print('       "http://localhost:9000/ecommerce-images/20260412_190326_yyy.png"')
    print('     ],')
    print('     "selected_image": "http://localhost:9000/ecommerce-images/20260412_190326_xxx.png",')
    print('     "metadata": {')
    print('       "storage_type": "minio",')
    print('       "image_urls": [...]')
    print('     }')
    print("   }")
    print()
    print("💡 优势:")
    print("   ✓ 图片持久化存储,不会丢失")
    print("   ✓ 可通过 HTTP URL 直接访问")
    print("   ✓ 支持 CDN 加速")
    print("   ✓ 易于备份和管理")
    print()


def main():
    """运行所有演示"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "MinIO 图片存储演示" + " " * 28 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    try:
        demo_upload()
        demo_batch_upload()
        demo_workflow_integration()
        
        print("=" * 70)
        print("🎉 演示完成!")
        print("=" * 70)
        print()
        print("📚 更多信息:")
        print("   • MinIO 使用指南: MINIO_GUIDE.md")
        print("   • API 文档: API_DOCUMENTATION.md")
        print("   • 快速开始: QUICKSTART.md")
        print()
        print("🔗 相关链接:")
        print("   • MinIO 控制台: http://localhost:9001")
        print("   • API 文档: http://localhost:8000/docs")
        print()
        
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        print("\n请确保:")
        print("  1. MinIO 服务正在运行 (Docker)")
        print("  2. .env 文件配置正确")
        print("  3. 已安装 minio 库: pip install minio")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

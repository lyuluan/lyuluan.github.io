import os
from PIL import Image
import argparse

def convert_png_to_jpg(input_path, output_path, max_size_kb=1024):
    """
    将 PNG 转换为 JPG 并压缩至指定大小
    :param input_path: 输入文件路径
    :param output_path: 输出文件路径
    :param max_size_kb: 最大文件大小 (KB)
    """
    try:
        # 打开 PNG 图像
        with Image.open(input_path) as img:
            # 处理透明背景（转换为白色背景）
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])  # 使用 alpha 通道作为蒙版
                img = background
            
            # 动态调整质量直至满足大小要求
            quality = 95
            while quality >= 50:  # 设置最低质量阈值
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
                file_size_kb = os.path.getsize(output_path) / 1024
                
                if file_size_kb <= max_size_kb:
                    print(f"✅ 成功转换: {os.path.basename(input_path)} "
                          f"大小: {file_size_kb:.2f}KB, 质量: {quality}")
                    return True
                
                quality -= 5  # 未满足则降低质量
        
        print(f"⚠️ 无法压缩到目标大小: {os.path.basename(input_path)}")
        return False

    except Exception as e:
        print(f"❌ 转换失败 {os.path.basename(input_path)}: {str(e)}")
        return False

def batch_convert(input_dir, output_dir, max_size_kb=1024):
    """
    批量转换文件夹内所有 PNG
    :param input_dir: 输入目录
    :param output_dir: 输出目录
    :param max_size_kb: 目标文件大小 (KB)
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    success_count = 0
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(
                output_dir, 
                f"{os.path.splitext(filename)[0]}.jpg"
            )
            if convert_png_to_jpg(input_path, output_path, max_size_kb):
                success_count += 1
    
    print(f"\n🎉 转换完成: 成功 {success_count} 张图片")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PNG 批量转 JPG 压缩工具')
    parser.add_argument('-i', '--input', required=True, help='PNG图片目录路径')
    parser.add_argument('-o', '--output', required=True, help='JPG输出目录路径')
    parser.add_argument('-s', '--size', type=int, default=1024, 
                        help='目标文件大小上限(KB)')
    
    args = parser.parse_args()
    
    print(f"🔧 开始转换: {args.input} -> {args.output}")
    batch_convert(args.input, args.output, args.size)
from PIL import Image


# 定义名为zero_fill的函数，用于将数字字符串右对齐并填充零以达到指定宽度
def zero_fill(value, width=8):
    """Return a string with the specified width by right-aligning the value and padding with zeros."""
    return str(value).zfill(width)


# 定义名为encode_pixel的函数，用于将二进制编码嵌入到RGB像素值中
def encode_pixel(rgb, code):
    """Encode the code into the RGB pixel value."""
    encoded_rgb = []
    # 遍历RGB值和二进制编码的每一位，并进行编码处理
    for value, bit in zip(rgb, code):
        encoded_value = (value - value % 2) + int(bit)
        encoded_rgb.append(encoded_value)
    return tuple(encoded_rgb)


# 定义名为get_code的函数，用于将图像的RGB像素值转换为二进制编码
def get_code(image):
    """Convert the image's RGB pixel values into a binary code."""
    code = ""
    # 遍历图像的像素值
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            # 获取像素值的RGB分量
            rgb = image.getpixel((i, j))
            # 将RGB分量的每个值转换为二进制编码，并拼接到code字符串中
            for value in rgb:
                code += zero_fill(bin(value).replace('0b', ''))
    return code


# 定义名为encrypt_image的函数，用于加密源图像并保存结果
def encrypt_image(source_image_path, watermark_image_path, output_image_path):
    """Encrypt the source image with the watermark image and save the result."""
    # 打开源图像和水印图像，并将它们转换为RGB模式
    source_image = Image.open(source_image_path).convert('RGB')
    watermark_image = Image.open(watermark_image_path).convert('RGB')

    # 获取水印图像的二进制编码
    code = get_code(watermark_image)
    code_len = len(code)

    count = 0
    # 遍历源图像的像素值
    for i in range(source_image.size[0]):
        for j in range(source_image.size[1]):
            # 如果已经嵌入完整的编码，就退出循环
            if count == code_len:
                break

            # 获取源图像的像素值
            pixel = source_image.getpixel((i, j))
            # 将源图像的像素值与编码进行嵌入
            updated_pixel = encode_pixel(pixel, code[count:count + 3])
            count += 3
            # 更新源图像的像素值
            source_image.putpixel((i, j), updated_pixel)

    # 保存加密后的图像
    source_image.save(output_image_path)


if __name__ == "__main__":
    # 定义源图像、水印图像和输出图像的文件路径
    source_path = 'src.png'
    watermark_path = 'wm.png'
    output_path = 'encrypted.png'

    # 调用encrypt_image函数进行图像加密处理
    encrypt_image(source_path, watermark_path, output_path)

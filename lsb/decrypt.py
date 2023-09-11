from PIL import Image


# 定义名为extract_watermark的函数，用于从图像中提取水印
def extract_watermark(img, length):
    """
    从图像中提取水印。

    Args:
        img (PIL.Image.Image): 输入图像。
        length (int): 要提取的水印的长度。

    Returns:
        str: 提取的水印二进制字符串。
    """
    # 获取图像的宽度和高度
    width = img.size[0]
    height = img.size[1]
    count = 0
    str_wm = ""

    # 遍历图像像素
    for i in range(width):
        for j in range(height):
            # 获取像素点的RGB值
            rgb = img.getpixel((i, j))
            # 提取R通道的水印
            if count % 3 == 0:
                count += 1
                str_wm = str_wm + str(rgb[0] % 2)
                if count == length:
                    break
            # 提取G通道的水印
            if count % 3 == 1:
                count += 1
                str_wm = str_wm + str(rgb[1] % 2)
                if count == length:
                    break
            # 提取B通道的水印
            if count % 3 == 2:
                count += 1
                str_wm = str_wm + str(rgb[2] % 2)
                if count == length:
                    break
        if count == length:
            break
    return str_wm


# 定义名为create_image_from_watermark的函数，用于从提取的水印创建图像
def create_image_from_watermark(str_wm, img_width, img_height):
    """
    从提取的水印创建图像。

    Args:
        str_wm (str): 提取的水印二进制字符串。
        img_width (int): 原始图像的宽度。
        img_height (int): 原始图像的高度。

    Returns:
        PIL.Image.Image: 从水印创建的图像。
    """
    str1 = []
    # 将水印二进制字符串按8位分组转换为十进制值
    for i in range(0, len(str_wm), 8):
        str1.append(int(str_wm[i:i + 8], 2))

    # 创建输出图像
    wm = Image.new("RGB", (img_width + 1, img_height + 1))
    flag = 0

    # 将水印值恢复为图像像素并填充到输出图像
    for m in range(0, img_width):
        for n in range(0, img_height):
            if flag == len(str1):
                break
            wm.putpixel((m, n), (str1[flag], str1[flag + 1], str1[flag + 2]))
            flag += 3
        if flag == len(str1):
            break

    return wm


if __name__ == "__main__":
    # 定义输入图像、水印图像和输出图像的文件路径
    image_path = 'encrypted.png'
    watermark_path = 'wm.png'
    output_path = 'decrypted.png'

    # 打开水印图像以获取水印的宽度、高度和长度
    w_image = Image.open(watermark_path)
    image_width = w_image.size[0]
    image_height = w_image.size[1]
    length = image_width * image_height * 24

    # 打开加密图像并转换为RGB模式，然后提取水印
    img = Image.open(image_path).convert('RGB')
    str_wm = extract_watermark(img, length)

    # 从提取的水印创建图像并保存
    img_out = create_image_from_watermark(str_wm, image_width, image_height)
    img_out.save(output_path)

from PIL import Image


def main():
    pic = Image.open('lena_gray.bmp')
    pic.save('lena_gray.png', 'PNG')
    pic.close()


if __name__ == '__main__':
    main()

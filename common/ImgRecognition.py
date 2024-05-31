# -*- coding: utf-8 -*-
import pytesseract
from PIL import Image


class ImageRecognizer:
    def __init__(self, tesseract_cmd=r'.\common\Tesseract-OCR\tesseract.exe'):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def RecognizeText(self, image_path):
        try:
            image = Image.open(image_path)
            # 使用 pytesseract 识别图片中的文字
            image_text = pytesseract.image_to_string(image).replace('\n', '')
            return image_text
        except Exception as e:
            return f"Error recognizing text: {e}"

    def RecognizeDigits(self, image_path):
        try:
            image = Image.open(image_path)
            # 如果只想识别数字，可以使用 config 参数
            custom_config = r'--oem 3 --psm 6 outputbase digits'
            digits = pytesseract.image_to_string(image, config=custom_config).replace('\n', '')
            return digits
        except Exception as e:
            return f"Error recognizing digits: {e}"

    def contrast_test(self, image_path_base, image_path_other):
        image_base = self.RecognizeText(image_path_base)
        image_other = self.RecognizeDigits(image_path_other)
        if image_base == image_other:
            return True
        else:
            return False


class ImageCropper:
    def __init__(self, image_path):
        self.image = Image.open(image_path)

    def crop(self, left, top, right, bottom):
        """
        裁切图片
        :param left: 裁切区域的左边界
        :param top: 裁切区域的上边界
        :param right: 裁切区域的右边界
        :param bottom: 裁切区域的下边界
        :return: 裁切后的图片对象
        """
        # 获取图像尺寸
        width, height = self.image.size
        # 确保裁切区域在图像范围内
        left = max(0, left)
        top = max(0, top)
        right = min(width, right)
        bottom = min(height, bottom)

        if left >= right or top >= bottom:
            raise ValueError("Invalid crop dimensions")

        cropped_image = self.image.crop((left, top, right, bottom))
        return cropped_image

    def save_cropped_image(self, cropped_image, save_path):
        """
        保存裁切后的图片
        :param cropped_image: 裁切后的图片对象
        :param save_path: 保存路径
        """
        cropped_image.save(save_path)

    def crop_and_save(self, left, top, right, bottom, save_path):
        cropped_image = self.crop(left=left, top=top, right=right, bottom=bottom)
        self.save_cropped_image(cropped_image, save_path)


# 示例用法
if __name__ == "__main__":
    # 如果需要，设置 tesseract 可执行文件的路径
    # recognizer = ImageRecognizer(tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe')
    recognizer = ImageRecognizer()

    # text = recognizer.RecognizeText('Test.png')
    # print("Recognized Text:", text)
    #
    # digits = recognizer.RecognizeDigits('Test.png')
    # print("Recognized Digits:", digits)
    #
    # bool = recognizer.contrast_test('Test.png', 'Test.png')
    # print("Recognized bool:", bool)

    image_path = '../Img/phone_shot.png'
    save_path = '../Img/phone_shot_out.png'

    # cropper = ImageCropper(image_path)
    # cropped_image = cropper.crop(left=300, top=100, right=800, bottom=200)
    # cropper.save_cropped_image(cropped_image, save_path)
    # print(f"Cropped image saved to {save_path}")

    cropper = ImageCropper(image_path)
    cropper.crop_and_save(left=50, top=1750, right=150, bottom=1820, save_path=save_path)
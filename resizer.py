import pyautogui
from PIL import Image
import io


def resize(measure_unit,size):
    screen_width, screen_height = pyautogui.size()
    if measure_unit == "width":      
        new_screen_width = (size * 100) / 1920
        new_screen_width = (new_screen_width * screen_width) / 100 
        return new_screen_width
    if measure_unit == "height":        
        new_screen_height = (size * 100) / 1080
        new_screen_height = (new_screen_height * screen_height) / 100 
        return new_screen_height


def resize_img(img_path):
    # Carregue a imagem
    img_byte_arr = io.BytesIO()
    image = Image.open(img_path)
    img_width, img_height = image.size
    img_new_width = int(resize('width', img_width))
    img_new_height = int(resize('height', img_height))
    # Redimensione a imagem para um tamanho de largura 500 pixels e altura 300 pixels
    image = image.resize((img_new_width, img_new_height))
    image = image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


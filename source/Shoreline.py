### Inicio importações
import rasterio
import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
### Fim importações

# path = dataset_path
# path_ = ""

def apply_filter(path, value_fG, value_tM, value_fC):
    banda = converter_imagem_array_numpy(path)
    filtro_G = filtro_gaussiano(banda, value_fG)
    trans_M = transformacao_morfologica(filtro_G, value_tM)
    thre = threshold(trans_M, 0)
    image_final = extração_bordas(thre, value_fC)

    exibir(image_final)

def open_image():
    dataset_path = filedialog.askopenfilename(
    initialdir = "/Downloads/",
    title = "Selecione a imagem",
    filetypes = (("Arquivos tif", "*.tif"), ("Todos os arquivos", "*.*")))

    global global_path 
    global_path = dataset_path

    return dataset_path
 

def configure_images(image_original, path):
    image_original = Image.open(path)
    image_resized = image_original.resize(size=[494, 334])
    new_image = ImageTk.PhotoImage(image_resized)

    return new_image

def configure_labels(image_label_original, image_label_filtrada):
    path = open_image()
    configure_image_original(image_label_original, path)
    configure_image_filtrada(image_label_filtrada, path)

### Início Método
def configure_image_original(image_label_original, path):

    image = configure_images(image_label_original, path)
    image_label_original.configure(image=image, width=493, height=333)
    image_label_original.image=image
### Fim Método 

### Início Método
def configure_image_filtrada(image_label_filtrada, path):

    image = configure_images(image_label_filtrada, path)
    image_label_filtrada.configure(image=image, width=493, height=333)
    image_label_filtrada.image=image
### Fim Método 

### -------------------------------------------------------------------------###

### Início Método 2
def converter_imagem_array_numpy(path):
    image_banda = rasterio.open(path)
    banda = image_banda.read(1)

    return banda
### Fim Método 2

### Início Método 3
def filtro_gaussiano(banda, value):
    # value tem que ser positivo e ímpar
    if(value % 2 == 0):
        value += 1
        
    filtro_gaussiano = cv2.GaussianBlur(banda, (value, value), 0)
    return filtro_gaussiano
### Fim Método 3

    ### Início Método 4
def transformacao_morfologica(filtro_gaussiano, value):

    kernel = np.ones((value,value), np.uint8)
    transformacao_morfologica = cv2.morphologyEx(filtro_gaussiano, cv2.MORPH_OPEN, kernel)

    return transformacao_morfologica
### Fim Método 4

### Início Método 5
def threshold(transformacao_morfologica, value):
    _,threshold = cv2.threshold(transformacao_morfologica, value, 255, cv2.THRESH_BINARY_INV);

    return threshold
### Fim Método 5

### Início Método 5
def extração_bordas(threshold, value):
    im_outCopy = np.uint8(threshold)
    image_final = cv2.Canny(im_outCopy,value,200)

    return image_final
    ### Fim Método 5

def exibir(image):
    cv2.imshow("Bordas", image)
    cv2.waitKey(0)

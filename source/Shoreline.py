### Inicio importações
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import rasterio
import cv2
import numpy as np
### Fim importações

class Shoreline():
    ### Inicio Método 
    def obter_path_image(self):
        dataset_path = filedialog.askopenfilename(
        initialdir = "/Downloads/",
        title = "Selecione a imagem",
        filetypes = (("Arquivos tif", "*.tif"), ("Todos os arquivos", "*.*")))
        
        return dataset_path
    ### Fim Método 
    
    ### Início Método 
    def redimensionar_image_root(self, dataset_path):
        image_original = Image.open(dataset_path)
        
        new_image = image_original.resize(size=[494, 334])
        
        image = ImageTk.PhotoImage(new_image)

        return image
    ### Fim Método 

    ### Início Método 
    def configure_label(self, label_original, label_filtrada):
        path = Shoreline.obter_path_image(self)
        image = Shoreline.redimensionar_image_root(self, path)

        label_original.configure(image=image, width=493, height=333)
        label_original.image=image

        label_filtrada.configure(image=image, width=493, height=333)
        label_filtrada.image=image

        return path

    ### Fim Método 

    ### Início Método 2
    def converter_imagem_array_numpy(self, image):
        banda = image.read(1)

        return banda
    ### Fim Método 2

    ### Início Método 3
    def filtro_gaussiano(self, banda, value):
        # value tem que ser positivo e ímpar
        filtro_gaussiano = cv2.GaussianBlur(banda, (value, value), 0)

        return filtro_gaussiano
    ### Fim Método 3

    ### Início Método 4
    def transformacao_morfologica(self, filtro_gaussiano, value):

        kernel = np.ones((value,value), np.uint8)
        transformacao_morfologica = cv2.morphologyEx(filtro_gaussiano, cv2.MORPH_OPEN, kernel)

        return transformacao_morfologica
    ### Fim Método 4

    ### Início Método 5
    def threshold(self, transformacao_morfologica, value):
        _, threshold = cv2.threshold(transformacao_morfologica, value, 255, cv2.THRESH_BINARY_INV);

        return threshold
    ### Fim Método 5

    ### Início Método 5
    def extração_bordas(self, threshold, value):
        im_outCopy = np.uint8(threshold)
        edges = cv2.Canny(im_outCopy,value,200)

        return edges
    ### Fim Método 5

    def exibir(self, edges):
        cv2.imshow("Bordas", edges)
        cv2.waitKey(0)

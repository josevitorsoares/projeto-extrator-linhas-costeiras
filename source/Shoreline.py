### Inicio importações
import rasterio
import cv2
import numpy as np
import matplotlib.pyplot as plt
from rasterio.plot import show
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from Filtro_Sobel import Filter_Sobel
### Fim importações

class Shoreline:

    def __init__(self):
        super().__init__()

        self.global_path = ""
        self.isApplied = False

    def open_image(self):
        dataset_path = filedialog.askopenfilename(
        initialdir = "/Downloads/",
        title = "Selecione a imagem",
        filetypes = (("Arquivos tif", "*.tif"), ("Arquivos tiff", "*.tiff")),)
    
        self.global_path = dataset_path

        return dataset_path

    def plot_image_original(self, figure_original, image_original):
        path = self.open_image(self)

        ax = figure_original.add_subplot(111)
        figure_original.subplots_adjust(bottom=0, right=1, top=1, left=0, wspace=0, hspace=0)

        with rasterio.open(r''f'{path}') as src_plot:
            show(src_plot, ax=ax, cmap='gist_gray')
        plt.close()
        ax.set(title="",xticks=[], yticks=[])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        image_original.draw()

    def plot_image_filtered(self, figure_filtered, image_filtered, image_final):
        ax = figure_filtered.add_subplot(111)
        figure_filtered.subplots_adjust(bottom=0, right=1, top=1, left=0, wspace=0, hspace=0)

        with rasterio.open(r''f'{image_final}') as src_plot:
            show(src_plot, ax=ax, cmap='gist_gray')
        plt.close()
        ax.set(title="",xticks=[], yticks=[])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        image_filtered.draw()

    def converter_imagem_array_numpy(self, path):
        image_banda = rasterio.open(path)
        banda = image_banda.read(1)
        
        return banda

    def filtro_gaussiano(self, banda, value):
    # value tem que ser positivo e ímpar
        if(value % 2 == 0):
            value += 1
            
        filtro_gaussiano = cv2.GaussianBlur(banda, (value, value), 0)
        return filtro_gaussiano

    def transformacao_morfologica(self, filtro_gaussiano, value):

        kernel = np.ones((value,value), np.uint8)
        transformacao_morfologica = cv2.morphologyEx(filtro_gaussiano, cv2.MORPH_OPEN, kernel)

        return transformacao_morfologica

    def threshold(self, transformacao_morfologica):
        _,threshold = cv2.threshold(transformacao_morfologica, 0, 255, cv2.THRESH_BINARY_INV);

        return threshold

    def extração_bordas(self, threshold, progress_bar):
        path_image_filtered = "assets/GeoTIFF/edges_output.tiff"
        teste = Filter_Sobel(self.global_path, threshold, path_image_filtered)
        
        teste.start()
        self.monitor(self, teste, progress_bar)

        return path_image_filtered  

    def monitor(self, thread, progress_bar):
        progress_bar.start()
        if(thread.is_alive()):
            # check the thread every 100ms
            self.after(100, lambda: self.monitor(thread))
        else:
            progress_bar.stop()
    
    def apply_filter(self, value_fG, value_tM, figure_filtered, image_filtered, progress_bar):
        self.isApplied = True
        file_extension = Path(self.global_path).suffix
        if(self.global_path == ""):
            messagebox.showerror(
                title="Nenhuma imagem selecionada",
                message="Selecione uma imagem para que possa aplicar os filtos.",
            )
        elif(file_extension != ".tiff" and file_extension != ".tif"):
            messagebox.showerror(
                title="Erro no formato da Imagem",
                message="A extensão da imagem está incorreta. Extensão correta: .tif ou .tiff"
            )
        else: 
            banda = self.converter_imagem_array_numpy(self, self.global_path)
            filtro_G = self.filtro_gaussiano(self,banda, value_fG)
            trans_M = self.transformacao_morfologica(self,filtro_G, value_tM)
            threshold = self.threshold(self, trans_M)
            image_final = self.extração_bordas(self, threshold, progress_bar)
            self.plot_image_filtered(self, figure_filtered, image_filtered, image_final)
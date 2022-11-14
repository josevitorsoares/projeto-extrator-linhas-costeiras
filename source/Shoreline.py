### Inicio importações
import time
import rasterio
import cv2
import numpy as np
import matplotlib.pyplot as plt
from rasterio.plot import show
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
### Fim importações

class Shoreline:

    global_path = ""
    isApplied = False
    metadados = ""
    temp_var = 0
    path_image_filtered = "assets/GeoTIFF/edges_output.tiff"
    
    def __init__(self):
        super().__init__()

    def open_image(self):
        dataset_path = filedialog.askopenfilename(
        initialdir = "/Downloads/",
        title = "Selecione a imagem",
        filetypes = (("Arquivos tif", "*.tif"), ("Arquivos tiff", "*.tiff")),)
    
        self.global_path = dataset_path

        return dataset_path

    def plot_image_original(self, figure_original, image_original):
        path = self.open_image(self)

        figure_original.clear()

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
        figure_filtered.clear()

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

    def plot_progress_bar(interface, progress_bar):
        progress_bar['value'] = 0
        time.sleep(0.5)
        while progress_bar['value'] < 100:
            progress_bar['value'] += 20
            #root.update_idletasks()
            interface.update()
            time.sleep(0.5)
        progress_bar['value'] = 0

    def converter_imagem_array_numpy(self):
        image_banda = rasterio.open(rf"{self.global_path}")
        self.metadados = image_banda.profile
        banda = image_banda.read(1)
        
        return banda

    def filtro_gaussiano(self, value):
        # value tem que ser positivo e ímpar
        banda = self.converter_imagem_array_numpy(self)
        if(value == 0):
            self.temp_var = banda
        elif(value % 2 == 0 and value != 0):
            value = value + 1
        
            filtro_gaussiano = cv2.GaussianBlur(banda, (value, value), 0)

            self.temp_var = filtro_gaussiano

    def transformacao_morfologica(self, value, ischecked):
        if(value == 0):
            self.threshold(self, self.temp_var, ischecked)
        else:
            kernel = np.ones((value,value), np.uint8)
            transformacao_morfologica = cv2.morphologyEx(self.temp_var, cv2.MORPH_OPEN, kernel)

            self.threshold(self, transformacao_morfologica, ischecked)


    def threshold(self, transformacao_morfologica, ischecked):
        if(ischecked == 1):
            _,self.thre = cv2.threshold(transformacao_morfologica, 0, 255, cv2.THRESH_BINARY);
            self.extração_bordas(self, self.thre)
        else:
            self.extração_bordas(self, transformacao_morfologica)

    def extração_bordas(self, threshold):
        im_outCopy = np.uint8(threshold)
        edges = cv2.Canny(im_outCopy,100,200)

        with rasterio.open(f'{self.path_image_filtered}', 'w', **self.metadados) as output_dataset:
            output_dataset.write(edges, 1)

    
    def apply_filter(self, value_fG, value_tM, figure_filtered, image_filtered, progress_bar, interface, ischecked):
        file_extension = Path(self.global_path).suffix
        if(self.global_path == ""):
            messagebox.showerror(
                title="Nenhuma imagem selecionada",
                message="Selecione uma imagem para que possa aplicar os filtos",
            )
            pass
        elif(file_extension != ".tiff" and file_extension != ".tif"):
            messagebox.showerror(
                title="Erro no formato da Imagem",
                message="A extensão da imagem está incorreta. Extensão correta: .tif ou .tiff"
            )
        else: 
            self.isApplied = True
            self.plot_progress_bar(interface, progress_bar)
            
            self.filtro_gaussiano(self, value_fG)
            self.transformacao_morfologica(self, value_tM, ischecked)

            self.plot_image_filtered(self, figure_filtered, image_filtered, self.path_image_filtered)
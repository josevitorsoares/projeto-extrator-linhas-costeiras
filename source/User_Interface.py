### Inicio importações
from ast import increment_lineno
from importlib.resources import path
from operator import ge
from tkinter import *
from tkinter import filedialog
from webbrowser import get
from PIL import ImageTk, Image
import Shoreline as shore
### Fim importações

class ExtratorLinhasCosteiras():

    @staticmethod
    def construtor_interface():
        root = Tk()
        root.title("Projeto: Extrator de Linhas Costeiras")

        ### Inicio Configuarações de dimensões e posicionamento da janela
        height = 560
        width = 1140

        width_screen = root.winfo_screenwidth()
        height_screen = root.winfo_screenheight()

        posiX = (width_screen/2) - (width/2)
        posiY = ((height_screen-(height_screen * 0.08))/2) - (height/2)

        root.geometry("%dx%d+%d+%d" % (width, height, posiX, posiY))
        root.resizable(False, False)
        ### Fim configuarações de dimensões e posicionamento da janela

        ### Inicio Adicionando o menu a janela
        menu = Menu(root)

        # File Menu

        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(
            label="Abrir Imagem", 
            command= lambda: 
                shore.configure_labels(
                    image_original,
                    image_filtered)),
        file_menu.add_separator()
        file_menu.add_command(label="Sair")
        menu.add_cascade(label="Arquivo", menu=file_menu)

        # Help Menu
        help_menu = Menu(menu, tearoff=0)
        help_menu.add_command(label="Sobre")
        menu.add_cascade(label="Ajuda", menu=help_menu)

        root.config(menu=menu)
        ### Fim adicionando o menu a janela

        ### Inicio Adição e posicionamento dos "images views" na janela
        label_image_original = Label(
            root, 
            text="Imagem Original",
            font="Fira 14")

        image_original = Label(
            root,
            text="Sua imagem abrirá aqui",
            bd=1,
            width=70,
            height=22,
            relief="raised")

        label_image_original.grid(row=0, column=1)
        image_original.grid(row=1, column= 1, padx=50)

        label_image_filtered = Label(
            root, 
            text="Imagem Com os Filtros",
            font="Fira 14")

        image_filtered = Label(
            root,
            text="Sua imagem abrirá aqui", 
            width=70,
            height=22,
            bd=1,
            relief="raised",
        )

        label_image_filtered.grid(row=0, column=2, padx=0)
        image_filtered.grid(row=1, column=2, padx=0)
        ### Fim Adição e posicionamento dos "images views" na janela

        ### Inicio Configurações de filtros

        ### Inicio Filtro Gaussiano
        label_filtro_gaussiano = Label(
            root,
        text="Filtro Gaussiano",
        font="Fira 14"
        )

        scale_filtro_gaussiano = Scale(
        root,
        from_=0,
        to=255,
        width=20,
        orient=HORIZONTAL,
        resolution=1,
        font="Fira 12",
        length=200,
        )

        label_linha = Label(text="").grid(rowspan=2, column=1)

        label_filtro_gaussiano.grid(row=4, column=1, pady=0, padx=0)
        scale_filtro_gaussiano.grid(row=5, column=1, pady=0)
        ### Fim Filtro Gaussiano

        ### Inicio Filtro Tras. Morforlogica
        label_transformacao_morfologica = Label(
            root,
            text="Transformação Morfológica",
            font="Fira 14"
        )

        scale_transformacao_morfologica = Scale(
            root,
            from_=1,
            to=255,
            width=20,
            orient=HORIZONTAL,
            resolution=1,
            font="Fira 12",
            length=250,
        )

        label_transformacao_morfologica.grid(row=4, columnspan=3, pady=0, padx=0)
        scale_transformacao_morfologica.grid(row=5, columnspan=3, pady=0)
        ### Fim Filtro Tras. Morforlogica

        ### Inicio Filtro Tras. Morforlogica
        label_canny = Label(
            root,
            text="Filtro Canny",
            font="Fira 14"
        )

        scale_canny = Scale(
            root,
            from_=100,
            to=200,
            width=20,
            orient=HORIZONTAL,
            resolution=1,
            font="Fira 12",
            length=200,
        )

        label_canny.grid(row=4, column=2,)
        scale_canny.grid(row=5, column=2, pady=0)
        ### Fim Filtro Tras. Morforlogica

        ### Fim Configurações de filtros

        ### Inicio Botões
        button_aplicar = Button(
            root,
            text="Aplicar Filtros",
            font="Fira 12",
            command= lambda: shore.apply_filter(
                path= shore.global_path,
                value_fG= scale_filtro_gaussiano.get(),
                value_tM= scale_transformacao_morfologica.get(),
                value_fC= scale_canny.get()
            )
        )

        button_exportar = Button(
            root,
            text="Exportar Imagem com os Filtros",
            font="Fira 12"
        )

        button_reverter = Button(
            root,
            text="Reverter",
            font="Fira 12",
        )

        button_reverter.grid(row=6, column=1, pady=30, padx=30)
        button_aplicar.grid(row=6, columnspan=3)
        button_exportar.grid(row=6, column=2)
        ### Fim Botões

        root.mainloop()

    # def apply_filter():
    #     banda = shore.converter_imagem_array_numpy(dataset_path)
    #     filtro_G = shore.filtro_gaussiano(banda, 0)
    #     trans_M = shore.transformacao_morfologica(filtro_G, 0)
    #     thre = shore.threshold(trans_M, 0)
    #     image_final =shore.extração_bordas(thre, 0)

    #     shore.exibir(image_final)


execute = ExtratorLinhasCosteiras()
execute.construtor_interface()
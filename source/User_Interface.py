### Inicio importações
from tkinter import *
import tkinter
from Shoreline import Shoreline 
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
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
                Shoreline.plot_image_original(
                    figure_original,
                    image_original)),
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
        
        figure_original = Figure(figsize=(5, 3.3), dpi=100)

        image_original = FigureCanvasTkAgg(figure_original, master=root,)
        image_original.draw()

        label_image_original.grid(row=0, columnspan=1)
        image_original.get_tk_widget().grid(row=1, columnspan=1, padx=47,)

        label_image_filtered = Label(
            root, 
            text="Imagem Com os Filtros",
            font="Fira 14")

        figure_filtered = Figure(figsize=(5, 3.3), dpi=100)

        image_filtered = FigureCanvasTkAgg(figure_filtered, master=root, )
        image_filtered.draw()

        label_image_filtered.grid(row=0, column=1, padx=0)
        image_filtered.get_tk_widget().grid(row=1, column=1, padx=0,)
        ### Fim Adição e posicionamento dos "images views" na janela

        ### Inicio Configurações de filtros

        ### Inicio Filtro Gaussiano
        label_filtro_gaussiano = Label(
            root,
        text="Filtro Gaussiano",
        font="Fira 14",
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

        label_filtro_gaussiano.grid(row=4, column=0, pady=0, padx=0)
        scale_filtro_gaussiano.grid(row=5, column=0, pady=0)
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

        label_transformacao_morfologica.grid(row=4, columnspan=2, padx=0)
        scale_transformacao_morfologica.grid(row=5, columnspan=2, padx=0)
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

        label_canny.grid(row=4, column=1,)
        scale_canny.grid(row=5, column=1, pady=0)
        ### Fim Filtro Tras. Morforlogica

        ### Fim Configurações de filtros

        ### Inicio Botões
        button_aplicar = Button(
            root,
            text="Aplicar Filtros",
            font="Fira 12",
            command= lambda: Shoreline.apply_filter(
                value_fG= scale_filtro_gaussiano.get(),
                value_tM= scale_transformacao_morfologica.get(),
                value_fC= scale_canny.get(),
                figure_filtered= figure_filtered,
                image_filtered= image_filtered
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

        button_reverter.grid(row=6, column=0, pady=30)
        button_aplicar.grid(row=6, columnspan=3, padx=0)
        button_exportar.grid(row=6, column=1,columnspan=2, padx=0)
        ### Fim Botões

        root.mainloop()

execute = ExtratorLinhasCosteiras()
execute.construtor_interface()
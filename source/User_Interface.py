### Inicio importações
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from Shoreline import Shoreline
### Fim importações

        # def get_path_image(label):
        #     path = filedialog.askopenfilename(
        #     initialdir = "/Downloads/",
        #     title = "Selecione a imagem",
        #     filetypes = (("Arquivos tif", "*.tif"), ("Todos os arquivos", "*.*")))
        
        #     image_original = Image.open(path)
        
        #     new_image = image_original.resize(size=[494, 334])
        
        #     image = ImageTk.PhotoImage(new_image)

        #     label.configure(image=image, width=494, height=334)
        #     label.image=image

class ExtratorLinhasCosteiras():

    @staticmethod
    def construtor_interface():
        root = Tk()
        root.title("Projeto: Extrator de Linhas Costeiras")
        
        shoreline = Shoreline()
        # path = shoreline.obter_path_image()
        # image_preview = shoreline.redimensionar_image_root(path)

        ### Inicio Configuarações de dimensões e posicionamento da janela
        height = 525
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
            command= lambda: shoreline.configure_label(image_original, image_filtered))
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
            # bg="yellow",
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

        spinbox_filtro_gaussiano =Spinbox(
        root,
        from_=0,
        to=255,
        width=5,
        font="Fira 12",
        )

        label_filtro_gaussiano.grid(row=3, column=1, pady=8)
        spinbox_filtro_gaussiano.grid(row=4, column=1, pady=0)
        ### Fim Filtro Gaussiano

        ### Inicio Filtro Tras. Morforlogica
        label_transformacao_morfologica = Label(
            root,
            text="Transformação Morfológica",
            font="Fira 14"
        )

        spinbox_transformacao_morfologica =Spinbox(
            root,
            from_=1,
            to=255,
            width=5,
            font="Fira 12",
            increment=1,
        )

        label_transformacao_morfologica.grid(row=3, columnspan=3, pady=10)
        spinbox_transformacao_morfologica.grid(row=4, columnspan=3, pady=0)
        ### Fim Filtro Tras. Morforlogica

        ### Inicio Filtro Tras. Morforlogica
        label_canny = Label(
            root,
            text="Filtro Canny",
            font="Fira 14"
        )

        spinbox_canny =Spinbox(
            root,
            from_=100,
            to=200,
            width=5,
            font="Fira 12",
            increment=1,
        )

        label_canny.grid(row=3, column=2,)
        spinbox_canny.grid(row=4, column=2, pady=0)
        ### Fim Filtro Tras. Morforlogica

        ### Fim Configurações de filtros

        ### Inicio Botões
        button_aplicar = Button(
            root,
            text="Aplicar Filtros",
            font="Fira 12",
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


execute = ExtratorLinhasCosteiras()
execute.construtor_interface()
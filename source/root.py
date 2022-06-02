from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image 

root = Tk()
root.title("Projeto Extrator de Linhas Costeiras")

### Configuarações de dimensões e posicionamento da janela
height = 600
width = 1100

width_screen = root.winfo_screenwidth()
height_screen = root.winfo_screenheight()

posiX = (width_screen/2) - (width/2)
posiY = ((height_screen-(height_screen * 0.08))/2) - (height/2)

root.geometry("%dx%d+%d+%d" % (width, height, posiX, posiY))
root.resizable(False, False)
### Fim configuarações de dimensões e posicionamento da janela

### Adicionando o menu a janela
menu = Menu(root)

# File Menu
file_menu = Menu(menu, tearoff=0)
file_menu.add_command(label="Abrir Imagem")
file_menu.add_separator()
file_menu.add_command(label="Sair")
menu.add_cascade(label="Arquivo", menu=file_menu)

# Help Menu
help_menu = Menu(menu, tearoff=0)
help_menu.add_command(label="Sobre")
menu.add_cascade(label="Ajuda", menu=help_menu)

root.config(menu=menu)
### Fim adicionando o menu a janela


root.mainloop()
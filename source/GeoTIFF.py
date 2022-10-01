import os
import shutil
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path
from Shoreline import Shoreline

class GeoTIFF:

    def __init__(self, path_raster):
        super().__init__()

        self.path_raster = path_raster

        self.export_geotiff()

    def export_geotiff(self):
        if (Shoreline.isApplied == False):
            messagebox.showerror(
                title="Nenhuma imagem selecionada",
                message="Selecione uma imagem e aplique os filtros para que possa realizar a exportação",
            )
        else:
            file_name = Path(self.path_raster).stem

            path_file = filedialog.askdirectory(
                title="Salvar GeoTIFF",
            )

            if (os.path.exists(self.path_raster) and os.path.exists(f"{path_file}/GEOTIFF-{file_name}.tiff") == True):
                messagebox.showerror(
                    title="Erro ao Exportar GeoTIFF",
                    message=f"Diretório inválido ou já existe um arquivo com o nome GEOTIFF-{file_name}.tiff",
                    )
            else:
                shutil.copy2("assets/GeoTIFF/edges_output.tiff", f"{path_file}/GEOTIFF-{file_name}.tiff")

                messagebox.showinfo(
                    title="Exportação Concluída",
                    message=f"O GeoTIff foi exportado com sucesso para: {path_file}",
                )
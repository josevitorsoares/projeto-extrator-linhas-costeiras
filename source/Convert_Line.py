import os
import numpy as np
import itertools
# import zipfile
import sys
from tkinter import messagebox
from tkinter import filedialog
from shapely.geometry import LineString, asLineString
from math import sqrt,ceil
from osgeo import gdal,ogr
from Shoreline import Shoreline

class ConvertLine:

#converte a imagem em um array multidimensional
    def imageToArray(rasterIn):
        img = gdal.Open(rasterIn)
        proj = img.GetProjection()
        band = img.GetRasterBand(1)
        array = np.array(img.ReadAsArray() * 255, dtype = np.uint8)
    
        return array
    
#captura os pontos com pixels de valor igual a 1
    def capturePoints(array):
        points =  np.argwhere(array == 1)
        return points

    def convertLineString(points):
        line = LineString(points)
        return line

    def pixelOffset2coord(rasterIn,xOffset,yOffset):
        raster = gdal.Open(rasterIn)
        geotransform = raster.GetGeoTransform()
        originX = geotransform[0]
        originY = geotransform[3]
        pixelWidth = geotransform[1]
        pixelHeight = geotransform[5]
        coordX = originX+pixelWidth*xOffset
        coordY = originY+pixelHeight*yOffset
        return coordX, coordY

    def convertToShapeFile(rasterIn, array, points):
        #maxima distancia entre os pontos
        raster = gdal.Open(rasterIn)
        geotransform = raster.GetGeoTransform()
        pixelWidth = geotransform[1]
        maxDistance = ceil(sqrt(2*pixelWidth*pixelWidth))
    
        count = 0
        roadList = np.where(array == 1)
        multipoint = ogr.Geometry(ogr.wkbMultiLineString)
        pointDict = {}
        for indexY in roadList[0]:
            indexX = roadList[1][count]
            Xcoord, Ycoord = ConvertLine.pixelOffset2coord(rasterIn,indexX,indexY)
            pointDict[count] = (Xcoord, Ycoord)
            count += 1
    
        multiline = ogr.Geometry(ogr.wkbMultiLineString)
        for i in itertools.combinations(pointDict.values(), 2):
            point1 = ogr.Geometry(ogr.wkbPoint)
            point1.AddPoint(i[0][0],i[0][1])
            point2 = ogr.Geometry(ogr.wkbPoint)
            point2.AddPoint(i[1][0],i[1][1])

            distance = point1.Distance(point2)

            if distance < maxDistance:
                line = ogr.Geometry(ogr.wkbLineString)
                line.AddPoint(i[0][0],i[0][1])
                line.AddPoint(i[1][0],i[1][1])
                multiline.AddGeometry(line)

        shpDriver = ogr.GetDriverByName("ESRI Shapefile")
        
        output_path = ConvertLine.getPathForSaveFiles()

        if os.path.exists(output_path):
            shpDriver.DeleteDataSource(output_path)
            outDataSource = shpDriver.CreateDataSource(output_path + '/shape_file.shp')
            outLayer = outDataSource.CreateLayer(output_path + '/shape_file.shp', geom_type=ogr.wkbMultiLineString )
            featureDefn = outLayer.GetLayerDefn()
            outFeature = ogr.Feature(featureDefn)
            outFeature.SetGeometry(multiline)
            outLayer.CreateFeature(outFeature)
            shpDriver = None

            messagebox.showinfo(
                title="Shape File salvo com sucesso",
                message="Os arquivos Shape File foram salvos com sucesso.",
            )
        else:
            messagebox.showerror(
                title="Caminho Inválido",
                message="O local selecionado para salvar o Shape File é inválido.",
            )


    def getPathForSaveFiles():
        path_files = filedialog.askdirectory(
                title="Salvar Shape File",
        )
        
        return path_files

    def exportShapeFile():
        if(Shoreline.global_path == ""):
            messagebox.showerror(
                title="Nenhuma imagem selecionada",
                message="Selecione uma imagem para que possa aplicar os filtos.",
            )
        elif(Shoreline.isApplied == False):
            messagebox.showerror(
                title="Nenhum Filtro Aplicado",
                message="Aplique os filtros na imagem para que possa exportá-la.",
            )
        else:
            rasterIn = Shoreline.global_path
            array = ConvertLine.imageToArray(rasterIn)
            points = ConvertLine.capturePoints(array)
            line = ConvertLine.convertLineString(points)
            ConvertLine.convertToShapeFile(rasterIn, array, points)
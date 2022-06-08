from osgeo import gdal,ogr
import numpy as np
from shapely.geometry import LineString, asLineString
from math import sqrt,ceil
import itertools
import os
import sys


#converte a imagem em um array multidimensional
def imageToArray(rasterIn):
    img = gdal.Open(rasterIn)
    proj = img.GetProjection()
    band = img.GetRasterBand(1)
    #Posso colocar da mesma forma do outro codigo
    #array = band.ReadAsArray()
    array = np.array(img.ReadAsArray() * 255, dtype = np.uint8)
    #print array
    return array
#captura os pontos com pixels de valor igual a 1
def capturePoints(array):
    points =  np.argwhere(array == 1)
    #print points
    return points

def convertLineString(points):
    line = asLineString(points)
    #print line
    return line

def convertToShapeFile(rasterIn, array, points):
    #maxima distancia entre os pontos
    raster = gdal.Open(rasterIn)
    geotransform = raster.GetGeoTransform()
    pixelWidth = geotransform[1]
    maxDistance = ceil(sqrt(2*pixelWidth*pixelWidth))
    #print maxDistance
    #
    count = 0
    roadList = np.where(array == 1)
    multipoint = ogr.Geometry(ogr.wkbMultiLineString)
    pointDict = {}
    for indexY in roadList[0]:
        indexX = roadList[1][count]
        Xcoord, Ycoord = pixelOffset2coord(rasterIn,indexX,indexY)
        pointDict[count] = (Xcoord, Ycoord)
        count += 1
    #print count
    # dict2wkbMultiLineString
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

    # wkbMultiLineString2shp
    shpDriver = ogr.GetDriverByName("ESRI Shapefile")
    #if os.path.exists('agorasim.shp'):
    #    shpDriver.DeleteDataSource('agorasim.shp')
    outDataSource = shpDriver.CreateDataSource('shape'+sys.argv[1]+'.shp')
    outLayer = outDataSource.CreateLayer('shape'+sys.argv[1]+'.shp', geom_type=ogr.wkbMultiLineString )
    featureDefn = outLayer.GetLayerDefn()
    outFeature = ogr.Feature(featureDefn)
    outFeature.SetGeometry(multiline)
    outLayer.CreateFeature(outFeature)
    print("fim")

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

def main(rasterIn):
    array = imageToArray(rasterIn)
    points = capturePoints(array)
    line = convertLineString(points)
    convertToShapeFile(rasterIn, array, points)

if __name__ == "__main__":
    # python convert_line.py 1985
    #carregando as bandas que serao utilizadas (WINDOWS)
    os.chdir(r'D:\DoutoradoUFC\submissoes\IJRS\demos\cenas_icapui')
    rasterIn = 'shoreline_'+sys.argv[1]+'.tif'
    main(rasterIn)

import rasterio
import cv2
import numpy as np

# carrega a imagem
dataset_path = './images/'
image = rasterio.open(dataset_path + 'extrapolation_1997.tif')

# transforma a imagem em um array numpy
banda1 = image.read(1)
print('original', banda1)
# abre a imagem usando o opencv
cv2.imshow("original",banda1)
cv2.waitKey(0)

# aplica o filtro gaussiano
filtro_gaussiano = cv2.GaussianBlur(banda1, (3, 3), 0)
#cv2.imshow("Filtro", filtro_gaussiano)
#cv2.waitKey(0)

# transformacao morfológica - elimina ruidos
# 2015 - 64. os demais 16/32
kernel = np.ones((64,64), np.uint8)
transformacao_morfologica = cv2.morphologyEx(filtro_gaussiano, cv2.MORPH_OPEN, kernel)
cv2.imshow("Morpho",transformacao_morfologica)
cv2.waitKey(0)

# threshold (binarização da imagem)
# seta os valores menores que zero para 0 e os maiores para 255
_, threshold = cv2.threshold(transformacao_morfologica, 0, 255, cv2.THRESH_BINARY_INV);
print(threshold)
cv2.imshow("threshold",threshold)
cv2.waitKey(0)

# extração das bordas
im_outCopy = np.uint8(threshold)
edges = cv2.Canny(im_outCopy,100,200)
cv2.imshow("Bordas", edges)
cv2.waitKey(0)

# pegando os metadados da imagem de entrada
metadados = image.profile
print(metadados)

# exportando a imagem
with rasterio.open(dataset_path + 'output.tiff', 'w', **metadados) as output_dataset:
    output_dataset.write(edges, 1)

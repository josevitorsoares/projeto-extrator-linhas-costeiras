from threading import Thread
import numpy as np
import rasterio
import cv2

class Filter_Sobel(Thread):

    def __init__(self, raster, threshold, path_output):
        super().__init__()
        self.raster = raster
        self.threshold = threshold
        self.path_output = path_output

        self.Sobel()

    def Sobel(self):

        image = rasterio.open(self.raster)

        #define the vertical filter
        vertical_filter = [[-1,-2,-1], [0,0,0], [1,2,1]]

        #define the horizontal filter
        horizontal_filter = [[-1,0,1], [-2,0,2], [-1,0,1]]

        image_original = np.expand_dims(self.threshold, axis=2)
        altura, largura, banda = image_original.shape

        #initialize the edges image
        edges_image = image_original.copy()

        #loop over all pixels in the image
        for row in range(3, altura-2):
            for col in range(3, largura-2):
        
                #create little local 3x3 box
                local_pixels = image_original[row-1:row+2, col-1:col+2, 0]
        
                #apply the vertical filter
                vertical_transformed_pixels = vertical_filter*local_pixels
                #remap the vertical score
                vertical_score = vertical_transformed_pixels.sum()/4
        
                #apply the horizontal filter
                horizontal_transformed_pixels = horizontal_filter*local_pixels
                #remap the horizontal score
                horizontal_score = horizontal_transformed_pixels.sum()/4
        
                #combine the horizontal and vertical scores into a total edge score
                edge_score = (vertical_score**2 + horizontal_score**2)**.5
        
                #insert this edge score into the edges image
                edges_image[row, col] = edge_score * 3

        #remap the values in the 0-1 range in case they went out of bounds
        edges_image = edges_image/edges_image.max()

        # cv2.imwrite(f"assets/GeoTIFF/edges_output.tiff", edges_image)

        metadados = image.profile

        # with rasterio.open(f'{path_output}', 'w', **metadados) as output_dataset:
        #     output_dataset.write(np.moveaxis(edges_image, [0, 1, 2], [1, 2, 0]))
        with rasterio.open(f'{self.path_output}', 'w', **metadados) as output_dataset:
            output_dataset.write(np.moveaxis(edges_image, [0, 1, 2], [1, 2, 0]))
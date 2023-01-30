# done manual

import matplotlib.pyplot as plt 
from sklearn.cluster import KMeans
import  numpy

img = plt.imread('Original-Image.jpg')
width = img.shape[0] 
height = img.shape[1]
img = img.reshape(width * height,3)
kmeans = KMeans(n_clusters=10).fit(img)
labels =kmeans.predict(img) 
clusters = kmeans.cluster_centers_

img2 = numpy.zeros((width,height,3), dtype=numpy.uint8)

index = 0
for x in range(width):
    for j in range(height):
        labels_of_pixel = labels[index]
        img2[x][j] = clusters[labels_of_pixel]
        index += 1 
plt.imshow(img2)
plt.show()
print(clusters) 
print(labels)
print(len(img2))

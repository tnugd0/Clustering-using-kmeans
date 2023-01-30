# done manual

import matplotlib.pyplot as plt # đọc bức ảnh => trả lại ma trận chứa giá trị RGB của từng pixel em nhé   
from sklearn.cluster import KMeans
import  numpy

img = plt.imread('Original-Image.jpg')
width = img.shape[0]  # shape trả về số pixel ở chiều ngang, docj, và màu theo không gian(3,2 chiều)
height = img.shape[1]
img = img.reshape(width * height,3) # điểu chỉnh lại bức ảnh với 3 chiều và có điểm = dài * rộng (biến nó thành hình ngang)
kmeans = KMeans(n_clusters=10).fit(img)
labels =kmeans.predict(img) # labels là nhãn ứng với từng pixel để có thể đổi màu 
clusters = kmeans.cluster_centers_ # cluster tọa độ màu RRB là điểm màu phổ biến nhất trong ảnh 

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

import pygame 
from random import randint 
import math 
from sklearn.cluster import KMeans 
 

pygame.init()

screen = pygame.display.set_mode((1200,700))

pygame.display.set_caption("kmeans visualization") 


clock = pygame.time.Clock()

background = (55, 171, 171)

background_panel = (189, 186, 43)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (147, 153, 35)
purple  = (255,0,255)
sky = (0,255,255)
orange = (255,125,25)
grape = (100,25,125)
grass = (55,155,65)
pink = (247, 0, 215)

colors = [red,green,blue,yellow,purple,sky,orange,grape,grass,pink]

font = pygame.font.SysFont('sans', 40)
font_small = pygame.font.SysFont('sans', 20) 

text_plus = font.render('+',True, white) 
text_minus = font.render('-',True, white)
text_run = font.render('Run',True, white)
text_al = font.render('Algorithm',True, white)
text_random = font.render('Random',True, white)
text_reset = font.render('Reset',True, white)
k = 0
error = 0
running = True 
points = [] 
clusters = [] 
labels = [] 



def distance(p1,p2): 
    return math.sqrt((p1[0]-p2[0]) * (p1[0]-p2[0]) + (p1[1]- p2[1])*(p1[1]- p2[1])) 

 
while  running:
    clock.tick(60) 
    screen.fill(background) 

    #START DRAW INTERFACE 

    #Draw panel 
    # vẽ hình chữ nhật 

    pygame.draw.rect(screen,black,(50,50,700,500))
    pygame.draw.rect(screen,background_panel,(55,55,690,490)) 
    
    # nút cộng 

    pygame.draw.rect(screen, black, (850,50,50,50))
    screen.blit(text_plus,(865,50))

    # nút trừ 
    pygame.draw.rect(screen, black, (950,50,50,50))
    screen.blit(text_minus,(970,50))

    # nút run 
    pygame.draw.rect(screen, black, (850,150,150,50))
    screen.blit(text_run,(890,150))

    # nuts random

    pygame.draw.rect(screen, black, (850,250,150,50))
    screen.blit(text_random,(870,250))

    # nút reset
    pygame.draw.rect(screen, black, (850,550,150,50))
    screen.blit(text_reset,(870,550))

    
    #K
    text_k = font.render("K = " + str(k),True, black)
    screen.blit(text_k,(1050,50))

    #algorithm 
    pygame.draw.rect(screen, black, (850,450,150,50))
    screen.blit(text_al,(860,450))
    mouse_x, mouse_y = pygame.mouse.get_pos() 
    # draw mouse position (hiện lên tọa độ của con chuột khi trogn panel) 
    if 50 < mouse_x < 750 and 50 < mouse_y < 550:
            text_mouse = font_small.render("(" + str(mouse_x - 50 ) + "," + str(mouse_y - 50 ) +")" ,True, black)
            screen.blit(text_mouse,(mouse_x + 20 ,mouse_y))
    # SETTING CÁC NÚT BẤM 

    for event in pygame.event.get():
        if event.type  ==  pygame.QUIT:  
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN: 

          
            if 50 < mouse_x < 750 and 50 < mouse_y < 550:
                labels = []
                point = [mouse_x - 50 ,mouse_y - 50 ] 
                points.append(point)
                # print(points)
            #change k +  
            if 850 < mouse_x < 900 and 50 < mouse_y < 100: 
                if k < 9:
                    k += 1 
            #change k - 
            if 950 < mouse_x < 1000 and 50 < mouse_y < 100: 
                if k > 0:
                    k -= 1
            # change run
            if 850 < mouse_x < 1000 and 150 < mouse_y < 200: 
                
                if clusters == []: 
                    continue
                labels = [] 
                for p in points:
                    distances_to_cluster = [] 
                    for c in clusters:
                        distances = distance(p,c)
                        distances_to_cluster.append(distances)
                    min_distance = min(distances_to_cluster)
                    label = distances_to_cluster.index(min_distance) 
                    labels.append(label)
                    # print(distances_to_cluster)
                
               
                for i in range(k):.) 
                    sum_x = 0
                    sum_y = 0 
                    count = 0 
                    for j in range(len(points)):
                        if labels[j] == i:
                            sum_x += points[j][0]
                            sum_y += points[j][1]
                            count += 1 
                    if count != 0:
                        new_cluster_x = sum_x/count 
                        new_cluster_y = sum_y/count
                        clusters[i] = [new_cluster_x,new_cluster_y]


            # change random 

            if 850 < mouse_x < 1000 and 250 < mouse_y < 300:
                labels = []
                clusters = []
                for x in range(k):
                    random_point = [randint(0,700), randint(0,500)]
                    
                    clusters.append(random_point)

            # change reset
            if 850 < mouse_x < 1000 and 550 < mouse_y < 600: 
                k = 0 
                points = []
                labels = [] 
                clusters = []
                error = 0 
                
            
            # change algorithm (dùng thuật toán có sẵn để tính)
            if 850 < mouse_x < 1000 and 450 < mouse_y < 500:
                try:

                    kmeans = KMeans(n_clusters=k).fit(points) 
                    labels = kmeans.predict(points)
                    clusters = kmeans.cluster_centers_
                except:
                    print("error")
    #draw cluster:
    for y in range(len(clusters)):
        pygame.draw.circle(screen, colors[y], (int(clusters[y][0]) + 50 ,int(clusters[y][1]) + 50),8)

    #draw point (vẽ nên các điểm được click vào trong các ô)
    for i in range(len(points)):
        pygame.draw.circle(screen,black, (points[i][0] + 50 ,points[i][1] + 50 ),6)
        if labels == []: 
            pygame.draw.circle(screen,white, (points[i][0] + 50 ,points[i][1] + 50 ),5.5)
        else: 
            pygame.draw.circle(screen,colors[labels[i]], (points[i][0] + 50 ,points[i][1] + 50 ),5.5)


    # calculate and drawa error 
    error = 0
    if clusters != [] and labels != []:
        for i in range(len(points)):
            error += distance(points[i], clusters[labels[i]]) 
            
    #Error text 
   
  
    text_error = font.render("Error = " + str(int(error)),True, black) # in lại error 
    screen.blit(text_error,(850,350))
    
    pygame.display.flip()
pygame.quit()




    


import pygame 
from random import randint # nhập số integer bất kỳ 
import math 
from sklearn.cluster import KMeans # nhập thư viện Kmeans từ sk
 
# create interface
pygame.init()

screen = pygame.display.set_mode((1200,700)) # tạo màn hình với chiều ngang 1200 dọc 700

pygame.display.set_caption("kmeans visualization") # ten cho ctrinh 


clock = pygame.time.Clock() # set fps cho giao dien de muot hon  

background = (55, 171, 171) # hệ màu rbg 

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

font = pygame.font.SysFont('sans', 40) # tạo font chữ để vẽ lên các nút ( font chữ sans , cỡ chứ 40 )
font_small = pygame.font.SysFont('sans', 20) # tạo font chữ để vẽ lên các nút ( font chữ sans , cỡ chứ 40 )

text_plus = font.render('+',True, white) # tạo ra nút dấu cộng 
text_minus = font.render('-',True, white)
text_run = font.render('Run',True, white)
text_al = font.render('Algorithm',True, white)
text_random = font.render('Random',True, white)
text_reset = font.render('Reset',True, white)
k = 0
error = 0
running = True 
points = [] # danh sách cái điểm tọa đọ được click trên panel 
clusters = [] # tọa độ các cụm gốc để so sánh nhest vafo ttam 
labels = [] # nhãn (khi tính được khoảng cách nhỏ nhất thì sẽ biết đc pointer thuộc cluster nào (đỏ, xanh, vàng)) (0,1,2,3,....) => tương ứng vs vị trí trong color

# tính khoảng cách của các points đến clusters rồi lấy giá trị nhỏ nhất r gắn tọa độ có giá trị nhỏ nhất giá trị của cluster

def distance(p1,p2): # p1, p2 là tọa độ của points vs clusters
    return math.sqrt((p1[0]-p2[0]) * (p1[0]-p2[0]) + (p1[1]- p2[1])*(p1[1]- p2[1])) # công thức tính khoảng cách

 
while  running:
    clock.tick(60) # fps = 60 
    screen.fill(background) # vẽ cho màu background 

    #START DRAW INTERFACE 

    #Draw panel 
    # vẽ hình chữ nhật 

    pygame.draw.rect(screen,black,(50,50,700,500)) # vẽ thành hình chữ nhật 
    pygame.draw.rect(screen,background_panel,(55,55,690,490)) # vẽ thành hình chữ nhật đè lên hình cũ (đề tọa ra viền đen)
    
    # nút cộng 

    pygame.draw.rect(screen, black, (850,50,50,50))
    screen.blit(text_plus,(865,50)) # dùng để vẽ (blit(a,b)) => a: chữ muốn viết, b: vị trí 

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
    text_k = font.render("K = " + str(k),True, black) # tạo ra chữ k 
    screen.blit(text_k,(1050,50))

    #algorithm 
    pygame.draw.rect(screen, black, (850,450,150,50))
    screen.blit(text_al,(860,450))
    mouse_x, mouse_y = pygame.mouse.get_pos() # lấy tọa độ của con trỏ chuột 
    # draw mouse position (hiện lên tọa độ của con chuột khi trogn panel) 
    if 50 < mouse_x < 750 and 50 < mouse_y < 550:
            text_mouse = font_small.render("(" + str(mouse_x - 50 ) + "," + str(mouse_y - 50 ) +")" ,True, black)
            screen.blit(text_mouse,(mouse_x + 20 ,mouse_y))
    # SETTING CÁC NÚT BẤM 

    for event in pygame.event.get():
        if event.type  ==  pygame.QUIT:  # nếu sự kiện (bấm nút chuột vào nuts tắt thì sẽ đóng ctrinh)
            running = False # khi ấn và =>> running = false =>>> dừng vào lặp
        if event.type == pygame.MOUSEBUTTONDOWN: # check xem bấm chuột hay kh

            # Add điểm giá trị (tọa độ) vào trong list points ban đầu 
            if 50 < mouse_x < 750 and 50 < mouse_y < 550:
                labels = [] # khi tạo điểm mới, mất hết label cũ reset lại về hết các điểm trắng 
                point = [mouse_x - 50 ,mouse_y - 50 ] # để đưa về tọa độ gốc (0,0)
                points.append(point)
                # print(points)
            #change k +  
            if 850 < mouse_x < 900 and 50 < mouse_y < 100: # check có bấm nút vào cộng hay kh 
                if k < 9: # 9 màu 
                    k += 1 
            #change k - 
            if 950 < mouse_x < 1000 and 50 < mouse_y < 100: # check có bấm nút vào trừ  hay kh 
                if k > 0:
                    k -= 1
            # change run
            if 850 < mouse_x < 1000 and 150 < mouse_y < 200: # check có bấm nút vào cộng hay kh 
                # gắn (thay đổi màu của các point ) vào cluster gần nhất 
                if clusters == []: # nếu kh có điểm cluster or chưa random thì kh thực hiện dòng dưới 
                    continue
                labels = [] # mỗi lần bấm run sẽ reset lại label, kh reset => bị các màu kh thay đổi 
                for p in points: # p là tọa độ của tất cả các point trên panel
                    distances_to_cluster = [] # gtri kcach 1 điểm tới cluster rồi lấy gtri nhỏ nhất (làm mới ở mỗi vòng lặp để xét từng các p )
                    for c in clusters:
                        distances = distance(p,c)
                        distances_to_cluster.append(distances)
                    min_distance = min(distances_to_cluster)
                    label = distances_to_cluster.index(min_distance) # biết đc vị trí của kc bé hơn =>> xem ứng với màu gì trong color  
                    labels.append(label)
                    # print(distances_to_cluster)
                
                # thay ddoori vị tí cluster vào ttam 
                for i in range(k): # có bnh k thì sẽ lọc bấy nhiều lần (lần lượt là 0,1,2,3..... => tương ứng vs màu đỏ, xanh,....) 
                    sum_x = 0
                    sum_y = 0 
                    count = 0  # tổng  số điểm trong cùng 1 loại => để chia tbinh
                    for j in range(len(points)):
                        if labels[j] == i: # xét labels[i] (nhãn của point) là màu gì (i là màu tương ứng 0,1,2,3,..)
                            sum_x += points[j][0] # tổng các điểm x 
                            sum_y += points[j][1] # tổng các điểm y 
                            count += 1 
                    if count != 0:
                        new_cluster_x = sum_x/count # toạ độ x mới của cluster trung tâm (tổng x / số x )
                        new_cluster_y = sum_y/count
                        clusters[i] = [new_cluster_x,new_cluster_y] # thay đổi tọa độ cũ thành mới 


            # change random 

            if 850 < mouse_x < 1000 and 250 < mouse_y < 300: # check có bấm nút vào cộng hay kh 
                labels = []
                clusters = [] # rỗng để khi ấn random không lưu lại giá trị cũ, (không bị có điểm cũ =>> hiện ra điểm mới)
                for x in range(k): # số điểm cluster dựa vào số k (k=1 = > 1 điểm ....)
                    random_point = [randint(0,700), randint(0,500)] # lấy số bất kỳ trong khoảng 0-700, 0-500
                    # =>>> panelcso tọa độ 700 x 500 
                    clusters.append(random_point)

            # change reset
            if 850 < mouse_x < 1000 and 550 < mouse_y < 600: # check có bấm nút vào cộng hay kh 
                k = 0 
                points = []
                labels = [] 
                clusters = []
                error = 0 
                
            
            # change algorithm (dùng thuật toán có sẵn để tính)
            if 850 < mouse_x < 1000 and 450 < mouse_y < 500: # check có bấm nút vào cộng hay kh 
                try:

                    kmeans = KMeans(n_clusters=k).fit(points) 
                    labels = kmeans.predict(points) # dự đoán gắn các điểm thành các label
                    clusters = kmeans.cluster_centers_ # tự động láy điểm chính giữa lấy điểm chính giữa 
                except:
                    print("error")
    #draw cluster:
    for y in range(len(clusters)):
        pygame.draw.circle(screen, colors[y], (int(clusters[y][0]) + 50 ,int(clusters[y][1]) + 50),8) # + 50 bỏ bớt phần rìa bên ngoài 

    #draw point (vẽ nên các điểm được click vào trong các ô)
    for i in range(len(points)):
        pygame.draw.circle(screen,black, (points[i][0] + 50 ,points[i][1] + 50 ),6) # vẽ đường tròn 
        if labels == []: # ban đầu chưa tính kcach, chưa có nhãn => các point sẽ màu trắng 
            pygame.draw.circle(screen,white, (points[i][0] + 50 ,points[i][1] + 50 ),5.5)
        else: # khi cos label => vẽ các màu cảu point theo cluster
            pygame.draw.circle(screen,colors[labels[i]], (points[i][0] + 50 ,points[i][1] + 50 ),5.5)


    # calculate and drawa error 
    error = 0
    if clusters != [] and labels != []: # chỉ tính khi điểm có lables & cluster nếu không thì error = 0 
        for i in range(len(points)):
            error += distance(points[i], clusters[labels[i]]) # point vs cluster tương ứng
            
    #Error text 
    #Error là khoảng cách của tất cả các nút đến điểm chính giữa 
    # => error càng bé =>> càng đúng 
    text_error = font.render("Error = " + str(int(error)),True, black) # in lại error 
    screen.blit(text_error,(850,350))
        # (screen,black) => như vẽ rec/ 6 => bán kính đường tròn / point => tâm đường tròn
    pygame.display.flip() # hiện tất cả các vẽ trong vòng lặp đc vex lên ctrinh 
pygame.quit()




    

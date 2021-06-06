import pygame, pymunk
import numpy as np
import matplotlib.pyplot as plt
pygame.init()
discretization = 1000
x = np.linspace(0,1,num = discretization)
fx= np.zeros(shape = discretization)

d=50

# boundary conditions u = 0
def laplacian(n):
    A = np.zeros(shape=(n,n))
    for i in range(n):
        A[i,i] = -2
        if i != 0:
            A[i,i-1] = 1
        if i != n-1:
            A[i,i+1] = 1
    return A

def boundary(fx,left,right):
    fx[0] = left
    fx[fx.size-1] = right
    return fx

def FD(fx):
    n = fx.size
    return np.matmul(laplacian(n),fx)

def update(fx,k = 1):
    return fx + FD(fx) * k

def map(top,bot,fx):
    return ((fx - bot)/(top-bot))

def enforce(top,bot,val):
    return int(min(max(bot,val),top))


screen = pygame.display.set_mode((1000,600))
screen.fill((255,255,255))
pixar = pygame.PixelArray(screen)

left=0
right=0
fx = boundary(fx,left,right)
top = 1
bot = -1
fx = map(top,bot,fx)
left2=fx[0]
right2=fx[fx.size-1]
pause = True
first = True
drawing = False
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                    pause = not pause
        if event.type == pygame.MOUSEBUTTONDOWN:
            (posx,posy) = pygame.mouse.get_pos()
            if posy < 450:
                drawing = True
                (lastposx, lastposy) = (posx,posy)
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                (posx,posy) = pygame.mouse.get_pos()
                if lastposx < posx:
                    fx[lastposx:posx] = 1-map(450,50,enforce(450,50,posy)) 
                else:
                    fx[posx:lastposx] = 1-map(450,50,enforce(450,50,posy)) 
                (lastposx, lastposy) = (posx,posy)


    clock = pygame.time.get_ticks()
    screen.fill((255,255,255))
    
    plot = (fx*400).astype(int)
    color = 255-(fx*510).astype(int)
    red = -np.minimum(color,0)
    blue = np.maximum(color,0)
    pixar[0][400-plot[0]] = (0,0,0) 
    pixar[:,479] = (0,0,0)
    pixar[:,580] = (0,0,0)

    for i in range(1,1000):
        a = plot[i-1]
        b = plot[i]
        if a > b:
            pixar[i,450-a:450-b+1] = (0,0,0) 
        else:
            pixar[i,450-b:450-a+1] = (0,0,0) 

        temp_red = enforce(255,0,red[i])
        temp_blue = enforce(255,0,blue[i])
        pixar[i,480:580] = (255-temp_blue,255-temp_red-temp_blue,255-temp_red)
    
    if not pause:
        for _ in range(d):
            fx = boundary(np.array(update(fx,k = d/1000)),left2,right2)
    if first or not pause:
        pygame.display.update()    

pygame.quit()
print(fx)
        
        
    
import os

x_len = 0
y_len = 0


def get_void_shape(x,y):
    L = []
    shape = []
    for x in range(0,x):
        L.append(0)
    for y in range(0,y):
        shape.append(L)
    return shape
        

def squareFinding(image,x_len = 0,y_len = 0):
    shapes = []
    for x in range(x_len):
        for y in range(y_len):
            if image[y][x] == 1:
                shape = get_void_shape(x_len,y_len)
                shape[x][y] = 1
                image[y][x] = 0
                #adding first colored pixel
                #looking for the next connected one
                keepLooking = True
                while keepLooking:
                    keepLooking = False
                    for i in -1,0,1:
                        for j in -1,0,1:
                            try:
                                if image[y+i][x+j] == 1:
                                    print(y+i,x+j)
                                    keepLooking = True 
                                    x = x + j
                                    y = y + i
                                    
                                    shape[x][y] = 1
                                    image[y][x] = 0   
                            except IndexError:
                                pass
                print(shape)
        
                    
                        
if __name__ == '__main__':
    y = 0
    x = 0
    image = []
    file = open('image2.py','r')
    for ligne in file:
        image.append([])
        x = 0
        for char in ligne:
            x += 1
            if char != '\n' and char != ' ':
                image[y].append(int(char))
        y += 1
            
                
                
    x = x - 1
    y = len(image)
    squareFinding(image,x,y)
    
        
                      
    

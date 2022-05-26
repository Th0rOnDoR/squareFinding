import os
from operator import itemgetter
from math import sqrt
#from tabulate import tabulate
import time


def zerolistmaker(n): #useless
    """Utility fonction to create void shape"""
    listofzeros = [0] * n
    return listofzeros

def getVoidShape(x,y): #useless
    """create an void image by adding list of 0"""
    shape = []
    for x in range(0,x):
        shape.append(zerolistmaker(y))
    return shape
    
def printShape(shape): #pretty useless
    """
    print shape, the default print() return the list so, 
    for debug, show a shape an human can understand
    """
    x = len(shape)
    y = len(shape[0])
    proceed_shape = getVoidShape(y,x) #getting a void image
    for i in range(x):
        for j in range(y):
            if str(shape[i][j]) == '0':   #changing for every value of the shape 0 to single quote, its 
                proceed_shape[j][i] = "'" #easier to understand than a full shape of 0 and 1
            else:
                proceed_shape[j][i] = str(shape[i][j]) #We do not touch to others values 
                #we rotate x and y to, else the shape would be to big to be show 
    #now, the shape is proceed, lets print it
    for j in range(y): #for each line 
        L = "".join(proceed_shape[j]) #merge shape line by line
        #if L != "'"*40: to removd void
        print(L)
    print('') #to separate shape from next one
    
def ExtractCaptchaFromFile(captchaPath): 
    """
    We extract the captcha from the file, but, because the file is rotated, we rotate the captchq
    thats a terrible way lf doing this but, great, it work.
    
    First of all, until a line count less than 15 times 1, 
    we will considerer line are some kind of interferance, so we will remove them
    then, we know the caltcha is 240 pixel by 40 so, so we dont care about some interferance after x = 240
    
    """    
    y = 0
    x = 0
    image = []
    decalage_x = 0 #first interferance
    decalage_x_fin = 0 #last one 
    end_decalage = False # end of first interferance
    file = open(captchaPath,'r') #opening captcha
    for ligne in file: #for each line
        y_ligne = [] #the line y
        x = 0
        s = 0
        for char in ligne: #for every char exept void or \n, adding it to y_ligne 
            if char != '\n' and char != ' ':
                s += int(char)
                x += 1 #counting number of x
                y_ligne.append(int(char))
        if s <15 and image.__len__() <= 240:
            image.append(y_ligne) #if ligne isnt in first interferance or last interferance
            end_decalage = True #adding it to the image
        elif not end_decalage: #first interferance
            decalage_x += 1
        else: #last interferance
            decalage_x_fin += 1
                
    
    y = len(image) #getting dimension
    proceed_image = getVoidShape(x,y)
    for j in range(y):
        for i in range(x):
            proceed_image[i][j] = image[j][i] #rotate the image
    #printShape(proceed_image)
    #print(decalage_x)
    return proceed_image, decalage_x, x, y
   
def GetSquares():
    results = []
    
    for file in os.listdir("square"):
        if file.endswith(".txt"):
            results.append('')
    for file in os.listdir("square"):
        if file.endswith(".txt"):
            #print(os.path.join("square/", file))
            name = os.path.join("square/", file)
            print(name)
            number = int(name.split('/')[1].split('.')[0])
            #name = "square/" + str(q) + ".txt"
            square,a,x_len_square,y_len_square = ExtractCaptchaFromFile(name)
            coordsSquare = [] #coords of every pixel being one
            #print(x_len_square,y_len_square)
            for x in range(x_len_square):
                for y in range(y_len_square):
                    if square[x][y] == 1:
                        #print(x,y)
                        #square[x][y] = 'x'
                        coord = [x,y]
                        coordsSquare.append(coord)
                        
            coordsSquare = sorted(coordsSquare, key=itemgetter(1))
            #printShape(coordsSquare)
            #print(coordsSquare)
            cte = coordsSquare[0][0]
            for i in range(len(coordsSquare)):
                a = coordsSquare[i][0]
                b = coordsSquare[i][1]
                #print(coordsSquare[i])
                coordsSquare[i] = [a-cte,b]
            results[number-1] = coordsSquare
    return results


def removeDuplicatesFromSquare():
    list_squares = GetSquares()
    graph = getVoidShape(len(list_squares), len(list_squares))
    to_show_graph = getVoidShape(len(list_squares), len(list_squares))
    i = 0
    for square in list_squares:
        other_squares = list_squares
        
        print(len(list_squares), i)
        index_other_square = 0
        for other_square in other_squares:
            good = 0
            total = 0
            for point in square:
                if point in other_square:
                    good += 1
                total += 1
            ratio = good/total
            if ratio > 0.9 and i != index_other_square:
                to_show_graph[i][index_other_square] = chr(int(ratio*260-170))
                graph[i][index_other_square] = ratio
            if ratio > 0.9:
                to_show_graph[i][index_other_square] = chr(int(ratio*260-170))
            index_other_square += 1
        i += 1
    printShape(to_show_graph)
    for x in range(len(graph)): #the tested graph
        for y in range(len(graph)): #the used graph for testing
            if graph[x][y] != 0:
                if graph[x][y] > graph[y][x]:
                    print(x+1,y+1)
                    graph[x][y] = 0
                    graph[y][x] = 0
                if graph[x][y] < graph[y][x]:
                    print(y+1,x+1)
                    graph[x][y] = 0
                    graph[y][x] = 0
            
if __name__ == '__main__':
    #GetSquares()
    removeDuplicatesFromSquare()

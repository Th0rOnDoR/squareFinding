maxx,maxy=0,0
    minx,miny=10000,10000
    for i in range(len(shape)):
        if shape[i][0]>maxx-1:
            maxx=shape[i][0]+1
        if shape[i][0]<minx:
            minx=shape[i][0]
        if shape[i][1]>maxy-1:
            maxy=shape[i][1]+1
        if shape[i][1]<miny:
            miny=shape[i][1]
    
    if maxx-minx<3 or maxy-miny<3:
        return [-2,0]
    rect=[]
    for x in range(maxx):
        row=[]
        for y in range(maxy):
            if (x,y) in shape:
                #print("*",end="")
                row+=[1]
            else:
                #print(" ",end="")
                row+=[0]
        #print()
        #rect+=[row]



    print("Triangle?", end=" ")
    #finding avg
    avg=[0,0]
    for i in shape:
        avg[0]+=i[0]
        avg[1]+=i[1]
    avg[0]/=len(shape)
    avg[1]/=len(shape)


    #finding farest from avg
    maxi=0
    maxd=0
    for i in range(len(shape)):
        dist=sqrdDist(avg,shape[i])
        if (dist>maxd):
            maxi=i
            maxd=dist
    #print(avg)
    print(shape[maxi],end="")
    
    #finding farest from avg-shape[maxi]
    rv=[shape[maxi][0]-avg[0],shape[maxi][1]-avg[1]]
    sv=avg
    maxd=0
    mind=0
    maxi2forRect=0
    maxi3forRect=0
    for i in range(len(shape)):
        #t=?
        t=distTOLine(sv,rv,shape[i])
        if t>maxd:
            maxd=t
            maxi2forRect=i
        if t<mind:
            mind=t
            maxi3forRect=i
    if maxd>abs(mind):
        maxi2=maxi2forRect
    else:
        maxi2=maxi3forRect
    #print(shape[maxi2])

    #finding farest from shape[maxi]-shape[maxi2] 
    maxd=0
    maxi3=0
    rv=[shape[maxi][0]-shape[maxi2][0],shape[maxi][1]-shape[maxi2][1]]
    sv=shape[maxi]
    for i in range(len(shape)):
        #t=?
        t=distTOLine(sv,rv,shape[i])
        if t==None:
            for i in shape:
                print(i)
        t=abs(t)
        if t>maxd:
            maxd=t
            maxi3=i
    #print(shape[maxi3])


    

    rv1=[shape[maxi][0]-shape[maxi2][0],shape[maxi][1]-shape[maxi2][1]]
    sv1=shape[maxi]
    rv2=[shape[maxi3][0]-shape[maxi2][0],shape[maxi3][1]-shape[maxi2][1]]
    sv2=shape[maxi3]
    rv3=[shape[maxi3][0]-shape[maxi][0],shape[maxi3][1]-shape[maxi][1]]
    sv3=shape[maxi]
    l1=rv1[0]**2+rv1[1]**2
    l2=rv2[0]**2+rv2[1]**2
    l3=rv3[0]**2+rv3[1]**2
    
    
    #finding dist
    sum=0
    for i in range(len(shape)):
        #t=?
        dist=min(abs(distTOLine(sv1,rv1,shape[i]))*l1,abs(distTOLine(sv2,rv2,shape[i]))*l2,abs(distTOLine(sv3,rv3,shape[i]))*l3)
        sum+=max(dist**1.3-1,0)
    
    print(sum/len(shape), end=" ")
    if (sum/len(shape)<120):
        print("Yes!")
        return [-1,avg]
    print("NO!",end=" ")
    print("Rectangle?", end= " ")




    #now checking rectangle
    maxi2=maxi2forRect
    maxi3=maxi3forRect

    #finding ones farest away from shape[maxi2]-shape[maxi3].. the one farer away from shape[maxi] becomes maxi4
    maxd=0
    mind=0
    maxi4_1=0
    maxi4_2=0
    rv=[shape[maxi3][0]-shape[maxi2][0],shape[maxi3][1]-shape[maxi2][1]]
    sv=shape[maxi2]
    for i in range(len(shape)):
        #t=?
        t=distTOLine(sv,rv,shape[i])
        if t>maxd:
            maxd=t
            maxi4_1=i
        if t<mind:
            mind=t
            maxi4_2=i
    if sqrdDist(shape[maxi4_1],shape[maxi])>sqrdDist(shape[maxi4_2],shape[maxi]):
        maxi4=maxi4_1
    else:
        maxi4=maxi4_2
    #print(shape[maxi4])


    #finding minimal distance from points
    sum=0
    rv1=[shape[maxi][0]-shape[maxi2][0],shape[maxi][1]-shape[maxi2][1]]
    sv1=shape[maxi]
    rv2=[shape[maxi3][0]-shape[maxi][0],shape[maxi3][1]-shape[maxi][1]]
    sv2=shape[maxi3]
    rv3=[shape[maxi4][0]-shape[maxi2][0],shape[maxi4][1]-shape[maxi2][1]]
    sv3=shape[maxi4]
    rv4=[shape[maxi3][0]-shape[maxi4][0],shape[maxi3][1]-shape[maxi4][1]]
    sv4=shape[maxi3]
    l1=rv1[0]**2+rv1[1]**2
    l2=rv2[0]**2+rv2[1]**2
    l3=rv3[0]**2+rv3[1]**2
    l4=rv4[0]**2+rv4[1]**2
    for i in range(len(shape)):
        #t=?
        t=min(abs(distTOLine(sv1,rv1,shape[i]))*l1,abs(distTOLine(sv2,rv2,shape[i]))*l2,abs(distTOLine(sv3,rv3,shape[i]))*l3,abs(distTOLine(sv4,rv4,shape[i]))*l4)
        sum+=max(t**1.3-1,0)
    print(sum/len(shape),end=" ")
    if (sum/len(shape)<75):
        print("YES!")
        return [2-sum/len(shape)/75,avg]
    elif  abs(abs((rv1[0]*rv4[0]+rv1[1]*rv4[1])/(l1*l4))-0.8)<0.4 and abs(abs(l1/l4)-1)<0.2 and abs(abs((rv2[0]*rv3[0]+rv2[1]*rv3[1])/(l2*l3))-0.8)<0.4 and abs(abs(l2/l3)-1)<0.2:
        return [1.1,avg]
    elif sum/len(shape)<150:
        print("maybe!")
        return [2-min(sum/len(shape)/75,2),avg]
    
    print("No! Splittable?",end=" ")



    #trying to split
    maxx=0
    maxy=0
    for i in range(len(shape)):
        if shape[i][0]>maxx-1:
            maxx=shape[i][0]+1
        if shape[i][1]>maxy-1:
            maxy=shape[i][1]+1
    rect=[]
    rect2=[]
    for x in range(maxx):
        row=[]
        row2=[]
        for y in range(maxy):
            if (x,y) in shape:
                print("*",end="")
                row+=[1]
                row2+=[[]]
            else:
                print(" ",end="")
                row+=[0]
                row2+=[[]]
        print()
        rect+=[row]
        rect2+=[row2]
    
    #rect= [[1 if (x,y) in shape else 0 for x in range(maxy)] for y in range(maxx)]

    #return [0,avg]
    for i in range(len(shape)):
        x1,y1=shape[i][0],shape[i][1]
        x=[x1-4,x1-3,x1-2,x1-1,x1,x1+1,x1+2,x1+3,x1+4]
        y=[y1-4,y1-3,y1-2,y1-1,y1,y1+1,y1+2,y1+3,y1+4]
        for a in x:
            for b in y:
                if a>-1 and b>-1 and a<maxx and b<maxy and abs(x1-a)+abs(y1-b)<6 and rect[a][b]!=0:
                    rect2[x1][y1]+=[[a,b]]

    for i in range(1,len(shape)):
        newshape=[shape[0]]
        j=0
        while j<len(newshape):
            if newshape[j] not in rect2[shape[i][0]][shape[i][1]]:
                for k in rect2[newshape[j][0]][newshape[j][1]]:
                    if rect[k[0]][k[1]]!=i+1:
                        rect[k[0]][k[1]]=i+1
                        newshape+=[(k[0],k[1])]
            j+=1
        if len(newshape)>30 and 30<len(shape)-len(newshape):
            print("YES!")
            print(shape[i])
            newshape2=[]
            for k in range(len(shape)):
                if shape[k] not in newshape:
                    newshape2+=[shape[k]]
            t=isTriangle(newshape)
            t2=isTriangle(newshape2)
            if t[0]>t2[0]:
                return t
            else:
                return t2
    print("No!")
    return [0,avg]
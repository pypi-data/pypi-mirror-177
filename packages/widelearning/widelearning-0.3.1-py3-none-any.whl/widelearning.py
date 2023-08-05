
import numpy as np
import pandas as pd

def txt_kernel(file_path):	
    f = open(file_path, 'r')
	
    weights = []

    for i in f:
        weights.append(i.strip().split(','))

    for j in weights:
        j.pop()

    for ii in weights:
        for i1, elem in enumerate(ii):
            ii[i1] = [[int(elem)]]
            
    with open('kernel.txt', 'w') as file:
        file.write(str(weights))

    return weights 
    
def vert(n):
    for i in range(len(n)):
        print(*[x for x in n],'',sep=',')

def hor(n):
    hr = []
    for i in n:
        hr.append(len(n)*[i])
	
    for k1 in range(len(hr)):
        print()
        for k2 in range(len(hr[k1])):
            print(hr[k1][k2], end=',')
            
def diag(d):
    n = [0, -2, -1, 1, 2]

    if(d % 2 == 0):
        m1 = d//2
        m2 = (d/2) - 1
    else:
        m1 = d // 2
        m2 = d // 2

    L = {}

    c = 1
    for i1 in range(int(m2)):
        L[c] = [n[3]]*(d-c) 
        c += 1
    for i2 in range(int(m1)):
        L[c] = [n[4]]*(d-c)
        c += 1
    
    c = -1
    for j1 in range(int(m2)):
        L[c] = [n[2]]*(d+c) 
        c -= 1
    for j2 in range(int(m1)):
        L[c] = [n[1]]*(d+c)
        c -= 1

    diag1 = 0
    for u in L:
        diag1 = diag1 + np.diag(L[u],u)
        z1 = np.diag(np.full(d,n[0]))+diag1
        
    z2 = np.fliplr(z1)

    for h in range(len(z1)):
        print()
        for g in range(len(z1[h])):
            print(z1[h][g], end=',')
            
    print()
    
    for hh in range(len(z2)):
        print()
        for gg in range(len(z2[hh])):
            print(z2[hh][gg], end=',')

def add_kernel(path, init_kernel):
    ff = open(path, 'r')
    
    w1 = init_kernel

    weights = []

    for i in ff:
        weights.append(i.strip().split(','))

    for j in weights:
        j.pop()
    
    for ii in weights:
        for i1, elem in enumerate(ii):
            ii[i1] = int(elem)
                               
    for i in range(len(w1)):
        for j in range(len(w1)):
            w1[i][j][0].append(weights[i][j])

    with open('kernel.txt', 'w') as file:
        file.write(str(w1))
        
    return w1
    
def top_bottom_class(train_path, top, other):
    all_classes = pd.read_csv(train_path)
    

    class_top = all_classes[all_classes["Wine"].isin(top)] 
    other_classes = all_classes[all_classes["Wine"].isin(other)] 

    class_top['Scalar_calc'] = ""
    other_classes['Scalar_calc'] = ""
    
    class_top.to_csv('class_top.csv')
    other_classes.to_csv('other_classes.csv')
    
    class_top = pd.read_csv('class_top.csv')
    other_classes = pd.read_csv('other_classes.csv')
    
    Alcohol = 0
    for i in range(len(class_top)):
        Alcohol += class_top['Alcohol'][i]
        
    Malic_acid = 0
    for i in range(len(class_top)):
        Malic_acid += class_top['Malic.acid'][i]
        
    Ash = 0
    for i in range(len(class_top)):
        Ash += class_top['Ash'][i]
        
    Acl = 0
    for i in range(len(class_top)):
        Acl += class_top['Acl'][i]
        
    Mg = 0
    for i in range(len(class_top)):
        Mg += class_top['Mg'][i]
    
    Phenols = 0
    for i in range(len(class_top)):
        Phenols += class_top['Phenols'][i]
        
    Flavanoids = 0
    for i in range(len(class_top)):
        Flavanoids += class_top['Flavanoids'][i]
        
    Nonflavanoid_phenols = 0
    for i in range(len(class_top)):
        Nonflavanoid_phenols += class_top['Nonflavanoid.phenols'][i]
        
    Proanth = 0
    for i in range(len(class_top)):
        Proanth += class_top['Proanth'][i]
        
    Color_int = 0
    for i in range(len(class_top)):
        Color_int += class_top['Color.int'][i]
        
    Hue = 0
    for i in range(len(class_top)):
        Hue += class_top['Hue'][i]
        
    OD = 0
    for i in range(len(class_top)):
        OD += class_top['OD'][i]
        
    Proline = 0
    for i in range(len(class_top)):
        Proline += class_top['Proline'][i]
    
    weights = [Alcohol, 
                  Malic_acid, Ash, Acl, Mg, Phenols, Flavanoids, Nonflavanoid_phenols, Proanth, Color_int, Hue, OD, Proline]
        
    for i in range(len(class_top['Wine'])):
        class_top['Scalar_calc'][i]=weights[0]*class_top['Alcohol'][i] + \
    weights[1]*class_top['Malic.acid'][i] + weights[2]*class_top['Ash'][i] + \
    weights[3]*class_top['Acl'][i] + weights[4]*class_top['Mg'][i] + \
    weights[5]*class_top['Phenols'][i] + weights[6]*class_top['Flavanoids'][i] + \
    weights[7]*class_top['Nonflavanoid.phenols'][i] + weights[8]*class_top['Proanth'][i] + \
    weights[9]*class_top['Color.int'][i] + weights[10]*class_top['Hue'][i] + \
    weights[11]*class_top['OD'][i] + weights[12]*class_top['Proline'][i]
    
    class_top = class_top.sort_values(by='Scalar_calc', ascending=False)
    
    for i in range(len(other_classes['Wine'])):
        other_classes['Scalar_calc'][i]=weights[0]*other_classes['Alcohol'][i] + \
    weights[1]*other_classes['Malic.acid'][i] + weights[2]*other_classes['Ash'][i] + \
    weights[3]*other_classes['Acl'][i] + weights[4]*other_classes['Mg'][i] + \
    weights[5]*other_classes['Phenols'][i] + weights[6]*other_classes['Flavanoids'][i] + \
    weights[7]*other_classes['Nonflavanoid.phenols'][i] + weights[8]*other_classes['Proanth'][i] + \
    weights[9]*other_classes['Color.int'][i] + weights[10]*other_classes['Hue'][i] + \
    weights[11]*other_classes['OD'][i] + weights[12]*other_classes['Proline'][i]
    
    other_classes = other_classes.sort_values(by='Scalar_calc', ascending=False)
    
    other_classes_max = other_classes['Scalar_calc'].max()
    
    up = 0
    for i in class_top['Scalar_calc']:
        if(i > other_classes_max):
            up+=1
        else:
            break
        
    other_classes.to_csv('other_classes.csv')
    other_classes = pd.read_csv('other_classes.csv')

    li = len(other_classes['Wine']) - 1
        
    lastindex_class_other_classes = other_classes['Wine'][li]
    
    down = 0
    for i in range(len(other_classes['Wine'])-1, 0, -1):
        if(other_classes['Wine'][i]==lastindex_class_other_classes):
            down+=1
        else:
            break
    
    other_classes.drop(other_classes.columns[0], axis=1, inplace=True)

    sum_up_down = up + down
    print('up = ', up)
    print('down = ', down)
    print('sum_up_down = ', sum_up_down)
    print('========= ', lastindex_class_other_classes)
    print('+++++++++++++++++++++++++')
    f = open('weights/weights.txt', 'w')
    f.write(str(weights))
    f.close()
    
    class_top.to_csv('files/class_top.csv')
    other_classes.to_csv('files/class_others.csv')

def scale_weights(up, down):

    class_top = pd.read_csv(up)
    class_others = pd.read_csv(down)
    
    Alcohol = 0
    for i in range(len(class_top)):
        Alcohol += class_top['Alcohol'][i]
        
    Malic_acid = 0
    for i in range(len(class_top)):
        Malic_acid += class_top['Malic.acid'][i]
        
    Ash = 0
    for i in range(len(class_top)):
        Ash += class_top['Ash'][i]
        
    Acl = 0
    for i in range(len(class_top)):
        Acl += class_top['Acl'][i]
        
    Mg = 0
    for i in range(len(class_top)):
        Mg += class_top['Mg'][i]
    
    Phenols = 0
    for i in range(len(class_top)):
        Phenols += class_top['Phenols'][i]
        
    Flavanoids = 0
    for i in range(len(class_top)):
        Flavanoids += class_top['Flavanoids'][i]
        
    Nonflavanoid_phenols = 0
    for i in range(len(class_top)):
        Nonflavanoid_phenols += class_top['Nonflavanoid.phenols'][i]
        
    Proanth = 0
    for i in range(len(class_top)):
        Proanth += class_top['Proanth'][i]
        
    Color_int = 0
    for i in range(len(class_top)):
        Color_int += class_top['Color.int'][i]
        
    Hue = 0
    for i in range(len(class_top)):
        Hue += class_top['Hue'][i]
        
    OD = 0
    for i in range(len(class_top)):
        OD += class_top['OD'][i]
        
    Proline = 0
    for i in range(len(class_top)):
        Proline += class_top['Proline'][i]
    
    weights_up = [Alcohol, 
                  Malic_acid, Ash, Acl, Mg, Phenols, Flavanoids, Nonflavanoid_phenols, Proanth, Color_int, Hue, OD, Proline]
    
    for i in range(len(class_top['Wine'])):
        class_top['Scalar_calc'][i]=weights_up[0]*class_top['Alcohol'][i] + \
        weights_up[1]*class_top['Malic.acid'][i] + weights_up[2]*class_top['Ash'][i] + \
        weights_up[3]*class_top['Acl'][i] + weights_up[4]*class_top['Mg'][i] + \
        weights_up[5]*class_top['Phenols'][i] + weights_up[6]*class_top['Flavanoids'][i] + \
        weights_up[7]*class_top['Nonflavanoid.phenols'][i] + weights_up[8]*class_top['Proanth'][i] + \
        weights_up[9]*class_top['Color.int'][i] + weights_up[10]*class_top['Hue'][i] + \
        weights_up[11]*class_top['OD'][i] + weights_up[12]*class_top['Proline'][i]

    for i in range(len(class_others['Wine'])):
        class_others['Scalar_calc'][i]=weights_up[0]*class_others['Alcohol'][i] + \
        weights_up[1]*class_others['Malic.acid'][i] + weights_up[2]*class_others['Ash'][i] + \
        weights_up[3]*class_others['Acl'][i] + weights_up[4]*class_others['Mg'][i] + \
        weights_up[5]*class_others['Phenols'][i] + weights_up[6]*class_others['Flavanoids'][i] + \
        weights_up[7]*class_others['Nonflavanoid.phenols'][i] + weights_up[8]*class_others['Proanth'][i] + \
        weights_up[9]*class_others['Color.int'][i] + weights_up[10]*class_others['Hue'][i] + \
        weights_up[11]*class_others['OD'][i] + weights_up[12]*class_others['Proline'][i]
        

    class_top = class_top.sort_values(by='Scalar_calc', ascending=False)
    class_others = class_others.sort_values(by='Scalar_calc', ascending=False)
    
    class_top.to_csv('class_top.csv')
    class_others.to_csv('class_others.csv')
    
    class_top = pd.read_csv('class_top.csv')
    class_others = pd.read_csv('class_others.csv')

    other_classes_max = class_others['Scalar_calc'].max()
    
    up = 0
    for i in class_top['Scalar_calc']:
        if(i > other_classes_max):
            up+=1
        else:
            break
        
    class_others.to_csv('other_classes.csv')
    class_others = pd.read_csv('other_classes.csv')

    li = len(class_others['Wine']) - 1
        
    lastindex_class_other_classes = class_others['Wine'][li]
    
    down = 0
    for i in range(len(class_others['Wine'])-1, 0, -1):
        if(class_others['Wine'][i]==lastindex_class_other_classes):
            down+=1
        else:
            break
    
    
    print(up)
    print(down)
    d_up = class_top['Scalar_calc'][up-1]
    print()

    class_d2 = class_others.sort_values(by='Scalar_calc')
    class_d2.to_csv('class_d2.csv')
    class_d2 = pd.read_csv('class_d2.csv')
    
    for i in range(down):
        d_down = class_d2['Scalar_calc'][i]
    
    print()

    mx = (d_up + class_others['Scalar_calc'].max())/2
    mn = (d_down + class_d2['Scalar_calc'][down])/2
    print()

    scaled_weights = [(2*weights_up[0])/(mx - mn),
           (2*weights_up[1])/(mx - mn),
           (2*weights_up[2])/(mx - mn),
           (2*weights_up[3])/(mx - mn),
           (2*weights_up[4])/(mx - mn),
           (2*weights_up[5])/(mx - mn),
           (2*weights_up[6])/(mx - mn),
           (2*weights_up[7])/(mx - mn),
           (2*weights_up[8])/(mx - mn),
           (2*weights_up[9])/(mx - mn),
           (2*weights_up[10])/(mx - mn),
           (2*weights_up[11])/(mx - mn),
           (2*weights_up[12])/(mx - mn),
           (-2*mn)/(mx - mn)-1]

    f = open('scaled_weights.txt', 'w')
    f.write(str(scaled_weights))
    f.close()
    
    return scaled_weights
    
def scale_weights_binary(up, down):

    class_top = pd.read_csv(up)
    class_others = pd.read_csv(down)
    
    Alcohol = 0
    for i in range(len(class_top)):
        Alcohol += class_top['Alcohol'][i]
        
    Malic_acid = 0
    for i in range(len(class_top)):
        Malic_acid += class_top['Malic.acid'][i]
        
    Ash = 0
    for i in range(len(class_top)):
        Ash += class_top['Ash'][i]
        
    Acl = 0
    for i in range(len(class_top)):
        Acl += class_top['Acl'][i]
        
    Mg = 0
    for i in range(len(class_top)):
        Mg += class_top['Mg'][i]
    
    Phenols = 0
    for i in range(len(class_top)):
        Phenols += class_top['Phenols'][i]
        
    Flavanoids = 0
    for i in range(len(class_top)):
        Flavanoids += class_top['Flavanoids'][i]
        
    Nonflavanoid_phenols = 0
    for i in range(len(class_top)):
        Nonflavanoid_phenols += class_top['Nonflavanoid.phenols'][i]
        
    Proanth = 0
    for i in range(len(class_top)):
        Proanth += class_top['Proanth'][i]
        
    Color_int = 0
    for i in range(len(class_top)):
        Color_int += class_top['Color.int'][i]
        
    Hue = 0
    for i in range(len(class_top)):
        Hue += class_top['Hue'][i]
        
    OD = 0
    for i in range(len(class_top)):
        OD += class_top['OD'][i]
        
    Proline = 0
    for i in range(len(class_top)):
        Proline += class_top['Proline'][i]
    
    weights_up = [Alcohol, 
                  Malic_acid, Ash, Acl, Mg, Phenols, Flavanoids, Nonflavanoid_phenols, Proanth, Color_int, Hue, OD, Proline]
    
    for i in range(len(class_top['Wine'])):
        class_top['Scalar_calc'][i]=weights_up[0]*class_top['Alcohol'][i] + \
        weights_up[1]*class_top['Malic.acid'][i] + weights_up[2]*class_top['Ash'][i] + \
        weights_up[3]*class_top['Acl'][i] + weights_up[4]*class_top['Mg'][i] + \
        weights_up[5]*class_top['Phenols'][i] + weights_up[6]*class_top['Flavanoids'][i] + \
        weights_up[7]*class_top['Nonflavanoid.phenols'][i] + weights_up[8]*class_top['Proanth'][i] + \
        weights_up[9]*class_top['Color.int'][i] + weights_up[10]*class_top['Hue'][i] + \
        weights_up[11]*class_top['OD'][i] + weights_up[12]*class_top['Proline'][i]

    for i in range(len(class_others['Wine'])):
        class_others['Scalar_calc'][i]=weights_up[0]*class_others['Alcohol'][i] + \
        weights_up[1]*class_others['Malic.acid'][i] + weights_up[2]*class_others['Ash'][i] + \
        weights_up[3]*class_others['Acl'][i] + weights_up[4]*class_others['Mg'][i] + \
        weights_up[5]*class_others['Phenols'][i] + weights_up[6]*class_others['Flavanoids'][i] + \
        weights_up[7]*class_others['Nonflavanoid.phenols'][i] + weights_up[8]*class_others['Proanth'][i] + \
        weights_up[9]*class_others['Color.int'][i] + weights_up[10]*class_others['Hue'][i] + \
        weights_up[11]*class_others['OD'][i] + weights_up[12]*class_others['Proline'][i]
        

    class_top = class_top.sort_values(by='Scalar_calc', ascending=False)
    class_others = class_others.sort_values(by='Scalar_calc', ascending=False)
    
    class_top.to_csv('class_top.csv')
    class_others.to_csv('class_others.csv')
    
    class_top = pd.read_csv('class_top.csv')
    class_others = pd.read_csv('class_others.csv')

    other_classes_max = class_others['Scalar_calc'].max()
    
    up = 0
    for i in class_top['Scalar_calc']:
        if(i > other_classes_max):
            up+=1
        else:
            break
        
    class_others.to_csv('other_classes.csv')
    class_others = pd.read_csv('other_classes.csv')

    li = len(class_others['Wine']) - 1
        
    lastindex_class_other_classes = class_others['Wine'][li]
    
    down = 0
    for i in range(len(class_others['Wine'])-1, 0, -1):
        if(class_others['Wine'][i]==lastindex_class_other_classes):
            down+=1
        else:
            break
    
    
    d_down = class_others['Scalar_calc'].min()
    d_up = class_top['Scalar_calc'].min()

    mx =  d_up
    mn = d_down
    
    print(up)
    print(down)

    print()

    scaled_weights = [(2*weights_up[0])/(mx - mn),
           (2*weights_up[1])/(mx - mn),
           (2*weights_up[2])/(mx - mn),
           (2*weights_up[3])/(mx - mn),
           (2*weights_up[4])/(mx - mn),
           (2*weights_up[5])/(mx - mn),
           (2*weights_up[6])/(mx - mn),
           (2*weights_up[7])/(mx - mn),
           (2*weights_up[8])/(mx - mn),
           (2*weights_up[9])/(mx - mn),
           (2*weights_up[10])/(mx - mn),
           (2*weights_up[11])/(mx - mn),
           (2*weights_up[12])/(mx - mn),
           (-2*mn)/(mx - mn)-1]

    f = open('scaled_weights.txt', 'w')
    f.write(str(scaled_weights))
    f.close()
    
    return scaled_weights

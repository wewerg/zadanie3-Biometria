import os
import sys
import numpy as np
from scipy import misc
from collections import namedtuple
from scipy import ndimage
from matplotlib import pyplot as plt
import time
from sklearn.preprocessing import scale
from sklearn.preprocessing import normalize
import tkinter


PATH = os.getcwd()+"/iris"
LEFT, RIGHT =  'left', 'right'
WIDTH = 480
HEIGHT = 20

#pomenovana ntica
Person = namedtuple("Person","left_temp1 left_mask1 right_temp1 right_mask1")

def use_mask(template, mask, sizex,sizey):
    result = np.zeros((sizex, sizey))
    print(result)
    for i in range(sizex):
        for j in range(sizey):
            if(template[i][j]) == 0 and (mask[i][j]) == 0:
                result[i,j]= 1
    #misc.imshow(result)
    #invertovanie
    for i in range(sizex):
        for j in range(sizey):
            if(result[i,j]) == 1:
                result[i,j]= 0
            else:
                result[i, j]= 1
    return result





def haming(oko1, oko2):
    """vypocitanie hamingovaj vzdialenosti"""
    haming = sum(abs(oko1-oko2))

    return haming.sum()

def normalize_me(matica):
    pole = []
    for riadok in matica:
        for i in riadok:
            if i is 255:
                pole.append(1)
            else:
                pole.append(0)
    return pole


def create_histogram():
    """histogram pocetnosti """
    pass

def load_all_data():
    alleyes = []
    for i in range(1,10):
        for j in range(1,3):
            alleyes.append(load_eye(i,j))
    print(alleyes)

def load_eye(i,s):
    """Nacita vsetky oci pre
        i subject
        s side
    """
    masks = []
    templates = []
    for j in range(1, 4):
        mask = misc.imread(PATH+"/00{}/{}/00{}_{}_{}_mask.bmp".format(i,s,i,s,j),mode='L')
        template = ndimage.imread(PATH+"/00{}/{}/00{}_{}_{}_template.bmp".format(i,s,i,s,j),mode='L')
        #misc.imshow(mask)

        masks.append(mask)
        templates.append(template)
    return templates, masks



def menu():
    ans = True
    while ans:
        print("""
        1.Porovnanie vzoriek
        2.Zobrazenie jednej vzorky
        3.Zobrazenie histogramu
        4.Exit/Quit
        """)
        ans = input("Co chces urobit ")
        if ans == "1":
            print("\n Student Added")
        elif ans == "2":
            print("\n Student Deleted")
        elif ans == "3":
            print("\n Student Record Found")
        elif ans == "4":
            print("\n Goodbye")
            ans = False
        elif ans != "":
            print("\n Not Valid Choice Try again")

def vypis_po_riadkoch(matica):
    pocet_stlpcov = matica.shape[1]
    pocet_riadkov = matica.shape[0]
    for i in range(pocet_riadkov):
        for j in range (pocet_stlpcov):
            print(matica.item(i,j), end=' ')
        print()
        input()

def vypis_po_riadkoch2(zoznam):
    pocet_stlpcov = len(zoznam)
    #pocet_riadkov = len(zoznam[0])
    for i in range(pocet_stlpcov):
        for j in range(i):
            print(zoznam[j])
        print()
        input()


def normalize_columns(arr):
    """znormovanie obrazkov"""
    return [normuj_rad(col) for col in arr]


def normuj_rad(arr):
    return [int(i/255) for i in arr]

def priprav_obraz(template,maska):
    znormovany_template = normalize_columns(template)
    pouzita_maska = use_mask(znormovany_template, maska, HEIGHT, WIDTH)
    return pouzita_maska

def porovnaj_2_obrazy(oko1, oko2):
    zoznam = []
    i = 0
    print("Hamingove vzdialenosti:")
    while (i < WIDTH):
        oko2 = np.roll(oko2, 1, axis=1)
        hamingova_vzdialenost = haming(oko1, oko2)
        i += 1
        zoznam.append(hamingova_vzdialenost)
        print(i,hamingova_vzdialenost)
    minimalna_hodnota = min(zoznam)
    index = zoznam.index(minimalna_hodnota)
    print("Najmensia hamingova vzdialenost: {}, pri rotacii: {}".format(minimalna_hodnota,index))
    return minimalna_hodnota, index



if __name__=="__main__":
    #load_all_data()
    np.set_printoptions(precision=3)
    templates, masks = load_eye(1,1)
    """iba zapis testovacich dat"""
    with open('workfile', 'w') as f:
        f.write(str(templates))


    #misc.imshow(mask[0])
    #misc.imshow(template[0])
    matica = np.matrix([[1,0, 0, 4, 5],[1,2,3,4,3],[1,2,0,4,5],[1,2,3,4,3]])
    matica2 = np.matrix([[1, 0, 2, 4, 6], [1, 2, 3, 4, 5], [1, 2, 0, 4, 5], [1, 2, 3, 4, 5]])
    matica3 = [255,0,0,255,255,0,0,255]

    #shift
    x = np.roll(matica, 2, axis=1)
    print("Hamingova vzdialenost je {}".format(haming(matica, matica2)))



    """
    print("Normovanie: ")
    znormovany_template = normalize_columns(templates[0])
    print(znormovany_template[0])
    print(masks[0])
    misc.imshow(znormovany_template)
    misc.imshow(masks[0])
    pouzita_maska = use_mask(znormovany_template,masks[0],HEIGHT,WIDTH)
    """
    """
    test rotacie
    i=0
    while (i<200):
        pouzita_maska = np.roll(pouzita_maska, 50, axis=1)
        misc.imshow(pouzita_maska)
        i+=20
    print()
    """
    oko1 = (priprav_obraz(templates[2], masks[2]))
    oko2 = (priprav_obraz(templates[0], masks[0]))
    #misc.imshow(oko1)
    #misc.imshow(oko2)

    porovnaj_2_obrazy(oko1, oko2)
    print("Hamingova vzdialenost je {}".format(haming(oko1, oko2)))


    """
    print(use_mask(matica,matica2,4,4))
    print("maska jednej osoby")
    print(masks[0])
    """

    #vypis_po_riadkoch2(mask[0])
    #normalize_columns(matica2)
    #merged = use_mask(template,mask,HEIGHT,WIDTH)


##########
    #priprava pre gui

    #top = tkinter.Tk()
    #top.mainloop()
#########
    #menu()
    #sys.exit(menu())
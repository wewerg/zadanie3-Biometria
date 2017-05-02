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



class person(object):
    def __init__(self,name,template,mask):
        self.name = name
        self.template = template
        self.mask = mask


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
            ans = menu_porovnanie_vzoriek()
        elif ans == "2":
            ans = menu_zobrazenie_jednej_vzorky()
        elif ans == "3":
            ans = menu_sprav_histogram()
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
    """
    Porovna zhodu 2 oci
    :param oko1: 
    :param oko2: 
    :return: index rotacie, hamingova vzdialenost
    """
    zoznam = []
    i = 0
    #print("Hamingove vzdialenosti:")
    while (i < WIDTH):
        oko2 = np.roll(oko2, 1, axis=1)
        hamingova_vzdialenost = haming(oko1, oko2)
        i += 1
        zoznam.append(hamingova_vzdialenost)
       #print(i,hamingova_vzdialenost)
    minimalna_hodnota = min(zoznam)
    index = zoznam.index(minimalna_hodnota)
    return  index, minimalna_hodnota

def zobraz_zhodu(oko1, oko2, rotacia):
    """
    Zobrazenie zhody 2 oci - sive su zhodne
    :param oko1: 
    :param oko2: 
    :param rotacia: 
    
    """
    oko2 = np.roll(oko2, rotacia, axis=1)
    sizex = HEIGHT
    sizey = WIDTH
    oci = np.zeros((sizex, sizey))
    for i in range(sizex):
        for j in range(sizey):
            if(oko1[i][j]) == 1 and (oko2[i][j]) == 1:
                oci[i,j]= 1
            elif (oko1[i][j]) == 1 and (oko2[i][j]) == 0:
                oci[i, j] = 0
            elif (oko1[i][j]) == 0 and (oko2[i][j]) == 1:
                oci[i, j] = 0
            else:
                oci[i, j] = 0
    misc.imshow(oci)

def index_to_degrees(index):
    return 360*index/WIDTH

def validate_imputs(subjekt,oko,vzorka1,vzorka2 = None):
    if vzorka2 is None:
        pass
    else:
        if (vzorka2 < 0) or (vzorka2 > 2):
            return False

    if (subjekt < 1) or (subjekt > 9):
        return False

    if (oko < 0) or (oko > 2):
        return False

    if (vzorka1 < 0) or (vzorka1 > 2):
        return False

    return True


def menu_porovnanie_vzoriek():
    print("Zadaj vzorky ktore chces porovnat:")
    subjekt = int(input("Vyber subjekt: 1-9 "))
    oko = int(input("Vyber oko: 1-2 "))
    vzorka1 = int(input("Vyber vzorku 1: 0-2 "))
    vzorka2 = int(input("Vyber vzorku 2: 0-2 "))

    if validate_imputs(subjekt,oko,vzorka1,vzorka2) is False:
        print("!!!!!!zle zadane parametre!!!!! ")
        return False

    templates, masks = load_eye(subjekt, oko)
    oko1 = (priprav_obraz(templates[vzorka1], masks[vzorka1]))
    oko2 = (priprav_obraz(templates[vzorka2], masks[vzorka2]))
    index, hamingova = porovnaj_2_obrazy(oko1, oko2)
    print("Najmensia hamingova vzdialenost: {}, pri rotacii: {}, v stupnoch : {}".format(hamingova, index, index_to_degrees(index)))
    zobraz_zhodu(oko1, oko2, index)

    return True

def menu_zobrazenie_jednej_vzorky():
    print("Zadaj vzorku ktoru chces zobrazit:")
    subjekt = int(input("Vyber subjekt: 1-9 "))
    oko = int(input("Vyber oko: 1-2 "))
    vzorka1 = int(input("Vyber vzorku 1: 0-2 "))


    if  validate_imputs(subjekt, oko, vzorka1) is False:
        print("zle zadane parametre ")
        return False

    templates, masks = load_eye(subjekt, oko)
    oko1 = (priprav_obraz(templates[vzorka1], masks[vzorka1]))
    misc.imshow(oko1)
    return True

def menu_sprav_histogram():
    print("Nacitanie vsetkych dat")
    vysledky_rovnake = []
    vysledky_rozne = []
    vsetky_oci = load_all_data() #toto je pole vsetkych subjektov
    for oko in vsetky_oci:
        okoPevne = priprav_obraz(oko.template[0], oko.mask[0])
        #porovnanie srovnakymi
        for vzorka in range (1,3):
            #v jednom oku 3 vzorky
            #teda to iste oko
            #print(oko.template[vzorka])
            #oko aj s maskou
            okoM = priprav_obraz(oko.template[vzorka],oko.mask[vzorka])
            index, hamingova = porovnaj_2_obrazy(okoPevne, okoM)
            vysledky_rovnake.append(hamingova)
        #tuto idu ine oka

        #index, hamingova = porovnaj_2_obrazy(oko1, oko2)

    testovacie_oko = vsetky_oci[0]
    okoPevne = priprav_obraz(testovacie_oko.template[0], testovacie_oko.mask[0])
    for i in range(1, 10):
        testovacie_oko2 = vsetky_oci[i]
        okoTest = priprav_obraz(testovacie_oko2.template[0], testovacie_oko2.mask[0])
        index, hamingova = porovnaj_2_obrazy(okoPevne, okoTest)
        vysledky_rozne.append(hamingova)

    #print(vysledky_rovnake)
    urob_histogram(vysledky_rovnake,vysledky_rozne)

def urob_histogram(vysledky_rovnake,vysledky_rozne):
    plt.hist([vysledky_rovnake,vysledky_rozne])
    plt.title("Histogram podobnosti")
    plt.xlabel("Podobnost")
    plt.ylabel("Pocetnost")

    #fig = plt.gcf()
    plt.show()




def load_all_data():
    alleyes = []
    for i in range(1,10):
        for j in range(1,3):
            templates, masks = load_eye(i, j)
            trieda = str(i)+str(j)
            alleyes.append(person(trieda,templates,masks))
    return alleyes

if __name__=="__main__":
    menu()

    #menu()
    sys.exit(menu())
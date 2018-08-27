# Sudoku

def sudoku(t):
    """Resi dani sudoku. V tabeli t velikosti 9 x 9 so ze vpisana nekatera stevila.
    Prazna polja so oznacena z 0."""
    
    def podrocje(n):
        if n < 3:
            return  3
        elif n < 6:
            return 6
        else:
            return 9
        

    def mozne_poteze(u,v):
        #poglej vrstico
        if t[u][v] != 0:
            return []
        mozne_stevilke = []
        vrednosti = t[u].copy()
        #dodam vrednosti v stolpcu
        for i in range(9):
            vrednosti.append(t[i][v])
        #dodam se vrednosti v kvadratku
        for row in t[podrocje(u)-3 : podrocje(u)]:
            for val in row[podrocje(v)-3 : podrocje(v)]:
                vrednosti.append(val)
        #vrednosti  = [y for x in vrednosti for y in x]
        for value in [1,2,3,4,5,6,7,8,9]:
            #preveri po vrstici
            if value not in vrednosti:
                mozne_stevilke.append(value)
        return mozne_stevilke
                



    def naslednje_polje(u,v):
        if v < 8:
            return (u, v+1)
        else:
            return (u+1, 0)
    
    def sestopaj(u,v):
        # (u,v) je koordinata, v kateri moramo preizkusiti vse moznosti.
        # premaknemo se v naslednje prazno polje
        while u < 9 and t[u][v] != 0: 
            (u,v) = naslednje_polje(u,v)
        if (u,v) == (9,0):
            # obdelali smo vsa polja in nasli resitev
            return t
        else:
            # izracunamo vse dovoljene poteze za polje (u,v)
            #print(t)
            for k in mozne_poteze(u,v):
                t[u][v] = k
                r = sestopaj(u,v)
                if r is None:
                    # odstranimo potezo
                    t[u][v] = 0
                else:
                    # nasli smo resitev
                    return r
            # Pregledali smo vse poteze, ni resitve
            return None
    # zacetni klic
    return sestopaj(0,0)

def narisi(t):
    """Narisi tabelo sudoku."""
    for vrstica in t:
        print(vrstica)
    print('\n')

# Glavni program

b = [[0,0,0, 9,0,4, 0,7,0],
     [0,4,0, 0,8,1, 0,0,5],
     [9,0,0, 0,0,0, 4,0,1],
     
     [0,0,3, 0,0,0, 0,5,7],
     [8,0,5, 0,0,0, 1,0,9],
     [1,6,0, 0,0,0, 3,0,0],
     
     [5,0,8, 0,0,0, 0,0,6],
     [7,0,0, 6,4,0, 0,3,0],
     [0,9,0, 8,0,7, 0,0,0]]


if sudoku(b) is not None:
    print('b solved')
    narisi(b)


# Primer zacetnega sudokuja:
a = [[5,3,0, 0,7,0, 0,0,0],
     [6,0,0, 1,9,5, 0,0,0],
     [0,9,8, 0,0,0, 0,6,0],
     
     [8,0,0, 0,6,0, 0,0,3],
     [4,0,0, 8,0,3, 0,0,1],
     [7,0,0, 0,2,0, 0,0,6],
     
     [0,6,0, 0,0,0, 2,8,0],
     [0,0,0, 4,1,9, 0,0,5],
     [0,0,0, 0,8,0, 0,7,9]]

if sudoku(a) is not None:
    print('a solved')
    narisi(a)


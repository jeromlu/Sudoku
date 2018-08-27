# Sudoku

def sudoku(t):
    """Resi dani sudoku. V tabeli t velikosti 9 x 9 so ze vpisana nekatera stevila.
    Prazna polja so oznacena z 0."""

    def mozne_poteze(u,v):
        # NE DELA!!!
        return [1,2,3,4,5,6,7,8,9]

    def naslednje_polje(u,v):
        if v < 8:
            return (u, v+1)
        else:
            return (u+1, 0)
    
    def sestopaj(u,v):
        # (u,v) je koordinata, v kateri moramo preizkusiti vse moznosti.
        # premaknemo se v naslednje prazno polje
        while u < 9 and t[u][v] != 0: (u,v) = naslednje_polje(u,v)
        if (u,v) == (9,0):
            # obdelali smo vsa polja in nasli resitev
            return t
        else:
            # izracunamo vse dovoljene poteze za polje (u,v)
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
    for v in t: print(v)

# Glavni program

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
    narisi(a)


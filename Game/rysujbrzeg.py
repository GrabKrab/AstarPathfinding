

def rysuj_brzeg(mapa, x, y):
    brzeg = ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12']
    woda = []
    for line in mapa:
        rzad_woda = []
        for l in line:
            rzad_woda.append(l)
        woda.append(rzad_woda)

    mX = len(mapa[0])
    mY = len(mapa)
    pm = mapa

    if pm[y][x] <= 20:  # czyli jest inne niż 'woda'
        # sprawdz dokoloła  i ustaw odpowiedni kafelek

        try:
            if pm[y][x-1] < 20:  # and woda[y][x-1] == '0':
                if pm[y-1][x-1] < 20 and pm[y+1][x-1] < 20:     # |
                    woda[y][x-1] = 1
            if pm[y][x-1] < 20:
                if pm[y-1][x-1] >= 20 and pm[y+1][x-1] < 20:    # /
                    woda[y][x-1] = 12
                if pm[y][x-1] < 0 and pm[y+1][x-1] >= 20:       # \
                    woda[y][x-1] = 9

            if pm[y-1][x-1] < 20:
                if pm[y-1][x] < 20 and pm[y][x-1] < 20:
                    woda[y-1][x-1] = 5
            if pm[y - 1][x - 1] < 20:# and woda[y - 1][x - 1] == 0:
                if pm[y-1][x] < 20 and pm[y][x-1] >= 20:
                    woda[y-1][x-1] = 2
                if pm[y-1][x] >= 20 and pm[y][x-1] < 20:
                    woda[y-1][x-1] = 1

            if pm[y+1][x-1] < 20:
                if pm[y+1][x] < 20 and pm[y][x-1] < 20:
                    woda[y + 1][x - 1] = 8
                if pm[y + 1][x] < 20 and pm[y][x - 1] >= 20:
                    woda[y + 1][x - 1] = 4
            if pm[y + 1][x - 1] < 20:# and woda[y + 1][x - 1] == 0:
                if pm[y + 1][x] >= 20 and pm[y][x - 1] < 20:
                    woda[y + 1][x - 1] = 1

            if pm[y-1][x] < 20:# and woda[y-1][x] == 0:
                if pm[y-1][x-1] < 20 and pm[y-1][x+1] < 20:
                    woda[y-1][x] = 2
            if pm[y - 1][x] < 20:
                if pm[y-1][x-1] < 20 and pm[y-1][x+1] >= 20:
                    woda[y-1][x] = 9
                if pm[y-1][x-1] >= 20 and pm[y-1][x+1] < 20:
                    woda[y-1][x] = 10

            if pm[y-1][x+1] < 20:
                if pm[y-1][x] < 20 and pm[y][x+1] < 20:
                    woda[y-1][x+1] = 6
            if pm[y - 1][x + 1] < 20:# and woda[y - 1][x + 1] == 0:
                if pm[y-1][x] < 20 and pm[y][x+1] >= 20:
                    woda[y-1][x+1] = 2
                if pm[y-1][x] >= 20 and pm[y][x+1] < 20:
                    woda[y-1][x+1] = 3

            if pm[y][x+1] < 20:# and woda[y][x+1] == 0:
                if pm[y-1][x+1] < 20 and pm[y+1][x+1] < 20:
                    woda[y][x+1] = 3
            if pm[y][x + 1] < 20:
                if pm[y-1][x+1] < 20 and pm[y+1][x+1] >= 20:
                    woda[y][x+1] = 10
                if pm[y-1][x+1] >= 20 and pm[y+1][x+1] < 20:
                    woda[y][x+1] = 11

            if pm[y+1][x+1] < 20:
                if pm[y][x+1] < 20 and pm[y+1][x] < 20:
                    woda[y+1][x+1] = 7
            if pm[y + 1][x + 1] < 20:# and woda[y + 1][x + 1] == 0:
                if pm[y][x+1] < 20 and pm[y+1][x] >= 20:
                    woda[y+1][x+1] = 3
                if pm[y][x+1] >= 20 and pm[y+1][x] < 20:
                    woda[y+1][x+1] = 4

            if pm[y+1][x] < 20:# and woda[y+1][x] == 0:
                if pm[y+1][x+1] < 20 and pm[y+1][x-1] < 20:
                    woda[y+1][x] = 4
            if pm[y + 1][x] < 20:
                if pm[y+1][x+1] < 20 and pm[y+1][x-1] >= 20:
                    woda[y+1][x] = 11
                if pm[y+1][x+1] >= 20 and pm[y+1][x-1] < 20:
                    woda[y+1][x] = 12

            if pm[y+1][x-1] < 20:
                if pm[y][x-1] < 20 and pm[y+1][x] < 20:
                    woda[y+1][x-1] = 8
            if pm[y + 1][x - 1] < 20:# and woda[y + 1][x - 1] == 0:
                if pm[y][x-1] < 20 and pm[y+1][x] >= 20:
                    woda[y+1][x-1] = 1
                if pm[y][x-1] >= 20 and pm[y+1][x] < 20:
                    woda[y+1][x-1] = 4

        except:
            pass

    return woda
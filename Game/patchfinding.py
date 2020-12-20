from Game.constants.constants import tile_dim, mapOffset, RED, GREEN, BLUE, YELLOW, PURPLE
import pygame
from queue import PriorityQueue
from Game.jednostki import Unit


class Pathfinding(object):
    """
    każda mapa posiada swoją kopię lecz zamiast wartości odpowiadających za tiles są tylko 'wartości kosztów'
    c = koszt przebycia tile'a ( nazwij zmienną map_costs lub object mapa.costs )
    from given: map = list [c,c,c,c,c,c]
                           [c,c,c,c,c,c]
                           [c,c,c,c,c,c]
                           [c,c,c,c,c,c]
                start = start coords [x,y]
                stop = destin coords [x,y]

    object:
     path.coords = [[x,y],[x,y],[x,y], ...]
     path.costs = [cost1,cost2,cost3, ...]
     path.steps = len(path.costs)
     path.total_costs = sum(path.costs)
     ...
     UPDATE:
        funkcja zwraca listę Path zawierającą:
        [[x, y, koszt_przejazdu],
         [x, y, koszt_przejazdu],
         ...
         [x, y, koszt_przejazdu]]
         Single node contains [Fcost, [X,Y]] where X, Y are absolute Map values (with added mapOffset)
    """

    def __init__(self, start, end, mapa, main_window):
        self.mapa = mapa.mapa
        self.mapa_costs = mapa.cost
        self.mainWindow = main_window   # ptrzebne do wyswietlania na mapie
        # self.openSet = PriorityQueue()     # [cost, [X, Y]]
        self.closeSet = []                # [cost, [X, Y]]
        self.neighbours = PriorityQueue()
        # self.cameF = []          # [cost, [X, Y]]
        # self.cameFrom = {}
        self.start = start
        self.end = end
        self.start_land = self.land_status(self.start)
        self.end_land = self.land_status(self.end)
        self.path = self.find_path(start, end, mapa)
        self.length = len(self.path if self.path else [])
        self.sh()

    def sh(self):
        print("self.start_land", self.start_land, self.start)
        print("self.end_land", self.end_land, self.end)
        print("mapa_cost of start = ", self.mapa_costs[self.start[1]][self.start[0]])
        print("mapa_cost of end = ", self.mapa_costs[self.end[1]][self.end[0]])

    def get_distance(self, node_start, node_end):

        """
        inaczej funkcja h()
        Node_start i node_end = tuple(x,y)
        Node_start = starting point on map
        Node_end = ending point on map

        Calculates the distance between starting and ending node.
        Every horiz/vertic move i distances cost of 10
        Every diagonal move is a distance of 14 (pitagoras)
        returns Hcost or Gcost
        """
        # horizontal distance between two nodes
        x1, x2 = node_start[0], node_end[0]
        y1, y2 = node_start[1], node_end[1]

        x = abs(x1 - x2)
        y = abs(y1 - y2)

        if x > y:
            return 14 * y + 10 * (x - y)
        else:
            return 14 * x + 10 * (y - x)

    def get_tempGscore(self, neigbour, current, start):
        from_start_to_current = self.get_distance(start, current)
        from_neigh_to_current = self.get_distance(neigbour, current)
        dist = from_neigh_to_current + from_start_to_current
        return dist

    def land_status(self, node):
        terrain = self.mapa[node[1]][node[0]]
        if 0 <= terrain < 20:
            return "sea"
        elif 54 <= terrain <= 59:
            return "mountain"
        elif 35 <= terrain <= 38:
            return "bridge"
        else:
            return "land"

    def is_obstacle(self, current_n, y, x):
        if self.start_land == "sea":
            if self.land_status(current_n) == "sea" or "bridge":
                #  jeżeli current = sea, to:
                if self.land_status((x, y)) == "land":  # wszystko co nie jest woda/brzegiem jest przeszkoda
                    return True
                else:
                    return False
            # elif self.land_status(current_n) == "bridge":  # jednostka morska przepływa pod mostem
            #     return False
        else:
            if self.land_status((x, y)) == "sea":  # wszystko poniżej co jest wodą
                return True
            elif self.land_status((x, y)) == "mountain":  # górami jest przeszkoda
                return True
            else:
                return False

    def get_neigbours(self, current_node, targetPos, start):
        cn = current_node[1]

        for yn in range(-1, 2):
            for xn in range(-1, 2):
                if yn == 0 and xn == 0:
                    continue
                else:
                    x = cn[0] + xn
                    y = cn[1] + yn
                    if x < 0 or y < 0:  # nie sprawdza poza mapą, bo po co
                        continue        # dodać jeszcze czy jest przejezdne
                    elif (x, y) in [n[1] for n in self.closeSet]:  # czy sprawdzany node jest w 'closed'
                        continue                                 # jet jest to skip
                    # elif self.mapa_costs[y][x] == 2:  # if obstacle - skip
                    #     continue
                    elif self.is_obstacle(cn, y, x):  # if obstacle is True - skip
                        continue
                    else:
                        nn = [x, y]  # nowy neigbour_node do sprawdzenia dystansu
                        self.neighbours.put((self.get_distance(nn, targetPos) +  # Hcost +
                                             self.get_distance(nn, cn) +  # od curren do aktualnego sasiada
                                             self.get_distance(start, cn),  # + od start do current
                                             (x, y)))

# Funkcje pomocnicze - rysowanie #

    def draw(self, score, xy, color, window):
        font = pygame.font.SysFont("arial", 15, True)
        # draws rectangles on the screen
        x = xy[0] - mapOffset[0]
        y = xy[1] - mapOffset[1]
        # pygame.draw.rect(window, (42, 186, 220), [x * tile_dim + tile_dim-8, y * tile_dim + tile_dim-8, 30, 30], 0)
        pygame.draw.rect(window, color, [x * tile_dim + tile_dim, y * tile_dim + tile_dim, 20, 20], 5)
        text = font.render(str(score), 1, (0, 0, 0))
        window.blit(text, (x * tile_dim + tile_dim - 8, y * tile_dim + tile_dim - 8))
        pygame.display.update()

    def show(self, sett, col, window):
        for score, xy in sett:
            self.draw(score, xy, col, window)

    def pause(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return
# funkcje pomocnicze koniec

    def reconstruct_path(self, came_from, current):
        # returns list of tuples containig path
        p = [self.end]
        self.draw(" ", self.start, PURPLE, window=self.mainWindow)
        self.draw(" ", self.end, PURPLE, window=self.mainWindow)

        while current in came_from.keys():
            current = came_from[current]
            p.append(current)
            self.draw(" ", current, PURPLE, window=self.mainWindow)
        return p[::-1]

    def find_path(self, start, end, mapa):

        """
        Gcost - distance from the starting node
        Hcost - distance from the end node
        Fcost - Gcost + Hcost
        """
        # check if comin from land to sea (or mountain)/ sea to land/ or is "flying"
        if self.start_land != self.end_land:
            return False

        # Initials
        came_from = {}
        g_score = {(x, y): float("inf") for y in range(len(mapa.mapa)) for x in range(len(mapa.mapa[0]))}
        f_score = g_score.copy()
        g_score[start] = 0
        f_score[start] = self.get_distance(start, end)

        openSet = PriorityQueue()  # inicjuje pusta liste Queue
        openSet.put(((self.get_distance(start, end)), start))

        open_set_hash = {start}  # no idea

        while not openSet.empty():
            current_node = openSet.get()   # takes the lowest value from 'open' and removes it form 'open'
            self.closeSet.append(current_node)  # add 'current' to 'closed'
            open_set_hash.remove(current_node[1])
            if current_node[1] == end:
                path = self.reconstruct_path(came_from, current_node[1])
                return path
            else:
                # jesli nie znalazlem sciezki, to wszyskie sasiady staja sie "open_setem",i zawieraja:
                self.get_neigbours(current_node, end, start)  # tworzy liste najbliższych sasiadow

                # self.draw(0, current_node[1], BLUE, self.mainWindow)
                # self.show(openSet.queue, GREEN, self.mainWindow)
                # self.show(self.closeSet, RED, self.mainWindow)

                #  main loop for searching neigbours:
                for n in self.neighbours.queue:  # n - checked node from 'neigbours' of 'current'
                    # self.draw(n[0], n[1], YELLOW, self.mainWindow)
                    # self.pause()
                    d = self.get_distance(current_node[1], n[1])  # gets the Gcost from current to neighbor
                    tentative_gscore = d + g_score[current_node[1]]  # Gcost from the start to neighbour through current
                    if tentative_gscore < g_score[n[1]]:
                        came_from[n[1]] = current_node[1]
                        g_score[n[1]] = tentative_gscore
                        f_score[n[1]] = g_score[n[1]] + self.get_distance(n[1], end)

                        if n[1] not in open_set_hash:
                            open_set_hash.add(n[1])
                            c = self.mapa_costs[n[1][1]][n[1][0]] * 10
                            openSet.put((f_score[n[1]] + c, n[1]))
                            print("openset ", openSet.queue)
                self.neighbours = PriorityQueue()  # makes neighbours empty for next evaluation
        return False

    # def make_nodes(self, x, y):
    #     """ -1 - nieprzejezdne
    #         fly_status = True = wszystko przejezdne
    #         1. tworzy listę_nodów - kopię mapy z samych 0
    #         2. reverse range tworzy nody (kwadraty o coraz mniejszych wartościach, aż do X,Y które sa rowne zero
    #         3. sumuje liste_nodów z warosciami 'kosztow' w zaleznosci czy jest w powietrzu, na ladzie, czy na wodzie
    #         4. Zwraca listę. Sumę 'mapa_costs' + nody (coraz wieksze liczby od miesjca poczatkowego)  """
    #
    #     # 1. tworzy liste_nodow z 0
    #     lista_nodow = []
    #     for i in range(mapaHgh):
    #         lista_n = []
    #         for j in range(mapaWid):
    #             lista_n.append(0)  # tworzę lista samych 0
    #         lista_nodow.append(lista_n)
    #
    #     # 2.
    #     # tworzy smae nody od największych az do zera
    #     # od zewnatrz zatacza kregi do srodka
    #     for c in range(100, -1, -1):
    #         for row in range(-c, c + 1):
    #             for col in range(-c, c + 1):
    #                 try:
    #                     lista_nodow[y + row][x + col] = c
    #                 except IndexError:  # jak wyjdzie poza brzegi mapy
    #                     continue
    #
    #     fly_status = False  # to będzie zmienna przypisana do jednostki, True = może wlatywac na góry
    #
    #     # 3. sumuje liste_nodów z warosciami 'kosztow' w zaleznosci czy jest w powietrzu, na ladzie, czy na wodzie
    #     # sumuję warości list 'nody' z listą kosztów 'mapa_costs'
    #     lista_nodcost = []
    #     if fly_status:
    #         return lista_nodow
    #     else:
    #         # jeśli nie lata, lista musi zostać zmodyfiowana w zależności czy jestem na ladzie, czy na wodzie
    #
    #         for i in range(mapaHgh):
    #             lista_n = []
    #             for j in range(mapaWid):
    #                 if self.mapa_costs[y][x] != 0:  # jeśli pkt_pocz == ląd (koszt wyzszy niz 0),
    #                                                 # to poruszam sie tylko po ladzie
    #                                                 # brak wejścia na góry, chya, że fly_status == True
    #                     if self.mapa_costs[i][j] != 0 and self.mapa_costs[i][j] != -2:
    #                         # jeśli !=0 czyli 'nie woda' i !=-2 czyli 'nie góry'
    #                         # wtedy spraw by nody dodawalo tylko dla ladu
    #                         # lista_n.append(lista_nodow[i][j] + self.mapa_costs[i][j])
    #                         lista_n.append(lista_nodow[i][j])
    #                     else:
    #                         lista_n.append(-1)  # jezeli woda/góry - zakaz wjazdu, (-1)
    #                 else:                       # jeśli jednak startuję z wody:
    #                     if self.mapa_costs[i][j] == 0:   # wtedy spraw by nody dodawalo tylko dla wody
    #                         # lista_n.append(lista_nodow[i][j] + self.mapa_costs[i][j])
    #                         lista_n.append(lista_nodow[i][j])
    #                     else:
    #                         lista_n.append(-1)  # jezeli ląd - zakaz wjazdu, (-1)
    #
    #                 # linia brzegowa będzie wspolna-przejsciowa, ale to musze przemyslec
    #                 # choc lepiej by było zeby na wodę wjezdzalo się z miasta
    #
    #             lista_nodcost.append(lista_n)
    #     # 4. zwrot
    #     return lista_nodcost
    #
    # def szukaj_mniejszych(self, x, y, lista_nodow):
    #     if lista_nodow[y][x] < 0:
    #         print('brak wjazdu!')
    #         return -1
    #     # funkcja szuka mniejszych wartości z nodów
    #     # value = wartośc noda z punktu docelowego (największa wartość)
    #     value = lista_nodow[y][x]
    #     # sasiedzi = [[-1, -1], [0, -1], [1, -1],        # a potem dodaje koszt terenu
    #     #             [-1, 0], [1, 0],
    #     #             [-1, 1], [0, 1], [1, 1]]
    #
    #     # kierunki, kolejnosc sprawdzania
    #     # N W E S       - północ, zachód, wschód, południe
    #     # NW NE SW SE   - płn.zach., płn.wsch, płd.zach, płd.wsch
    #     # szukamy wśród sąsiadów wartości najmniejszych
    #     around_tile_list = []
    #
    #     for sas in self.sasiedzi:
    #         if y + sas[1] < 0 or y + sas[1] > len(lista_nodow) - 1:  # czy nie jesteśmy poza mapą w Y
    #             continue
    #         elif x + sas[0] < 0 or x + sas[0] > len(lista_nodow[0]) - 1:  # czy nie jesteśmy poza maą w X
    #             continue
    #         else:
    #             atl = lista_nodow[y + sas[1]][x + sas[0]]
    #             if atl < 0:
    #                 around_tile_list.append(99)
    #             else:
    #                 around_tile_list.append(atl)
    #             continue    # mam liste wszystkich sąsiadow
    #
    #     print("ATL", around_tile_list)
    #     mini = min(around_tile_list)  # ustalam wartość najmniejszą (najmniejszy nod)
    #     print('mini nodowe', mini)
    #
    #     mniejsze = []  # lista najmniejszych wartości z list nodów
    #
    #     # iteration w poszukiwaniu wartosci mniejszych niz value:
    #
    #     for v in range(len(around_tile_list)):
    #         if around_tile_list[v] != mini:
    #             print('rejectet index of ATL', v)
    #             continue
    #         else:
    #             print('acepted index of ATL', v)
    #             koszt = self.mapa_costs[y + self.sasiedzi[v][1]][x + self.sasiedzi[v][0]]
    #             mniejsze.append((x + self.sasiedzi[v][0], y + self.sasiedzi[v][1], koszt))
    #             # mam listę (x, y, wartosc kosztu przejazdu) dla liczb mniejszych sasiadow
    #     # jezeli lista 'mniejsze' zawiera wiecej niz 1 element,
    #     # szukam mniejszych kosztow
    #     # pozostałe eliminuje z listy pop()
    #     print("mniejsze", mniejsze)
    #
    #     mi = []  # lista kosztów wyciagnieta z listy 'mniejsze'
    #     najmniejsze = []  # lista
    #     if len(mniejsze) > 1:
    #         for m in mniejsze:
    #             mi.append(m[2])  #wyciagam tylko koszty i robie z nich liste
    #         mini = min(mi)  # wyciagam wartosc najmniejsza (najmniejszy koszt)
    #         print('mini kosztowe', mini)
    #         print('mniejszesz', mniejsze)
    #         # eliminuje z listy 'mniejsze' wpisy o wiekszym kosznie niż 'mini'
    #         for m in mniejsze:   # iteruje po liscie i tworzę nowa zawierajaca tylko wartosci najniejsze
    #             if m[2] == mini:
    #                 najmniejsze.append(m)
    #         return najmniejsze
    #     else:
    #         return mniejsze
    #
    # def make_path(self, x, y, nod):
    #     return self.szukaj_mniejszych(x, y, nod)
    #
    # def znajdz_path(x, y, lista_nodow):
    #     path = []
    #     xkonc, ykonc = x, y
    #     value = lista_nodow[y][x]  # y in map type lists is always first
    #     path.append([x, y, value])
    #     step = szukaj_mniejszych2(x, y, lista_nodow, value)  # step to lista najmniejszych dokoloa współrzednych
    #     step_next = []
    #     while True:
    #         for s in step:
    #             print("s in step ", s)
    #             x = s[0]
    #             y = s[1]
    #             value = s[2]
    #             step_next.append(
    #                 szukaj_mniejszych2(x, y, lista_nodow, value))  # step to lista najmniejszych dokoloa współrzednych
    #             # step next może mieć zdublowane wpisy, gdyż sąsiedzi step magą mieć tych samych sąsiadów "step_next"
    #             # należy uzunąć duble (i triple)
    #             for sn in step_next:
    #                 pass
    #
    #             # teraz musze wybrac tę pozycje ze zmiennej "step", dla której "step_next" jest najmniejsze
    #
    #         # step = szukaj_mn_kosztow(x, y, lista_nodow, value)
    #         # path.append(list(step))
    #         print("step", step)
    #         # print("value", value)
    #         print("path w funkcji znajdz droge", path)
    #         x = step[0]
    #         y = step[1]
    #         break
    #     path.reverse()
    #     return path

# def szukaj_mn_kosztow(x, y, lista_nodow, value):    # ta funkcja najpierw szka mnijeszych kosztów przejazdu
#     # szukamy wśród sąsiadów kosztów z mapLegenda2
#     koszty_terenu = []
#     for sas in sasiedzi:
#         if y + sas[1] < 0 or y + sas[1] > len(lista_nodow) - 1:  # czy nie jesteśmy poza mapą w Y
#             continue
#         elif x + sas[0] < 0 or x + sas[0] > len(lista_nodow[0]) - 1:  # czy nie jesteśmy poza maą w X
#             continue
#         koszt_terenu = mapLegenda2.get(mapa[y + sas[1]][x + sas[0]])
#         koszty_terenu.append(koszt_terenu[2])   # tworzy list wszystkich kosztów terenu wokol X,Y
#
#     # musze wyeliminować "-1" i nadac im wartość np."99"
#     for k in koszty_terenu:
#         if k == 0:
#             koszty_terenu[koszty_terenu.index(0)] = 99

    # values_list = []
    # koszty_min = []
    # # iteration w poszukiwaniu wartosci mniejszych niz value:
    # for k in koszty_terenu:
    #     if koszty_terenu[k] == -1 or koszty_terenu[v] > value:
    #         continue
    #     else:
    #         mniejsze.append((x + sasiedzi[v][0], y + sasiedzi[v][1], values_list[v]))
    #         # mam listę (x, y, wartość) dla liczb mniejszych
    # # wyciagam wartości kosztu terenu z mapLegend, dodaję do mniejsze[2] (values)
    # # szukam najmniejszej (najtańszej)
    # # print(mniejsze)
    # nod_kosztowy = []   # suma warosci z noda (z mniejsze) i kosztu ruchu
    # for mn in mniejsze:
    #     koszt_ruchu = mapLegenda2.get(mapa[mn[1]][mn[0]])
    #     nod_kosztowy.append(koszt_ruchu[2] + mn[2])
    #     # print("nod kosztowy", nod_kosztowy)
    # print("mniejsze ", mniejsze)
    # print("koszt nodowy", nod_kosztowy)
    # i = nod_kosztowy.index(min(nod_kosztowy))   # index najniższej wartości
    # print("index najmiejszego noda_kosztowego ",i)
    # return mniejsze[i][0], mniejsze[i][1], nod_kosztowy[i]  # zwracam współrzędne najniższego koszu

#
# def znajdz_path(x, y, lista_nodow):
#     path = []
#     xkonc, ykonc = x, y
#     value = lista_nodow[y][x]   # y in map type lists is always first
#     path.append([x, y, value])
#     step = szukaj_mniejszych2(x, y, lista_nodow, value)   # step to lista najmniejszych dokoloa współrzednych
#     step_next = []
#     while True:
#         for s in step:
#             print("s in step ", s)
#             x = s[0]
#             y = s[1]
#             value = s[2]
#             step_next.append(szukaj_mniejszych2(x, y, lista_nodow, value))  # step to lista najmniejszych dokoloa
#             współrzednych
#             # step next może mieć zdublowane wpisy, gdyż sąsiedzi step magą mieć tych samych sąsiadów "step_next"
#             # należy uzunąć duble (i triple)
#             for sn in step_next:
#                 pass
#
#             # teraz musze wybrac tę pozycje ze zmiennej "step", dla której "step_next" jest najmniejsze
#
#         # step = szukaj_mn_kosztow(x, y, lista_nodow, value)
#         # path.append(list(step))
#         print("step", step)
#         # print("value", value)
#         print("path w funkcji znajdz droge", path)
#         x = step[0]
#         y = step[1]
#         break
#     path.reverse()
#     return path
#
#
# def znajdz_path(x, y, lista_nodow):
#     path = []
#     xkonc, ykonc = x, y
#     value = lista_nodow[y][x]   # y in map type lists is always first
#     path.append([x, y, value])
#     while value > 0:
#         step = szukaj_mniejszych(x, y, lista_nodow, value)
#
#         # step = szukaj_mn_kosztow(x, y, lista_nodow, value)
#         path.append(list(step))
#         # print("xkonc", xkonc)
#         # print("value", value)
#         # print("path ", path)
#         x = step[0]
#         y = step[1]
#         value -= 1
#     path.reverse()
#     return path




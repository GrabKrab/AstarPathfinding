class Unit(object):
    def __init__(self, name, picture, value, prodcost, prodtime, strength, move, bonus, hill, wood, fly, position):
        self._name = name
        self._picture = picture
        self._value = value
        self._prodcost = prodcost
        self._prodtime = prodtime
        self._stregth = strength
        self.move = move
        self.bonus = bonus
        self.hill = hill
        self.wood = wood
        self.fly = fly
        self.position = position  # [x, y]




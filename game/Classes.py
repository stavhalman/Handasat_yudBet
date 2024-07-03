import pygame


class Item():

    def __init__(self,id,quentity) -> None:
        self._id = id
        self._quentity = quentity
        
    def get_id(self) -> str:
        return self._id
    
    def get_quentity(self) -> int:
        return self._quentity
    
    def add(self,quentity_to_add):
        self._quentity+=quentity_to_add
        

class Game_Object():

    def __init__(self,x,y,picture,hp,mp,inventory) -> None:

        self._killer = None
        self._x = x
        self._y = y
        self._picture = pygame.image.load(picture).convert()
        self._picture.set_colorkey((255,255,255))
        self._w = self._picture.get_width()
        self._h = self._picture.get_height()
        self._hp = hp
        self._mp = mp
        self._inventory = inventory
    
    def move(self,x,y):
        self._x+=x
        self._y+=y

    def update(self,screen):

        if self._killer is not None:
            self.give_items(self._killer)
            del self
        screen.blit(self._picture,(self._x,self._y))

    def give_items(self,killer):
        for item_to_give in self._inventory:
            killer.add_item(item_to_give)
            del item_to_give

    def add_item(self,item_to_add):
        for item in self._inventory:
            if item.get_id().equal(item_to_add.get_id()):
                item.add(item_to_add.get_quentity())
                return True
        self._inventory.append(item_to_add)


class Player(Game_Object):
    
    def __init__(self, x, y, picture, hp, mp, inventory, status_effects, keys) -> None:

        Game_Object.__init__(self,x,y,picture,hp,mp,inventory)

        self._status_effects = status_effects
        self._movment_multiplayer = 20
        self._keys = keys
    
    def move(self, screen, objects):

        up = pygame.key.get_pressed()[self._keys["up"]]
        down = pygame.key.get_pressed()[self._keys["down"]]
        right = pygame.key.get_pressed()[self._keys["right"]]
        left = pygame.key.get_pressed()[self._keys["left"]]

        x = int(right)-int(left)
        y = int(down)-int(up)

        x_to_move = (x-abs(y)/2*x)*self._movment_multiplayer
        y_to_move = (y-abs(x)/2*y)*self._movment_multiplayer

        for obj in objects:

            obj.move(-x_to_move,-y_to_move)
            obj.update(screen)
    
    def update(self,screen,objects):

        self.move(screen, objects)
        Game_Object.update(self,screen)

class chunk():

    def __init__(self,x,y,chunk_type):
        self._x = x
        self._y = y
        self._type:str = chunk_type
        self._objects = []
        if self._type.equal("forest"):

class world():

    def __init__(self,name):
        self._name = name
        self._chunks:chunk = []


        for i in range(-1,1):
            for j in range(-1,1):
                self._chunks.append(chunk())

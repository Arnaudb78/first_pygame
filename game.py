import time
import pygame
import pytmx
import pyscroll
import pytmx.util_pygame

from player import Player

class Game:

    def __init__(self):

        self.map = "world"
        
        # creer la fenêtre du jeu
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Game Pygame")

        # charger la map
        tmx_data = pytmx.util_pygame.load_pygame('assets/map/map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # generer un player
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # definir une liste qui stock les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

        #definir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if(pressed[pygame.K_w]):
            self.player.move_up()
            self.player.change_animation('up')
        elif(pressed[pygame.K_s]):
            self.player.move_down()
            self.player.change_animation('down')
        elif(pressed[pygame.K_a]):
            self.player.move_left()
            self.player.change_animation('left')
        elif(pressed[pygame.K_d]):
            self.player.move_right()
            self.player.change_animation('right')
        elif(pressed[pygame.K_SPACE]):
            self.player.move_back()

    def switch_house(self):
         # charger la map
        tmx_data = pytmx.util_pygame.load_pygame('assets/map/house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # definir une liste qui stock les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

        #definir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name("exit_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        #recuperer le point de spawn dans la maison 
        spawn_house_point = tmx_data.get_object_by_name("spawn_house")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 20



    def switch_world(self):
         # charger la map
        tmx_data = pytmx.util_pygame.load_pygame('assets/map/map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # definir une liste qui stock les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

        #definir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

         #recuperer le point de spawn dans la maison 
        spawn_house_point = tmx_data.get_object_by_name("enter_house_exit")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y + 20
        
    def update(self):
        self.group.update()

        #verifier l'entrer dans la maison
        if self.map == "world" and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = "house"

        #verifier la sortie de la maison
        if self.map == "house" and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()
            self.map = "world"

        # verification collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):

        # FPS
        clock = pygame.time.Clock()

        # boucle de jeu 
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect) #centrer sur le player
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()
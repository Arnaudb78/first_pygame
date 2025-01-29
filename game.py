import time
import pygame
import pytmx
import pyscroll
import pytmx.util_pygame

from player import Player

class Game:

    def __init__(self):
        
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
            print(obj)
            if obj.name == "collision":
                print(obj.x, obj.y, obj.width, obj.height)
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

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
        
    def update(self):
        self.group.update()

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
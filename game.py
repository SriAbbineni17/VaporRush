import pygame
import math
from PIL import Image
from PIL import GifImagePlugin
from sys import exit
from pygame.locals import *
from pygame import mixer

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('VaporRush/assets/laser.png').convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (100,100))
    def __init__(self, pos, angle, slope):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.image.load('VaporRush/assets/laser.png').convert_alpha(), angle)
        self.rect = self.image.get_rect(bottomleft = pos)
        self.x_increment = float(slope[0])/math.sqrt((slope[1])**2 + slope[0]**2)
        self.y_increment = float(slope[1])/math.sqrt((slope[1])**2 + slope[0]**2)
    def update(self):
        self.rect.left += self.x_increment * 20
        self.rect.bottom += self.y_increment * 20
    def getSlope(self):
        return self.slope
    def checkCollision(self, brect):
        if self.rect.colliderect(brect):
            brect.left = 1000
    def render(self):
        screen.blit(self.image, self.rect)
        
pygame.init()
def display_score():
    current_time = (pygame.time.get_ticks()//600 - start_time)
    score_surf = test_font.render(f'{current_time}', False, "Gold")
    score_rect = score_surf.get_rect(center = (475,100))
    screen.blit(score_surf, score_rect)
    return current_time
mixer.init()
mixer.music.load('VaporRush/assets/Pyxis.wav')
start_time = 0
press_time = -301
# Setting the volume
mixer.music.set_volume(0.5)
# play music
mixer.music.play(loops=-1)

screen = pygame.display.set_mode((950, 600))
pygame.display.set_caption('VAPORRUSH')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)

# Color values
Gold = (255, 215, 0)
Green = (0,200,0)
Black = (0,0,0)
Gray = (30,30,30)
Purple = (130,68,204)
a_press = False
d_press = False
game_state = False

# #setup disco gif, frame, and count
# discogif = Image.open("assets/disco.gif")
# frame = 0
# count = 0
afro = pygame.image.load('VaporRush/assets/afro.png').convert_alpha()
boombox = pygame.image.load('VaporRush/assets/boombox.png').convert_alpha()
laser = pygame.image.load('VaporRush/assets/laser.png').convert_alpha()

# Text
title = test_font.render('VAPORRUSH', False, Purple)
play = test_font.render('Play?', False, Purple)


afroxpos = 500
boomboxpos = 500
end_score = 0
frame_num = 0
delay = 0
# Rectangles
afroRect = afro.get_rect(topleft = (200, 400))
boomboxRect = boombox.get_rect(midbottom = (1000, 526))
titleRect = title.get_rect(center = (475, 80)) 
playRect = play.get_rect(center = (475, 250))

player_gravity = 0
floor = afroRect.bottom
face_left = False
lasers = []
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and afroRect.bottom == floor and game_state != False:
                player_gravity = -20        
            elif event.key == pygame.K_a:
                afro = pygame.image.load('VaporRush/assets/afro.png').convert_alpha()
                afro = pygame.transform.flip(afro, True, False).convert_alpha()
                face_left = True
                a_press = True
            elif event.key == pygame.K_d:
                afro = pygame.image.load('VaporRush/assets/afro.png').convert_alpha()
                face_left = False
                d_press = True
            elif event.key == pygame.K_w and afroRect.bottom == floor:
                player_gravity = -20   
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                a_press = False
            elif event.key == pygame.K_d:
                d_press = False
        if a_press:
            afroRect.left -= 10
        elif d_press:
            afroRect.right += 10
        
    if game_state:
        if frame_num > 59:
            frame_num = 0
        disco = pygame.image.load('VaporRush/assets/disco_frames/frame_' + str(frame_num) + '_delay-0.08s.gif').convert_alpha()
        
        delay += 1
        if delay == 3:
            delay = 0
            frame_num += 1
        
        discoRect = disco.get_rect(topleft = (0,0))
        clock = pygame.time.Clock()
        screen.blit(disco, (0,0))
        screen.blit(afro, afroRect)
        
        if pygame.mouse.get_pressed() == (1,0,0):
            laser_time = pygame.time.get_ticks() - press_time
            if(laser_time > 300):
                press_time = pygame.time.get_ticks()
                mouse_pos = pygame.mouse.get_pos()
                if (face_left):
                    if (mouse_pos[0] > afroRect.topleft[0]):
                        afro = pygame.transform.flip(afro, True, False).convert_alpha()
                        initial_pos = (afroRect.midright[0] - 50, afroRect.midright[1] + 10)
                        angle = math.degrees(math.atan(-(mouse_pos[1] - initial_pos[1])/(mouse_pos[0] - initial_pos[0])))
                        face_left = False
                    else:
                        initial_pos = (afroRect.midleft[0] - 50, afroRect.midleft[1] + 10)
                        angle = math.degrees(math.atan(-(mouse_pos[1] - initial_pos[1])/(mouse_pos[0] - initial_pos[0])))
                else:
                    if (mouse_pos[0] < afroRect.topright[0]):
                        afro = pygame.transform.flip(afro, True, False).convert_alpha()
                        initial_pos = (afroRect.midleft[0] - 50, afroRect.midleft[1] + 10)
                        angle = math.degrees(math.atan(-(mouse_pos[1] - initial_pos[1])/(mouse_pos[0] - initial_pos[0])))
                        face_left = True
                    else:
                        initial_pos = (afroRect.midright[0] - 50, afroRect.midright[1] + 10)
                        angle = math.degrees(math.atan(-(mouse_pos[1] - initial_pos[1])/(mouse_pos[0] - initial_pos[0])))
                slope = (mouse_pos[0] - initial_pos[0], (mouse_pos[1] - initial_pos[1]))
                lasers.append(Laser(initial_pos, angle, slope))
                lasers[len(lasers) - 1].render()
        length = len(lasers)
        for i in lasers:
            i.checkCollision(boomboxRect)
            i.update()
            i.render()
            # if i[0] > 1500 or i[1] > 1500:
            #     lasers.remove(i)
            #     length -= 1
        display_score()
        boomboxRect.left -= 6
        if (boomboxRect.left <= -200):
            boomboxRect.left = 1000
        if (afroRect.left <= -200):
            afroRect.left = 1000
        if (afroRect.right >= 1100):
            afroRect.right = -50
        
        player_gravity += .8
        afroRect.top += player_gravity
        if afroRect.bottom >= floor:
            afroRect.bottom = floor
            
        if afroRect.colliderect(boomboxRect):
            end_score = display_score()
            game_state = False
        screen.blit(boombox, boomboxRect)
    else:
        # setup screen
        vapor = pygame.image.load('VaporRush/assets/vapor.png').convert_alpha()
        vapor_scaled = pygame.transform.scale(vapor, (950, 600))
        end_score_surf = test_font.render("Score: " + f'{end_score}', False, "Purple")
        end_score_rect = end_score_surf.get_rect(center = (475,175))
        screen.blit(vapor_scaled, (0,0))
        screen.blit(end_score_surf, end_score_rect)
        screen.blit(title, titleRect)
        screen.blit(play, playRect)
        
        
        boomboxRect.left = 1000
        afroRect.left = 200
        
        # pygame.draw.rect(screen, Purple, playRect)
    
        keys=pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if keys[K_SPACE]:
            start_time = pygame.time.get_ticks()//600
            game_state = True
        if playRect.collidepoint(mouse_pos) and pygame.mouse.get_pressed() == (1, 0, 0):
                lasers = []
                laser_surfaces = []
                start_time = pygame.time.get_ticks()//600
                game_state = True
        
    pygame.display.update()
    clock.tick(60)
                

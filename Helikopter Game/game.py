import random 
import sys
import pygame 


def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,580))
    screen.blit(floor_surface,(floor_x_pos + 576,580))

def create_obstacle():
    random_obstacle_pos = random.choice(obstacle_height)
    bottom_obstacle = obstacle_surface.get_rect(midtop = (700,random_obstacle_pos))      # put acc half to screen
    top_obstacle = obstacle_surface.get_rect(midbottom = (700,random_obstacle_pos-250))
    return bottom_obstacle,top_obstacle

def move_obstacles(obstacles):
    global obstacle
    for obstacle in obstacles:
        obstacle.centerx -= obs_speed         # control obstacle speed
    return obstacles 

def draw_obstacles(obstacles):
    global obstacle
    for obstacle in obstacles:
        if obstacle.bottom >= 600:    # bottom point is screen height
            screen.blit(obstacle_surface, obstacle)
        else:
            flip_obstacle = pygame.transform.flip(obstacle_surface, False, True) # false>flip in x direction,True>flip in y
            screen.blit(flip_obstacle, obstacle)

def check_collisions(obstacles):
    global can_score
    for obstacle in obstacles:
        if heli_rect.colliderect(obstacle):
            death_sound.play()
            can_score = True
            return 0
    if heli_rect.top <= 15 or heli_rect.bottom >= 550:
        death_sound.play()
        can_score = True
        return 0
    
    return 1

def rotate_bird(heli):
    new_heli = pygame.transform.rotozoom(heli, -heli_movement * 2.0,1)      # rotation of heli
    return new_heli

def score_display(game_state):
    
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f"Score : {int(score)}",True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}",True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,500))
        screen.blit(high_score_surface,high_score_rect)
  
def update_high_score(score, high_score):
    if score > high_score:
        high_score = score 
    return high_score

def obstacle_score_check():
    global score, can_score
 
    if obs_list:
        for obstacle in obs_list:
            if 98 < obstacle.centerx < 102 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if obstacle.centerx < 0:
                can_score = True

'''def level():
    global obs_time
    global score
    if score == 5:
        obs_time = 500
    return obs_time'''

    





# MAIN BODY

#pygame.mixer.pre_init(frequency=44100, size = 16, channels= 1, buffer = 512)    # to avoid audio buffer
pygame.init()                   

screen = pygame.display.set_mode((576,600))                 # set window screen and ratio
fpsclock = pygame.time.Clock()                              # limit frame rate
pygame.display.set_caption("Helikopter")                    
game_font = pygame.font.Font('04B_19.ttf',40)               # import fonts
game_font2 = pygame.font.Font('04B_19.ttf',20)


# VARIABLES 
gravity = 0.15
heli_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True
start_game = True
obs_time = 1500                                                # for levels 
obs_speed = 2.5


# BACKGROUND
bg_surface = pygame.image.load('assets/bg.jpg').convert()
bg_surface = pygame.transform.scale(bg_surface, (576,600))

# FLOOR
floor_surface = pygame.image.load('assets/city-line.png').convert_alpha()
floor_surface = pygame.transform.scale(floor_surface, (600,20))
floor_x_pos = 0

# HELIKOPTER
heli_surface = pygame.image.load('assets/H.png').convert_alpha()
heli_surface = pygame.transform.scale(heli_surface, (60,40))
heli_rect = heli_surface.get_rect(center = (100,300))               # take heli as a rectangle

# OBSTACLES/BUILDINGS
obstacle_surface = pygame.image.load('assets/B.png').convert_alpha()
obstacle_surface = pygame.transform.scale(obstacle_surface, (80,400))
obs_list = []                                                       # creating list for obstacles
SPAWNOBS = pygame.USEREVENT                                         # timer for obs 
pygame.time.set_timer(SPAWNOBS, obs_time)                           # time after which obs appears
obstacle_height = [200, 300, 400]                                   # possible pipe heights position

# GAMEOVER
game_over_surface = pygame.image.load('assets/g_o.png').convert_alpha()
game_over_surface = pygame.transform.scale(game_over_surface, (180,250))
game_over_rect = game_over_surface.get_rect(center = (288,300))



#SOUNDS
move_sound = pygame.mixer.Sound('sound/sfx_swooshing.wav')
death_sound = pygame.mixer.Sound('sound/c1.wav')
heli_sound = pygame.mixer.Sound('sound/sfx_heli.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT, 100)

x = False

# GAME LOOP (Start Screen)

while True:
    
    screen.blit(bg_surface,(0,0)) 
    start_surface = game_font2.render(str("PRESS SPACE TO START THE GAME"),True,(255,255,255))
    start_rect = start_surface.get_rect(center = (288,100))
    screen.blit(start_surface,start_rect)
    pygame.display.update()
    for event in pygame.event.get():   
        if event.type == pygame.QUIT:                           # to terminate exceution 
            pygame.quit()
            sys.exit() 

        if event.type == pygame.KEYDOWN:                        # takes user input to move heli
            if event.key == pygame.K_SPACE:
                x = True
    

    # MAIN GAME LOOP
    while x == True:

        
        '''e = pygame.event.wait()

        while e.type != pygame.KEYDOWN:
            screen.blit(bg_surface,(0,0))
            start_surface = game_font2.render(str("PRESS SPACE TO START THE GAME"),True,(255,255,255))
            start_rect = start_surface.get_rect(center = (288,100))
            screen.blit(start_surface,start_rect)
            e = pygame.event.wait()
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
        e = pygame.event.wait()
        while  e.type != pygame.KEYDOWN:
            e = pygame.event.wait()'''

        '''for event in pygame.event.get():                 # event loop : looks for events 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_game:'''

        #screen.blit(bg_surface,(0,0)) 
        

        for event in pygame.event.get():                 # event loop : looks for events 
            
            if event.type == pygame.QUIT:                # to terminate exceution 
                pygame.quit()
                sys.exit()
            
            
            
            if event.type == pygame.KEYDOWN:                        # takes user input to move heli
                
                if event.key == pygame.K_SPACE and game_active == True:    # and start_game == True:
                    heli_movement = 0
                    heli_movement -= 4                                          # heli move up, HELI SPEED  
                    move_sound.play()                                           # heli sound
                if event.key == pygame.K_SPACE and game_active == False:    # and start_game == False:       # To end and restart
                    game_active = True  
                    #start_game = True
                    obs_list.clear ()                       # empty list to stop the obstacles and then restart
                    heli_rect.center = (100, 300)           # move heli to center again
                    heli_movement = 0 
                    score = 0
                    obs_speed= 2.5


            if event.type == SPAWNOBS:
                obs_list.extend(create_obstacle())              # adding more obstacle to the list/ create
                #print(obs_list)                             # only to check if obs are creating, to be deleted


        screen.blit(bg_surface,(0,0))                       # to add background surface

        if game_active == True:
            
            '''start_surface = game_font.render(str('press space'),True,(255,255,255))
            start_rect = start_surface.get_rect(center = (288,100))
            screen.blit(start_surface,start_rect)
            game_active = 1'''
        
            #screen.blit(bg_surface,(0,0))
        
            # HELI
            heli_movement += gravity     
                            
            rotated_bird = rotate_bird(heli_surface)        # f takes original bird surface and rotates it
            heli_rect.centery += heli_movement              # move heli y axis by gravity
            screen.blit(rotated_bird,heli_rect)             # display heli surface

            game_active = check_collisions(obs_list)        # f call to check collision

            # OBSTACLES
            obs_list = move_obstacles(obs_list)                 # update moved list of obs
            draw_obstacles(obs_list)                            # draw obs
            
            obstacle_score_check()                              # score  check with obs
            score_display('main_game')                           # main game describes gaem state

            if score >= 5 and score <=10:
                obs_speed = 3

            if score >= 11 and score<=15:
                obs_speed = 4

            if score >= 16 and score<=20:
                obs_speed = 5
            if score >= 21 and score<=25:
                obs_speed = 6
            if score >= 26:
                obs_speed = 7       

            #level()
        elif game_active == False:
            screen.blit(game_over_surface, game_over_rect)
            high_score = update_high_score(score, high_score)       # f call to update highscore
            score_display('game_over')                         # display score

         
        
        '''start_surface = game_font2.render(str("PRESS SPACE TO START THE GAME"),True,(255,255,255))
        start_rect = start_surface.get_rect(center = (288,100))
        screen.blit(start_surface,start_rect)'''
        

        # FLOOR
        floor_x_pos -= 1
        draw_floor()
        if floor_x_pos <= -576:
            floor_x_pos = 0
        

        pygame.display.update()            
        fpsclock.tick(120)                              # frame rate
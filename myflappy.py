import pygame, sys, random 

def draw_floor():			# showing to floor
	screen.blit(floor_surface,(floor_x_pos,900))
	screen.blit(floor_surface,(floor_x_pos + 576,900))

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))		# here "-300" means distance between two pipes 
	bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
	return bottom_pipe,top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 5				# moving pipe to the left

	visible_pipes = [pipe for pipe in pipes if pipe.right > -50]			# deleting old pipes or showing thhose pipes which here on the screen
	# print(visible_pipes)
	return visible_pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 1024:			# only lower pipe will reach it
			screen.blit(pipe_surface,pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface,False,True)			#(x=False,y=True) that means we are flipping in y direction...you also can use roate 180 degree to flip or rotate our pip
			screen.blit(flip_pipe,pipe)

def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):			# it is automatically check this two rectangle does they collite or not
			# death_sound.play()
			death_sound.play()
			return False

	if bird_rect.top <= 0 or bird_rect.bottom >= 900:			# when our bird out of the screen 
		death_sound.play()
		return False

	return True

nm=1
def rotate_bird(bird):
	global nm
	if nm ==1:
		new_bird = pygame.transform.rotozoom(bird,bird_movement * 3,1)		# here "-bird_movement * 3" is rotation degree and 1 is scale..it is usefull when you wanna scale up or wanna big our picture....1 means 1 scale or no scale
		nm=2
	else:
		new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)	
		nm=1
	return new_bird

def bird_animation():
	new_bird = bird_surface
	new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))		# (100,bird_rect.centery).....x position must be same...but y position must be before bird y position....otherwise they will easily caught that we changed our bird
	return new_bird,new_bird_rect

def score_display(game_state):
	if game_state == True:
		score_surface = game_font.render(str(int(score)),True,(255,255,255))		# here True means antialias...no need to know....we converting our number into string because if we wanna  display it must be string
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)
	else:			# means game over
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,850))
		screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):			# updating high score
	if score > high_score:
		high_score = score
	return high_score

def pipe_score_check():
	global score, can_score 
	
	if pipe_list:
		for pipe in pipe_list:
			if 95 < pipe.centerx < 105 and can_score:			# here bird x=100 is not changing...so if pipe is go on that location that means bird crossed the pipe
				score += 1
				score_sound.play()
				can_score = False			
			if pipe.centerx < 0:
				can_score = True
# pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)		# here 40 is font-size

pygame.display.set_icon(pygame.image.load('assets/bird.png').convert_alpha())
pygame.display.set_caption('Fazle Flappy ')

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = False			# so now initially game will not start until you press up
score = 0
high_score = 0
can_score = True

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0


'''
bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_surface = pygame.transform.scale2x(bird_surface)

# bird_rect = bird_surface.get_rect()		
# print(bird_rect.center)			# By default our center or top left where our pygame show this image
# bird_rect = bird_surface.get_rect(center = (0,0))		# saw where it's center....it position works from his center

bird_rect = bird_surface.get_rect(center = (100,512))			# now this image center or top left is (100,512)...so now if we show this image it will show on that location		
print(bird_rect.center)

'''
# bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
# bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
# bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())

bird_downflap = pygame.image.load('assets/bird.png').convert_alpha()

bird_surface = bird_downflap
bird_rect = bird_surface.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1			# if you want add another new userevent then you need to give another new increasing number..
pygame.time.set_timer(BIRDFLAP,200)


pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)			# after 1200 mili second or 1.2 second  automatically create a event called "SPAWNPIPE"
pipe_height = [400,600,800]
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
# score_sound_countdown = 100


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if (event.key == pygame.K_SPACE or event.key == pygame.K_UP ) and game_active:
				bird_movement = 0
				bird_movement -= 10
				flap_sound.play()

			if (event.key == pygame.K_SPACE or event.key == pygame.K_UP ) and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (100,512)
				bird_movement = 0
				score = 0
				can_score=True

		if event.type == SPAWNPIPE:			# Accessing our own created event which will happend after 1.2 second
			pipe_list.extend(create_pipe())
			# print(create_pipe())

		if event.type == BIRDFLAP:		
			# we have only bird image..so it's not necessary	
			# if bird_index < 2:
			# 	bird_index += 1
			# else:
			# 	bird_index = 0

			bird_surface,bird_rect = bird_animation()


	screen.blit(bg_surface,(0,0))

	if game_active:
		# Bird
		bird_movement+=gravity		# increasing bird movement
		bird_rect.centery+=bird_movement		# increasing bird center "y" or downing the bird
		rotated_bird = rotate_bird(bird_surface)

		screen.blit(rotated_bird,bird_rect)		# that means (rotated_bird,(100,512)) and (100,512) from bird center
		
		game_active=check_collision(pipe_list)

		# pipes
		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)

		# Score
		pipe_score_check()

		score_display('main_game')
	else:
		screen.blit(game_over_surface,game_over_rect)
		high_score = update_score(score,high_score)
		# score_display('game_over')
		score_display(game_active)		# it's better to use rather than string

	# Floor
	floor_x_pos -= 1
	draw_floor()
	if floor_x_pos <= -576:
		floor_x_pos = 0				# WE ARE again showing our floor
	

	pygame.display.update()
	clock.tick(100)

import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

#screen dimensions
screen_width = 1500
screen_height = 700

#font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

#open game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('The Lunar Experiment')

#define game variables
tile_size = 50
game_over = 0
main_menu = True
score = 0

#colors
#define colours
white = (255, 255, 255)
blue = (0, 0, 255)

#load images
restart_img = pygame.image.load('lunarexperiment/restart_btn.png')
start_img = pygame.image.load('lunarexperiment/start_btn.png')
exit_img = pygame.image.load('lunarexperiment/exit_btn2.png')
koexit_img = pygame.image.load('lunarexperiment/exit_btn3.png')
cat_standing_1 = pygame.image.load('lunarexperiment/finalcat1.2.png')
cat_standing_2 = pygame.image.load('lunarexperiment/finalcat2.2.png')
background = pygame.image.load('lunarexperiment/BACKGROUND.png')
sludge = pygame.image.load('lunarexperiment/sludge.png')
endpoint = pygame.image.load('lunarexperiment/endpoint.png')
enemy = pygame.image.load('lunarexperiment/evilguy.png')
coin = pygame.image.load('lunarexperiment/coins.png')

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))
class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		#draw button
		screen.blit(self.image, self.rect)

		return action

class Player():
	def __init__(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range (1, 3):
			img_right = pygame.image.load(f'lunarexperiment/catstand{num}.png')
			img_right = pygame.transform.scale(img_right, (55, 50))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('lunarexperiment/ghost.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True
	def update(self, game_over):
		dx = 0
		dy = 0
		walk_cooldown = 8


		if game_over == 0:
			#get keypresses
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]

			#handle animation
			if self.counter > walk_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]

			#add gravity
			self.vel_y += 1
			if self.vel_y > 10:
					self.vel_y >10
			dy += self.vel_y

			# check for collision
			self.in_air = True
			for tile in world.tile_list:
				# check for collision in x direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				# check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					# check if below the ground i.e. jumping
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					# check if above the ground i.e. falling
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False

			#check for enemies
			if pygame.sprite.spritecollide(self, enemy_group, False):
				game_over = -1

			# check for lava
			if pygame.sprite.spritecollide(self, sludge_group, False):
				game_over = -1

			# check for exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1

			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy

		elif game_over == -1:
			self.image = self.dead_image
			if self.rect.y > 200:
				self.rect.y -= 5

		#draw player
		screen.blit(self.image, self.rect)

		return game_over

	def reset(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(1, 3):
			img_right = pygame.image.load(f'lunarexperiment/catstand{num}.png')
			img_right = pygame.transform.scale(img_right, (55, 50))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('lunarexperiment/ghost.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True

class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		rock_img = pygame.image.load('lunarexperiment/rocktexture1.png')
		space_rock = pygame.image.load('lunarexperiment/spacerock.png')
		sludge = pygame.image.load('lunarexperiment/sludge.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(rock_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(space_rock, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					sludge = Sludge(col_count * tile_size, row_count * tile_size)
					sludge_group.add(sludge)
				if tile == 4:
					exit = Exit(col_count * tile_size, row_count * tile_size)
					exit_group.add(exit)
				if tile == 5:
					enemy = Enemy(col_count * tile_size, row_count * tile_size + 21)
					enemy_group.add(enemy)
				if tile == 6:
					coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					coin_group.add(coin)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('lunarexperiment/evilguy.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1

class Sludge(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('lunarexperiment/sludge.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('lunarexperiment/coins.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('lunarexperiment/endpoint.png')
		self.image = pygame.transform.scale(img, (tile_size, (tile_size)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

#groups
coin_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
sludge_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#display coin
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

#create the world
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 6, 0, 1],
[1, 2, 2, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 2, 2, 0, 0, 0, 6, 0, 0, 5, 0, 0, 0, 6, 0, 2, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 6, 1],
[1, 1, 1, 1, 1, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 6, 0, 0, 2, 2, 2, 2, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 6, 0, 0, 0, 0, 2, 2, 3, 3, 1, 1, 1, 2, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1],
[1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

player = Player(100, screen_height - 130)

world = World(world_data)

#buttons
restart_button = Button(screen_width // 2 - 625, screen_height // 2 + -50, restart_img)
start_button = Button(screen_width // 2 - 625, screen_height // 2 - 175, start_img)
exit_button = Button(screen_width // 2 - 605, screen_height // 2 - 25, exit_img)

run = True
while run:

	clock.tick(fps)

	screen.blit(background, (0, 0))

	if main_menu == True:
		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False
	else:
		world.draw()

		if game_over == 0:
			enemy_group.update()
			# update score
			# check for coin
			if pygame.sprite.spritecollide(player, coin_group, True):
				score += 1
			draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)

		enemy_group.draw(screen)
		sludge_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)

		game_over = player.update(game_over)

		# if died
		if game_over == -1:
			if restart_button.draw():
				player.reset(100, screen_height - 130)
				game_over = 0


		# completed the level
		if game_over == 1:
				draw_text('YOU WIN!', font, white, (screen_width // 2) + 180, (screen_height // 2) - 40)


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()

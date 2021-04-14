import pygame
from level import Level


class Player:

    def __init__(self, level: Level):

        self.level = level

        # set images
        self.images = {
            'run': pygame.image.load('assets/images/run.png').convert(),
            'stand': pygame.image.load('assets/images/stand.png').convert(),
            'up': pygame.image.load('assets/images/up.png').convert(),
            'down': pygame.image.load('assets/images/down.png').convert(),
            'dead': pygame.image.load('assets/images/dead.png').convert(),
            'collide': pygame.image.load('assets/images/collide.png').convert()
        }
        self.particle = pygame.image.load('assets/images/particle.png').convert()

        self.rect = self.images['stand'].get_rect()
        self.rect.x = 50
        self.rect.y = 368
        self.floor = 368

        self.vel_x = 0
        self.vel_y = 0
        self.grav = 1
        self.jump = 0

        self.score = 0
        self.combo = 0

        self.life = self.level.duration + 10
        self.shield = 20

        self.collide = False
        self.run = False
        self.ended = False

        self.particles = []

    def update(self):
        if self.life:
            self.collide = False
            for obstacle in self.level.obstacles:
                obstacle.x -= self.vel_x
                if self.rect.colliderect(obstacle):
                    self.damage()
                    self.collide = True
                    self.combo = 0
                    self.jump = 0
                    if self.vel_y < 0:
                        self.vel_y = 0
            if not self.collide:
                self.vel_y -= self.grav
            self.rect.y -= self.vel_y
            if self.rect.y >= self.floor:
                self.rect.y = self.floor
                self.vel_y = 0
                self.jump = 0

            for obstacle in self.level.obstacles:
                if self.rect.colliderect(obstacle):
                    if not self.collide:
                        self.rect.bottom = obstacle.top
                    if self.vel_y < 0:
                        self.vel_y = 0
                    self.jump = 0

            if self.level.obstacles:
                self.score += self.combo
            self.particles.append(self.rect.y)
            if len(self.particles) > self.combo:
                self.particles = self.particles[-1:-self.combo]

        if self.life < 0:
            self.life = 0
        if self.life == 0:
            self.level.song.stop()

        new_obstacles = []
        new_colors = []
        for index, obstacle in enumerate(self.level.obstacles):
            if obstacle.x > -100:
                new_obstacles.append(self.level.obstacles[index])
                new_colors.append(self.level.colors[index])
        self.level.obstacles = new_obstacles
        self.level.colors = new_colors
        if not len(self.level.obstacles):
            self.level.song.set_volume(self.level.song.get_volume()/1.01)

    def damage(self):
        self.shield -= 1
        if self.shield < 0:
            self.life += self.shield
            self.shield = 0

    def draw(self, game):
        game.fill((0, 0, 20))
        pygame.draw.rect(game, (255, 240, 240), (0, 400, 800, 100))
        for distance, pos_y in enumerate(self.particles):
            game.blit(self.particle, (self.rect.x - 1 - distance, pos_y))
        for index in range(len(self.level.obstacles)):
            if self.level.obstacles[index].x < 801:
                pygame.draw.rect(game, self.level.colors[index], self.level.obstacles[index])
        if not self.life:
            game.blit(self.images['dead'], (self.rect.x, self.rect.y))
        elif not self.run:
            game.blit(self.images['stand'], (self.rect.x, self.rect.y))
        elif self.collide:
            game.blit(self.images['collide'], (self.rect.x, self.rect.y))
        elif self.vel_y > 0:
            game.blit(self.images['up'], (self.rect.x, self.rect.y))
        elif self.vel_y < 0:
            game.blit(self.images['down'], (self.rect.x, self.rect.y))
        else:
            game.blit(self.images['run'], (self.rect.x, self.rect.y))

    def spacebar(self):
        if not self.run:
            self.run = True
            self.vel_x = 4
            self.level.song.play()

        if self.jump < 2:
            self.jump += 1
            if self.level.obstacles:
                self.combo += 1
                self.shield += self.combo
                if self.shield > 100:
                    self.shield = 100
            if self.vel_y < 0:
                self.vel_y = 10
            else:
                self.vel_y += 15
        if not self.life:
            self.ended = True

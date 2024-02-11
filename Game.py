# Import the pygame module
import pygame
import random
import sys
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

FRAMES = 60
TIME = 40
ACTIONS_PER_SECOND = 5
ACTION_EVERY = FRAMES // ACTIONS_PER_SECOND
FRAMES_TO_END = FRAMES * TIME

Starting_Position = [[20,20],[20,SCREEN_HEIGHT-20],[SCREEN_WIDTH-20,20],[SCREEN_WIDTH-20,SCREEN_HEIGHT-20]]



        
class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the player, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.surf = pygame.Surface([width, height])
        self.surf.fill(WHITE)
        self.surf.set_colorkey(WHITE)

        #Initialise attributes of the car.
        self.width = width
        self.height = height
        self.color = color
        self.speed_x = 0
        self.speed_y = 0
        
        self.acceleration = 0.5
        self.deselaration = 0.1

        # Draw the player
        pygame.draw.circle(self.surf, self.color, (self.width//2, self.height//2), 5)
        self.rect = self.surf.get_rect(center=(random.choice(Starting_Position)))
    
    # Move the sprite based on user keypresses
    def update(self, player_actions):
        if player_actions[0]:
            self.speed_y += -self.acceleration
            if self.speed_y < -5:
                self.speed_y = -5
        if player_actions[1]:
            self.speed_y += self.acceleration
            if self.speed_y > 5:
                self.speed_y = 5
        if player_actions[2]:
            self.speed_x += -self.acceleration
            if self.speed_x < -5:
                self.speed_x = -5
        if player_actions[3]:
            self.speed_x += self.acceleration
            if self.speed_x > 5:
                self.speed_x = 5
        if not player_actions[0] and not player_actions[1]:
            if self.speed_y > 0:
                self.speed_y -= self.deselaration
            if self.speed_y < 0:
                self.speed_y += self.deselaration
        if not player_actions[2] and not player_actions[3]:
            if self.speed_x > 0:
                self.speed_x -= self.deselaration
            if self.speed_x < 0:
                self.speed_x += self.deselaration
        # Move the sprite
        self.rect.move_ip(self.speed_x, self.speed_y)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Target(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        super(Target, self).__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill(BLUE)

        pygame.draw.circle(self.surf, BLUE, (15, 15), 5)
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        )
        
def does_collide(rect1, rect2):
    if rect1.x < rect2.x + rect2.width and rect1.x + rect1.width > rect2.x and rect1.y < rect2.y + rect2.height and rect1.height + rect1.y > rect2.y:
        return True
    return False

def player_input(keypresses,player1,player2):
    input = [False, False, False, False]
    if keypresses[K_UP] and player2 == 'human':
        input[0] = True
    if keypresses[K_DOWN] and player2 == 'human':
        input[1] = True
    if keypresses[K_LEFT] and player1 == 'human':
        input[2] = True
    if keypresses[K_RIGHT] and player1 == 'human':
        input[3] = True

    if player1 == 'agent':
        action = agent1_action()
        if action == 0:
            input[2] = True
        elif action == 2:
            input[3] = True
    if player2 == 'agent':
        action = agent2_action()
        if action == 0:
            input[0] = True
        elif action == 2:
            input[1] = True
    return input

def agent1_action():
    action = random.choice([0,1,2])
    return action
    
def agent2_action():
    action = random.choice([0,1,2])
    return action

def main(player1='human',player2='human',ui = True):
    if player1 == 'human' or player2 == 'human':
        ui = True

    # Initialize pygame
    pygame.init()
    if ui:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Instantiate player and target.
    player = Player('red',20,20)
    target = Target(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    running = True
    frame = 0
    next_action = ACTION_EVERY
    total_actions = 0
    # Main loop
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        # Player Actions
        if next_action == ACTION_EVERY:
            pressed_keys = pygame.key.get_pressed()
            player_actions = player_input(pressed_keys,player1,player2)
            next_action = 0
            total_actions += 1
        player.update(player_actions)
        next_action += 1

        if ui:
            # Fill the screen with black
            screen.fill((0, 0, 0))

            # Draw the target
            screen.blit(target.surf, target.rect)

            # Draw the player on the screen
            screen.blit(player.surf, player.rect)

        # Check if the player has collided with the target
        if does_collide(player.rect, target.rect):
            # Check player speed
            if player.speed_x < 2.5 and player.speed_y < 2.5 and player.speed_x > -2.5 and player.speed_y > -2.5:
                print("You win!")
                running = False
                
            #running = False
        if ui:
            # Update the display
            pygame.display.flip()
        else:
            print('Player location: ',player.rect)

        # Ensure program maintains a rate of 60 frames per second
        pygame.time.Clock().tick(FRAMES)
        frame += 1
        if frame == FRAMES_TO_END:
            running = False
    print('Total actions: ', total_actions)


if __name__ == '__main__':
    # get arguments
    player1 = sys.argv[1]
    player2 = sys.argv[2]
    if len(sys.argv) > 3:
        ui = sys.argv[3]
    else:
        ui = True

    main(player1,player2,ui)
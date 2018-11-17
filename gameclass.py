"""
Class for racing game
"""
import pygame
from typing import Tuple, List
from mario import Mario
from background import Background
from random import choice
from obstacle import Obstacle


def collision_between(mario: Mario, obstacle: Obstacle) -> bool:
    """
    Return whether or not there is overlapping between Mario and the obstacle.
    """
    mario_rect = mario.image.get_rect()
    obstacle_rect = obstacle.image.get_rect()
    obs_span = (obstacle.x, obstacle.x + obstacle_rect.size[0], obstacle.y, obstacle.y + obstacle_rect.size[1])
    mario_span = (mario.x_cor, mario.x_cor + mario_rect.size[0], mario.y_cor, mario.y_cor + mario_rect.size[1])

    check_x_ok = obs_span[1] < mario_span[0] or obs_span[0] > mario_span[1]
    check_y_ok = obs_span[3] < mario_span[2] or obs_span[2] > mario_span[3]

    return not (check_x_ok or check_y_ok)


def generate_obstacle(x, y) -> Obstacle:
    """
    Generate an obstacle.
    """
    new_obstacle = Obstacle(x, y)
    return new_obstacle


def accelerating_true(character: Mario, background: Background):
    """
    Changes Mario's position, speed and acceleration when accelerating is true.
    """
    if character.acceleration < 0:
        character.acceleration = 0
    elif 0 <= character.acceleration < 15:
        character.acceleration += 0.05
    if character.acceleration >= 0 and character.speed < 15:
        character.speed += character.acceleration

    background.speed = character.speed

    background.move_background(background.x_cor, background.y_cor + background.speed)


def decelerating_true(character: Mario, background: Background):
    """
    Changes Mario's position, speed and acceleration when accelerating is true.
    """
    if character.acceleration > 0:
        character.acceleration = 0
    elif 0 >= character.acceleration > -15:
        character.acceleration -= 0.08

    if character.acceleration < 0 and character.speed > -15:
        character.speed += character.acceleration
    background.speed = character.speed

    background.move_background(background.x_cor, background.y_cor + background.speed)


def hor_accelerating_true(character: Mario):
    """
    Changes Mario's position, speed and acceleration when accelerating is true.
    """
    if 0 <= character.hor_acceleration < 1:
        character.hor_acceleration += 0.1
    elif character.hor_acceleration < 0:
        character.hor_acceleration = 0.1
    if character.hor_acceleration >= 0 and character.hor_speed < 7:
        character.hor_speed += character.hor_acceleration

    character.move_mario(character.x_cor + character.hor_speed, character.y_cor)


def hor_decelerating_true(character: Mario):
    """
    Changes Mario's position, speed and acceleration when accelerating is true.
    """
    if 0 >= character.hor_acceleration > -1:
        character.hor_acceleration -= 0.1
    elif character.hor_acceleration > 0:
        character.hor_acceleration = -0.1

    if character.hor_acceleration < 0 and character.hor_speed > -7:
        character.hor_speed += character.hor_acceleration
    character.move_mario(character.x_cor + character.hor_speed, character.y_cor)


def update_background(display, background):
    """
    Update the background camera to follow Mario.
    """
    x, y = background.x_cor, background.y_cor
    display.blit(background.img, (x, y))


def no_vert_command(character, background):
    """
    Adjust the acceleration, speed and location the character and the background when no key is pressed.
    """
    change = 0.5
    # slowly bring the speed down or up to 0
    if character.speed >= 0.5 or character.speed <= -0.5:
        character.speed *= 0.5
    else:
        character.speed = 0

    # set background speed to character speed
    background.speed = character.speed
    # character.move_mario(character.x_cor, character.y_cor + character.speed)
    background.move_background(background.x_cor, background.y_cor + background.speed)


def no_hor_command(character, background):
    """
    Adjust the acceleration, speed and location the character and the background when no key is pressed.
    """
    change = 0.0
    if character.hor_speed >= 0.3 or character.hor_speed <= -0.3:
        character.hor_speed *= 0.5
    else:
        character.hor_speed = 0
    character.move_mario(character.x_cor + character.hor_speed, character.y_cor)


def choose_obstacle_coordinates(curr_ok_x: List[int], curr_ok_y: List[int]) -> Tuple[int, int]:
    """
    Generate obstacle coordinates.
    """
    x, y = choice(curr_ok_x), choice(curr_ok_y)
    curr_ok_y.remove(y)
    curr_ok_x.remove(x)
    curr_ok_x.extend(curr_ok_x)
    curr_ok_x.append(x)
    return (x, y)


def main():
    """
    The main game loop
    """

    # The eligible x and y coordinates
    eligible_x = [120, 240, 355]
    eligible_y = [30 - 750, 300 - 750, 620 - 720]

    # The current eligible x and y coordinates (make sure there is enough space for Mario)
    current_eligible_x = eligible_x[:]
    current_eligible_y = eligible_y[:]

    # Choose an coordinates for the obstacles
    obstacle1 = choose_obstacle_coordinates(current_eligible_x, current_eligible_y)
    obstacle2 = choose_obstacle_coordinates(current_eligible_x, current_eligible_y)
    obstacle3 = choose_obstacle_coordinates(current_eligible_x, current_eligible_y)

    obstacles = [Obstacle(obstacle1[0], obstacle1[1]),
                 Obstacle(obstacle2[0], obstacle2[1]),
                 Obstacle(obstacle3[0], obstacle3[1])]

    # Reset the currently eligible x and y coordinates
    current_eligible_x = eligible_x[:]
    current_eligible_y = eligible_y[:]

    pygame.init()

    # lane
    background = Background("/Users/tonynguyen/Desktop/ML/MachineLearning/evolution/lane3.jpeg", 0, -1000)

    # dimensions
    display_width = 550
    display_height = 750

    game_display = pygame.display.set_mode((display_width, display_height))  # game frame

    game_display.blit(background.img, (0, -1000))

    mario = Mario(266, 680, obstacles)

    def display_mario(x, y):
        """
        Display mario onto the game screen.
        """
        img = mario.image
        game_display.blit(img, (x, y))
        pygame.display.update()

    display_mario(mario.x_cor, mario.y_cor)

    pygame.display.update()
    pygame.display.set_caption("2D Mario Kart!")  # Game title

    clock = pygame.time.Clock()

    def update_game():
        """
        Update the game.
        """
        display_mario(mario.x_cor, mario.y_cor)
        pygame.display.update()
        clock.tick(150)

    running = True
    accelerating = False
    decelerating = False
    hor_accelerating = False
    hor_decelerating = False

    obstacle_generate_threshold = 860
    crash = False
    score = 0
    idle_time = 0

    while running:
        score += 1

        # Mario should not be idle (vertically) for too long (increase idle time for every iteration he is vertically
        # idle)
        if mario.speed == 0:
            idle_time += 1

        # reset Mario's idle time to 0 once he is moved (vertically)
        if mario.speed != 0 and idle_time > 0:
            idle_time = 0

        # Mario cannot crash to the sides
        if mario.x_cor <= 106.1421875 or mario.x_cor >= 402.54199218749966:
            crash = True

        # if Mario's idle time is >= 30, ends game through crash
        if idle_time >= 30:
            crash = True

        # display game over banner when crashed
        if crash:
            pygame.draw.rect(game_display, (255, 0, 0), (0, 150, 800, 200))
            game_display.blit(pygame.font.SysFont("Arial", 100).render("Game Over!", True, (0, 0, 0)), (80, 220))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    pass

        # if Mario is still alive
        else:
            # blit back to beginning to make the game go on forever
            if -410 <= background.y_cor <= -375:
                background.move_background(background.x_cor, -1000)
                update_background(game_display, background)

            # Mario accelerating vertically
            if accelerating:
                accelerating_true(mario, background)
                update_background(game_display, background)
                update_game()

            # Mario decelerating vertically
            if decelerating:
                decelerating_true(mario, background)
                update_background(game_display, background)
                update_game()

            # Mario is not accelerating nor decelerating but is still moving due to speed != 0
            elif not accelerating and not decelerating and mario.speed != 0:
                no_vert_command(mario, background)
                update_background(game_display, background)
                update_game()

            # Mario accelerating horizontally
            if hor_accelerating:
                hor_accelerating_true(mario)
                update_background(game_display, background)
                update_game()

            # Mario decelerating horizontally
            if hor_decelerating:
                hor_decelerating_true(mario)
                update_background(game_display, background)
                update_game()

            # Mario is not accelerating nor decelerating but is still moving horizontally due to hor_speed != 0
            elif not hor_accelerating and not hor_decelerating and mario.hor_speed != 0:
                no_hor_command(mario, background)
                update_background(game_display, background)
                update_game()

            # Note that decelerating and accelerating are relative: decelerating is accelerating in the negative
            # directions (left and down) while accelerating means accelerating in the positive directions (up and right)

            # Move the obstacles
            for obstacle in obstacles:
                obstacle.speed = background.speed
                obstacle.move()
                game_display.blit(obstacle.image, (obstacle.x, obstacle.y))
                pygame.display.update()
                # Remove an obstacle if it has been passed
                if obstacle.y > 750:
                    obstacles.pop(obstacles.index(obstacle))

            # Generate more obstacles as Mario travels through the map
            if background.travelled >= obstacle_generate_threshold:
                obstacle_generate_threshold += 860
                new_obstacle1 = choose_obstacle_coordinates(current_eligible_x, current_eligible_y)
                new_obstacle2 = choose_obstacle_coordinates(current_eligible_x, current_eligible_y)
                new_obstacle3 = choose_obstacle_coordinates(current_eligible_x, current_eligible_y)

                current_eligible_x = eligible_x[:]
                current_eligible_y = eligible_y[:]

                obstacles.append(Obstacle(new_obstacle1[0], new_obstacle1[1]))
                obstacles.append(Obstacle(new_obstacle2[0], new_obstacle2[1]))
                obstacles.append(Obstacle(new_obstacle3[0], new_obstacle3[1]))

            mario.update_obstacle_distance(obstacles)

            for obstacle in obstacles:
                if collision_between(mario, obstacle):
                    crash = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    key = event.unicode
                    # if key is w or up then accelerate
                    if key == "w" or key == "\uf700":
                        accelerating = True
                    elif key == "s" or key == "\uf701":
                        decelerating = True
                    elif key == "d" or key == "\uf703":
                        hor_accelerating = True
                    elif key == "a" or key == "\uf702":
                        hor_decelerating = True
                elif event.type == pygame.KEYUP:
                    key = event.key
                    # if key is 119 (w) or 273 (up) then stop accelerating
                    if key == 119 or key == 273:
                        accelerating = False
                    elif key == 115 or key == 274:
                        decelerating = False
                    elif key == 100 or key == 275:
                        hor_accelerating = False
                    elif key == 97 or key == 276:
                        hor_decelerating = False


if __name__ == "__main__":
    main()

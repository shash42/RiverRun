# Initialization
# pep8recheck final code
from config import *
import random
import math
import pygame
from pygame import mixer
pygame.init()
clock = pygame.time.Clock()
mixer.music.load(background_music)
# Global constants to be shifted to config

# Other globals
num_platforms = int(((screen_height - platform_width) / (platform_width +
                                                         river_width)))
moving_obstacle_speed = [0, 0, 0]
platforms = []
players = []
game_delay = 0
timer_started = 0
start_time = 0
passed_time = 0
running = True

# Sounds
failed_sound = mixer.Sound(fail_sound_file)
success_sound = mixer.Sound(succ_sound_file)

# Fonts
font_title = pygame.font.Font(font_titles, title_font_size)
font_space = pygame.font.Font(font_texts, space_font_size)
font_score = pygame.font.Font(font_texts, score_size)
font_round_over = pygame.font.Font(font_texts, round_over_size)
font_timer = pygame.font.Font(font_texts, timer_size)
font_game_over = pygame.font.Font(font_texts, game_over_size)
font_footer = pygame.font.Font(font_texts, footer_font_size)

# Load images
player1_image = pygame.image.load(player1_imgfile)
player2_image = pygame.image.load(player2_imgfile)
fixed_obstacle_image = []
moving_obstacle_image = []
hello_bg = pygame.image.load(bg_image)

# Set display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(game_caption)


def populate_fixed_obstacle_images():
    fixed_obstacle_image.append(pygame.image.load(fo1_image))
    fixed_obstacle_image.append(pygame.image.load(fo2_image))
    fixed_obstacle_image.append(pygame.image.load(fo3_image))


def populate_moving_obstacle_images():
    # 0 is fisher, 1 is crocodile, 2 is jet-ski
    moving_obstacle_image.append(pygame.image.load(mo1_image))
    moving_obstacle_image.append(pygame.image.load(mo2_image))
    moving_obstacle_image.append(pygame.image.load(mo3_image))


# The player class
class Player(pygame.sprite.Sprite):

    def __init__(self, init_x, init_y, p_image):
        super(Player, self).__init__()
        self.image = p_image
        self.rect = self.image.get_rect()
        self.rect.left = init_x
        self.rect.top = init_y
        self.speed = player_movement
        self.change_x = 0
        self.change_y = 0
        self.obstacle_score = 0
        self.time_taken = 0
        self.rounds_won = 0
        self.speed_factor = 1
        self.completed_last_round = 0

    def draw(self):
        screen.blit(self.image, self.rect)


class FixedObstacle(pygame.sprite.Sprite):

    # Design choice: Fixed obstacles are are on the platform
    def __init__(self, init_x1, init_x2, init_y, fo_image):
        super(FixedObstacle, self).__init__()
        self.image = fo_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # starting xpos is random in given section
        self.rect.left = random.randint(init_x1, init_x2)
        self.rect.top = init_y
        self.contributed_score = 0

    def draw(self):
        screen.blit(self.image, self.rect)


class MovingObstacle(pygame.sprite.Sprite):

    def __init__(self, init_x1, init_x2, init_y, mo_type):
        super(MovingObstacle, self).__init__()
        self.obs_type = mo_type
        self.image = moving_obstacle_image[self.obs_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = moving_obstacle_speed[self.obs_type]
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(init_x1, init_x2)
        self.rect.top = init_y
        self.contributed_score = 0

    def draw(self):
        screen.blit(self.image, self.rect)


class Platform():
    def create_fixed_obstacles(self):
        # iterating over sections which platform is divided into
        for j in range(0, int((screen_width / FO_placing)) + 1):
            # choose whether this section has an obstacle
            make_fo_here = random.randint(0, 3)
            if make_fo_here != 3:
                spritewidth = 32
                spriteheight = 32
                if make_fo_here == 2:
                    spritewidth = 91
                    spriteheight = 27
                # passing range for random selection of x
                curr_x1 = j * FO_placing
                curr_x2 = (j + 1) * FO_placing - spritewidth
                # y coordinate (center of platform)
                curr_y = self.upper_y + \
                    int(((platform_width - spriteheight) / 2))
                self.fixed_obstacles.append(
                    FixedObstacle(
                        curr_x1,
                        curr_x2,
                        curr_y,
                        fixed_obstacle_image[make_fo_here]))

    def create_moving_obstacles(self):
        # fisher(0) top, ski(1) middle, croc(2) lowest
        make_fisher_here = random.randint(0, moving_obstacle_chance[0])
        make_ski_here = random.randint(0, moving_obstacle_chance[1])
        make_croc_here = random.randint(0, moving_obstacle_chance[2])
        if make_fisher_here != 0:
            curr_x1 = 0
            curr_x2 = screen_width
            curr_y = self.lower_y
            self.moving_obstacles.append(MovingObstacle(curr_x1, curr_x2,
                                                        curr_y, 0))
        if make_ski_here != 0:
            curr_x1 = 0
            curr_x2 = screen_width
            curr_y = self.lower_y + 60
            self.moving_obstacles.append(MovingObstacle(curr_x1, curr_x2,
                                                        curr_y, 1))
        if make_croc_here != 0:
            curr_x1 = 0
            curr_x2 = screen_width
            curr_y = self.lower_y + 90
            self.moving_obstacles.append(MovingObstacle(curr_x1, curr_x2,
                                                        curr_y, 2))

    # upper has smaller coordinate as system is top to bottom
    def __init__(self, platform_no):  # no. is top to bottom
        self.upper_y = platform_no * (platform_width + river_width)
        self.lower_y = self.upper_y + platform_width
        self.river_y = self.lower_y + river_width
        self.fixed_obstacles = []
        self.moving_obstacles = []
        self.num = platform_no
        # Last platform has no river below it
        if platform_no == num_platforms:
            self.river_y = self.lower_y
        # Player starting platforms don't have obstacles
        if self.num != 0 and self.num != num_platforms:
            self.create_fixed_obstacles()
        # Last platform has no river below it
        if platform_no < num_platforms:
            self.create_moving_obstacles()

    def draw(self):
        pygame.draw.rect(
            screen,
            platform_color,
            (0,
             self.upper_y,
             screen_width,
             platform_width))

    def draw_fixed(self):
        for fo in self.fixed_obstacles:
            fo.draw()

    def draw_moving(self, player):
        for mo in self.moving_obstacles:
            if mo.obs_type == 2:
                to_draw = 0
                dist1_x = abs(player.rect.left - mo.rect.left)
                dist1_y = abs(player.rect.top - mo.rect.top)
                if dist1_x < croc_show_buffer[0] and dist1_y < croc_show_buffer[1]:
                    to_draw = 1
                if to_draw:
                    mo.draw()
            else:
                mo.draw()


def create_platforms():
    del platforms[:]
    for i in range(0, int(num_platforms) + 1):
        platforms.append(Platform(i))


def check_movements(event, player1, player2):

    global timer_started
    global start_time

    if event.type == pygame.KEYDOWN:
        # Pause game on pressing escape
        if event.key == pygame.K_ESCAPE:
            paused = 1
            while paused == 1:
                for event2 in pygame.event.get():
                    if event2.type == pygame.QUIT:
                        return False
                    if event2.type == pygame.KEYDOWN:
                        if event2.key == pygame.K_ESCAPE:
                            paused = 0
        # Timer starts on first keypress
        if timer_started == 0:
            timer_started = 1
            start_time = pygame.time.get_ticks()

        # Player 1 Movement
        if event.key == pygame.K_LEFT:
            player1.change_x -= player1.speed
        if event.key == pygame.K_RIGHT:
            player1.change_x += player1.speed
        if event.key == pygame.K_UP:
            player1.change_y -= player1.speed
        if event.key == pygame.K_DOWN:
            player1.change_y += player1.speed

        # Player 2 Movement
        if event.key == pygame.K_a:
            player2.change_x -= player2.speed
        if event.key == pygame.K_d:
            player2.change_x += player2.speed
        if event.key == pygame.K_w:
            player2.change_y -= player2.speed
        if event.key == pygame.K_s:
            player2.change_y += player2.speed

    if event.type == pygame.KEYUP:
        # Player 1 Movement
        if event.key == pygame.K_LEFT and player1.change_x < 0:
            player1.change_x = 0
        if event.key == pygame.K_RIGHT and player1.change_x > 0:
            player1.change_x = 0
        if event.key == pygame.K_UP and player1.change_y < 0:
            player1.change_y = 0
        if event.key == pygame.K_DOWN and player1.change_y > 0:
            player1.change_y = 0

        # Player 2 Movement
        if event.key == pygame.K_a and player2.change_x < 0:
            player2.change_x = 0
        if event.key == pygame.K_d and player2.change_x > 0:
            player2.change_x = 0
        if event.key == pygame.K_w and player2.change_y < 0:
            player2.change_y = 0
        if event.key == pygame.K_s and player2.change_y > 0:
            player2.change_y = 0
    return True


def update_movements(player1, player2):
    player1.rect.left += player1.change_x
    player1.rect.top += player1.change_y
    player2.rect.left += player2.change_x
    player2.rect.top += player2.change_y


def check_boundaries(player):
    if(player.rect.left > screen_width - 32):
        player.rect.left = screen_width - 32
    if(player.rect.left < 0):
        player.rect.left = 0
    if(player.rect.top > screen_height - 32):
        player.rect.top = screen_height - 32
    if(player.rect.top < 0):
        player.rect.top = 0


def check_collision(player):
    for platform in platforms:
        fixed_collides = pygame.sprite.spritecollide(
            player, platform.fixed_obstacles, False, pygame.sprite.collide_mask)
        moving_collides = pygame.sprite.spritecollide(
            player, platform.moving_obstacles, False, pygame.sprite.collide_mask)
        if len(fixed_collides):
            return True
        if len(moving_collides):
            return True
    return False


def half_round_over(success):
    mixer.music.stop()
    if success == 0:
        failed_sound.play()
        end_text = font_round_over.render(crash_message, True, (0, 0, 0))
    else:
        success_sound.play()
        end_text = font_round_over.render(cross_message, True, (0, 0, 0))
    text_x = int((screen_width - round_over_size) / 2) + round_over_shift[0]
    text_y = int((screen_height - round_over_size) / 2) + round_over_shift[1]
    screen.blit(end_text, (text_x, text_y))


def player_start(player, start_top):
    # Where to start
    if start_top == 0:
        player.rect.left = player1_start_x
        player.rect.top = player1_start_y
    else:
        player.rect.left = player2_start_x
        player.rect.top = player2_start_y
    # Update Speed
    # print(moving_obstacle_base_speed, player.speed_factor)
    for i in range(0, 3):
        moving_obstacle_speed[i] = moving_obstacle_base_speed[i] \
            * player.speed_factor

    # Scoring
    player.obstacle_score = 0


def check_completed(player, start_top):
    if start_top == 0:
        if player.rect.top <= platform_width - 32:
            return True
    if start_top == 1:
        if player.rect.top >= screen_height - platform_width:
            return True
    return False


def check_crossings(player, start_top):
    for platform in platforms:
        for fo in platform.fixed_obstacles:
            # An obstacle can contribute to score only once
            if not fo.contributed_score:
                if start_top and player.rect.top > fo.rect.top:
                    fo.contributed_score = 1
                    player.obstacle_score += fixed_obstacle_contribution
                elif start_top == 0 and player.rect.top < fo.rect.top:
                    fo.contributed_score = 1
                    player.obstacle_score += fixed_obstacle_contribution
        for mo in platform.moving_obstacles:
            # An obstacle can contribute to score only once
            if not mo.contributed_score:
                if start_top and player.rect.top > mo.rect.top:
                    mo.contributed_score = 1
                    player.obstacle_score += moving_obstacle_contribution
                elif start_top == 0 and player.rect.top < mo.rect.top:
                    mo.contributed_score = 1
                    player.obstacle_score += moving_obstacle_contribution


def display_score(player):
    score_text = font_score.render("Score: " + str(player.obstacle_score),
                                   True, screen_text_color)
    text_x = score_text_pos[0]
    text_y = score_text_pos[1]
    screen.blit(score_text, (text_x, text_y))


def display_time(passed_time):
    timer_text = font_timer.render("Timer: " + str(passed_time),
                                   True, screen_text_color)
    text_x = timer_text_pos[0]
    text_y = timer_text_pos[1]
    screen.blit(timer_text, (text_x, text_y))


def round_over(winner):
    if winner == 0:
        end_text = font_round_over.render(p1_win_text,
                                          True, screen_text_color)
    else:
        end_text = font_round_over.render(p2_win_text,
                                          True, screen_text_color)
    text_x = int((screen_width - round_over_size) / 2) + winner_shift[0]
    text_y = int((screen_height - round_over_size) / 2) + winner_shift[1]
    screen.blit(end_text, (text_x, text_y))


def update_winner(player1, player2):
    winner = player2
    # If both completed, one with less time wins
    if player1.completed_last_round and player2.completed_last_round:
        if player1.time_taken < player2.time_taken:
            winner = player1
    # If only one completed he wins
    elif player1.completed_last_round:
        winner = player1
    elif player2.completed_last_round:
        winner = player2
    # If both failed to complete one with more obstacle score wins
    else:
        if player1.obstacle_score > player2.obstacle_score:
            winner = player1
    winner.rounds_won += 1
    winner.speed_factor *= speed_multiplier
    if winner is player1:
        # print("player 1 wins")
        round_over(0)
    else:
        # print("player 2 wins")
        round_over(1)
    pygame.display.update()
    pygame.time.delay(round_delay)


def display_footer(round_num, show_right, prev_player):
    # On the left side of the footer
    past_round_info = "Round: " + str(round_num + 1) + "   |   P1 Wins: " + str(
        players[0].rounds_won) + "   P2 Wins: " + str(players[1].rounds_won)
    footer_left_text = font_footer.render(
        past_round_info, True, screen_text_color)
    text_x = footer_left_pos[0]
    text_y = footer_left_pos[1]
    screen.blit(footer_left_text, (text_x, text_y))
    # On the right side of the footer
    if show_right:
        prev_player_info = "Opponent score: " + \
            str(prev_player.obstacle_score) + "    Opponent Time: " + str(prev_player.time_taken)
        footer_right_text = font_footer.render(
            prev_player_info, True, screen_text_color)
        text_x = footer_right_pos[0]
        text_y = footer_right_pos[1]
        screen.blit(footer_right_text, (text_x, text_y))


def half_round(player, start_top, idx, round_num):
    # timing parameters
    global timer_started
    global start_time
    global passed_time
    game_delay = 0
    timer_started = 0
    start_time = 0
    passed_time = 0

    player_start(player, start_top)
    # print(moving_obstacle_speed)
    create_platforms()

    global running
    while running:
        screen.fill(river_color)
        # If quit is pressed half_round returns false
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            quit_check = check_movements(event, players[0], players[1])
            if not quit_check:
                return False
        update_movements(players[0], players[1])
        check_boundaries(player)

        collided = check_collision(player)
        check_crossings(player, start_top)

        passed_time = pygame.time.get_ticks() - start_time
        passed_time = int(passed_time / 100)
        if timer_started == 0:
            passed_time = 0
        player.time_taken = passed_time

        # Draw platforms
        for platform in platforms:
            for mo in platform.moving_obstacles:
                mo.rect.left += mo.speed
                mo.rect.left %= screen_width + 64
                # mo.rect.left -= 64

            platform.draw()
            platform.draw_fixed()
            platform.draw_moving(player)
        display_score(player)
        display_time(passed_time)
        display_footer(round_num, start_top, players[1 - idx])

        # Draw players
        player.draw()

        has_completed = check_completed(player, start_top)

        if collided:
            player.completed_last_round = 0
            half_round_over(0)
            game_delay = round_delay

        if has_completed:
            player.completed_last_round = 1
            half_round_over(1)
            game_delay = round_delay

        pygame.display.update()
        # Make pause if required
        pygame.time.delay(game_delay)

        # Here, if delay = 1000, half_round is over properly
        if game_delay == round_delay:
            if start_top == 1:
                # if whole round is over re-draw to show who won
                screen.fill(river_color)
                for platform in platforms:
                    platform.draw()
                    platform.draw_fixed()
                    platform.draw_moving(player)
                display_score(player)
                display_time(passed_time)
                display_footer(round_num, start_top, players[1 - idx])
                update_winner(players[0], players[1])
            return True

        clock.tick(ticks_per_loop)


def game_over():
    screen.fill(river_color)
    winner_text = p2_win_text
    if(players[0].rounds_won > players[1].rounds_won):
        winner_text = p1_win_text
    game_over_text = font_game_over.render("Game Over", True,
                                           screen_text_color)
    game_over_text2 = font_game_over.render(winner_text, True,
                                            screen_text_color)
    text_x = int((screen_width - game_over_size) / 2) + game_over_shift[0]
    text_y = int((screen_height - game_over_size) / 2) + game_over_shift[1]
    screen.blit(game_over_text, (text_x, text_y))
    screen.blit(game_over_text2, (text_x - int((game_over_size / 2)),
                                  text_y + 2 * game_over_size))
    pygame.display.update()
    pygame.time.delay(game_over_delay)


def hello():
    screen.blit(pygame.transform.smoothscale(
        hello_bg, (screen_width, screen_height)), (0, 0))
    title_text = font_title.render(game_caption, True, screen_text_color)
    space_text = font_space.render(space_caption, True, space_color)
    text_x = int((screen_width - title_font_size) / 2) + title_shift[0]
    text_y = int((screen_height - title_font_size) / 2) + title_shift[1]
    screen.blit(title_text, (text_x, text_y))
    screen.blit(space_text, (space_pos[0], space_pos[1]))
    pygame.display.update()
    temp_running = True
    while temp_running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                temp_running = False
            if event.type == pygame.QUIT:
                return False
    return True


def main():
    quit_check = hello()
    if not quit_check:
        return
    populate_fixed_obstacle_images()
    populate_moving_obstacle_images()
    players.append(Player(player1_start_x, player1_start_y, player1_image))
    players.append(Player(player2_start_x, player2_start_y, player2_image))
    rounds = 0  # No. of rounds completed
    mixer.music.play(-1)
    while rounds < num_of_rounds:
        mixer.music.play(-1)
        idx = rounds % 2    # Used to see which player starts at top
        half_1 = half_round(players[idx], 0, idx, rounds)
        if not half_1:
            return
        mixer.music.play(-1)
        idx = 1 - idx
        half_2 = half_round(players[idx], 1, idx, rounds)
        if not half_2:
            return
    #    print(players[0].rounds_won, players[1].rounds_won)
    #   print(players[0].speed_factor, players[1].speed_factor)
        rounds += 1
    game_over()


main()

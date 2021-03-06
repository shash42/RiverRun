screen_width = 1200
screen_height = 1000
player1_start_x = 584
player1_start_y = screen_height - 32
player2_start_x = 584
player2_start_y = 0
platform_width = 40
river_width = 120
FO_placing = 150  # section width for fixed obstacle placement
platform_color = (255, 234, 167)
river_color = (0, 206, 201)
player_movement = 1
moving_obstacle_base_speed = [-1, 2, -1.25]  # fisher-ski-croc (-1, 2, -1.25)
moving_obstacle_chance = [3, 3, 3]  # 1/x chance of not occuring
croc_show_buffer = [200, 100]  # x, y distance in which croc shows

# shift lists are for text placement
# some text positionings
title_font_size = 200
font_texts = 'astron boy.ttf'
font_titles = 'iomanoid.ttf'
title_shift = [-250, -150]
space_color = (255, 255, 255)
space_font_size = 50
space_pos = [400, screen_height - 100]
round_over_shift = [-100, -25]
winner_shift = [-200, -25]
round_over_size = 100
score_size = 40
score_text_pos = [2, 2]
timer_size = 40
timer_text_pos = [screen_width - 200, 2]
game_over_size = 120
game_over_shift = [-200, -150]
game_over_delay = 2000
footer_font_size = 26
footer_left_pos = [10, screen_height - footer_font_size - 10]
footer_right_pos = [screen_width - 410, screen_height - footer_font_size - 10]

# other display and game variables
screen_text_color = (0, 0, 0)
round_delay = 2000
num_of_rounds = 5
speed_multiplier = 1.2
fixed_obstacle_contribution = 5
moving_obstacle_contribution = 10
ticks_per_loop = 1000

# string constants
background_music = 'background.wav'
player1_imgfile = 'player1.png'
player2_imgfile = 'player2.png'
game_caption = "RiverRun"
bg_image = "riverrun.jpg"
fo1_image = "couple.png"
fo2_image = "palm.png"
fo3_image = "log.png"
mo1_image = "fisher.png"
mo2_image = "jet-ski.png"
mo3_image = "crocodile.png"
p1_win_text = "Player 1 Wins"
p2_win_text = "Player 2 Wins"
space_caption = "Press Space to Start"
fail_sound_file = "boing_x.wav"
succ_sound_file = "applause.wav"
crash_message = "Failed"
cross_message = "Success"

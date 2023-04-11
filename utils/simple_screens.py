#   This file contains the contents of the few screens in the game that are never changing, and only show certains values

import pygame
import time
import utils.functions as f

def screen_menu(screen, current_screen, color_text_background, screen_width, screen_height, small_font, medium_font, large_font, color_black, color_button):
    #   Draw title background
    pygame.draw.rect(screen, color_text_background, (0,0,screen_width,150))

    #   Draw title
    f.draw_text(screen, "Multiply & Subtract", (screen_width / 2), 75, large_font, color_black)

    #   Draw buttons
    #       Play button
    play_button = f.draw_button(screen, "Play", medium_font, (screen_width / 2), 275, color_black, color_button)
    #       Instructions button
    instructions_button = f.draw_button(screen, "Instructions", medium_font, (screen_width / 2), 350, color_black, color_button)

    #   Draw footer
    f.draw_text(screen, "Made by Kristaps Ālmanis 211RDB061", (screen_width / 2), 575, small_font, color_black)

    #   Check if button is clicked
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        mouse = pygame.mouse.get_pos()
        #   Switch to "Play" screen
        if play_button.collidepoint(mouse):
            time.sleep(0.2)
            current_screen = "Play"
        #   Switch to "Instructions" screen
        elif instructions_button.collidepoint(mouse):
            time.sleep(0.2)
            current_screen = "Instructions"

    return current_screen


def screen_instructions(screen, current_screen, color_text_background, screen_width, screen_height, small_font, medium_font, large_font, color_black, color_button):
    #   Draw title background
    pygame.draw.rect(screen, color_text_background, (0,0,screen_width,150))

    #   Draw title
    f.draw_text(screen, "Instructions", (screen_width / 2), 75, large_font, color_black)

    #   Draw instructions text
    f.draw_text(screen, "-  Each player starts with a score of 31.", 15, 200, small_font, color_black, True)
    f.draw_text(screen, "-  Players take turns of choosing two numbers from a pile of numbers.", 15, 220, small_font, color_black, True)
    f.draw_text(screen, "-  Both numbers are multiplied.", 15, 240, small_font, color_black, True)
    f.draw_text(screen, "-  The result is then subtracted from players score.", 15, 260, small_font, color_black, True)
    f.draw_text(screen, "-  If a player reaches a negative number, he automatically loses.", 15, 280, small_font, color_black, True)
    f.draw_text(screen, "-  Winner is the player who gets exactly 0.", 15, 300, small_font, color_black, True)
    f.draw_text(screen, "-  If there are no more numbers in the pile, and both players have positive, non zero scores, then the winner is whoever", 15, 320, small_font, color_black, True)
    f.draw_text(screen, "   has the score closest to zero.", 15, 340, small_font, color_black, True)

    #   Draw back button
    back_button = f.draw_button(screen, "Back", medium_font, 130, 550, color_black, color_button)

    #   Check if button is clicked
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        mouse = pygame.mouse.get_pos()
        #   Switch to "Menu" screen
        if back_button.collidepoint(mouse):
            time.sleep(0.2)
            current_screen = "Menu"

    return current_screen



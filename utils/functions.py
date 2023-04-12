#   This file contains helper functions for the game

import pygame
from collections import Counter
import random
import time

#   Function used to draw buttons
def draw_button(screen, string, font, x_coordinate, y_coordinate, text_color, button_color):
    button = pygame.Rect(0, 0, 200, 50)
    button.center = (x_coordinate, y_coordinate)
    text = font.render(string, True, text_color)
    text_rect = text.get_rect()
    text_rect.center = button.center
    pygame.draw.rect(screen, button_color, button)
    screen.blit(text, text_rect)

    return button


#   Function used to draw buttons containing numbers in the game
def draw_pile_button(screen, pile, nr, font, x_coordinate, y_coordinate, text_color, button_color):
    if len(pile) >= nr:
        button = pygame.Rect(0, 0, 30, 30)
        button.center = (x_coordinate, y_coordinate)
        text = font.render(str(pile[nr-1]), True, text_color)
        text_rect = text.get_rect()
        text_rect.center = button.center
        pygame.draw.rect(screen, button_color, button)
        screen.blit(text, text_rect)

        return button
    
    else:
        return None


#   Function used to draw text
def draw_text(screen, string, x_coordinate, y_coordinate, font, text_color, manual=False):
    text = font.render(str(string), True, text_color)
    if manual:
        screen.blit(text, (x_coordinate, y_coordinate))
    else:
        textRect = text.get_rect()
        textRect.center = (x_coordinate, y_coordinate)
        screen.blit(text, textRect)


#   Function to show player images
def draw_player(screen, name, type, x_coordinate, y_coordinate, font, text_color, img_index=None):
    if type == "human":
        player_img = pygame.image.load(f"assets/avatars/human{img_index}.png")
    elif type == "ai":
        player_img = pygame.image.load(f"assets/avatars/ai.png")

    player_img = pygame.transform.scale(player_img, (200, 200))
    screen.blit(player_img, (x_coordinate,y_coordinate))

    text = font.render(name, True, text_color)
    screen.blit(text, (x_coordinate+70,y_coordinate+220))


#   Function to generate a pile of numbers for the game
def generate_pile():
    pile = []
    for i in range(12):
        while True:
            rand = random.randrange(1,5)
            if Counter(pile)[rand] != 4:
                break
        pile.append(rand)

    return pile


#   Function to update the player chosen numbers on screen
def update_value(pile, first_multiplier, second_multiplier, nr):
    if first_multiplier == "":
        first_multiplier = pile[nr]
    elif second_multiplier == "":
        second_multiplier = pile[nr]

    return first_multiplier, second_multiplier


#   Function to check whether a button has been pressed in game
def check_game_button(button, button_pressed, mouse, first_multiplier, second_multiplier, pile, nr):
    if button and not button_pressed and button.collidepoint(mouse):
        time.sleep(0.2)
        first_multiplier, second_multiplier = update_value(pile, first_multiplier, second_multiplier, nr)
        button_pressed = True

    return button_pressed, first_multiplier, second_multiplier


#   Function to check whether the game has ended
def check_winner(player1_score, player2_score, pile):
    if player1_score == 0 or player2_score < 0:
        return "Player 1"
    if player2_score == 0 or player1_score < 0:
        return "Player 2"
    if len(pile) == 0:
        if player1_score < player2_score:
            return "Player 1"
        if player2_score < player1_score:
            return "Player 2"
        else:
            return "Tie"
        
    return None
import pygame
import sys
import random
import time

from utils.logic import game_state
import utils.functions as f
import utils.simple_screens as s

#   Initialize Pygame
pygame.init()

#   Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kristaps Ālmanis 211RDB061")

#   Fonts and colors
small_font = pygame.font.SysFont("assets/fonts/OpenSans-Regular.ttf", 20)
medium_font = pygame.font.SysFont("assets/fonts/OpenSans-Regular.ttf", 28)
large_font = pygame.font.SysFont("assets/fonts/OpenSans-Regular.ttf", 60)
color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_background = (200, 200, 200)
color_text_background = (75, 100, 115)
color_button = (75, 100, 200)

#   Setting default values for various variables
current_screen = "Menu"
player1_index = player2_index = turn = winner = depth = ai_move = first_button = second_button = third_button = fourth_button = fifth_button = sixth_button = seventh_button = eighth_button = ninth_button = tenth_button = eleventh_button = twelfth_button = None
first_button_pressed = second_button_pressed = third_button_pressed = fourth_button_pressed = fifth_button_pressed = sixth_button_pressed = seventh_button_pressed = eighth_button_pressed = ninth_button_pressed = tenth_button_pressed = eleventh_button_pressed = twelfth_button_pressed = False
start_score = 31

#   Game
while True:
    #   Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    #   Draw background
    screen.fill(color_background)

    #   Draw game screens
    #       Menu screen
    if current_screen == "Menu":
        current_screen = s.screen_menu(screen, current_screen, color_text_background, screen_width, screen_height, small_font, medium_font, large_font, color_black, color_button)

    #       Instructions screen
    elif current_screen == "Instructions":
        current_screen = s.screen_instructions(screen, current_screen, color_text_background, screen_width, screen_height, small_font, medium_font, large_font, color_black, color_button)
    
    #       Game mode choice screen
    elif current_screen == "Play":
        #   Draw title background
        title_background = pygame.draw.rect(screen, color_text_background, (0,0,screen_width,150))

        #   Draw title
        f.draw_text(screen, "Choose game mode", (screen_width / 2), 75, large_font, color_black)

        #   Draw buttons for choosing game mode
        #       2 player game mode choices
        f.draw_text(screen, "2 Players", (screen_width / 2), 225, medium_font, color_black)
        pvp_p1_button = f.draw_button(screen, "Player 1 starts", medium_font, (screen_width / 4), 225, color_black, color_button)
        pvp_p2_button = f.draw_button(screen, "Player 2 starts", medium_font, (screen_width / 4 * 3), 225, color_black, color_button)
        #       AI game mode choices
        f.draw_text(screen, "vs AI", (screen_width / 2), 400, medium_font, color_black)
        ai_p1_button = f.draw_button(screen, "You start", medium_font, (screen_width / 4), 400, color_black, color_button)
        ai_ai_button = f.draw_button(screen, "AI starts", medium_font, (screen_width / 4 * 3), 400, color_black, color_button)
        
        #   Back button
        back_button = f.draw_button(screen, "Back", medium_font, 130, 550, color_black, color_button)

        #   Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            #   Set up 2 player game if one of the buttons are pressed
            if pvp_p1_button.collidepoint(mouse) or pvp_p2_button.collidepoint(mouse):
                time.sleep(0.2)
                player1_index, player2_index = random.sample(range(1,7), 2)
                player1_score = player2_score = start_score
                pile = f.generate_pile()
                ai_move = None
                first_multiplier = second_multiplier = result = ""
                current_screen = "Game_2P"
                if pvp_p1_button.collidepoint(mouse):
                    turn = "Player 1"
                else:
                    turn = "Player 2"
            #   Set up AI game if one of the buttons are pressed
            elif ai_p1_button.collidepoint(mouse) or ai_ai_button.collidepoint(mouse):
                time.sleep(0.2)
                game_state.registry = []
                player1_index = random.randrange(1,7)
                player1_score = ai_score = start_score
                pile = f.generate_pile()
                if ai_p1_button.collidepoint(mouse):
                    root_state = game_state(player1_score, ai_score, pile, 1, "Player 1")
                    turn = "Player 1"
                else:
                    root_state = game_state(player1_score, ai_score, pile, 1, "AI")
                    turn = "AI"
                root_state.add_to_registry()
                root_state.set_mini_maxi_players()
                root_state.generate_tree()
                root_state.minimax_evaluation()
                depth = 1
                first_multiplier = second_multiplier = result = ""
                ai_move = None
                current_screen = "Game_AI"
            #   Switch back to "Menu" screen
            elif back_button.collidepoint(mouse):
                time.sleep(0.2)
                current_screen = "Menu"

    #   Main game screen
    elif current_screen == "Game_2P" or current_screen == "Game_AI":
        #   Draw background
        background = pygame.draw.rect(screen, color_text_background, (0,0,screen_width,screen_height/2))

        #   Draw player images and names
        f.draw_player(screen, "Player 1", "human", 20, 20, medium_font, color_black, player1_index)
        if current_screen == "Game_AI":
            f.draw_player(screen, "AI", "ai", screen_width - 230, 20, medium_font, color_black)
        else:
            f.draw_player(screen, "Player 2", "human", screen_width - 230, 20, medium_font, color_black, player2_index)

        #   Draw current score
        if current_screen == "Game_AI":
            f.draw_text(screen, f"{player1_score} : {ai_score}", screen_width/2, 165, large_font, color_black)
        else:
            f.draw_text(screen, f"{player1_score} : {player2_score}", screen_width/2, 165, large_font, color_black)

        #   Draw whose turn it is
        if current_screen == "Game_AI":
            if turn == "AI":
                f.draw_text(screen, "AI is thinking!", screen_width/2, 250, medium_font, color_black)
            else:
                f.draw_text(screen, "Your turn!", screen_width/2, 250, medium_font, color_black)
        else:
            f.draw_text(screen, f"{turn} turn!", screen_width/2, 250, medium_font, color_black)

        if ai_move:
            f.draw_text(screen, f"AI chose {ai_move[0]} and {ai_move[1]}", screen_width-130, 350, small_font, color_black)

        #   Draw the pile of numbers 
        if turn == "AI":
            first_button_pressed = second_button_pressed = third_button_pressed = fourth_button_pressed = fifth_button_pressed = sixth_button_pressed = seventh_button_pressed = eighth_button_pressed = ninth_button_pressed = tenth_button_pressed = eleventh_button_pressed = twelfth_button_pressed = True
        start_x = 225
        start_y = 500
        first_button = f.draw_pile_button(screen, pile, 1, medium_font, start_x+50, start_y, color_black, color_button)
        second_button = f.draw_pile_button(screen, pile, 2, medium_font, start_x+100, start_y, color_black, color_button)
        third_button = f.draw_pile_button(screen, pile, 3, medium_font, start_x+150, start_y, color_black, color_button)
        fourth_button = f.draw_pile_button(screen, pile, 4, medium_font, start_x+200, start_y, color_black, color_button)
        fifth_button = f.draw_pile_button(screen, pile, 5, medium_font, start_x+250, start_y, color_black, color_button)
        sixth_button = f.draw_pile_button(screen, pile, 6, medium_font, start_x+300, start_y, color_black, color_button)
        seventh_button = f.draw_pile_button(screen, pile, 7, medium_font, start_x+50, start_y+50, color_black, color_button)
        eighth_button = f.draw_pile_button(screen, pile, 8, medium_font, start_x+100, start_y+50, color_black, color_button)
        ninth_button = f.draw_pile_button(screen, pile, 9, medium_font, start_x+150, start_y+50, color_black, color_button)
        tenth_button = f.draw_pile_button(screen, pile, 10, medium_font, start_x+200, start_y+50, color_black, color_button)
        eleventh_button = f.draw_pile_button(screen, pile, 11, medium_font, start_x+250, start_y+50, color_black, color_button)
        twelfth_button = f.draw_pile_button(screen, pile, 12, medium_font, start_x+300, start_y+50, color_black, color_button)

        #   Pause when it is AIs turn, to help the other player follow the game
        if turn == "AI":
            pygame.display.flip()
            pygame.time.wait(1000)

        #   Draw the calculations area for players
        first_multiplier_background = pygame.draw.rect(screen, color_white, (300,350,50,60))
        f.draw_text(screen, "x", 355, 370, medium_font, color_black, True)
        second_multiplier_background = pygame.draw.rect(screen, color_white, (370,350,50,60))
        f.draw_text(screen, "=", 425, 358, large_font, color_black, True)
        result_background = pygame.draw.rect(screen, color_white, (455,350,70,60))

        #   Draw the numbers users press on
        f.draw_text(screen, first_multiplier, 313, 363, large_font, color_black, True)
        f.draw_text(screen, second_multiplier, 378, 363, large_font, color_black, True)

        #   Draw the result, if it exists
        if first_multiplier != "" and second_multiplier != "":
            result = first_multiplier * second_multiplier
        else:
            result = ""
        f.draw_text(screen, result, 463, 360, large_font, color_black, True)

        #   Draw reset and accept and home buttons if it is not AIs turn
        if turn != "AI":
            reset_button = f.draw_button(screen, "Reset", medium_font, 130, 550, color_black, color_button)
            accept_button = f.draw_button(screen, "Accept", medium_font, screen_width-130, 550, color_black, color_button)
            home_button = f.draw_button(screen, "Home", medium_font, 130, 350, color_black, color_button)
        #   If it is AIs turn, then AI makes a move
        elif turn == "AI":
            #   Find the exact current state in the generated game tree
            current_state = game_state(player1_score, ai_score, pile, depth, "AI")
            for state in game_state.registry:
                if state == current_state:
                    #   Find the best move to take
                    for p in state.children:
                        print(p)
                    print()
                    first_multiplier, second_multiplier = ai_move = state.ai_choose_move()
                    ai_score -= first_multiplier * second_multiplier
                    pile.remove(int(first_multiplier))
                    pile.remove(int(second_multiplier))
                    first_button_pressed = second_button_pressed = third_button_pressed = fourth_button_pressed = fifth_button_pressed = sixth_button_pressed = seventh_button_pressed = eighth_button_pressed = ninth_button_pressed = tenth_button_pressed = eleventh_button_pressed = twelfth_button_pressed = False
                    first_multiplier = second_multiplier = result = ""
                    depth += 1
                    turn = "Player 1"
                    winner = f.check_winner(player1_score, ai_score, pile)
                    if winner:
                        if current_screen == "Game_AI":
                            previous_screen = "Game_AI"
                        else:
                            previous_screen = "Game_2P"
                        current_screen = "End_game"
                    break
                

        #   Check and react accordingly if a button is pressed
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            #   Check if one of the game buttons is pressed
            first_button_pressed, first_multiplier, second_multiplier = f.check_game_button(first_button, first_button_pressed, mouse, first_multiplier, second_multiplier, pile, 0)
            second_button_pressed, first_multiplier, second_multiplier = f.check_game_button(second_button, second_button_pressed, mouse, first_multiplier, second_multiplier, pile, 1)
            third_button_pressed, first_multiplier, second_multiplier = f.check_game_button(third_button, third_button_pressed, mouse, first_multiplier, second_multiplier, pile, 2)
            fourth_button_pressed, first_multiplier, second_multiplier = f.check_game_button(fourth_button, fourth_button_pressed, mouse, first_multiplier, second_multiplier, pile, 3)
            fifth_button_pressed, first_multiplier, second_multiplier = f.check_game_button(fifth_button, fifth_button_pressed, mouse, first_multiplier, second_multiplier, pile, 4)
            sixth_button_pressed, first_multiplier, second_multiplier = f.check_game_button(sixth_button, sixth_button_pressed, mouse, first_multiplier, second_multiplier, pile, 5)
            seventh_button_pressed, first_multiplier, second_multiplier = f.check_game_button(seventh_button, seventh_button_pressed, mouse, first_multiplier, second_multiplier, pile, 6)
            eighth_button_pressed, first_multiplier, second_multiplier = f.check_game_button(eighth_button, eighth_button_pressed, mouse, first_multiplier, second_multiplier, pile, 7)
            ninth_button_pressed, first_multiplier, second_multiplier = f.check_game_button(ninth_button, ninth_button_pressed, mouse, first_multiplier, second_multiplier, pile, 8)
            tenth_button_pressed, first_multiplier, second_multiplier = f.check_game_button(tenth_button, tenth_button_pressed, mouse, first_multiplier, second_multiplier, pile, 9)
            eleventh_button_pressed, first_multiplier, second_multiplier = f.check_game_button(eleventh_button, eleventh_button_pressed, mouse, first_multiplier, second_multiplier, pile, 10)
            twelfth_button_pressed, first_multiplier, second_multiplier = f.check_game_button(twelfth_button, twelfth_button_pressed, mouse, first_multiplier, second_multiplier, pile, 11)
            #   If reset button is pressed, then delete user choices
            if reset_button.collidepoint(mouse):
                time.sleep(0.2)
                first_multiplier = second_multiplier = ""
                first_button_pressed = second_button_pressed = third_button_pressed = fourth_button_pressed = fifth_button_pressed = sixth_button_pressed = seventh_button_pressed = eighth_button_pressed = ninth_button_pressed = tenth_button_pressed = eleventh_button_pressed = twelfth_button_pressed = False
            #   If home button is pressed, then switch back to "Menu" screen
            if home_button.collidepoint(mouse):
                time.sleep(0.2)
                current_screen = "Menu"
            #   If accept button is pressed and numbers are chosen, then make move using chosen numbers
            if accept_button.collidepoint(mouse) and first_multiplier != "" and second_multiplier != "":
                time.sleep(0.2)
                pile.remove(int(first_multiplier))
                pile.remove(int(second_multiplier))
                first_button_pressed = second_button_pressed = third_button_pressed = fourth_button_pressed = fifth_button_pressed = sixth_button_pressed = seventh_button_pressed = eighth_button_pressed = ninth_button_pressed = tenth_button_pressed = eleventh_button_pressed = twelfth_button_pressed = False
                first_multiplier = second_multiplier = ""
                if turn == "Player 1":
                    if current_screen == "Game_AI":
                        turn = "AI"
                        depth += 1
                    else:
                        turn = "Player 2"
                    player1_score -= int(result)
                elif turn == "Player 2":
                    turn = "Player 1"
                    player2_score -= int(result)
                result = ""

                if current_screen == "Game_AI":
                    winner = f.check_winner(player1_score, ai_score, pile)
                else:
                    winner = f.check_winner(player1_score, player2_score, pile)

                if winner:
                    if current_screen == "Game_AI":
                        previous_screen = "Game_AI"
                    else:
                        previous_screen = "Game_2P"
                    current_screen = "End_game"



    elif current_screen == "End_game":
        #   Draw title background
        title_background = pygame.draw.rect(screen, color_text_background, (0,0,screen_width,150))

        #   Draw game result
        if winner == "Tie":
            f.draw_text(screen, "Tie game!", (screen_width / 2), 75, large_font, color_black)
        else:
            if previous_screen == "Game_AI":
                if winner == "Player 1":
                    f.draw_text(screen, "You win!", (screen_width / 2), 75, large_font, color_black)
                if winner == "Player 2":
                    f.draw_text(screen, "AI wins!", (screen_width / 2), 75, large_font, color_black)
            else:
                f.draw_text(screen, f"{winner} wins!", (screen_width / 2), 75, large_font, color_black)

        f.draw_text(screen, "End result:", screen_width/2, 300, medium_font, color_black)
        if previous_screen == "Game_AI":
            f.draw_text(screen, f"{player1_score} : {ai_score}", screen_width/2, 350, large_font, color_black)
        else:
            f.draw_text(screen, f"{player1_score} : {player2_score}", screen_width/2, 350, large_font, color_black)

        if winner == "Player 1":
            f.draw_player(screen, "WINNER", "human", 50, 175, medium_font, color_black, player1_index)
            f.draw_player(screen, "WINNER", "human", screen_width-250, 175, medium_font, color_black, player1_index)
        if winner == "Player 2":
            if previous_screen == "Game_AI":
                f.draw_player(screen, "WINNER", "ai", 50, 175, medium_font, color_black)
                f.draw_player(screen, "WINNER", "ai", screen_width-250, 175, medium_font, color_black)
            else:    
                f.draw_player(screen, "WINNER", "human", 50, 175, medium_font, color_black, player2_index)
                f.draw_player(screen, "WINNER", "human", screen_width-250, 175, medium_font, color_black, player2_index)

        home_button = f.draw_button(screen, "Home", medium_font, 130, 550, color_black, color_button)

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if home_button.collidepoint(mouse):
                time.sleep(0.2)
                current_screen = "Menu"


    pygame.display.flip()
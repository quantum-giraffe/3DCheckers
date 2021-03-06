import pygame
import Values as v
import StartScreen
from classChecker import *

global current_player

def Commands_processing():

    global done
    try:
        Commands_processing.step_started
    except:
        Commands_processing.step_started = False

    try:
        if Commands_processing.valids:
            pass
    except:
        Commands_processing.valids = [[], False]

    try:
        pos=Commands_processing.pos
        pos1=Commands_processing.pos1
    except:
        Commands_processing.pos=(0,0)
        Commands_processing.pos1=(0,0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            v.done = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                StartScreen.Menu(v.window, v.width, [v.KEY_CONTINUE, v.KEY_RESTART, v.KEY_EXIT]).menu()
        if not Commands_processing.step_started:
            if pygame.mouse.get_pressed()[0]:
                pos = (pygame.mouse.get_pos()[0] // (v.width // 8), pygame.mouse.get_pos()[1] // (v.width // 8))
                Commands_processing.pos = pos
                if  v.field_checkers[pos[0]][pos[1]]:
                    if  v.field_checkers[pos[0]][pos[1]][0].color == v.current_player:
                        Commands_processing.valids = v.field_checkers[pos[0]][pos[1]][0].valid_steps(v.field_checkers, v.current_player)
                        if Commands_processing.valids[0]:
                            Commands_processing.step_started=True
                            break

        while Commands_processing.step_started:
            flag=False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    v.done = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Commands_processing.valids[0] = []
                        Commands_processing.step_started=False
                        flag=True
                        StartScreen.Menu(v.window, v.width, [v.KEY_CONTINUE, v.KEY_RESTART, v.KEY_EXIT]).menu()
                        break
                if pygame.mouse.get_pressed()[0]:
                    pos1 = (pygame.mouse.get_pos()[0] // (v.width // 8), pygame.mouse.get_pos()[1] // (v.width // 8))
                    Commands_processing.pos1 = pos1
                    if pos1 == pos:
                        Commands_processing.step_started = False
                        Commands_processing.valids[0] = []
                        break
                    if Commands_processing.valids[0].count(pos1):
                        if v.field_checkers[pos[0]][pos[1]][0].step(pos1[0], pos1[1], v.field_checkers, v.current_player, v.count_checkers):
                            Commands_processing.pos = pos1
                            pos = Commands_processing.pos
                            Commands_processing.valids[0] = v.field_checkers[pos[0]][pos[1]][0].cut_steps(v.field_checkers)
                            flag=True
                            break
                        else:
                            v.current_player *= -1
                            Commands_processing.step_started = False
                            Commands_processing.valids[0] = []
            if flag:
                break
        break

    return Commands_processing.valids[0]

def win(window):
    pygame.draw.rect(window, (50, 100, 50), ((0, 0), (v.width, int(v.width // 2))))
    pygame.draw.rect(window, (150, 100, 150), ((0, int(v.width // 2)), (v.width, int(v.width // 2))))
    pygame.draw.rect(window, (250, 200, 00), ((0, int(v.width * 3 // 7)), (v.width, v.width * 1 // 7)))
    if v.count_checkers[0]==0:
        font_pos_win = (int(v.width // 6), int(v.width * 4 // 6))
        font_pos_def = (int(v.width  // 6), int(v.width // 6))
    else:
        font_pos_win = (int(v.width // 6), int(v.width // 6))
        font_pos_def = (int(v.width // 6), int(v.width * 4 // 6))
    Text = pygame.font.Font(None, 60).render('   ПОБЕДА', True, (250, 250, 250))
    window.blit(Text, font_pos_win)
    Text = pygame.font.Font(None, 60).render('ПОРАЖЕНИЕ', True, (250, 250, 250))
    window.blit(Text, font_pos_def)
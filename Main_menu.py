import pygame
import os

pygame.init()

def main_menu(Screen_Width, Screen_Height, background_image_path, Screen,dino_img,ground_img):
    background_image = pygame.image.load(background_image_path).convert()
    background_image = pygame.transform.smoothscale(background_image, (Screen_Width, Screen_Height))

    ground=pygame.transform.scale(pygame.image.load(ground_img), (1100,HEIGHT-500))


    dino= pygame.transform.scale(
    pygame.image.load(dino_img), (50, 50))

    button_width = 200
    button_height = 50
    button_color = (255, 22, 15) 
    button_hover_color = (254, 147, 36)
    small_font = pygame.font.Font(None, 24)

    is_sound_on = True

    while True:
        Screen.blit(background_image, (0, 0))
        Screen.blit(dino,((WIDTH/2)-20,HEIGHT/3))
        Screen.blit(ground,(0,HEIGHT-100))
        

        compete_ai_rect = pygame.Rect((Screen_Width/2)-100, 290, button_width, button_height)
        compete_ai = small_font.render("Compete with A.i", True, (255, 255, 255))
        compete_ai_text = compete_ai.get_rect(center=compete_ai_rect.center)

        Train_ai_rect = pygame.Rect((Screen_Width/2)-100, 360, button_width, button_height)
        Train_ai_sur = small_font.render("Train A.i", True, (255, 255, 255))
        Train_ai_text = Train_ai_sur.get_rect(center=Train_ai_rect.center)

        Play_alone_rect = pygame.Rect((Screen_Width/2)-100, 430, button_width, button_height)
        Play_alone_sur = small_font.render("Play yourself", True, (255, 255, 255))
        Play_alone_text = Play_alone_sur.get_rect(center=Play_alone_rect.center)

        quit_button_rect = pygame.Rect((Screen_Width/2)-100, 500, button_width, button_height)
        quit_text = small_font.render("Quit Game", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)

        mouse_pos = pygame.mouse.get_pos()
        for button_rect, button_text_rect in [
            (compete_ai_rect, compete_ai_text),
            (Train_ai_rect, Train_ai_text),
            (Play_alone_rect, Play_alone_text),
            (quit_button_rect, quit_text_rect)]:

            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(Screen, button_hover_color, button_rect)
            else:
                pygame.draw.rect(Screen, button_color, button_rect)

        Screen.blit(compete_ai, compete_ai_text)
        Screen.blit(Train_ai_sur, Train_ai_text)
        Screen.blit(Play_alone_sur, Play_alone_text)
        Screen.blit(quit_text, quit_text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if compete_ai_rect.collidepoint(mouse_pos):
                    print("Game start")
                elif Train_ai_rect.collidepoint(mouse_pos):
                    print("Train start")
                    is_sound_on = not is_sound_on
                elif Play_alone_rect.collidepoint(mouse_pos):
                    print("Play alone start")
                    is_sound_on = not is_sound_on
                elif quit_button_rect.collidepoint(mouse_pos):
                    print("Quit start")
                    pygame.quit()
                    return

if __name__ == '__main__':
    WIDTH = 1100
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    main_menu(WIDTH, HEIGHT, background_image_path=os.path.join(os.path.dirname(__file__), "bg.png"), Screen=screen,dino_img=os.path.join(os.path.dirname(__file__), "bird1.png"),ground_img=os.path.join(os.path.dirname(__file__), "ground.png"))

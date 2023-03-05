# Naef's Aim Trainer
# Game where circles randomly appear on screen and the aim
# is to click on as many circles as possible in 60 seconds
# A misclick results in a lower score

import pygame
import time
import random
import math
from pygame.time import Clock

# Color palette and fontx
init_color = (0, 0, 0)
button_text_color = (255, 255, 255)
text_color = (0, 0, 0)
highlight_text_color = (29, 28, 85)
our_colour = (255, 0, 0)
game_font = 'Assets/light_pixel-7.ttf'

import cv2
# main function
def main():
    # initialize pygame
    pygame.init()
    pygame.font.init()
    game = Game()
    game.play_game()
def face():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    # capture frames from a camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # loop runs if capturing has been initialized.
    while 1:

    	# reads frames from a camera
    	ret, img = cap.read()

    	# convert to gray scale of each frames
    	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    	# Detects faces of different sizes in the input image
    	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    	for (x,y,w,h) in faces:
    		# To draw a rectangle in a face
    		cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
    		roi_gray = gray[y:y+h, x:x+w]
    		roi_color = img[y:y+h, x:x+w]

    		eyes = eye_cascade.detectMultiScale(roi_gray)


    		# Detects eyes of different sizes in the input image
    		eyes = eye_cascade.detectMultiScale(roi_gray)
    		for (ex,ey,ew,eh) in eyes:
    			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,255),2)

            # To draw a rectangle in eyes

    	# Display an image in a window
    	cv2.imshow('img',img)

    	# Wait for Esc key to stop
    	k = cv2.waitKey(30) & 0xff
    	if k == 27:
    		break


    # Close the window
    cap.release()

    # De-allocate any associated memory usage
    cv2.destroyAllWindows()

class Game():

    def __init__(self):

        self.window_width = 720
        self.window_height = 680
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.window.fill(init_color)
        pygame.display.flip()
        pygame.display.set_caption("Rebooter's Aim Trainer")
    def play_game(self):

        self.clock = Clock()
        self.game_end = False
        self.active = False
        circle_x = random.randint(50, self.window_width - 50)
        circle_y = random.randint(120, self.window_height - 50)
        self.circle = [circle_x, circle_y]
        self.width_of_circle = random.randint(16,20)
        self.correct_click = 0
        self.total_click = 0
        self.sensitivity = 1
        self.crosshair_location = [self.window_width//2, self.window_height//2]
        self.text = ''
        self.input_box = pygame.draw.rect(self.window, text_color, (400, 300, 200, 75))
        self.back_button_box = pygame.draw.rect(self.window, init_color, (180, 500, 360, 75))

        self.main_menu()

    def aim_game(self):

        self.main_menu_check = False
        self.game_end = False
        self.correct_click = 0
        self.total_click = 0
        self.score = 0
        total_time = 5

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        start_time = pygame.time.get_ticks()
        while True:
            self.handle_events()
            seconds = (pygame.time.get_ticks() - start_time)//1000
            time_seconds = total_time - seconds
            self.window.fill(init_color)
            self.draw_game(time_seconds)
            if time_seconds <= 0:
                break
            self.clock.tick(60)
            pygame.display.update()
        self.end_game()


    def draw_time(self, time_seconds):
        time_font = pygame.font.Font(game_font, 50)
        textsurface = time_font.render(f'Time left: {time_seconds}', False, text_color)
        x_space = (pygame.display.get_surface().get_size()[0] - textsurface.get_width())//2
        self.window.blit(textsurface, (x_space, 25))

    def draw_game(self, time_seconds):
        game_background = pygame.image.load('Assets/GameBackground.png')
        self.window.blit(game_background, (0, 0))
        self.draw_time(time_seconds)
        game_ball = pygame.image.load('Assets/pixellball.png')
        game_ball_coords = [self.circle[0]-self.width_of_circle, self.circle[1]-self.width_of_circle]
        game_ball = pygame.transform.scale(game_ball, (2*self.width_of_circle, 2*self.width_of_circle))
        self.window.blit(game_ball, game_ball_coords)
        self.custom_crosshair()
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif self.active:
                    if event.key == pygame.K_RETURN:
                        try:
                            self.sensitivity = round(float(self.text), 2)
                        except:
                            self.sensitivity = 1
                        self.text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                elif event.key == pygame.K_r and self.game_end:
                    self.aim_game()
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONUP:
                if not self.game_end:
                    sq_x = (self.crosshair_location[0] - self.circle[0] + self.width_of_circle//2)**2
                    sq_y = (self.crosshair_location[1] - self.circle[1] + self.width_of_circle//2)**2
                    if math.sqrt(sq_x + sq_y) < self.width_of_circle + 5:
                        target_hit_sound = pygame.mixer.Sound('Assets/TargetHit.wav')
                        pygame.mixer.Sound.play(target_hit_sound)
                        self.correct_click += 1
                        self.score += 100
                        self.circle[0] = random.randint(50, self.window_width - 50)
                        self.circle[1] = random.randint(120, self.window_height - 50)
                        self.width_of_circle = random.randint(16,20)
                    self.total_click += 1

                if self.start_button.collidepoint(pygame.mouse.get_pos()) and self.main_menu_check:
                    click_sound = pygame.mixer.Sound('Assets/MouseClick.wav')
                    pygame.mixer.Sound.play(click_sound)
                    self.aim_game()
                if self.options_button.collidepoint(pygame.mouse.get_pos()) and self.main_menu_check:
                    click_sound = pygame.mixer.Sound('Assets/MouseClick.wav')
                    pygame.mixer.Sound.play(click_sound)
                    self.options_menu()
                if self.back_button_box.collidepoint(pygame.mouse.get_pos()) and self.options_menu_check:
                    click_sound = pygame.mixer.Sound('Assets/MouseClick.wav')
                    pygame.mixer.Sound.play(click_sound)
                    self.main_menu()
                if self.input_box.collidepoint(pygame.mouse.get_pos()) and self.options_menu_check:
                    click_sound = pygame.mixer.Sound('Assets/MouseClick.wav')
                    pygame.mixer.Sound.play(click_sound)
                    self.active = True
                else:
                    self.active = False

    def custom_crosshair(self):

        mouse_movement = pygame.mouse.get_rel()
        self.crosshair_location[0] += mouse_movement[0]* self.sensitivity
        self.crosshair_location[1] += mouse_movement[1]* self.sensitivity
        crosshair_image = pygame.image.load('Assets/crosshair.png')
        crosshair_image = pygame.transform.scale(crosshair_image, (20, 20))
        self.window.blit(crosshair_image, self.crosshair_location)

    def main_menu(self):

        self.main_menu_check = True
        self.options_menu_check = False

        while True:
            self.handle_events()
            self.start_button = pygame.draw.rect(self.window, init_color, (120, 400, 200, 75))
            self.options_button = pygame.draw.rect(self.window, init_color, (400, 400, 200, 75))

            background_image = pygame.image.load('Assets/MenuBackground.png')
            background_image = pygame.transform.scale(background_image, (720, 680))
            self.window.blit(background_image, (0,0))

            menu_font = pygame.font.Font(game_font, 45)
            menu_string ='Aim Trainer'
            textsurface = menu_font.render(menu_string, False, text_color)
            x_space = (pygame.display.get_surface().get_size()[0] - textsurface.get_width())//2
            self.window.blit(textsurface, (x_space, 150))

            menu_font = pygame.font.Font(game_font, 25)
            play_button_image = pygame.image.load('Assets/Button.png')
            play_button_image = pygame.transform.scale(play_button_image, (200, 75))
            self.window.blit(play_button_image, (120, 400))
            play_button_text = 'Start'
            textsurface = menu_font.render(play_button_text, False, button_text_color)
            x_space = 120 + (200 - textsurface.get_width())//2
            y_space = 400 + (80 - textsurface.get_height())//2
            self.window.blit(textsurface, (x_space, y_space))

            options_button_image = pygame.image.load('Assets/Button.png')
            options_button_image = pygame.transform.scale(options_button_image, (200, 75))
            self.window.blit(options_button_image, (400, 400))
            option_button_text = 'Options'
            textsurface = menu_font.render(option_button_text, False, button_text_color)
            x_space = 400 + (200 - textsurface.get_width())//2
            y_space = 400 + (80 - textsurface.get_height())//2
            self.window.blit(textsurface, (x_space, y_space))

            menu_font = pygame.font.Font(game_font, 20)
            menu_string ='*Press Escape at any time to leave the game*'
            textsurface = menu_font.render(menu_string, False, highlight_text_color)
            x_space = (pygame.display.get_surface().get_size()[0] - textsurface.get_width())//2
            self.window.blit(textsurface, (x_space, 580))

            pygame.display.update()

    def options_menu(self):

        self.options_menu_check = True
        self.main_menu_check = False
        box = ''

        while True:
            self.handle_events()
            self.back_button_box = pygame.draw.rect(self.window, init_color, (280, 500, 200, 75))
            self.input_box = pygame.draw.rect(self.window, (0,0,0), (420, 300, 200, 75))

            background_image = pygame.image.load('Assets/PlainBackground.png')
            background_image = pygame.transform.scale(background_image, (720, 680))
            self.window.blit(background_image, (0,0))

            option_menu_font = pygame.font.Font(game_font, 40)
            option_menu_string ='Options Menu'
            textsurface = option_menu_font.render(option_menu_string, False, text_color)
            x_space = (pygame.display.get_surface().get_size()[0] - textsurface.get_width())//2
            self.window.blit(textsurface, (x_space, 140))

            option_menu_font = pygame.font.Font(game_font, 30)
            input_text = "Sensitivity :"
            textsurface = option_menu_font.render(input_text, False, text_color)
            x_space = (360 - textsurface.get_width())
            self.window.blit(textsurface, (x_space, 320))

            if self.active:
                box = "SelectedBox"
            else:
                box = "UnselectedBox"

            options_button_image = pygame.image.load(f'Assets/{box}.png')
            options_button_image = pygame.transform.scale(options_button_image, (200, 75))
            self.window.blit(options_button_image, (410, 300))
            textsurface = option_menu_font.render(self.text, False, text_color)
            x_space = 410 + (200 - textsurface.get_width())//2
            y_space = 300 + (80 - textsurface.get_height())//2
            self.window.blit(textsurface, (x_space, y_space))

            options_button_image = pygame.image.load('Assets/Button.png')
            options_button_image = pygame.transform.scale(options_button_image, (200, 75))
            window_space = (self.window_width - 200)//2
            self.window.blit(options_button_image, (window_space, 500))
            option_button_text = 'Back'
            textsurface = option_menu_font.render(option_button_text, False, button_text_color)
            x_space = window_space + (200 - textsurface.get_width())//2
            y_space = 500 + (80 - textsurface.get_height())//2
            self.window.blit(textsurface, (x_space, y_space))

            pygame.display.update()
    def end_game(self):

        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        self.game_end = True

        game_end_sound = pygame.mixer.Sound('Assets/GameEnd.wav')
        pygame.mixer.Sound.play(game_end_sound)

        self.score -= (self.total_click - self.correct_click)*20

        while True:
            self.handle_events()

            background_image = pygame.image.load('Assets/PlainBackground.png')
            background_image = pygame.transform.scale(background_image, (720, 680))
            self.window.blit(background_image, (0,0))

            if self.total_click == 0:
                accuracy = 0
            else:
                accuracy = round((self.correct_click/self.total_click) * 100, 2)

            end_font = pygame.font.Font(game_font, 25)
            score_string = f'Score : '
            textsurface = end_font.render(score_string, False, text_color)
            x_space = (pygame.display.get_surface().get_size()[0] - textsurface.get_width())//2
            self.window.blit(textsurface, (x_space, 240))

            score_string = f'{self.score}'
            textsurface = end_font.render(score_string, False, our_colour)
            x_space = (pygame.display.get_surface().get_size()[0] - textsurface.get_width()) // 1.5
            self.window.blit(textsurface, (x_space, 240))

            accuracy_string = f'Accuracy : '
            textsurface = end_font.render(accuracy_string, False, text_color)
            x_space = (pygame.display.get_surface().get_size()[0] - textsurface.get_width())//2
            self.window.blit(textsurface, (x_space, 330))

            accuracy_string = f'{accuracy}%'
            textsurface = end_font.render(accuracy_string, False, our_colour)
            x_space = (pygame.display.get_surface().get_size()[0] - textsurface.get_width()) // 1.4
            self.window.blit(textsurface, (x_space, 330))

            restart_string = "Press \'R\' to restart"
            textsurface = end_font.render(restart_string, False, highlight_text_color)
            x_space = (pygame.display.get_surface().get_size()[0] - textsurface.get_width())//2
            self.window.blit(textsurface, (x_space, 520))

            pygame.display.update()

# call to main function
main()

import cv2
import pygame


screen_width = 600
screen_height = 800
fps = 60


cap = cv2.VideoCapture('assets/videos/Shuffle Board Stock Footage.mp4')
success, img = cap.read()
shape = img.shape[1::-1]
wn = pygame.display.set_mode(shape)
clock = pygame.time.Clock()

while success:
    clock.tick(24)
    success, img = cap.read()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            success = False
    try:
        wn.blit(pygame.image.frombuffer(img.tobytes(), shape, "BGR"), (0, 0))
    except:
        cap = cv2.VideoCapture('assets/videos/Shuffle Board Stock Footage.mp4')
        success, img = cap.read()

    pygame.display.update()

pygame.quit()


import pygame

def main(argv):
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Roflmao test')
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                break
        else:
            continue
        pygame.quit()
        return

__all__ = ["main"]

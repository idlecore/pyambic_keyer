import pygame, sys, array

BACKGROUND = (0, 0, 0)

pygame.mixer.pre_init(channels=1, buffer=1024)
pygame.init()
WINDOW = pygame.display.set_mode((400, 200))
pygame.display.set_icon(pygame.image.load('./img/Sprite-0001.png'))
pygame.display.set_caption("pyambic keyer")
fpsClock = pygame.time.Clock()

dit = False
dah = False

WPM = 15
# 1 WPM is equal to 1200 ms per element or each element is 5% of a minute.
DIT_LENGTH = int(1200/WPM)
DAH_LENGTH = DIT_LENGTH*3

ditClock = 0
dahClock = 0
clearClock = 0
alternationFlag = True
alternationPriority = 0

font = pygame.font.SysFont("Arial", 12)

class Note(pygame.mixer.Sound):

    def __init__(self, frequency, volume=.1):
        self.frequency = frequency
        pygame.mixer.Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(pygame.mixer.get_init()[0] / self.frequency))
        samples = array.array("h", [0] * period)
        amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
        for time in range(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples


def update_fps_counter():
    text = font.render(str(int(-1 if fpsClock.get_fps() in [float("-inf"), float("inf")] else fpsClock.get_fps())), 0, pygame.Color((255,0,0)))
    WINDOW.blit(text, (0,0))

def morse_loop():
    global ditClock, dahClock, clearClock, BACKGROUND, alternationFlag, alternationPriority
    BACKGROUND = (0,0,0)

    if pygame.time.get_ticks() - clearClock >= DIT_LENGTH:
        if dit and dah:
            if alternationPriority == 1:
                if alternationFlag:
                    ditClock = pygame.time.get_ticks()
                else:
                    dahClock = pygame.time.get_ticks()
            else:
                if alternationFlag:
                    dahClock = pygame.time.get_ticks()
                else:
                    ditClock = pygame.time.get_ticks()

            alternationFlag = not alternationFlag

        elif dit:
            ditClock = pygame.time.get_ticks()
        elif dah:
            dahClock = pygame.time.get_ticks()

    if pygame.time.get_ticks() - ditClock < DIT_LENGTH:
        BACKGROUND = (255, 255, 255)
        Note(140).play(-1, DIT_LENGTH, 0)
        clearClock = pygame.time.get_ticks()

    if pygame.time.get_ticks() - dahClock < DAH_LENGTH:
        BACKGROUND = (255, 255, 255)
        Note(140).play(-1, DAH_LENGTH, 0)
        clearClock = pygame.time.get_ticks()

    



def main():
    global dit, dah, ditClock, dahClock, alternationPriority, alternationFlag
    looping = True

    while looping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("left")
                    dit = True
                    if dah:
                        alternationPriority = 0
                elif event.key == pygame.K_RIGHT:
                    print("right")
                    dah = True
                    if dit:
                        alternationPriority = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    print("left up")
                    dit = False
                    alternationFlag = 0
                elif event.key == pygame.K_RIGHT:
                    print("right up")
                    dah = False
                    alternationFlag = 0
            

        morse_loop()
        WINDOW.fill(BACKGROUND)
        update_fps_counter()
        fpsClock.tick()
        pygame.display.flip()

    
    WINDOW.fill(BACKGROUND)
    pygame.display.update()

if __name__ == "__main__":
    main()
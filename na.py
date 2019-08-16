import pygame, math, sys, random

class pattern:

    def __init__(self, size, surface):
        self.x, self.y = size
        self.surface = surface
        self.point = (self.x//2, self.y//2)
        self.angle = math.pi

    def color(self):
        while True:
            RGBs = [0,0,0]
            for i in range(3):
                for j in range(255):
                    RGBs[i] = 255-j
                    RGBs[(i+1)%3] = j
                    yield RGBs

    def move(self, x, y, angle=None, length=5):
        angle = random.randint(1,4)*math.pi/2 if not angle else angle
        xt = math.cos(angle)*length
        yt = math.sin(angle)*length
        return int(x+xt), int(y-yt)

    def valid_move(self, x, y):
        if x>self.x or x<0:
            return False
        if y>self.y or y<0:
            return False
        return True

    def update(self):
        x, y = self.point
        while True:
            xt, yt = self.move(x, y)
            if self.valid_move(xt, yt):
                break
        self.point = (xt,yt)
        return (x,y), (xt,yt)


class main:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = (660, 660)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, 0, 32)
        self._running = True
        self.patterns = [pattern(self.size, self._display_surf) for i in range(50)]
        self.color = self.patterns[0].color()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        for pattern in self.patterns:
            self.point = pattern.update()
            pygame.draw.line(self._display_surf, next(self.color), self.point[0], self.point[1])
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = main()
    theApp.on_execute()

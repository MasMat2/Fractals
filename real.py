import pygame, sys, time


class console:
    def __init__(self):
        pass


class line:
    def __init__(self):
        self.lines = []
        self.top = None
        self.end = None
        self.observer = None

    def add_observer(self, observer):
        self.observer = observer

    def reset(self):
        self.top, self.end = None, None
        if self.observer:
            self.observer.on_notify(action="reset")

    def add_line(self, pos):
        if self.top == None:
            self.top = pos
            self.end = None
        else:
            self.end = pos
            self.lines += ((self.top, self.end),)
            self.reset()


class axis:
    def __init__(self, size, display):
        self.x, self.y = size[0], size[1]
        self.display = display
        self.cir = [
            ((1, 1), (100, 255, 0)),
            ((50, 4), (100, 255, 0)),
            ((7, -6), (100, 255, 0)),
            ((-5, -4), (100, 255, 0)),
        ]
        self.mode = "point"
        self.lines = line()
        self.lines.add_observer(self)

    def grid(self):
        for i in range(0, self.x, 20):
            pygame.draw.line(self.display, (100, 100, 100), (i, 0), (i, self.y))
        for i in range(0, self.y, 20):
            pygame.draw.line(self.display, (100, 100, 100), (0, i), (self.x, i))
        pygame.draw.line(
            self.display, (0, 255, 255), (self.x // 2, 0), (self.x // 2, self.y)
        )
        pygame.draw.line(
            self.display, (0, 255, 255), (0, self.y // 2), (self.x, self.y // 2)
        )

    def parse_input(self, pos):
        x = (pos[0] - self.x // 2) / 20
        y = (self.x // 2 - pos[1]) / 20
        return (x, y)

    def add_point(self, pos, color):
        self.cir.append((self.parse_input(pos), color))

    def draw(self):
        for i in self.cir:
            x = int(self.x // 2 + i[0][0] * 20)
            y = int(self.y // 2 - i[0][1] * 20)
            pygame.draw.circle(self.display, i[1], (x, y), 2)
        for m, l in self.lines.lines:
            pygame.draw.line(self.display, (255, 255, 255), m, l)

    def on_notify(self, pos=(-1, -1), action="draw"):
        if action == "draw":
            if self.mode == "point":
                self.add_point(pos, (100, 255, 0))
            if self.mode == "line":
                self.add_point(pos, (60, 255, 255))
                self.lines.add_line(pos)
        if action == "reset":
            for i in range(len(self.cir) - 1, 0, -1):
                if self.cir[-1][1] != (100, 255, 0):
                    self.cir.remove(self.cir[-1])
                else:
                    break


class main:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = (600, 600)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, 0, 32)
        self._running = True
        self.axis = axis(self.size, self._display_surf)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                self.axis.mode = "line"
            if event.key == pygame.K_PERIOD:
                self.axis.mode = "point"
                self.axis.lines.reset()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.axis.on_notify(pygame.mouse.get_pos())

    def on_loop(self):
        self._display_surf.fill((0, 0, 0))
        self.axis.grid()

    def on_render(self):
        self.axis.draw()
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

import pygame, sys, time


class axis:
    def __init__(self, size, display):
        self.x, self.y = size[0], size[1]
        self.display = display

    def draw(self):
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


class lines:
    def __init__(self, size, surface):
        self.lines = []
        self.point = (-1, -1)

        self.x, self.y = size[0], size[1]
        self.display = surface

        self.top, self.end = None, None

    def reset(self):
        self.top, self.end = None, None
        self.point = (-1, -1)

    def add_line(self, pos):
        if self.top == None:
            self.top = pos
            self.end = None
            self.point = pos

        else:
            self.end = pos
            self.lines += ((self.top, self.end),)
            self.reset()

    def draw(self):
        pygame.draw.circle(self.display, (0, 0, 255), self.point, 2)
        for m, l in self.lines:
            pygame.draw.line(self.display, (255, 255, 255), m, l)


class points:
    def __init__(self, size, surface):
        self.x, self.y = size[0], size[1]
        self.display = surface
        self.cir = []

    def add_point(self, pos):
        self.cir.append(pos)

    def draw(self):
        for i in self.cir:
            pygame.draw.circle(self.display, (0, 255, 100), i, 2)


class console:
    def __init__(self, size, surface):
        self.x, self.y = size[0], size[1]
        self.surface = surface

    def draw(self):
        pygame.font.init()
        font = pygame.font.SysFont("Eurostile Normal", 30)
        text = font.render("GeeksForGeeks", True, (0, 0, 255))
        textRect = text.get_rect()
        textRect.center = (self.x - 80, 20)
        self.surface.blit(text, textRect)

class function:
    def __init__(self):
        self.fx = 'x^2'
        for x in range(10):
            print(exec(self.fx))


class application:
    def __init__(self, size, surface):
        self.x, self.y = size
        self.surface = surface
        self.mode = "point"

        self.axis = axis(size, self.surface)
        self.lines = lines(size, self.surface)
        self.points = points(size, self.surface)
        self.console = console(size, self.surface)

    def parse_input(self, pos):
        x = (pos[0] - self.x // 2) / 20
        y = (self.x // 2 - pos[1]) / 20
        return (x, y)

    def ch_mode(self, mode="point"):
        if mode in ["point", "line"]:
            self.mode = mode
        self.reset_all()

    def reset_all(self):
        self.lines.reset()

    def draw(self):
        self.axis.draw()
        self.lines.draw()
        self.points.draw()
        self.console.draw()

    def on_notify(self, pos=(-1, -1), action="draw"):
        if action == "draw":
            if self.mode == "point":
                self.points.add_point(pos)
            if self.mode == "line":
                self.lines.add_line(pos)


class main:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = (600, 600)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, 0, 32)
        self._running = True
        self.application = application(self.size, self._display_surf)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                self.application.ch_mode("line")
            if event.key == pygame.K_PERIOD:
                self.application.ch_mode("point")
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.application.on_notify(pygame.mouse.get_pos())

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.application.draw()
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

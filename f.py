import pygame, sys, time


class fractal:
    def __init__(self, size, display):
        self.size = size
        self.traing = []
        self.display = display
        x = self.size[0]
        y = self.size[1]
        self.a = (
            (3 * x // 10, 11 * y // 20),
            (7 * x // 10, 11 * y // 20),
            (x // 2, 9 * y // 10),
        )
        self.b = (
            (1 * x // 10, 9 * y // 10),
            (9 * x // 10, 9 * y // 10),
            (x // 2, 2 * y // 10),
        )

    def recur_triangle(self, triangle):
        left, right, bott = triangle
        lenght_x, length_y = (abs(left[0] - bott[0]) // 2, abs(left[1] - bott[1]) // 4)
        more = [[], [], []]
        for i in range(3):
            x = (triangle[i][0] + triangle[(i + 1) % 3][0]) // 2
            y = (triangle[i][1] + triangle[(i + 1) % 3][1]) // 2
            if i == 0:
                more[i] = (
                    (x - lenght_x, y - length_y * 2),
                    (x + lenght_x, y - length_y * 2),
                    (x, y),
                )
            elif i == 1:
                more[i] = (
                    (x, y),
                    (x + lenght_x * 2, y),
                    (x + lenght_x, y + length_y * 2),
                )
            else:
                more[i] = (
                    (x - lenght_x * 2, y),
                    (x, y),
                    (x - lenght_x, y + length_y * 2),
                )
        return more

    def geta(self, triangles):
        new = []
        for triangle in triangles:
            t = self.recur_triangle(triangle)
            new += t
        return new

    def fractal_iteration(self):
        triangles = [self.a]
        for i in range(10):
            triangles = self.geta(triangles)
            yield triangles


class main:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = (512, 512)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, 0, 32)
        self._running = True
        self.fractal1 = fractal(self.size, self._display_surf)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self._display_surf.fill((0, 0, 0))
        pygame.draw.polygon(self._display_surf, (0, 255, 255), self.fractal1.b)
        pygame.draw.polygon(self._display_surf, (0, 0, 0), self.fractal1.a)
        self.fract = self.fractal1.fractal_iteration()

    def on_render(self):
        try:
            tr = next(self.fract)
        except:
            fract = self.fractal1.fractal_iteration()
            tr = next(fract)
        for i in tr:
            pygame.draw.polygon(self._display_surf, (0, 0, 0), i)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        self.on_loop()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
            time.sleep(2)
        self.on_cleanup()


if __name__ == "__main__":
    theApp = main()
    theApp.on_execute()

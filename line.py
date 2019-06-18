import pygame, math

class line:
    def __init__(self, num_points, size):
        self.x = size[0]
        self.y = size[1]
        self.num_points = num_points
        spacing = (self.x//2)//(self.num_points)
        print(spacing)
        self.points = [(i, 0) for i in range(0, self.x//2, spacing)]
        self.angle = math.pi/360

    def move(self):
        self.drawn_points = []
        for i in range(self.num_points):
            point = self.points[i]
            angle = math.pi*i/(30*self.num_points)
            y = point[1]*math.cos(angle)+point[0]*math.sin(angle)
            x = point[0]*math.cos(angle)-point[1]*math.sin(angle)
            self.points[i] = (x,y)
            self.drawn_points.append((x+self.x//2, y+self.y//2))
        return self.drawn_points


class main:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = (512, 512)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, 0, 32)
        self._running = True
        self.line = line(32, self.size)
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self.points = self.line.move()

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        pygame.draw.lines(self._display_surf, (0,0,255), False, self.points)
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

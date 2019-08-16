import pygame, sys, math

class observer:
    def __init__(self):
        self.observer_list = []

    def add(self, objs):
        self.observer_list += objs

    def notify(self, pos):
        for observer in self.observer_list:
            d = observer.on_notify(pos)
            if d: return d

        return None


class slider:
    def __init__(self, pos, name, tree):
        self.x, self.y = pos
        self.height = 200
        self.name = name
        self.rect_width, self.rect_height = 20, 10
        self.slide = pygame.Rect((self.x-10,self.y+self.height/2-self.rect_height/2),(self.rect_width, self.rect_height))
        self.degrees = math.degrees(math.pi*(self.slide.y - self.y+self.rect_height/2)/(self.height))
        self.trees = tree

    def on_notify(self, pos):
        if (abs(pos[0]-self.x)<20) and (self.y<pos[1] and (self.y+self.height> pos[1])):
            self.slide.move_ip(0, pos[1]-self.slide.y)
            self.degrees = math.degrees(math.pi*(self.slide.y - self.y+self.rect_height/2)/(self.height))
            if self.name == "teta1": return (self.trees.teta[0], -math.radians(self.degrees))
            else :return (math.radians(self.degrees),self.trees.teta[1])
        return None


    def draw(self, surface):
        myfont = pygame.font.SysFont("", 15)
        textsurface = myfont.render(
            f"{self.name}  {round(self.degrees,2)}", False, (0,0,0)
        )
        textRect = textsurface.get_rect()
        textRect.center = (self.x, self.y-10)
        surface.blit(textsurface, textRect)

        pygame.draw.line(surface, (0,0,0), (self.x, self.y), (self.x, self.y+self.height), 2)
        pygame.draw.rect(surface, (0,0,110), self.slide)


class tree:
    def __init__(self, size, k, teta):
        self.w, self.h = size
        self.lenght = 100
        self.k = k
        self.teta = teta
        self.max = 15

    def update(self, teta):
        if teta:
            self.teta = teta

    def draw(self, surface, line=None, angle=math.pi/2, it=1):
        if not line: line = [(self.w/2, self.h), (self.w/2, self.h*3/4)]
        if it > self.max: return 0
        if it> 7*self.max//10: pygame.draw.line(surface, (71,148,71),line[0], line[1])
        else: pygame.draw.line(surface, (102,51,0),line[0], line[1])

        for i in range(2):
            x = self.lenght*(self.k[i]**it)*math.cos(angle + self.teta[i]) + line[-1][0]
            y = -self.lenght*(self.k[i]**it)*math.sin(angle + self.teta[i]) + line[-1][1]
            self.draw(surface,[line[-1], (x,y)], angle+self.teta[i], it+1)


class main:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = (600, 500)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, 0 , 32)
        self._running = True
        self.tree = tree(self.size, [0.65, 0.75], [math.radians(20), -math.radians(10)])
        self.sliders = [slider((490, 50), "teta1", self.tree), slider((560, 50), "teta2", self.tree)]
        self.observers = observer()
        self.observers.add(self.sliders)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            degrees = self.observers.notify(pygame.mouse.get_pos())
            self.tree.update(degrees)
            self.on_loop()

    def on_loop(self):
        self._display_surf.fill((255,255,255))
        self.tree.draw(self._display_surf)
        for slider in self.sliders:
            slider.draw(self._display_surf)
        pygame.display.update()

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        self.on_loop()
        while ( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    theApp = main()
    theApp.on_execute()

import pygame
import random
import numpy as np

# try to replicate this https://www.reddit.com/r/pygame/comments/ipz0l5/proper_ray_casting_in_pygame/

class fakeline:
    # debug and to store data
    # not meant for users to see normally
    # press q to see
    def __init__(self,startpos = pygame.Vector2(0,0),endpos = pygame.Vector2(0,0),x=1,y=1):
        self.startpos = startpos
        self.endpos = endpos
        self.x=x
        self.y=y
    def get_startpos(self):
        return self.startpos
    def get_endpos(self):
        return self.endpos

class clippedRects:
    def __init__(self,rect_idx, dist):
        self.rect_idx = rect_idx
        self.dist = dist
    def __repr__(self):
        # lambda functions and debug print purposes
        # call with print(list that contains this obj)
        return repr({'idx': self.rect_idx,'dist':self.dist})
    def getidx(self):
        return self.rect_idx
    def getdist(self):
        return self.dist   

def rand_rects():
    rects = []
    for _ in range(random.randint(5,5)):
        x = random.randint(0,screen_Wdith)
        y = random.randint(0,screen_height)
        w = random.randint(50,300)
        h = w
        rects.append(pygame.Rect(x,y,w,h))
    return rects

def draw_text(text, pos):
    img = font.render(text, True, "BLACK")
    screen.blit(img, pos)

def draw_rects(rects):
    for idx, rec in enumerate(rects):
        pygame.draw.rect(screen,"gray",rec)
        # labels for rectangles
        draw_text("Rect: "+str(idx),rec.topleft)

def main_loop():
    running = True
    debug = False
    rects = rand_rects()
    while running:
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")
        debugScreen = pygame.surface.Surface(size=(screen_Wdith,screen_height))
        draw_rects(rects)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    # press q for debug
                    if debug:
                        debug = False
                    else:
                        debug = True
                if keys[pygame.K_r]:
                    # press r to reset
                    main_loop()
            if event.type == pygame.MOUSEMOTION:
            # if event.type == pygame.mouse.:
                # if pygame.mouse.get_pressed()[0]:
                if pygame.mouse.get_focused():
                    mouse_pos = pygame.mouse.get_pos()
                    num_of_bisection = 4
                    lines = []
                    lines_data = []
                    # radius=np.sqrt((screen_Wdith-mouse_pos[0])**2 + (screen_height-mouse_pos[1])**2)
                    radius=np.sqrt((screen_Wdith)**2 + (screen_height)**2)
                    # theta = np.linspace(0, 2*np.pi,num_of_lines,endpoint=False)*6
                    theta = np.linspace(0, 2*np.pi,num_of_lines,endpoint=False)
                    xx = mouse_pos[0] + (radius * np.cos(theta))
                    yy = mouse_pos[1] - (radius * np.sin(theta))
                    # xx=np.clip(xx,0,screen_Wdith)
                    # yy=np.clip(yy,0,screen_height)
                    # for x in range(int(100)):
                    for x in range(int(num_of_lines)):
                        """
                            basic circle equation
                            (endx - startx)^2 + (endy-starty)^2 = r^2
                            r = radius

                            # getting radius
                            r = euclidean dist between start coords and end coords
                            r = sqrt( ( (endx - startx)^2 + (endy-starty)^2) )

                            # getting the angle
                            go through each angle from 0 to 2pi
                            theta = np.linspace(0, 2*np.pi, num_of_lines)

                            # getting the next end points
                            endx = startx + (r * np.cos(theta))
                            endy = starty - (r * np.sin(theta)) 
                            *** note that endy needs to be subtracted because the y-coords increases as we move down
                            *** unlike conventional cartisean planes where y-coords decreases as we move down
                        """
                        if debug:
                            line = pygame.draw.line(screen,(250,100,0,1),mouse_pos,(xx[x],yy[x]))
                        else:
                            line = pygame.draw.line(debugScreen,(250,100,0,1),mouse_pos,(xx[x],yy[x]))
                        lines.append(line)
                        lines_data.append(fakeline(mouse_pos,(xx[x],yy[x])))
                    # rect to line
                    rtl = dict()
                    for idx, line in enumerate(lines):
                        # what are all the collisions for this current line?
                        clipped_list = []
                        all_collision = line.collidelistall(rects)
                        # if collision exists
                        if all_collision:
                            line_origin = lines_data[idx].get_startpos()
                            line_end = lines_data[idx].get_endpos()
                            vectorized_origin = pygame.math.Vector2(line_origin)
                            
                            for curr_rec in all_collision:
                                curr_recx = rects[curr_rec].centerx
                                curr_recy = rects[curr_rec].centery
                                dist = vectorized_origin.distance_to(pygame.Vector2(curr_recx,curr_recy))
                                # print("rect ",x)
                                # print("distance to", dist)
                                if debug:
                                    pygame.draw.line(screen,"yellow",line_origin,(curr_recx,curr_recy),5)

                                clipped = clippedRects(curr_rec,dist)
                                clipped_list.append(clipped)

                        if clipped_list:
                            closest_to_line = min(clipped_list, key=lambda x: x.getdist())
                            closest_idx = closest_to_line.getidx()
                            # print("try to see if min works on list of objs", closest_to_line)
                            collided = rects[closest_idx].clipline(line_origin,line_end)
                            # collided is a tuple of (x,y) coords
                            if collided:
                                pygame.draw.line(screen,"green",line_origin,collided[0],2)
                                if closest_idx not in rtl:
                                    rtl[closest_idx] = []
                                # dict keeps closest {rect_id: (x,y)}
                                rtl[closest_idx].append(collided[0])
                    
                    # highlights rectangles in blue that are hit with line
                    for x in rtl.keys():
                        if len(rtl[x]) > 1:
                            pygame.draw.lines(screen,"blue",False,rtl[x],5)
                        else:
                            pygame.draw.line(screen,"blue",rtl[x][0],rtl[x][0],5)

            pygame.display.update()
    # pygame.QUIT event means the user clicked X to close your window
    pygame.quit()

# static variables
pygame.init()
screen_Wdith = 1280
screen_height= 720
screen = pygame.display.set_mode((screen_Wdith,screen_height))
num_of_lines = 360
fraction = 3
frac_win_size_x = int((pygame.display.get_window_size()[0]) / fraction)
frac_win_size_y = int((pygame.display.get_window_size()[1]) / fraction)
font = pygame.font.Font(None,24)

# call main loop
main_loop()

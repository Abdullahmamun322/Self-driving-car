import pygame
import heapq

pygame.init()
window = pygame.display.set_mode((1200, 400))
track = pygame.image.load("track9.png")
car = pygame.image.load("tesla.png")
car = pygame.transform.scale(car, (30, 60))

car_x, car_y = 153, 300
goal = (1050, 50)  
grid_size = 30  

# A* Algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
def a_star_search(start, goal, grid):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  
            neighbor = (current[0] + dx, current[1] + dy)
            if grid.get(neighbor, 255) == 0: 
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return [] 
def create_grid(surface):
    grid = {}
    for x in range(0, surface.get_width(), grid_size):
        for y in range(0, surface.get_height(), grid_size):
            color = surface.get_at((x + grid_size // 2, y + grid_size // 2))[0]
            grid[(x // grid_size, y // grid_size)] = color
    return grid


grid = create_grid(track)
start = (car_x // grid_size, car_y // grid_size)
goal = (goal[0] // grid_size, goal[1] // grid_size)
path = a_star_search(start, goal, grid)

drive = True
clock = pygame.time.Clock()
path_index = 0

while drive:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            drive = False

    if path_index < len(path):
        target = path[path_index]
        target_x = target[0] * grid_size
        target_y = target[1] * grid_size

        if abs(car_x - target_x) < 2 and abs(car_y - target_y) < 2:
            path_index += 1
        else:
            if car_x < target_x:
                car_x += 2
            elif car_x > target_x:
                car_x -= 2
            if car_y < target_y:
                car_y += 2
            elif car_y > target_y:
                car_y -= 2

    window.blit(track, (0, 0))
    window.blit(car, (car_x, car_y))
    pygame.display.update()

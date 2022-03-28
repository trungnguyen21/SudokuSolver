import pygame
import requests
import buttons

difficulty = 'easy'

WIDTH = 550
background_color = (255,250,250)
original_color = (52, 34, 50)
buffer = 5 

response = requests.get(f"https://sugoku.herokuapp.com/board?difficulty={difficulty}")
grid = response.json()['board']
grid_original = [grid[x][y] for y in range(len(grid[0])) for x in range(len(grid))]

def possible(number):
    if number == 0:
        return True
    return False

def check_valid(position, number):
    #check if the number contained in the row
    for i in range(0, len(grid[0])):
        if grid[position[0]][i] == number:
            return False

    #check if the number contained in the column
    for i in range(0, len(grid[0])):
        if grid[i][position[1]] == number:
            return False
    
    #check if the number contained in the square
    x_pos = (position[0] // 3) * 3
    y_pos = (position[1] // 3) * 3

    for i in range(0, 3):
        for j in range(0, 3):
            if grid[x_pos+i][y_pos+j] == number:
                return False
    
    #else
    return True

#check if the puzzle is solved
done = 0
time = 15 #increase to see slo-mo
def solve(win):
    font = pygame.font.SysFont('Montseratt', 35)    
    for i in range(0, len(grid[0])):
        for j in range(len(grid[0])):
            if possible(grid[i][j]):
                for number in range(1, 10):
                    if check_valid((i, j), number):
                        grid[i][j] = number
                        value = font.render(str(number), True, (77, 245, 82))
                        win.blit(value, ((j + 1) * 50 + 20, (i + 1) * 50 + 15))
                        pygame.display.update()
                        pygame.time.delay(time)
                        
                        global done
                        solve(win)
                        if done == 1:
                            return 

                        grid[i][j] = 0
                        pygame.draw.rect(win, background_color, ((j+1)*50 + buffer, (i+1)*50 + buffer, 50-2*buffer, 50-2*buffer))
                        pygame.display.update()
                return
    done = 1

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("SUDOKU")
    win.fill(background_color)
    font = pygame.font.SysFont('Montseratt', 35)    

    #add buttons here
    check_img = pygame.image.load('check.png').convert_alpha()
    solve_button = buttons.Button(50, 10, check_img, 0.05)

    stop_img = pygame.image.load('stop.png').convert_alpha()
    stop_button = buttons.Button(100, 10, stop_img, 0.05)

    #draw the bold lines separate squares of 3x3
    for i in range(10):
        if i % 3 == 0:
            pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 4)
            pygame.draw.line(win, (0,0,0), (50, 50+50*i), (500, 50 + 50*i), 4)

    #draw the grid 
    for i in range(0,10):
        pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 2)
        pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 2)
    pygame.display.update()
    
    #populating the grid aka generate new board
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if 0 < grid[i][j] < 10:
                value = font.render(str(grid[i][j]), True, original_color)
                win.blit(value, ((j+1)*50 + 20, (i+1)*50 + 15))
    pygame.display.update()

    while True:
        if solve_button.draw(win):
            solve(win)
        if stop_button.draw(win):
            pygame.quit()
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pygame.display.update()

if __name__ == '__main__':
    main()

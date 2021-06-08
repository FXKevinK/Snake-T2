import subprocess as sp
from os import path
from random import randint
from tkinter import *
import pygame as pg
from PIL import ImageTk, Image

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
BLUE = (112, 161, 215)
GREEN = (133, 202, 119)
RED = (255, 100, 90)

HEAD = (210, 145, 188)
BACKGROUND = (255, 244, 156)
BODY = (224, 187, 228)

DOWN = 0
RIGHT = 1
UP = 2
LEFT = 3
HS_FILE = "highscore.txt"

# semua objek dalam screen adalah spot
class Spot:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.f = 0
    self.g = 0
    self.neighbors = []
    self.camefrom = []
    self.obstacle = False

    global level
    if randint(1, rows - 2) < level:    # < jumlah obstacle dlm 1 tempat
        self.obstacle = True
        
  def show(self, color):
    pg.draw.rect(screen, color, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])

  def add_neighbors(self):
    if self.x > 1:
        self.neighbors.append(grid[self.x - 1][self.y])

    if self.y > 1:
        self.neighbors.append(grid[self.x][self.y - 1])

    if self.x < rows - 2:
        self.neighbors.append(grid[self.x + 1][self.y])

    if self.y < cols - 2:
        self.neighbors.append(grid[self.x][self.y + 1])

def load_data():
    # load high score
    global highscore
    with open(path.join(path.dirname(__file__), HS_FILE), 'r') as f:
        try:
            highscore = int(f.read())
        except:
            highscore = 0


def getpath(food1, snake1):
  food1.camefrom = []     # init food camefrom

  for s in snake1: s.camefrom = []    #init snake camefrom

  openset = [snake1[-1]]  #openset diinisiasi dengan kepala snake
  closedset = []
  dir_array1 = []

  while 1:
    if not openset:
      print("No way to Food")
      break

    current1 = min(openset, key=lambda x: x.f)    #current 1 = nilai minimum f dalam openset

    temp = []
    for i in range(len(openset)):
      if openset[i] != current1:
        temp.append(openset[i])
    
    openset = temp              # keluarin current 1 dari open set
    closedset.append(current1)  # masukin current 1 ke closed set
    
    for neighbor in current1.neighbors:
      if neighbor not in closedset and not neighbor.obstacle and neighbor not in snake1:
        tempg = neighbor.g + 1

        if neighbor in openset:
          if tempg < neighbor.g:
            neighbor.g = tempg

        else:
          neighbor.g = tempg
          openset.append(neighbor)

        neighbor.f = neighbor.g
        neighbor.camefrom = current1

    if current1 == food1: break

  while current1.camefrom:
    if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
      dir_array1.append(UP)

    elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
      dir_array1.append(DOWN)

    elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
      dir_array1.append(LEFT)

    elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
      dir_array1.append(RIGHT)
        
    current1 = current1.camefrom

  #print(dir_array1)

  for i in range(rows):
    for j in range(cols):
      grid[i][j].camefrom = []
      grid[i][j].f = 0
      grid[i][j].g = 0
      
  return dir_array1

def drawGrid(w, rows, surface):
  sizeBtwn = w / rows

  x = 0
  y = 0
  for i in range(rows):
    x += sizeBtwn
    y += sizeBtwn

    pg.draw.line(surface, WHITE, (x, 0), (x, w))
    pg.draw.line(surface, WHITE, (0, y), (w, y))
 
  pass

def redrawWindow(surface):
  global rows, width
  surface.fill(BACKGROUND)
  drawGrid(width, rows, surface)

############################ DECLARATION ###################################
pg.init()
root = Tk()
destroyed = False
toMainMenu = True

cols = 24
rows = 24

width = 720
height = 720
wr = width/cols
hr = height/rows
direction = 1
level = 1

with open(path.join(path.dirname(__file__), HS_FILE), 'r') as f:
    try:
        highscore = int(f.read())
    except:
        highscore = 0

screen = pg.display.set_mode([width, height])
pg.display.set_caption("SNAKE GAME")
clock = pg.time.Clock()

#buat grid
grid = []
for i in range(rows):
  grid.append([])
  for j in range(cols):
    grid[i].append(Spot(i,j))

#tiap grid tau neighbornya
for i in range(rows):
  for j in range(cols):
    grid[i][j].add_neighbors()


snake = [grid[rows//2][cols//2]]                      # posisi awal snake di tengah grid
food = grid[randint(1, rows-2)][randint(1, cols-2)]   # posisi awal makanan random di grid
current = snake[-1]                                   # posisi saat ini(head)

dir_array = getpath(food, snake)
score = 0

sp.call('clear',shell=True)
print("Score = ",score)
out = False
done = False
isSetup = True
modeAI = True
#-------------------------------- END DECLARATION -------------------------------------#

################### END MESSAGE #####################################
def Again():
  global destroyed
  root.destroy()
  destroyed = True
  mainMenu()

def Exit():
  global done, out
  print('EXIT GAME')
  done = True
  out = True
  root.destroy()

def endMessage(content):
  root.title("\tSNAKE GAME - GAME OVER")
  root.geometry('360x144')
  root.resizable(False, False)

  myLabel = Label(root, text=content)
  myLabel.pack()

  global highscore
  if score > highscore:
        highscore = score
        myLabel = Label(root, text="NEW HIGH SCORE!!!\n"+"High Score: " + str(highscore))
        myLabel.pack()
        with open(path.join(path.dirname(__file__), HS_FILE), 'w') as f:
            f.write(str(score))
  else:
        myLabel = Label(root, text="High Score: " + str(highscore))
        myLabel.pack()
  pg.display.flip()

  myYesButton = Button(root, text="Play again", command=Again)
  myYesButton.pack()

  myNoButton = Button(root, text="Exit", command=Exit)
  myNoButton.pack()

  root.mainloop()

def message_box(content):
  root.title("Key pressed")
  messageFrame = LabelFrame(root, padx=10, pady=10)
  messageFrame.pack(padx=10, pady=10)

  myLabel = Label(messageFrame, text=content)
  myLabel.pack()

  myNoButton = Button(messageFrame, text="OK", command=Exit)
  myNoButton.pack()

  root.mainloop()

#-------------------------- END MESSAGE -----------------------------------#

################################## MAIN PROGRAM ############################################
while not done:
  pg.display.set_caption("SNAKE GAME    Your Score : "+str(score))
  if toMainMenu:
    mainMenu()
    toMainMenu = False
  
  if isSetup:
    setup()
    isSetup = False

  if destroyed:
    root = Tk()
    destroyed = False

  pg.time.delay(0) #makin besar makin lambat
  clock.tick(12)        #kecepatan game, makin besar makin cepat
  redrawWindow(screen)  #background color map

  if modeAI: 
    direction = dir_array.pop(-1)

  if direction == DOWN:
    snake.append(grid[current.x][current.y + 1])
  
  elif direction == RIGHT:
    snake.append(grid[current.x + 1][current.y])
  
  elif direction == UP:
    snake.append(grid[current.x][current.y - 1])
  
  elif direction == LEFT:
    snake.append(grid[current.x - 1][current.y])
  
  current = snake[-1]

  # kali dia makan, skor++
  if current.x == food.x and current.y == food.y:
    score = score + 1
    load_data()
    sp.call('clear',shell=True)
    print("Level = ",level)
    print("Size = ",cols)
    print("Score = ",score)
    while 1:
      food = grid[randint(1, rows - 2)][randint(1, cols - 2)]   # posisi makanan baru dirandom
      if not (food.obstacle or food in snake): break
        
    dir_array = getpath(food, snake)
  
  else: snake.pop(0)      #pop bagian belakang

  # warna badan ular
  for spot in snake:
    spot.show(BODY)

  # warna obstacle
  for i in range(rows):
    for j in range(cols):
      if grid[i][j].obstacle or i == 0 or j == 0 or i == rows-1 or j == cols-1:
        grid[i][j].show(RED)

  # mati manual
  for i in range(rows):
    for j in range(cols):
      if grid[i][j].obstacle or i == 0 or j == 0 or i == rows-1 or j == cols-1:
        if current.x == i and current.y == j:
          print("GAME OVER!!!")
          pg.display.set_caption("SNAKE GAME - GAME OVER!!!")
          endMessage('GAME OVER!!!' + "\nSCORE : "+ str(score) +"\n")

  food.show(GREEN)
  snake[-1].show(HEAD)
  pg.display.flip()

  if not dir_array:
    print("GAME OVER!!!")
    pg.display.set_caption("SNAKE GAME - GAME OVER!!!")
    endMessage('GAME OVER!!!' + "\nSCORE : "+ str(score) +"\n")

  for event in pg.event.get():
    if event.type == pg.QUIT:
      done = True

    elif event.type == pg.KEYDOWN:
      if event.key == pg.K_q or event.key == pg.K_ESCAPE:
        print("ESC or Q pressed, EXIT GAME")
        message_box("ESC or Q pressed, EXIT GAME" + "\nSCORE : "+ str(score) +"\n")
        done = True

      if event.key == pg.K_w or event.key == pg.K_UP: direction = UP
      if event.key == pg.K_s or event.key == pg.K_DOWN: direction = DOWN
      if event.key == pg.K_a or event.key == pg.K_LEFT: direction = LEFT
      if event.key == pg.K_d or event.key == pg.K_RIGHT: direction = RIGHT
########################################END OF MAIN####################
    
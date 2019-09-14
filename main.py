import time
import sys
from copy import deepcopy
FRAMES_PER_SEC = 1
def render(string):
    for i in range(80):
        print()
    sys.stdout.write(string)
    time.sleep(1/FRAMES_PER_SEC)
    sys.stdout.flush()

def matToStr(mat):
    return ''.join([''.join(row) for row in mat])
background = """
                 _,--=--._
               ,'         `.
              -             -
         ____'               `____
  -=====::(+):::::::::::::::::(+)::=====-
           (+).""""""""""""",(+)
               .           ,
                 `  -=-  '
                 /        \\
                /          \\
               /            \\
              /              \\
             /                \\
            /                  \\
       """

def gen_frames(background, initial, delta_path, img_mat):
    # Given coordinate path and image, output desired frames
    frames = []
    y, x = initial
    for dy, dx in delta_path:
        x += dx
        y += dy
        f = deepcopy(background)
        for i, row in enumerate(img_mat):
            for j, letter in enumerate(row):
                f[y+i][x+j] = letter
        frames.append(f)
    return frames

def renderFrames(background, delta_path, img_mat):
    bg = [list("{}{}\n".format(row, ' '*(65-len(row)))) for row in background.split("\n")]
    frames = gen_frames(bg, (14,20), delta_path, img_mat)
    for frame in frames:
        render(matToStr(frame))

while True:
  user_input = input("> ")
  if user_input == "cd ..":
    img_mat =[[" ","0"," "],
              ["/","|","\\"],
              ["/"," ","\\"]]
    delta_path = [(-1,0),(-1,0),(-1,0),(-1,0), (-1,0)]
    renderFrames(background, delta_path, img_mat)
  elif user_input == "quit":
    break
  else:
    print("Command not supported!")

#!/usr/local/bin/python3
import time
import sys
import os
from copy import deepcopy
FRAMES_PER_SEC = 5
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
           (+).'''''''''''''',(+)
               .           ,
                 `  -=-  '
                 /        \\
                /          \\
               /            \\
              /              \\
             /                \\
            /                  \\
       """
person_in_ufo = """
                 _,--=--._
               ,'    _    `.
              -    /(_)\\_o  -
         ____'     /_ _]     `____
  -=====::(+):::::::::::::::::(+)::=====-
           (+).'''''''''''''',(+)
               .           ,
                 `  -=-  '
                 /        \\
                /          \\
               /            \\
              /              \\
             /                \\
            /                  \\


       """
second_background = """









                   ,-=-.
                ---.....---
                   `-=-'
       """
goodbye = """
        ----------
       | Goodbye! |
        ----------
                \\
                  ,-=-.
                --.....--
                  `-=-'

       """
goodbye_animation = [goodbye, goodbye, goodbye, goodbye,
       """
        



                    ,
                   -+-
                    '

       """,
       """
        



                    
                    + 
                    

       """,
       """
        



                    
                     
                    

       """, '']

def get_warphole(dirname, max_len):
    padding = f"{' ' * ((max_len - len(dirname)) // 2)}"
    warphole = '\n'
    warphole += f"{padding}  {'_' * len(dirname)}  \n"
    warphole += f"{padding} /{' ' * len(dirname)}\\ \n"
    warphole += f"{padding} \\{'_' * len(dirname)}/ \n"
    warphole += f"{padding}\033[91m  {dirname}  \033[00m\n"
    return warphole

def get_warphole_str(directory_list, max_len):
    rows = []
    curr_row_length = 0
    partitions = [[]] # list of rows of directories
    partition_index = 0
    for dirname in directory_list:
        curr_row_length += len(dirname) + len('  ') * 2
        if curr_row_length >= max_len:
            partitions.append([dirname])
            partition_index += 1
            curr_row_length = 0
        else:
            partitions[partition_index].append(dirname)

    for partition in partitions:
        top = ''.join([f"  {'_' * len(dirname)}  " for dirname in partition])
        middle = ''.join([f" /{' ' * len(dirname)}\\ " for dirname in partition])
        bottom = ''.join([f" \\{'_' * len(dirname)}/ " for dirname in partition])
        labels = ''.join([f"\033[91m  {dirname}  \033[00m" for dirname in partition])
        rows.append('\n'.join([top, middle, bottom, labels]))
    return '\n'.join(rows)

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

def renderFrames(background, initial_pos, delta_path, img_mat):
    max_len = max([len(row) for row in background.split("\n")])
    bg = [list("{}{}\n".format(row, ' '*(max_len-len(row)))) for row in background.split("\n")]
    frames = gen_frames(bg, initial_pos, delta_path, img_mat)
    for frame in frames:
        render(matToStr(frame))

def base_frame():
    renderFrames(person_in_ufo, (0,0), [(0,0)], [])

base_frame()
while True:
    # renderFrames(person_in_ufo, [(0,0)], [])
    print('> ', end='')
    userCommand = input().split(" ")
    firstCommand = userCommand[0]
    max_len = max([len(row) for row in background.split("\n")])
    if firstCommand == 'ls':
        base_frame()
        if len(userCommand) > 1:
            print(get_warphole_str(dirnames, max_len))
        else:
            dirnames = [dirname for dirname in os.listdir() if dirname[0] != '.'] # exclude hidden files
            print(get_warphole_str(dirnames, max_len))
    elif firstCommand == 'cd':
        if len(userCommand) > 1:
            try:
                os.chdir(userCommand[1])
            except:
                print('Directory not found--you may have tried a file')
                print('Use ls to find what directories are available')
                continue
            if userCommand[1] == "..":
                img_mat =[["/","0","\\"],
                          ["/","|","\\"],
                          ["/"," ","\\"]]
                delta_path = [(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0)]
                renderFrames(get_warphole('.. (the parent directory)', max_len) + second_background, (14,20), delta_path, img_mat)
                renderFrames(background, (14,20), delta_path, img_mat)
            else:
                img_mat =[["/","0","\\"],
                          ["/","|","\\"],
                          ["/"," ","\\"]]
                delta_path = [(1,0),(1,0),(1,0),(1,0), (1,0),(1,0), (1,0)]
                renderFrames(background + get_warphole(userCommand[1], max_len), (8,20), delta_path, img_mat)
                renderFrames(get_warphole(userCommand[1], max_len) + second_background, (4,20), delta_path, img_mat)
            base_frame()
            print(f'You changed directory to "{os.getcwd()}"!')
        else:
            print("You're not allowed to use cd without naming a directory after it!")
    elif firstCommand == 'pwd':
        print(os.getcwd())
    elif firstCommand == 'exit' or firstCommand == 'quit':
        for frame in goodbye_animation:
            render(frame)
        break
    else:
      print('Command not supported!')

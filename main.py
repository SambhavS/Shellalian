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
 \033[95m                _,--=--._
               ,'         `.
              -             -
         ____'               `____
  -=====::(+):::::::::::::::::(+)::=====-
           (+).'''''''''''''',(+)
               .           ,
                 `  -=-  '\033[00m
                 /        \\
                /          \\
               /            \\
              /              \\
             /                \\
            /                  \\

       """
person_in_ufo = """
\033[95m                 _,--=--._
               ,'    \033[32m_\033[95m    `.
              -    \033[32m/(_)\\\033[95m    -
         ____'     \033[32m/_o_\\\033[95m      `____
  -=====::(+):::::::::::::::::(+)::=====-
           (+).'''''''''''''',(+)
               .           ,
                 `  -=-  '\033[00m
                 /        \\
                /          \\
               /            \\
              /              \\
             /                \\
            /                  \\



       """
second_background = """










\033[95m                   ,-=-.
                ---.....---
                   `-=-'\033[00m
       """
goodbye = """
        ----------
       | Goodbye! |
        ----------
                \\
\033[95m                  ,-=-.
                --.....--
                  `-=-'\033[00m

       """
goodbye_animation = [goodbye, goodbye, goodbye, goodbye,
       """
 \033[93m        



                    ,
                   -+-
                    '

       """,
       """
        



                    
                    + 
                    

       """,
       """
        



                    
                     
                    

       """, '\033[00m']

help_message = 'Use cd to change directories and ls to list what is available in the directory.\nDirectories will show up as warpholes and files will show up as stars.'

def get_warphole(dirname, max_len):
    padding = f"{' ' * ((max_len - len(dirname)) // 2)}"
    warphole = '\n'
    warphole += f"\033[34m{padding}  {'_' * len(dirname)}  \n"
    warphole += f"{padding} /{' ' * len(dirname)}\\ \n"
    warphole += f"{padding} \\{'_' * len(dirname)}/ \n"
    warphole += f"{padding}\033[95m  {dirname}  \033[00m\n"
    return warphole

def get_star_str(filename_list, max_len):
    rows = []
    curr_row_length = 0
    partitions = [[]] # list of rows of directories
    partition_index = 0
    for filename in filename_list:
        curr_row_length += len(filename) + 4
        if curr_row_length >= max_len:
            partitions.append([filename])
            partition_index += 1
            curr_row_length = 0
        else:
            partitions[partition_index].append(filename)

    for partition in partitions:
        top = ''.join([f"\033[93m  {' ' * (len(filename) // 2)};{' ' * (len(filename) // 2)}" for filename in partition])
        middle = ''.join([f"  {' ' * (len(filename) // 2 - 2)}--+--{' ' * (len(filename) // 2 - 2)}" for filename in partition])
        bottom = ''.join([f"  {' ' * (len(filename) // 2)}!{' ' * (len(filename) // 2)}" for filename in partition])
        labels = ''.join([f"\033[91m  {filename}\033[00m" for filename in partition])
        rows.append('\n'.join([top, middle, bottom, labels]))
    return '\n'.join(rows)

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
        top = ''.join([f"\033[34m  {'_' * len(dirname)}  " for dirname in partition])
        middle = ''.join([f" /{' ' * len(dirname)}\\ " for dirname in partition])
        bottom = ''.join([f" \\{'_' * len(dirname)}/ " for dirname in partition])
        labels = ''.join([f"\033[95m  {dirname}  \033[00m" for dirname in partition])
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
print(help_message)
while True:
    # renderFrames(person_in_ufo, [(0,0)], [])
    print('> ', end='')
    userCommand = input().split(" ")
    firstCommand = userCommand[0]
    max_len = max([len(row) for row in background.split("\n")])
    if firstCommand == 'ls':
        base_frame()
        if len(userCommand) > 1:
            if os.path.isdir(userCommand[0]):
                print(get_warphole_str([userCommand[0]], max_len))
            else:
                print(get_star_str([userCommand[0]], max_len))
        else:
            dirnames = [name for name in os.listdir() if name[0] != '.' and os.path.isdir(name)] # exclude hidden files
            filenames = [name for name in os.listdir() if name[0] != '.' and not os.path.isdir(name)]
            print(get_star_str(filenames, max_len))
            print(get_warphole_str(dirnames, max_len))
    elif firstCommand == 'cd':
        if len(userCommand) > 1:
            try:
                os.chdir(userCommand[1])
            except:
                print('\033[91mDirectory not found--you may have tried a file')
                print('Use ls to find what directories are available\033[00m')
                continue
            img_mat =[["\033[32m/","0","\\\033[00m"],
                          ["\033[32m/","|","\\\033[00m"],
                          ["\033[32m/"," ","\\\033[00m"]]
            if userCommand[1] == "..":
                
                delta_path = [(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0)]
                renderFrames(get_warphole('.. (the parent directory)', max_len) + second_background, (14,20), delta_path, img_mat)
                renderFrames(background, (14,20), delta_path, img_mat)
            else:
                delta_path = [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0)]
                renderFrames(background + get_warphole(userCommand[1], max_len), (8,20), delta_path, img_mat)
                renderFrames(get_warphole(userCommand[1], max_len) + second_background, (4,20), delta_path, img_mat)
            base_frame()
            print(f'\033[96mYou changed directory to "{os.getcwd()}"!\033[00m')
        else:
            print("\033[91mChanging to home directory with cd not supported\033[00m")
    elif firstCommand == 'pwd':
        print(os.getcwd())
    elif firstCommand == 'exit' or firstCommand == 'quit':
        for frame in goodbye_animation:
            render(frame)
        break
    elif firstCommand == 'help':
        print(help_message)
    else:
      print('\033[91mCommand not supported!\033[00m')
      print(help_message)

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pygame, sys
import cv2 as cv


#line 118 - size change, line 135 - input location change

pygame.init()

def displayImage(screen, px, topleft, prior):
    # ensure that the rect always has positive width, height
    x, y = topleft
    width = pygame.mouse.get_pos()[0] - topleft[0]
    height = pygame.mouse.get_pos()[1] - topleft[1]
    if width < 0:
        x += width
        width = abs(width)
    if height < 0:
        y += height
        height = abs(height)

    # eliminate redundant drawing cycles (when mouse isn't moving)
    current = x, y, width, height

    if not (width and height):
        return current
    if current == prior:
        return current

    # draw transparent box and blit it onto canvas
    screen.blit(px, px.get_rect())
    im = pygame.Surface((width, height))
    im.fill((128, 128, 128))
    pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
    im.set_alpha(128)
    screen.blit(im, (x, y))
    pygame.display.flip()

    # return current box extents
    return (x, y, width, height)


def setup(path):
    px = pygame.image.load(path)
    px = pygame.transform.scale(px, ((int)(width / 5), (int)(height / 5)))
    screen = pygame.display.set_mode(px.get_rect()[2:])
    screen.blit(px, px.get_rect())
    pygame.display.flip()
    return screen, px


def mainLoop(screen, px):
    topleft = bottomright = prior = None
    n = 0
    while n != 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if not topleft:
                    topleft = event.pos
                else:
                    bottomright = event.pos
                    n = 1
        if topleft:
            prior = displayImage(screen, px, topleft, prior)
    return (topleft + bottomright)

def btn1():  # crop image in selected area
   screen, px = setup(input_loc)
   left, upper, right, lower = mainLoop(screen, px)

   if right < left:
       left, right = right, left
   if lower < upper:
       lower, upper = upper, lower

   left = left * 5
   right = right * 5
   upper = upper * 5
   lower = lower * 5

   croppedImg = img[upper:lower + 1, left:right + 1, :]
   pygame.display.quit()
   cv.imwrite(output_loc, croppedImg)
   sys.exit()

def btn2():
    screen, px = setup(input_loc)
    left, upper, right, lower = mainLoop(screen, px)

    if right < left:
        left, right = right, left
    if lower < upper:
        lower, upper = upper, lower

    left = left * 5
    upper = upper * 5
    lower = lower * 5

    croppedImg = img[upper:lower + 1, left:lower + 1, :]
    pygame.display.quit()
    cv.imwrite(output_loc, croppedImg)
    sys.exit()

def btn3():  # crop image in selected height(1:1 ratio)
    screen, px = setup(input_loc)
    left, upper, right, lower = mainLoop(screen, px)

    if right < left:
        left, right = right, left
    if lower < upper:
        lower, upper = upper, lower

    left = left * 5
    upper = upper * 5
    #change your size of image
    size = 100

    croppedImg = img[upper:(upper + size), left:(left + size), :]
    pygame.display.quit()
    cv.imwrite(output_loc, croppedImg)
    sys.exit()

root = tk.Tk()

root.title = "Cropping Image"
root.resizable(False, False)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                           filetypes=(
                                               ("all files", "*.*"), ("jpeg files", "*.jpg"), ("png files", "*.png")))
input_loc = root.filename                                               
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
input_loc = root.filename #input your file address here
#output_loc = root.filename  <- using this line will replace original by cropped image.
output_loc = "croped_Image.png"

img = cv.imread(input_loc, -1)
height, width, channel = img.shape

#win = tk.Tk()


button1 = ttk.Button(root, text='선택 영역 자르기', command=lambda:btn1())
button1.grid(column=0, row=0, pady=5, padx=2)

button2 = ttk.Button(root, text='1:1 비율로 자르기', command=lambda:btn2())
button2.grid(column=1, row=0, pady=5, padx=2)

button3 = ttk.Button(root, text='선택한 크기로 자르기(1:1)', command=lambda:btn3())
button3.grid(column=1, row=1, pady=5, padx=2)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
button3 = ttk.Button(root, text='선택한 크기로 자르기(1:1)', command=lambda:btn3())
button3.grid(column=1, row=1, pady=5, padx=2)

enteredSize = ttk.Entry(root, width=14)
enteredSize.grid(column=0, row=1, pady=5, padx=2)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
root.mainloop()
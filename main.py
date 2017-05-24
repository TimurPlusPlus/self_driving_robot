import tkinter as tk

from PIL import Image

from robot import Robot as bot

x1 = 0
x2 = 40
y1 = 170
y2 = 190
img = './images/track3.png'

root = tk.Tk()
root.title('Differential drive robot')
c = tk.Canvas(root, width=900, height=900)
c.pack()


track = tk.PhotoImage(file=img)
c.create_image(0, 0, image=track, anchor=tk.NW)
rect = c.create_polygon((x1, y1), (x2, y1),
                        (x2, y2), (x1, y2), fill='blue')

track_pil = Image.open(img)
robot = bot.Robot(x1, y1, x2, y2, max_speed=0.5)

def main():
   global robot
   global c
   global rect

   robot.move(track_pil)
   c.delete(rect)

   rect = c.create_polygon(
       (robot.x1, robot.y1), (robot.x2, robot.y2),
       (robot.x3, robot.y3), (robot.x4, robot.y4), fill='blue')

   root.after(10, main)

main()

root.mainloop()

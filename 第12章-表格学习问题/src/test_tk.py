import tkinter as tk

def on_canvas_click(event):
    print(f"Canvas clicked at ({event.x}, {event.y})")

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# 绘制一个矩形
canvas.create_rectangle(50, 50, 350, 350, fill='blue')

# 绑定鼠标点击事件
canvas.bind('<Button-1>', on_canvas_click)

root.mainloop()

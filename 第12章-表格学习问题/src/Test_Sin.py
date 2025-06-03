from treelib import Tree
import numpy as np
import matplotlib.pyplot as plt

       
def func(x):
    return 2*np.cos(x) - np.sin(2*x*np.pi)

def draw_func(start, end, step):
    x = np.linspace(start, end, step)
    y = func(x)
    plt.plot(x, y)
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    return 

def get_best_x(start, end, step):
    x = np.linspace(start, end, step)
    y = func(x)
    max_index = np.argmax(y)
    return x[max_index], y[max_index]

if __name__ == '__main__':
    # 画出函数图像
    draw_func(-1, 1, 100)
    x, y = get_best_x(-1, 1, 100)
    print(f"Best x: {x}, Best y: {y}")  


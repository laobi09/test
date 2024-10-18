import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse, sys

def randomGrid(N):
    return np.random.choice([255, 0],N*N, p=[0.2,0.8]).reshape(N,N)



def addGlider(i, j, grid):
    glider = np.array([[0,0,255],
                       [255,0,255],
                       [0,255,255]])
    grid[i:i+3, j:j+3]=glider

def update(frameNum, img, grid, N):
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            left = (i-1)%N
            right = (i+1)%N
            up = (j-1)%N
            down = (j+1)%N
            total = int((
                grid[i, up] + grid[i, down] + 
                grid[left, j] + grid[right, j] +
                grid[left, up] + grid[right, up] +
                grid[left, down] + grid[right, down])/255)

            if grid[i,j] == 255:
                if total < 2 or total > 3:
                    newGrid[i,j] = 0
            else:
                if total == 3:
                    newGrid[i,j] = 255
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img


def main():
    # 输入参数
    parser = argparse.ArgumentParser(description="Runs Conway's Game of life simulation.")
    parser.add_argument('--N', required=False)
    parser.add_argument('--interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    args = parser.parse_args()
    
    # 设置网格尺寸
    N = 500
    # 设置动画更新间隔
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    grid = np.array([])
    if args.glider:
        grid = np.zeros(N*N).reshape(N,N)
        addGlider(1, 1, grid)
    else:
        if args.N and int(args.N)>8:
            N = int(args.N)
        grid = randomGrid(N)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N),
                                  frames=10, interval=updateInterval)
    plt.show()

if __name__ == '__main__':
    main()


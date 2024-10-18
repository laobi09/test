import turtle, math, random, argparse
import numpy as np
from PIL import Image
from datetime import datetime

def draw_circle(x, y, r, t):
    from math import cos, sin
    t.up()
    t.setpos(x+r, y)
    t.down()
    for i in range(0,360, 1):
        a = math.radians(i)
        t.setpos(x+r*math.cos(a), y+r*math.sin(a))
            
class Spiro:
    def __init__(self, xc, yc, col, R, r, l):
        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.step = 5
        self.drawingComplete = False
        self.setparams(xc, yc, col, R, r, l)
        self.restart()
        print('Spiro --init --ok')
        

    def setparams(self, xc, yc, col, R, r, l):
        self.a = 0.0
        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.col = col
        self.t.color(*col)
        self.l = l
        self.k = r / float(R)
        gcdVal = math.gcd(self.r, self.R)
        self.nRot = self.r // gcdVal

    def restart(self):
        self.drawingComplete = False
        self.t.showturtle()
        self.t.up()
        R, k, l= self.R, self.k, self.l
        a = 0.0
        x = R*((1-k)*math.cos(a)+l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a)-l*k*math.sin((1-k)*a/k))
        try:
            self.t.setpos(self.xc + x, self.yc + y)
        except Exception:
            print('Spiro Restart Exception')
            exit(0)
        self.t.down()

    def draw(self):
        R, k, l= self.R, self.k, self.l
        for i in range(0, 360*self.nRot+1, self.step):
            a = math.radians(i)
            x = R*((1-k)*math.cos(a)+l*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a)-l*k*math.sin((1-k)*a/k))
            try:
                self.t.setpos(self.xc + x, self.yc + y)
            except Exception:
                print("Spiro Draw Exception")
                exit()
        self.t.hideturtle()

    def update(self):
        if self.drawingComplete:
            return
        # 递增角度
        R, k, l= self.R, self.k, self.l
        self.a += self.step
        a = math.radians(self.a)
        x = R*((1-k)*math.cos(a)+l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a)-l*k*math.sin((1-k)*a/k))
        # print(f'Update@     x={x} y={y}')
        try:
            self.t.setpos(self.xc + x, self.yc + y)
        except Exception:# 迭代深度极限
            print("Spiro Update Exception")
            exit(0)
        # 如果繁花曲线已经绘制完毕，就设置相应的标志
        if self.a >= 360*self.nRot:
            self.drawingComplete = True
            self.t.hideturtle()
        

    def clear(self):
        self.t.up()
        self.t.clear()
 
class SpiroAnimator:
    def __init__(self, N):
        # 定时器，单位ms
        self.deltaT = 10 

        self.width = turtle.window_width()
        self.height = turtle.window_height()
        self.restarting = False

        # 创建Spiro对象
        self.spiros = []
        for i in range(N):
            rparams = self.genRandomParams()
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)

        print('SpiroAnimator --init --ok')

        # 调用定时器
        turtle.ontimer(self.update, self.deltaT)

    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint((2*R-width)//2, (width-2*R)//2)
        yc = random.randint((2*R-height)//2, (height-2*R)//2)
        col = (random.random(),random.random(),random.random())
        return (xc, yc, col, R, r, l)

    def restart(self):
        if self.restarting:
            return
        else:
            self.restarting = True
        for spiro in self.spiros:
            spiro.clear()
            rparams = self.genRandomParams()
            spiro.setparams(*rparams)
            spiro.restart()
        self.restarting = False
        print('SpiroAnimator --restart --ok')
        


    def update(self):
        nComplete = 0
        for spiro in self.spiros:
            spiro.update()
            if spiro.drawingComplete:
                nComplete += 1
        if nComplete == len(self.spiros):
            self.restart()
        try:
            turtle.ontimer(self.update, self.deltaT)
        except Exception:
            print('SpiroAnimator update exception')
            exit(0)

    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()

# 将繁花曲线保存为图像
def saveDrawing():
    turtle.hideturtle()
    dateStr = (datetime.now()).strftime("%d_%b_%Y-%H%M%S")
    filename = 'spiro-' + dateStr
    print(f"saving drawing to {filename}.eps/png")
    canvas = turtle.getcanvas()
    canvas.postscript(file=filename+'.eps')
    image = Image.open(filename+'.eps')
    image.save(filename+'.png', 'png')
    turtle.showturtle()

       
def main():
    print("generating spirograh...")
    print()
    descStr = """这个程序使用模块turtle绘制繁花曲线
    如果运行时没有指定参数，这个程序会绘制随机的繁花曲线
    参数说明：
    R： 外圆半径
    r： 内圆半径
    l： 孔洞距离与r的比值"""
    parser = argparse.ArgumentParser(description=descStr)
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False, help="The three arguments in sparams: R, r, l.")
    args = parser.parse_args()

    turtle.setup(width=0.8)
    turtle.shape('turtle')
    turtle.title('Spirographs')
    turtle.onkey(saveDrawing, "s")
    turtle.listen()

    turtle.hideturtle()
    # 检查参数并绘制繁花曲线
    if args.sparams:
        params = [float(x) for x in args.sparams]
        col = (0, 0, 0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        spiroAnim = SpiroAnimator(4)
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        turtle.onkey(spiroAnim.restart, "space")
    turtle.mainloop()


if __name__ == '__main__':
    main()

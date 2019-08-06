'''
设置：单点的动画移动
'''
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.artist import Artist
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


class Point_Move:
    showverts = True
    offset = 0.1 # 距离偏差设置

    def __init__(self):
        # 创建figure（绘制面板）、创建图表（axes）
        self.fig, self.ax = plt.subplots()
        # 设置标题
        self.ax.set_title('Click and drag a point to move it')
        # 设置坐标轴范围
        self.ax.set_xlim((-2, 4))
        self.ax.set_ylim((-2, 4))
        # 设置初始值
        self.x = [1,2]
        self.y = [1,2]
        # 绘制2D的动画line
        self.line = Line2D(self.x, self.y, ls="",
                           marker='o', markerfacecolor='r',
                           animated=True)
        self.ax.add_line(self.line)
        # 标志值设为none
        self._ind = None
        # 设置画布，方便后续画布响应事件
        canvas = self.fig.canvas
        self.fig.canvas.mpl_connect('draw_event', self.draw_callback)
        self.fig.canvas.mpl_connect('button_press_event', self.button_press_callback)
        self.fig.canvas.mpl_connect('button_release_event', self.button_release_callback)
        self.fig.canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
        self.canvas = canvas
        plt.grid()
        plt.show()


    # 界面重新绘制
    def draw_callback(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)

    def get_ind_under_point(self, event):
        'get the index of the vertex under point if within epsilon tolerance'
        # 在公差允许的范围内，求出鼠标点下顶点坐标的数值
        xt,yt = np.array(self.x),np.array(self.y)
        d = np.sqrt((xt-event.xdata)**2 + (yt-event.ydata)**2)
        indseq = np.nonzero(np.equal(d, np.amin(d)))[0]
        ind = indseq[0]
        # 如果在公差范围内，则返回ind的值
        if d[ind] >=self.offset:
            ind = None
        return ind

    # 鼠标被按下，立即计算最近的顶点下标
    def button_press_callback(self, event):
        'whenever a mouse button is pressed'
        if not self.showverts: return
        if event.inaxes==None: return
        if event.button != 1: return
        self._ind = self.get_ind_under_point(event)

    # 鼠标释放后，清空、重置
    def button_release_callback(self, event):
        'whenever a mouse button is released'
        if not self.showverts: return
        if event.button != 1: return
        self._ind = None

    # 鼠标移动的事件
    def motion_notify_callback(self, event):
        'on mouse movement'
        if not self.showverts: return
        if self._ind is None: return
        if event.inaxes is None: return
        if event.button != 1: return
        # 更新数据
        x,y = event.xdata, event.ydata
        self.x[self._ind] = x
        self.y[self._ind] = y
        # 根据更新的数值，重新绘制图形
        self.line = Line2D(self.x, self.y, ls="",
                           marker='o', markerfacecolor='r',
                           animated=True)
        self.ax.add_line(self.line)
        # 恢复背景
        self.canvas.restore_region(self.background)
        self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)

if __name__ == '__main__':
    Point_Move()



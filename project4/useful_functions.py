import numpy as np
import matplotlib.pyplot as plt

class DrawPopulation:
    def __init__(self, data):
        plt.switch_backend('QtAgg')
        self.data = data
        self.fig = plt.figure()
        self.draw_setup()
        self.cid = self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.run_flag = 1
    
    def draw_setup(self):
        # this just plots the sample/given data
        ax = self.fig.add_subplot(projection='3d')
        data_class0 = self.data[:, self.data[3]<self.data[2]]
        data_class1 = self.data[:, self.data[3]>self.data[2]]
        ax.scatter(data_class0[0], data_class0[1], data_class0[3], marker='x', color='green')
        ax.scatter(data_class1[0], data_class1[1], data_class1[3], marker='o', color='red')
        plt.title("Sample Population")

    def run_drawing(self):
        while self.run_flag:
            plt.draw()
            plt.pause(0.001)

    def on_close(self, event):
        self.run_flag = 0
        plt.close(fig=self.fig)

class DrawLSR:
    def __init__(self, data, sample):
        plt.switch_backend('QtAgg')
        self.data = data
        self.sample = sample
        self.fig = plt.figure()
        self.draw_setup()
        self.cid = self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.run_flag = 1
    
    def draw_setup(self):
        # this just plots the sample/given data
        ax = self.fig.add_subplot(projection='3d')
        data_class0 = self.data[:, self.data[3]<self.data[2]]
        data_class1 = self.data[:, self.data[3]>self.data[2]]
        ax.scatter(data_class0[0], data_class0[1], data_class0[3], marker='.', color='green')
        ax.scatter(data_class1[0], data_class1[1], data_class1[3], marker='.', color='red')
        sample_class0 = self.sample[:, self.sample[3]<self.sample[2]]
        sample_class1 = self.sample[:, self.sample[3]>self.sample[2]]
        ax.scatter(sample_class0[0], sample_class0[1], sample_class0[3], marker='x', color='green')
        ax.scatter(sample_class1[0], sample_class1[1], sample_class1[3], marker='o', color='red')
        ax.set_xlabel('x0')
        ax.set_ylabel('x1')
        ax.set_zlabel('likelyhood of class 1')
        plt.title("LSR")

    def run_drawing(self):
        while self.run_flag:
            plt.draw()
            plt.pause(0.001)

    def on_close(self, event):
        self.run_flag = 0
        plt.close(fig=self.fig)

class DrawQLSR:
    def __init__(self, data, sample):
        plt.switch_backend('QtAgg')
        self.data = data
        self.sample = sample
        self.fig = plt.figure()
        self.draw_setup()
        self.cid = self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.run_flag = 1
    
    def draw_setup(self):
        # this just plots the sample/given data
        ax = self.fig.add_subplot(projection='3d')
        data_class0 = self.data[:, self.data[3]<self.data[2]]
        data_class1 = self.data[:, self.data[3]>self.data[2]]
        ax.scatter(data_class0[0], data_class0[1], data_class0[3], marker='.', color='green')
        ax.scatter(data_class1[0], data_class1[1], data_class1[3], marker='.', color='red')
        sample_class0 = self.sample[:, self.sample[3]<self.sample[2]]
        sample_class1 = self.sample[:, self.sample[3]>self.sample[2]]
        ax.scatter(sample_class0[0], sample_class0[1], sample_class0[3], marker='x', color='green')
        ax.scatter(sample_class1[0], sample_class1[1], sample_class1[3], marker='o', color='red')
        ax.set_xlabel('x0')
        ax.set_ylabel('x1')
        ax.set_zlabel('likelyhood of class 1')
        plt.title("Quadratic LSR")

    def run_drawing(self):
        while self.run_flag:
            plt.draw()
            plt.pause(0.001)

    def on_close(self, event):
        self.run_flag = 0
        plt.close(fig=self.fig)
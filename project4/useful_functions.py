import numpy as np
import matplotlib.pyplot as plt

x_test_class_0, y_test_class_0, x_test_class_1, y_test_class_1 = np.loadtxt('outputFile.dat').T
xtest0 = np.array([x_test_class_0, y_test_class_0]) # generate the test data for class 0 
xtest1 = np.array([x_test_class_1, y_test_class_1]) # generate the test data for class 1 

class DrawOneDataset:
    def __init__(self, data, marker0, marker1, color0, color1, label0, label1, title):
        plt.switch_backend('QtAgg')
        self.data = data
        self.title = title
        self.marker0 = marker0
        self.marker1 = marker1
        self.color0 = color0
        self.color1 = color1
        self.label0 = label0
        self.label1 = label1
        self.fig = plt.figure()
        self.draw_setup()
        self.cid = self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.run_flag = 1
    
    def draw_setup(self):
        # this just plots the sample/given data
        ax = self.fig.add_subplot(projection='3d')
        data_class0 = self.data[:, self.data[3]<self.data[2]]
        data_class1 = self.data[:, self.data[3]>self.data[2]]
        ax.scatter(data_class0[0], data_class0[1], data_class0[3], marker=self.marker0, color=self.color0, label=self.label0)
        ax.scatter(data_class1[0], data_class1[1], data_class1[3], marker=self.marker1, color=self.color1, label=self.label1)
        ax.set_xlabel('X0')
        ax.set_ylabel('X1')
        ax.set_zlabel('Likelyhood of Class 1')
        ax.legend()
        plt.title(self.title)

    def run_drawing(self):
        while self.run_flag:
            plt.draw()
            plt.pause(0.001)

    def on_close(self, event):
        self.run_flag = 0
        plt.close(fig=self.fig)

# class DrawTwoDataset:
#     def __init__(self, data0, data1, marker00, marker01, marker10, marker11, color00, color01, color10, color11, legend00, legend01, legend10, legend11, title):
#         plt.switch_backend('QtAgg')
#         self.data0 = data0
#         self.data1 = data1
#         self.marker00 = marker00
#         self.marker01 = marker01
#         self.marker10 = marker10
#         self.marker11 = marker11
#         self.color00 = color00
#         self.color01 = color01
#         self.color10 = color10
#         self.color11 = color11
#         self.legend00 = legend00
#         self.legend01 = legend01
#         self.legend10 = legend10
#         self.legend11 = legend11
#         self.title = title
#         self.fig = plt.figure()
#         self.draw_setup()
#         self.cid = self.fig.canvas.mpl_connect('close_event', self.on_close)
#         self.run_flag = 1
    
#     def draw_setup(self):
#         # this just plots the sample/given data
#         ax = self.fig.add_subplot(projection='3d')
#         data_class0 = self.data0[:, self.data0[3]<self.data0[2]]
#         data_class1 = self.data0[:, self.data0[3]>self.data0[2]]
#         ax.scatter(data_class0[0], data_class0[1], data_class0[3], marker=self.marker00, color=self.color00, label=self.legend00)
#         ax.scatter(data_class1[0], data_class1[1], data_class1[3], marker=self.marker01, color=self.color01, label=self.legend01)
#         sample_class0 = self.data1[:, self.data1[3]<self.data1[2]]
#         sample_class1 = self.data1[:, self.data1[3]>self.data1[2]]
#         ax.scatter(sample_class0[0], sample_class0[1], sample_class0[3], marker=self.marker10, color=self.color10, label=self.legend10)
#         ax.scatter(sample_class1[0], sample_class1[1], sample_class1[3], marker=self.marker11, color=self.color11, label=self.legend11)
#         ax.set_xlabel('X0')
#         ax.set_ylabel('X1')
#         ax.set_zlabel('Likelyhood of Class 1')
#         ax.legend()
#         plt.title(self.title)

#     def run_drawing(self):
#         while self.run_flag:
#             plt.draw()
#             plt.pause(0.001)

#     def on_close(self, event):
#         self.run_flag = 0
#         plt.close(fig=self.fig)

class DrawTwoDataset:
    def __init__(self, data0, data1, marker00, marker01, marker10, marker11, color00, color01, color10, color11, legend00, legend01, legend10, legend11, title):
        self.data0 = data0
        self.data1 = data1
        self.marker00 = marker00
        self.marker01 = marker01
        self.marker10 = marker10
        self.marker11 = marker11
        self.color00 = color00
        self.color01 = color01
        self.color10 = color10
        self.color11 = color11
        self.legend00 = legend00
        self.legend01 = legend01
        self.legend10 = legend10
        self.legend11 = legend11
        self.title = title
        self.fig = plt.figure()
        self.draw_setup()

    def draw_setup(self):
        # this just plots the sample/given data
        ax = self.fig.add_subplot()
        data_class0 = self.data0[:, self.data0[3]<self.data0[2]]
        data_class1 = self.data0[:, self.data0[3]>self.data0[2]]
        # Plot test data for class 0 and class 1
        ax.plot(xtest0[0,:], xtest0[1,:], 'g.', label='Class 0 Test', markersize=1)
        ax.plot(xtest1[0,:], xtest1[1,:], 'r.', label='Class 1 Test', markersize=1)
        # End of Angel's edit

        ax.scatter(data_class0[0], data_class0[1], marker=self.marker00, color=self.color00, label=self.legend00)
        ax.scatter(data_class1[0], data_class1[1], marker=self.marker01, color=self.color01, label=self.legend01)

        sample_class0 = self.data1[:, self.data1[3]<self.data1[2]]
        sample_class1 = self.data1[:, self.data1[3]>self.data1[2]]
        ax.scatter(sample_class0[0], sample_class0[1], marker=self.marker10, color=self.color10, label=self.legend10)
        ax.scatter(sample_class1[0], sample_class1[1], marker=self.marker11, color=self.color11, label=self.legend11)
        
        ax.set_xlabel('X0')
        ax.set_ylabel('X1')
        ax.legend()
        ax.set(xlim=(-1.918,4.6887), ylim=(-2.549,3.5951))
        plt.title(self.title)

    def run_drawing(self):
        plt.show()


class DrawThreeDataset:
    def __init__(self, data0, data1, data2, title):
        plt.switch_backend('QtAgg')
        self.data0 = data0
        self.data1 = data1
        self.data2 = data2
        self.title = title
        self.fig = plt.figure()
        self.draw_setup()
        self.cid = self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.run_flag = 1
    
    def draw_setup(self):
        # this just plots the sample/given data
        ax = self.fig.add_subplot(projection='3d')
        data_class0 = self.data0[:, self.data0[3]<self.data0[2]]
        data_class1 = self.data0[:, self.data0[3]>self.data0[2]]
        ax.scatter(data_class0[0], data_class0[1], data_class0[3], marker='*', color='green')
        ax.scatter(data_class1[0], data_class1[1], data_class1[3], marker='*', color='red')
        data1_class0 = self.data1[:, self.data1[3]<self.data1[2]]
        data1_class1 = self.data1[:, self.data1[3]>self.data1[2]]
        ax.scatter(data1_class0[0], data1_class0[1], data1_class0[3], marker='x', color='green')
        ax.scatter(data1_class1[0], data1_class1[1], data1_class1[3], marker='o', color='red')
        data2_class0 = self.data2[:, self.data2[3]<self.data2[2]]
        data2_class1 = self.data2[:, self.data2[3]>self.data2[2]]
        ax.scatter(data2_class0[0], data2_class0[1], data2_class0[3], marker='D', color='green')
        ax.scatter(data2_class1[0], data2_class1[1], data2_class1[3], marker='D', color='red')
        ax.set_xlabel('x0')
        ax.set_ylabel('x1')
        ax.set_zlabel('likelyhood of class 1')
        plt.title(self.title)

    def run_drawing(self):
        while self.run_flag:
            plt.draw()
            plt.pause(0.001)

    def on_close(self, event):
        self.run_flag = 0
        plt.close(fig=self.fig)
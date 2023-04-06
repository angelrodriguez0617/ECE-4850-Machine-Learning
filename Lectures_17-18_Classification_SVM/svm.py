import os
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import random
from sklearn.model_selection import train_test_split 
from sklearn.svm import SVC

dir = r'C:\Users\10801309\OneDrive - Utah Valley University\Desktop\ECE 4850\ECE-4850\Lectures_17-18_Classification_SVM\train'
categories = ['Cat', 'Dog']
data = []

for category in categories:
    path = os.path.join(dir, category)
    label = categories.index(category)
    print(label)


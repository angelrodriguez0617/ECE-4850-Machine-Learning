import os
import numpy as np
import cv2
import random
# import time
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib

dir = r'/storage/ml/dataset/test_face'

categories = ['Positive', 'Negative']

data = []

# go through each image for each category
for category in categories:
    # get the path to the category in the database
    path=os.path.join(dir,category)
    # get the label for each category
    label=categories.index(category)
    # print that label
    print(f'Processing images for label: {label}, {categories[label]}')

    # look at each image in each category
    for img in os.listdir(path):
        # get the path to the individual image
        imgpath = os.path.join(path,img)
        # error checking
        try:
            # read in the image
            img = cv2.imread(imgpath, 0)
            # flatten the image into a 1-D array
            img = np.array(img).flatten()
            # append the image and it's label to our list images in ram
            data.append([img, label])
        except Exception as e:
            # no real error handling?
            pass

# print the length (number of photos) of our dataset
print(f'Number of images imported: {len(data)}')

random.shuffle(data)
features = []
labels = []

for feature, label in data:
    features.append(feature)
    labels.append(label)

# xtrain, xtest, ytrain, ytest = train_test_split(features, labels, test_size=0.3, random_state=35)

save_directory = r'../svm_models_rbf'
model_name = r'svm_epoch_15.pickle'

model = joblib.load(f'{save_directory}/{model_name}')

accuracy = model.score(features, labels)
print(f'Loaded model accuracy: {accuracy}')
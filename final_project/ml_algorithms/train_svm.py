import os
import numpy as np
import cv2
import random
# import time
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib

dir = r'/storage/ml/dataset/ECE4850-Faces'

categories = ['Angel', 'Austin', 'Other', 'Shekaramiz']

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

# this is to store the accuracy each epoch for comparing
accuracy_per_epoch = np.array([])

# make sure we have a place to save the svm models
save_directory = r'../svm_models'
os.makedirs(save_directory, exist_ok=True)

# train for ten epocs
for i in range(10):
    print(f'Starting epoch {i}')

    # shuffle the data
    random.shuffle(data)
    features = []
    labels = []

    # pull the features and labels out of the data
    for feature, label in data:
        features.append(feature)
        labels.append(label)

    # split the dataset for verification
    xtrain, xtest, ytrain, ytest = train_test_split(features, labels, test_size=0.3, random_state=35)
    # define the SVM model
    model = SVC(C=1, kernel='linear', gamma='auto')
    # train the model
    print(f'\t...training model...')
    model.fit(xtrain, ytrain)

    # test the model on the portion of the dataset we saved for testing
    prediction = model.predict(xtest)
    accuracy = model.score(xtest, ytest)

    # print our findings
    print(f'\t...accuracy for epoch {i}: {accuracy}...')

    # we need to keep track of the accuracy each epoch
    accuracy_per_epoch = np.append(accuracy_per_epoch, accuracy)

    # save the model only if its better than the others
    if accuracy >= np.max(accuracy_per_epoch):
        print(f'\t...saving model for epoch {i}...')
        # I think this is just an efficient wrapper for pickle that comes with sklearn
        joblib.dump(model, f'{save_directory}/svm_epoch_{i}.pickle')

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pickle
import random
# import time
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
dir = r'C:\Users\10801309\OneDrive - Utah Valley University\Desktop\ECE 4850\ECE-4850\Lectures_17-18_Classification_SVM\train'

categories = ['Cat','Dog']

data =[]
for category in categories:
    path=os.path.join(dir,category)
    label=categories.index(category)
    print(label)

    for img in os.listdir(path):
        imgpath=os.path.join(path,img)
        try:
            pet_img=cv2.imread(imgpath,0)
            #cv2.imshow('image',pet_img)
            pet_img=cv2.resize(pet_img,(120,120))
            image=np.array(pet_img).flatten()
            data.append([image,label])
        except Exception as e:
            pass

#cv2.waitKey(0) 
#cv2.destroyAllWindows()

print(len(data))
"""
pick_in = open('data.pickle','wb')
pickle.dump(data,pick_in)
pick_in.close()

pick_in = open('data.pickle','rb')
data=pickle.load(pick_in)
pick_in.close()
"""

for i in range(10):

    random.shuffle(data)
    features = []
    labels = []

    for feature, label in data:
        features.append(feature)
        labels.append(label)

    xtrain, xtest, ytrain, ytest = train_test_split(features, labels, test_size=0.1)
    model = SVC(C=1, kernel='linear', gamma='auto')
    model.fit(xtrain,ytrain)

    prediction = model.predict(xtest)
    acurracy = model.score(xtest, ytest)

    print(f'accuracy: {acurracy}')
    print(f'prediction: {categories[prediction[10]]}')

    pet = xtest[10].reshape(120, 120)
    plt.imshow(pet, cmap='gray')
    plt.show()

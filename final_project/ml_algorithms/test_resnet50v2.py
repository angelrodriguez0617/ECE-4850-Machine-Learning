from tensorflow import keras
import numpy as np
import random

# height
img_n_size = 720
# width
img_m_size = 960

# imports our 'test' dataset
test_dataset = keras.preprocessing.image_dataset_from_directory(
            directory=f"/storage/ml/dataset/test_face",
            labels='inferred',
            label_mode='categorical',
            color_mode='rgb',
            shuffle=False,
            batch_size=4,
            image_size=(img_n_size, img_m_size)
)

# random_number = random.randrange(40)
# training_dataset, test_dataset = keras.preprocessing.image_dataset_from_directory(
#             directory=f"/storage/ml/dataset/ECE4850-Faces",
#             labels='inferred',
#             label_mode='categorical',
#             color_mode='rgb',
#             batch_size=4,
#             image_size=(img_n_size, img_m_size),
#             validation_split=0.3,
#             seed=35,
#             shuffle=False,
#             subset='both'
# )

class_names = test_dataset.class_names

# loads the saved model
model = keras.saving.load_model(r'../resnet50v2_model')

# run predictions and evaluate test dataset
prediction = model.predict(test_dataset)
values = model.evaluate(test_dataset)

prediction_labels = np.argmax(prediction, axis=-1)

print('')
print(['Angel', 'Austin', 'Other', 'Shekaramiz'])
print(prediction)
print('')
print('wining predictions:')
print(prediction_labels)
print(np.take(class_names, prediction_labels))
print('')
print('Loss, Accuracy')
print(values)
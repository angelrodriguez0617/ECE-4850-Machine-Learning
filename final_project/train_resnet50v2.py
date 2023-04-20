import os
from contextlib import redirect_stdout
from tensorflow import keras

# Angel, Austin, Shekaramiz, Other_Person, Background
num_output_classes = 4
# height
img_n_size = 720
# width
img_m_size = 960
# this describes how many times we want to feed the data in
num_epochs = 30

# these import our data as a 'tensorflow dataset' object
# useful for managing input data
training_dataset, validation_dataset = keras.preprocessing.image_dataset_from_directory(
            directory=f"/storage/ml/dataset/ECE4850-Faces",
            label_mode='categorical',
            color_mode='rgb',
            batch_size=4,
            image_size=(img_n_size, img_m_size),
            validation_split=0.3,
            seed=35,
            subset='both'
)

# make sure we have a directory to save the model we will create
save_directory = f'resnet50v2_model'
os.makedirs(save_directory, exist_ok=True)
# this is a callback: callbacks tell keras to do something while training
# this one saves the model any time it reaches its best performance
save_model = keras.callbacks.ModelCheckpoint(
            save_directory,
            monitor='val_loss',
            mode='auto',
            save_best_only=True)

# this imports the built in ResNet50V2 model
base_model = keras.applications.ResNet50V2(include_top=False, weights=None, input_shape=(img_n_size, img_m_size, 3))

# get the output of the ResNet50V2 model
output = base_model.output
# pooling (basically to convert our 4D output to a 2D output)
output = keras.layers.GlobalAveragePooling2D()(output)
# fully connected layer, one neuron for each of our outputs
output = keras.layers.Dense(num_output_classes, activation='softmax')(output)

# this defines the model by feeding it the begining and the end of the model
model = keras.models.Model(inputs=base_model.input, outputs=output)
# this basically finalizes our model, or makes it ready for training/usage
model.compile(optimizer='Adam', metrics=['accuracy'], loss='categorical_crossentropy')

# this is the function that trains our model
model.fit(
    x=training_dataset,
    validation_data=validation_dataset,
    epochs=num_epochs,
    callbacks=[save_model]
)

# this saves a summary of our model
with open(f'resnet50v2_model_summary.txt', 'w') as f:
    with redirect_stdout(f):
        model.summary()
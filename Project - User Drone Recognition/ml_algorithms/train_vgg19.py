import os
from contextlib import redirect_stdout
from tensorflow import keras

# Angel, Austin, Shekaramiz, Other_Person, Background
num_output_classes = 2
# height
img_n_size = 720
# width
img_m_size = 960
# this describes how many times we want to feed the data in
num_epochs = 15

# these import our data as a 'tensorflow dataset' object
# useful for managing input data
training_dataset = keras.preprocessing.image_dataset_from_directory(
            directory=f"/storage/ml/dataset/ECE4850-Faces-Reduced-Split/Train",
            label_mode='categorical',
            color_mode='rgb',
            batch_size=4,
            image_size=(img_n_size, img_m_size),
            shuffle=True
)
validation_dataset = keras.preprocessing.image_dataset_from_directory(
            directory=f"/storage/ml/dataset/ECE4850-Faces-Reduced-Split/Test",
            label_mode='categorical',
            color_mode='rgb',
            batch_size=4,
            image_size=(img_n_size, img_m_size),
            shuffle=True
)

# make sure we have a directory to save the model we will create
save_directory = r'../vgg19_model'
os.makedirs(save_directory, exist_ok=True)
# this is a callback: callbacks tell keras to do something while training
# this one saves the model any time it reaches its best performance
save_model = keras.callbacks.ModelCheckpoint(
            save_directory,
            monitor='val_loss',
            mode='auto',
            save_best_only=True)

tensorboard_callback = keras.callbacks.TensorBoard(log_dir="../vgg19_tensorboard")

# this imports the built in VGG19 model
base_model = keras.applications.VGG19(include_top=False, weights=None, input_shape=(img_n_size, img_m_size, 3))

inputs = keras.Input(shape=(img_n_size, img_m_size, 3))
output = keras.layers.RandomFlip('horizontal')(inputs)
output = keras.layers.RandomRotation(0.1)(output)
output = keras.layers.RandomContrast(0.1)(output)
output = keras.layers.RandomBrightness(0.1)(output)
output = keras.applications.vgg19.preprocess_input(output)
# get the output of the VGG19 model
output = base_model(output)
# pooling (basically to convert our 4D output to a 2D output)
output = keras.layers.GlobalMaxPooling2D()(output)
output = keras.layers.Dropout(0.2)(output)
output = keras.layers.Dense(4096, activation='relu')(output)
output = keras.layers.Dense(4096, activation='relu')(output)
# fully connected layer, one neuron for each of our outputs
output = keras.layers.Dense(num_output_classes, activation='softmax')(output)

# this defines the model by feeding it the begining and the end of the model
model = keras.models.Model(inputs=inputs, outputs=output)
# this basically finalizes our model, or makes it ready for training/usage
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001), metrics=['accuracy'], loss='categorical_crossentropy')

# this is the function that trains our model
model.fit(
    x=training_dataset,
    validation_data=validation_dataset,
    epochs=num_epochs,
    callbacks=[save_model, tensorboard_callback]
)

# this saves a summary of our model
with open(r'../vgg19_model_summary.txt', 'w') as f:
    with redirect_stdout(f):
        model.summary()
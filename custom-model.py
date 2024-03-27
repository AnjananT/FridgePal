import tensorflow as tf
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import pandas as pd

train_root = r'C:\Users\anjan\OneDrive\Documents\makeUoftDataset\train'
val_root = r'C:\Users\anjan\OneDrive\Documents\makeUoftDataset\validate'
test_root = r'C:\Users\anjan\Downloads\archive (4)\fruits-360-original-size\fruits-360-original-size\Test'

train_data = pd.read_csv(train_root)
val_data = pd.read_csv(val_annotations)
test_data = pd.read_csv(test_annotations)

train_grouped_annotations = train_data.groupby('filename')['class'].apply(list).reset_index()
val_grouped_annotations = val_data.groupby('filename')['class'].apply(list).reset_index()
test_grouped_annotations = test_data.groupby('filename')['class'].apply(list).reset_index()

datagen = ImageDataGenerator(rescale=1./255)

train_datagen = datagen.flow_from_dataframe(
    dataframe=train_grouped_annotations
    x_col='filename',
    y_col='class'
    #brightness_range=[0.5,1.5],
    #channel_shift_range=30.0,
    fill_mode='nearest')

val_datagen = ImageDataGenerator(rescale = 1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_dataframe(
    train_root, 
    target_size=(100,100),
    class_mode='categorical',
    batch_size=126
)
val_generator = val_datagen.flow_from_directory(
    val_root,
    target_size=(100,100),
    class_mode='categorical',
    batch_size=126
)
test_generator=test_datagen.flow_from_directory(
    test_root,
    target_size=(100,100),
    class_mode='categorical',
    batch_size=126
)

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(filters=32, kernelsize= (5,5), activation='relu', input_shape=(100,100,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(filters=64, kernelsize=(5,5), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(filters=128, kernelsize=(5,5), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.5),

    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(24, activation='softmax')
])

model.summary()

model.compile(loss = 'categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

history = model.fit(train_generator, epochs=25, steps_per_epoch=20, validation_data=val_generator, verbose=1, validation_steps=3)

test_loss, test_accuracy = model.evaluate(test_generator)
print("Test loss:", test_loss)
print("Test Accuracy:", test_accuracy)

model.save("testMakeUoft.keras")

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label='Training Accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation Accuracy')
plt.plot(len(epochs), test_accuracy, 'g', label='Test Accuracy')
plt.title('Training, validation, test accuracy')
plt.legend(loc=0)
plt.figure()

plt.show()

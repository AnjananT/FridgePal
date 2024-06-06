import tensorflow as tf
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

train_root = r'C:\Users\anjan\OneDrive\Documents\fridgePalDataset\train'
val_root = r'C:\Users\anjan\OneDrive\Documents\fridgePalDataset\validate'
test_root = r'C:\Users\anjan\OneDrive\Documents\fridgePalDataset\test'

train_datagen = ImageDataGenerator(
   # rescale = 1./255,
    rotation_range =20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    #shear_range=0.2,
    #zoom_range=0.2,
    #horizontal_flip=True,
    #brightness_range=[0.5,1.5],
    #channel_shift_range=30.0,
    fill_mode='nearest')

val_datagen = ImageDataGenerator()
test_datagen = ImageDataGenerator()

train_generator = train_datagen.flow_from_directory(
    train_root, 
    target_size=(128,128),
    class_mode='categorical',
    batch_size=32
)
val_generator = val_datagen.flow_from_directory(
    val_root,
    target_size=(128,128),
    class_mode='categorical',
    batch_size=32
)
test_generator=test_datagen.flow_from_directory(
    test_root,
    target_size=(128,128),
    class_mode='categorical',
    batch_size=32
)

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=(128,128,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),


    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.2),

    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax')
])

model.summary()

model.compile(loss = 'categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

history = model.fit(train_generator, epochs=15, steps_per_epoch=10, validation_data=val_generator, verbose=1, validation_steps=3)

#test_loss, test_accuracy = model.evaluate(test_generator)
#print("Test loss:", test_loss)
#print("Test Accuracy:", test_accuracy)

model.save("testMakeUoft.keras")

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label='Training Accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation Accuracy')
#plt.plot(len(epochs), test_accuracy, 'g', label='Test Accuracy')
plt.title('Training, validation')
plt.legend(loc=0)
plt.figure()

plt.show()

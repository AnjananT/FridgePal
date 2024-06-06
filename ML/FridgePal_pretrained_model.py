import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

train_root = r'C:\Users\anjan\OneDrive\Documents\makeUoftDataset\train'
val_root = r'C:\Users\anjan\OneDrive\Documents\makeUoftDataset\validate'
test_root = r'C:\Users\anjan\Downloads\archive (4)\fruits-360-original-size\fruits-360-original-size\Test'

# Load pre-trained model
base_model = tf.keras.applications.MobileNetV2(input_shape=(100, 100, 3), include_top=False, weights='imagenet')

# Freeze pre-trained layers
base_model.trainable = False

# Add custom classification head
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
output_layer = tf.keras.layers.Dense(4, activation='softmax')

# Combine base model with custom head
model = tf.keras.Sequential([
    base_model,
    global_average_layer,
    output_layer
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Define data generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

val_datagen = ImageDataGenerator(rescale=1./255)
#test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_root,
    target_size=(100, 100),
    class_mode='categorical',
    batch_size=32
)
val_generator = val_datagen.flow_from_directory(
    val_root,
    target_size=(100, 100),
    class_mode='categorical',
    batch_size=32
)

#test_generator = test_datagen.flow_from_directory(
 #   test_root,
  #  target_size=(100, 100),
   # class_mode='categorical',
   # batch_size=32
#)

# Train the model
history = model.fit(train_generator, epochs=25, steps_per_epoch=5, validation_data=val_generator, verbose=1, validation_steps=3)

# Save the model
model.save("fine_tuned_model2.keras")

# Plot training history
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label='Training Accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend(loc=0)
plt.figure()

plt.plot(epochs, loss, 'r', label='Training Loss')
plt.plot(epochs, val_loss, 'b', label='Validation Loss')
plt.title('Training and Validation Loss')
plt.legend(loc=0)
plt.figure()

plt.show()
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.datasets import cifar10
from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D

def train_model(x_train, y_train, x_test, y_test, model_name):
    
    num_classes = 11
    batch_size = 32
    epochs = 25
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)
    
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same', input_shape=\
        x_train.shape[1:]))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    
    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))
    
    
    opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-06)
    
    
    model.compile(loss='categorical_crossentropy', optimizer=\
        opt, metrics=\
        ['accuracy'])
    
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    
    model.fit(x_train, y_train, batch_size=\
        batch_size, epochs=\
        epochs, validation_data=\
        (x_test, y_test), shuffle=\
        True)
    
    model.save(model_name)
    
    
    scores = model.evaluate(x_test, y_test, verbose=1)
    return (scores[0], scores[1])
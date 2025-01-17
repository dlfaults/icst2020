import datetime
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

now = datetime.datetime.now

batch_size = 128
num_classes = 5
epochs = 5

(img_rows, img_cols) = (28, 28)

filters = 32

pool_size = 2

kernel_size = 3

input_shape = (img_rows, img_cols, 1)

def train(model, train, test, num_classes, model_name):
    x_train = train[0].reshape((train[0].shape[0],) + input_shape)
    x_test = test[0].reshape((test[0].shape[0],) + input_shape)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('')
    x_train /= 255
    x_test /= 255
    
    
    y_train = keras.utils.to_categorical(train[1], num_classes)
    y_test = keras.utils.to_categorical(test[1], num_classes)
    
    model.compile(loss='categorical_crossentropy', optimizer=\
        'adadelta', metrics=\
        ['accuracy'])
    
    model.fit(x_train, y_train, batch_size=\
        batch_size, epochs=\
        epochs, verbose=\
        1, validation_data=\
        (x_test, y_test))
    model.save(model_name)
    score = model.evaluate(x_test, y_test, verbose=0)
    return (score[0], score[1])

def train_model(x_train, y_train, x_test, y_test, model1_name, model2_name):
    
    x_train_lt5 = x_train[y_train < 5]
    y_train_lt5 = y_train[y_train < 5]
    x_test_lt5 = x_test[y_test < 5]
    y_test_lt5 = y_test[y_test < 5]
    
    x_train_gte5 = x_train[y_train >= 5]
    y_train_gte5 = y_train[y_train >= 5] - 5
    x_test_gte5 = x_test[y_test >= 5]
    y_test_gte5 = y_test[y_test >= 5] - 5
    
    
    feature_layers = [\
        Conv2D(filters, kernel_size, padding=\
        'valid', input_shape=\
        input_shape), \
        Activation('relu'), \
        Conv2D(filters, kernel_size), \
        Activation('relu'), \
        MaxPooling2D(pool_size=pool_size), \
        Dropout(0.25), \
        Flatten()]
    
    
    classification_layers = [\
        Dense(128), \
        Activation('relu'), \
        Dropout(0.5), \
        Dense(num_classes), \
        Activation('softmax')]
    
    
    
    model = Sequential(feature_layers + classification_layers)
    
    
    (loss1, acc1) = train(model, 
        (x_train_lt5, y_train_lt5), 
        (x_test_lt5, y_test_lt5), num_classes, model1_name)
    
    
    for l in feature_layers:
        l.trainable = False
    
    
    (loss2, acc2) = train(model, 
        (x_train_gte5, y_train_gte5), 
        (x_test_gte5, y_test_gte5), num_classes, model2_name)
    
    return (loss1, acc1, loss2, acc2)
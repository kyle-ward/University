from keras.datasets import mnist
from keras.models import Sequential
# 堆叠神经网络的载体
from keras.layers import Dense
# 全连接层，可作为一层神经网络（两个神经元的隐藏层就是一个Dense）
from keras.optimizers import SGD
import matplotlib.pyplot as plt
from keras.utils import to_categorical

(X_train, Y_train), (X_test, Y_test) = mnist.load_data()

print("X_train.shape: " + str(X_train.shape))
print("Y_train.shape: " + str(Y_train.shape))
print("X_test.shape: " + str(X_test.shape))
print("Y_test.shape: " + str(Y_test.shape))

# print(Y_train[0])
# plt.imshow(X_train[0], cmap='gray')
# plt.show()

X_train = X_train.reshape(60000, 784) / 255.0
X_test = X_test.reshape(10000, 784) / 255.0

Y_train = to_categorical(Y_train, 10)
Y_test = to_categorical(Y_test, 10)


model = Sequential()
model.add(Dense(units=255, activation='relu', input_dim=784))
model.add(Dense(units=255, activation='relu'))
model.add(Dense(units=255, activation='relu'))
# model.add(Dense(units=8, activation='relu'))
model.add(Dense(units=10, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01), metrics=['accuracy'])


history = model.fit(X_train, Y_train, epochs=10, validation_data=(X_test, Y_test))
# history = model.fit(X_train, Y_train, epochs=100, batch_size=1024)
# 可视化损失函数
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend(['Train', 'Test'])
plt.title('Loss function')
plt.show()
# 可视化准确率
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Test'])
plt.title('Accuracy')
plt.show()
# 计算测试集准确率并输出
loss, accuracy = model.evaluate(X_test, Y_test)
print("Loss:", loss)
print("Accuracy:", accuracy)

'''
model.fit(X_train, Y_train, epochs=100, batch_size=1024)
loss, accuracy = model.evaluate(X_test, Y_test)
print("loss: " + str(loss))
print("accuracy: " + str(accuracy))
'''
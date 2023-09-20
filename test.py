import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras.datasets.mnist as mnist

data = mnist.load_data()
(x_train, y_train), (x_test, y_test) = data
x_train = x_train.reshape(x_train.shape[0], -1) /255.0
x_test = x_test.reshape(x_test.shape[0], -1) / 255.0
# print(x_train[0].shape, x_test[0].shape)


def init_params():
    #Hidden Layer parameters
    W1 = np.random.randn(10, 784) * np.sqrt(2/784)
    b1 = np.zeros((10, 1))
    
    #Output layer parameters
    W2 = np.random.randn(10, 10) * np.sqrt(2/10)
    b2 = np.zeros((10, 1))
    
    return W1, b1, W2, b2

def ReLU(Z):
    return np.maximum(0,Z)

def softmax(Z):
    e_Z = np.exp(Z - np.max(Z, axis=0, keepdims=True))
    A = e_Z / np.sum(e_Z, axis=0, keepdims=True)
    return A


def forward_prop(W1,b1,W2,b2,X):
    Z1=W1.dot(X.T)+b1
    A1=ReLU(Z1)
    Z2=W2.dot(A1)+b2
    A2=softmax(Z2)
    return Z1,A1,Z2,A2


def cust_one_hot(Y):
    one_hot_Y = np.zeros((Y.size,Y.max()+1))
    one_hot_Y[np.arange(Y.size),Y]=1
    return one_hot_Y


def deriv_ReLU(Z):
    return Z>0


# def back_prop(Z1,A1,Z2,A2,W2,Y):
#     one_hot_Y = one_hot(Y)
#     m= Y.size
#     dZ2 = A2-one_hot_Y
#     dW2= 1/m*dZ2.dot(A1.T)
#     db2= 1/m*np.sum(dZ2,axis=1,keepdims=True)
#     dZ1= W2.T.dot(dZ2)*deriv_ReLU(Z1)
#     dW1=1/m* dZ1.dot(X.T)
#     db1=1/m* np.sum(dZ1,axis=1,keepdims=True)
#     return dW1,db1,dW2,db2


# def back_prop(Z1, A1, Z2, A2, W2, Y, X):
#     print("Y shape:", Y.shape)
#     print("Y value:", Y)
#     one_hot_Y = cust_one_hot(Y)
#     m = Y.size
#     dZ2 = 2*(A2.T - one_hot_Y)
#     dW2 = dZ2.T.dot(A1) / m  
#     db2 = np.sum(dZ2, axis=1, keepdims=True) / m
    
#     dZ1 = W2.dot(dZ2) * deriv_ReLU(Z1) 
#     dW1 = dZ1.dot(X) / m
#     db1 = np.sum(dZ1, axis=1, keepdims=True) / m
#     return dW1, db1, dW2, db2

def back_prop(Z1, A1, Z2, A2, W2, Y, X):
    one_hot_Y = cust_one_hot(Y)
    m = Y.size
    dZ2 = 2*(A2.T - one_hot_Y)
    dW2 = A1.dot(dZ2.T) / m  
    db2 = np.sum(dZ2, axis=1, keepdims=True) / m
    
    dZ1 = W2.dot(dZ2) * deriv_ReLU(Z1) 
    dW1 = dZ1.dot(X) / m
    db1 = np.sum(dZ1, axis=1, keepdims=True) / m
    return dW1, db1, dW2, db2



def update_params(W1,b1,W2,b2,dW1,db1,dW2,db2,alpha):
    W1= W1-alpha*dW1
    b1= b1- alpha*db1
    W2 = W2 - alpha*dW2
    b2= b2- alpha*db2.T
    return W1,b1,W2,b2

def get_predictions(A2):
    return np.argmax(A2,axis=1)

def get_accuracy(predictions,Y):
    print(predictions,Y)
    return np.sum(predictions==Y)/Y.size

def loss_and_accuracy(y_pred, y_true):
    #Cross-Entropy Loss
    epsilon = 1e-10  #Constant
    m = y_true.shape[0]
    pred_loss = np.clip(y_pred, epsilon, 1.0 - epsilon)
    loss = -np.sum(y_true * np.log(pred_loss)) / m
    
    #Accuracy
    accuracy = np.mean(y_pred == y_true)
    return loss, accuracy

def compute_cost(A2, Y):
    m = Y.shape[1]
    cost = -1/m * np.sum(Y * np.log(A2 + 1e-8))  
    return cost

def gradient_descent(X,Y,iterations,alpha):
    W1,b1,W2,b2=init_params()
    for i in range (iterations):
        Z1,A1,Z2,A2=forward_prop(W1,b1,W2,b2,X)
        dW1,db1,dW2,db2=back_prop(Z1,A1,Z2,A2,W2,Y,X)
        W1,b1,W2,b2 = update_params(W1,b1,W2,b2,dW1,db1,dW2,db2,alpha)
        if i%30 ==0:
            print('Epoch: ', i)
            pred = np.argmax(a2, 0)
            loss, accuracy = loss_and_accuracy(pred, Y)
            print(f'Loss: {loss:.4f}\t Accuracy: {accuracy*100:.2f} %')     
    return W1,b1,W2,b2

# x_train = x_train.T
y_train_onehot = cust_one_hot(y_train.astype(int))  
W1,b1,W2,b2= gradient_descent(x_train,y_train,2001,0.06)
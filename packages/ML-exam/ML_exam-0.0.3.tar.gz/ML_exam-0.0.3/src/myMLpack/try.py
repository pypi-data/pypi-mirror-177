import numpy as np
np.random.seed(2)

X = np.random.randn(2,3)
y = np.random.randn(1,3) > 0

def sig(Z):
    s = 1/(1+np.exp(-Z)) 
    return s

def tanh(Z):
    s = (np.exp(Z) - np.exp(-Z)) / (np.exp(Z) + np.exp(-Z)) 
    return s

def relu(Z):
    s = np.maximum(0,Z) 
    return s

def leaky_relu(Z):
    s = np.maximum(0.01,Z)
    return s

def shape(X,y):
    n_x = X.shape[0]
    n_h1 = 4
    n_h2 = 2
    n_y = y.shape[0] 

    return (n_x, n_h1, n_h2, n_y)


def initial_params(n_x, n_h1, n_h2, n_y):
    np.random.seed(2)
    w1 = np.random.randn(n_h1, n_x) * 0.01
    b1 = np.zeros((n_h1,1))

    w2 = np.random.randn(n_h2, n_h1) * 0.01
    b2 = np.zeros((n_h2,1))

    w3 = np.random.randn(n_y, n_h2) * 0.01
    b3 = np.zeros((n_y, 1))


    return {'w1': w1, 'b1': b1, 'w2': w2, 'b2': b2, 'w3': w3, 'b3': b3}


def fwd_prop(X,params):
    w1 = params['w1']
    b1 = params['b1']
    w2 = params['w2']
    b2 = params['b2']
    w3 = params['w3']
    b3 = params['b3']

    z1 = np.dot(w1,X) + b1
    a1 = tanh(z1)

    z2 = np.dot(w2,a1) + b2
    a2 = tanh(z2)

    z3 = np.dot(w3,a2) + b3
    a3 = sig(z3)

    return a3, {'z1': z1, 'a1': a1, 'z2': z2, 'a2': a2, 'z3': z3, 'a3': a3}


def compute_cost(a3,y):
    m = y.shape[1]
    logp = np.multiply(y,np.log(a3)) + np.multiply((1-y), np.log(1-a3))
    cost = -np.sum(logp)/m
    
    return cost

def bwd_prop(params, catch, X, y):
    w1 = params['w1']
    b1 = params['b1']
    w2 = params['w2']
    b2 = params['b2']
    w3 = params['w3']
    b3 = params['b3']

    a1 = catch['a1']
    a2 = catch['a2']
    a3 = catch['a3']

    m = y.shape[1]

    dz3 = a3 - y 
    dw3 = np.dot(dz3, a2.T)/m
    db3 = np.sum(dz3,  axis=1,  keepdims=True) / m

    dz2 = np.dot(w3.T, dz3) * (1 - a2**2)
    dw2 = np.dot(dz2, a1.T)/m
    db2 = np.sum(dz2,  axis=1,  keepdims=True) / m  

    dz1 = np.dot(w2.T, dz2)*(1 - a1**2)
    dw1 = np.dot(dz1, X.T)/m
    db1 = np.sum(dz1,  axis=1,  keepdims=True) / m


    return {'dw1':dw1, 'db1': db1, 'dw2': dw2, 'db2': db2, 'dw3': dw3, 'db3': db3}

  
def update(params, grade, lr = 0.01):
    w1 = params['w1']
    b1 = params['b1']
    w2 = params['w2']
    b2 = params['b2']
    w3 = params['w3']
    b3 = params['b3']

    dw1 = grade['dw1']
    db1 = grade['db1']
    dw2 = grade['dw2']    
    db2 = grade['db2']    
    dw3 = grade['dw3']    
    db3 = grade['db3']    

    w1 = w1 - (lr * dw1)
    b1 = b1 - (lr * db1)
    w2 = w2 - (lr * dw2)
    b2 = b2 - (lr * db2)
    w3 = w3 - (lr * dw3)
    b3 = b3 - (lr * db3)

    return {'w1': w1, 'b1': b1, 'w2': w2, 'b2': b2, 'w3': w3, 'b3': b3}

def NN(X, Y, itr = 10000, print_cost = False):
    np.random.seed(3)
    n_x, n_h1, n_h2, n_y = shape(X,Y)

    parameters = initial_params(n_x, n_h1, n_h2, n_y)

    for i in range(0, itr):
        A3, cache = fwd_prop(X, parameters)
        cost = compute_cost(A3, y)
        grades = bwd_prop(parameters, cache, X, Y)
        parameters = update(parameters, grades, lr= 0.01)

        if print_cost and i%1000 == 0:
            print(f'cost {i}:{cost}')

    return parameters

fin_parameters = NN(X,y, print_cost= True)


def predict_dec (parameters, X):

    A2, _ = fwd_prop(X, params=parameters)
    predictions = (A2>0.5)
    return predictions

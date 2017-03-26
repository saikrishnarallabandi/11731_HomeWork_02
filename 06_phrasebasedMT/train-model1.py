from ibm1 import IBM as ibm 
import sys

train_input = sys.argv[1]
train_output = sys.argv[2]
iterations = 8

ibm1 = ibm(train_input,train_output, iterations)
ibm1.train_me()

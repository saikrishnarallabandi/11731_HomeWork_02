import numpy as np 
from collections import defaultdict, Counter 
from itertools import count, chain 
import math, sys 
from sys import stdout
from decimal import Decimal as D
import time
from collections import defaultdict,namedtuple
from itertools   import product,repeat
import random

class IBM():
  
    def __init__(self,train_input,train_output,max_iter=8):
       self.train_input = train_input
       self.train_output = train_output
       self.max_iter = max_iter
       self.output_file = sys.argv[3]
       self.print_flag = 0
       
    def train_me(self):
        self.get_bitext()
        self.bi_counts_dict = defaultdict(float)
        self.input_counts_dict = defaultdict(float)
        self.output_counts_dict = defaultdict(float)
        
        # Theta
        self.theta = defaultdict(lambda: 1.0/len(self.output_dict))
        print "Theta: ", len(self.theta)
	print "Theta Initialization done" 	
        self.output_count = defaultdict(lambda: 0.0)
        self.total = defaultdict(lambda: 0.0)
        self.s_total = defaultdict(lambda: 0.0)
	
        for iteration in range(self.max_iter):
          #random.shuffle(self.bitext)
          ll = 0.0

          # E Step : Get counts based on 
          for idx, (input_array, output_array) in enumerate(self.bitext):
             for input_word in input_array:
	         sum_variable = 0.0
	         for output_word in output_array:
		     key = str(input_word) + '_' + str(output_word)
		     sum_variable += self.theta[key] + 1.0		 
  	         for output_word in output_array:
		     key = str(input_word) + '_' + str(output_word)
		     self.output_count[key] += self.theta[key]/sum_variable
		     self.total[str(output_word)] += self.theta[key]/float(sum_variable) 
	  print "E Step done"
	
          # M Step: Update Theta based on counts
          for key  in self.output_count.keys():
	       output_word = key.split('_')[1]
	       self.theta[key] = self.output_count[key]/self.total[output_word]
	  print "M Step Done"

          # Likelihood
          for idx, (input_array, output_array) in enumerate(self.bitext):
             for input_word in input_array:
	         sum_variable = 0.0
	         for output_word in output_array:
		     key = str(input_word) + '_' + str(output_word)
		     sum_variable += self.theta[key]	
		 ll += math.log(sum_variable)
	     ll +=  math.log(self.epsilon)-float(len(input_array))*math.log(float(len(output_array)))
	  print "Loglikelihood"
	  print ll / float(self.total_words)
	  #print ll / float(len(self.output_dict))
	  
	  # Align
	  self.align()

	
       
    def get_bitext(self):
	self.bitext = []
	src,tgt = self.train_input, self.train_output
	src_lines = open(src).readlines()
        tgt_lines = open(tgt).readlines()
        self.output_dict = defaultdict(lambda: len(self.output_dict))
        self.input_dict = defaultdict(lambda: len(self.output_dict))
        src_array = []
        tgt_array = []
        src_array_words = []
        tgt_array_words = []
        self.total_words = 0
        
	for src_line, tgt_line in zip(src_lines, tgt_lines):
           src_words = src_line.split() 
           tgt_words = tgt_line.split()  + ['NULL']
           src_array.append([self.input_dict[w] for w in src_words])
           tgt_array.append([self.output_dict[w] for w in tgt_words])
           src_array_words.append(src_words)
           tgt_array_words.append(tgt_words)
           self.total_words += len(tgt_words)
        #self.bitext = zip(src_array,tgt_array)
        self.bitext = zip(src_array_words, tgt_array_words)
        self.epsilon = 1.0/ max([len(line)for line in [pair[1] for pair in self.bitext]])
        print "Epsilon: ", self.epsilon

    
       
    def align(self):
        output_file = open(self.output_file,"w")
        for indx, (e, f) in enumerate(self.bitext):
            results = []
            for i in range(len(e)):
                max_j, max_prob = -1, 0.0
                for j in range(len(f)):
		    key = str(e[i]) + '_' + str(f[j])
		    #print key, self.theta[key], max_prob
                    if (self.theta[key]) > max_prob:
                        max_j = j
                        max_prob = self.theta[key]
                results.append(str(i)+ '_' + str(max_j))
            line = " ".join(results)
            #if len(e) < 6:
            #   print e, f, line
            output_file.write(line+"\n")

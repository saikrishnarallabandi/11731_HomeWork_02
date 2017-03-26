from collections import Counter, defaultdict
import numpy as np
import math

def phrase_extract(es,fs,A):
    phrases = []
    
    es_aligns = [[] for i in range(len(es))]
    fs_aligns = [[] for i in range(len(fs))]
    
    #print es_aligns
    #print fs_aligns

    for alignment in A:
        t = [int(x) for x in alignment.split('_')]
        es_aligns[t[0]].append(t[1])
        fs_aligns[t[1]].append(t[0])
        
    length_output = len(fs)
    length_alignment = len(A)
    length_input = len(es)
    null_align = 1
    
    '''
    print '\n\n\n'
    print "         Length of input sentence is ", length_input
    print "         ", es
    print "         ", fs
    print "         Length of alignment is ", length_alignment
    print "         Length of output sentence is ", length_output
    print "         Alignment is ", A
    print '\n'
    '''

    for i1 in range(length_input):
        for i2 in range(i1, length_input):
            A_segment = [A[i] for i in range(i1, i2)]
            #print "Segment: ", A_segment
            target_phrase = [int(a.split('_')[0]) for a in A_segment]
            #print "Target Phrase is ", target_phrase
            # Check if target phrase is quasi-consecutive
            if len(target_phrase) > 0 and quasi_consecutive(target_phrase, A, null_align):
               # Calculate span j1 to j2 in F
               j1 = min(target_phrase)
               j2 = max(target_phrase)
               #print j1, j2
               # All positions in E that correspond to Fj1j2
               A_segment = [A[i] for i in range(j1, j2+1)]
               positions = [a.split('-')[0] for a in A_segment]
               eng_phrase = ' '.join(es[i1:i2+1])
               ger_phrase = ' '.join(fs[j1:j2+1])
               # Add to set of extracted phrases.
               if len(eng_phrase) < 1 or len(ger_phrase) < 1:
		    continue
               phrases += [(eng_phrase, ger_phrase)]
    #print phrases
    return phrases           	  
	  
	  

def extract(es,fs,A):
    phrases = [()]
    length_output = len(fs)+1
    length_alignment = len(A)
    length_input = len(es)
    null_align = 1
    print '\n\n\n'
    print "         Length of input sentence is ", length_input
    print "         ", es
    print "         ", fs
    print "         Length of alignment is ", length_alignment
    print "         Length of output sentence is ", length_output
    print "         Alignment is ", A
    print '\n'
    for i1 in range(length_output):
        for i2 in range(i1, length_output):
	    #print "i1: ", i1, "i2: ",i2 
            # Extract target phrase - All positions in F that correspond to Ei1i2
            A_segment = [A[i] for i in range(i1, i2)]
            print " Segment is ", A_segment
            target_phrase = [int(a.split('-')[0]) for a in A_segment]
            print "Target Phrase is ", target_phrase
            # Check if target phrase is quasi-consecutive
            if len(target_phrase) > 0 and quasi_consecutive(target_phrase, A, null_align):
               # Calculate span j1 to j2 in F
               j1 = min(target_phrase)
               j2 = max(target_phrase)
               print j1, j2
               # All positions in E that correspond to Fj1j2
               A_segment = [A[i] for i in range(j1, j2+1)]
               positions = [a.split('-')[0] for a in A_segment]
               eng_phrase = ' '.join(es[i1:i2+1])
               ger_phrase = ' '.join(fs[j1:j2+1])
               # Add to set of extracted phrases.
               if len(eng_phrase) < 1 or len(ger_phrase) < 1:
		    continue
               phrases += [(eng_phrase, ger_phrase)]
    #print phrases
    return phrases           
               



def quasi_consecutive(phrase, alignment, null_align):
     #print phrase
     phrase = list(phrase)
     phrase.sort()     
     flag = True
     previous = phrase[0]
     i = 1
     while i < len(phrase):
         if phrase[i] != previous + 1:
	    if len(alignment[previous+1]) != 0:
	        flag = False
	 else:
	    i += 1
	 previous += 1
     return flag	 

def get_bitext(train_input, train_output):
        # O/P: [ ( ['with', 'vibrant', ..], ['mit', 'hilfe',..] ), ([], []) , ..]"""
        bitext = []
        src,tgt = train_input, train_output
        f = open(src)
        src_lines = f.readlines()
        f = open(tgt)
        tgt_lines = f.readlines()
        f.close()
        src_array = []
        tgt_array = []
        for src_line, tgt_line in zip(src_lines, tgt_lines):
           src_words = src_line.split()
           tgt_words = tgt_line.split() +  ['NULL']
           src_array.append(src_words)
           tgt_array.append(tgt_words)
        bitext = zip(src_array,tgt_array)
        return bitext 

import sys

train_input = sys.argv[1]
train_output = sys.argv[2]
alignments_file = sys.argv[3]

f = open(alignments_file)
alignments = f.readlines()
bitext = get_bitext(train_input, train_output)
g = open(sys.argv[4],'w')
extracted_phrases = []
ep_counts = defaultdict(lambda: defaultdict(lambda: 0))
for idx, (es,fs) in enumerate(bitext):
   if idx % 300 == 1:
       print "Processed ", idx, "sentences"
   align = alignments[idx].split()
   phrs = phrase_extract(es, fs, align)
   if len(phrs) > 2:
      for phrase in phrs:
	  ep = ' '.join(k for k in phrase[0])
	  fp = ' '.join(k for k in phrase[1])
	  ep_counts[ep][fp] += 1
	  ep_counts[ep][0] += 1


for ep, fps in ep_counts.iteritems():
        count_e = float(fps[0])
        for fp, count_fe in fps.iteritems():
            if fp == 0:
                continue
            val = math.log(count_fe/count_e)
            if val != 0:
                val *= -1
            g.write(fp + '|||' + ep + '|||' + str(val) + '\n')    
            #print('%s\t%s\t%.4f' % (fp, ep, val), file=outfile)
g.close()            
'''            


     if len(phrs[0]) < 4:
       extracted_phrases.append(phrs)  
counter = Counter(extracted_phrases[0:2])
for (e,f) in counter.keys():
       #print e ,f 
       g.write(e + '|||' + f + '|||' +  str(np.log(counter[(e,f)])) + '\n')
g.close()     
   #raw_input("Press Enter to continue...")
   #print EXT
   #for e, f in EXT:
   #     print("{}{}{}".format(''.join(e), delimiter, ''.join(f))) 
'''
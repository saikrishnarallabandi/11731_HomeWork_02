import sys
from collections import defaultdict
from __future__ import print_function



phrase = sys.argv[1]
output_fst = sys.argv[2]
ep = '<eps>'
last_id = 0

fst_states = {0:defaultdict(lambda: len(fst_states))}

previous = 0

with open(phrase, 'r') as f:
    with open(output_fst, 'w') as out:
        for line in f:
            spl = line.strip().split('|||')

            source_words = spl[0].split()
            target_words = spl[1].split()
            prob = float(spl[2])
            # Add input
            for word in source_words:
                current = fst_states[previous][word+ep]

                if current not in fst_states:
                    print('%d %d %s %s' % (previous, current, word, ep), file=out)
                    fst_states[current] = defaultdict(lambda: len(fst_states))

                previous = current
            # Add output
            for word in target_words:
                current = fst_states[previous][ep+word]

                if current not in fst_states:
                    print('%d %d %s %s' % (previous, current, ep, word), file=out)
                    fst_states[current] = defaultdict(lambda: len(fst_states))

                previous = current

            print('%d %d %s %s %.4f' % (previous, 0, ep, ep, prob), file=out)
            previous = 0

        print('%d %d %s %s' % (0, 0, '</s>', '</s>'), file=out)
        print('%d %d %s %s' % (0, 0, '<unk>', '<unk>'), file=out)
        print('0', file=out)

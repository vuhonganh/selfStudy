"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming.
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""

import itertools



def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    days = (mon, tue, wed, thu, fri) = (2, 3, 4, 5, 6)
    orderings = list(itertools.permutations(days))

    for (Hamming, Knuth, Minsky, Simon, Wilkes) in orderings:
        if Knuth == Simon + 1:  # 6
            for (programmer, writer, manager, designer, _) in orderings:
                if (Knuth == manager + 1 and
                    thu != designer and
                    programmer != Wilkes and
                    writer != Minsky):
                    for (laptop, droid, tablet, iphone, _) in orderings:
                        if (
                            set([laptop, Wilkes]) == set([mon, writer]) and
                            set([programmer, droid]) == set([Wilkes, Hamming]) and
                            (iphone == tue or tablet == tue) and
                            designer != droid and
                            wed == laptop and
                            Knuth != manager and
                            tablet != manager and
                            tablet != fri):
                            return sort_dict({'Hamming': Hamming, 'Knuth': Knuth,
                                              'Minsky': Minsky, 'Simon': Simon,
                                              'Wilkes': Wilkes})


def sort_dict(name_day):
    return sorted(name_day, key=lambda day: name_day[day])

assert logic_puzzle() == ['Wilkes', 'Simon', 'Knuth', 'Hamming', 'Minsky']
print logic_puzzle()


def logic_puzzle_2():  # GENERATOR ver
    "Return a list of the names of the people, in the order they arrive."
    days = (mon, tue, wed, thu, fri) = (2, 3, 4, 5, 6)
    possible_days = list(itertools.permutations(days))

    a_gens = ((Wilkes, Hamming, Minsky, Knuth, Simon, manager, writer, designer, programmer, tablet, droid, iphone, laptop)
              for (Wilkes, Hamming, Minsky, Knuth, Simon) in possible_days
              if Knuth == Simon + 1  # 6
              for (programmer, writer, manager, designer, _) in possible_days
              if Knuth == manager + 1  # 10
              and thu != designer  # 7
              and programmer != Wilkes and writer != Minsky  # 2, 4
              for (laptop, droid, tablet, iphone, _) in possible_days
              if set([laptop, Wilkes]) == set([mon, writer])  # 11
              and set([programmer, droid]) == set([Wilkes, Hamming])  # 3
              and (iphone == tue or tablet == tue)  # 12
              and designer != droid  # 9
              and Knuth != manager and tablet != manager  # 5
              and wed == laptop  # 1
              and fri != tablet  # 8
              )
    (Wilkes, Hamming, Minsky, Knuth, Simon, manager, writer, designer, programmer, tablet, droid, iphone, laptop) = next(a_gens)

    print 'Wilkes = ', Wilkes
    print 'Hamming = ', Hamming
    print 'Minsky = ', Minsky
    print 'Knuth = ', Knuth
    print 'Simon = ', Simon
    print 'tablet = ', tablet
    print 'laptop = ', laptop
    print 'iphone = ', iphone
    print 'droid = ', droid
    print 'manager = ', manager
    print 'writer = ', writer
    print 'programmer = ', programmer
    print 'designer = ', designer


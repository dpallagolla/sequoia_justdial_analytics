from __future__ import print_function
import sys
from difflib import SequenceMatcher


def mean(numbers):
    """
    Returns the arithmetic mean of a numeric list.
    see: http://mail.python.org/pipermail/python-list/2004-December/294990.html
    """
    return float(sum(numbers)) / float(len(numbers))


def median(numbers):
    """
    Return the median of the list of numbers.
    see: http://mail.python.org/pipermail/python-list/2004-December/294990.html
    """

    # Sort the list and take the middle element.
    n = len(numbers)
    copy = sorted(numbers)
    if n & 1:  # There is an odd number of elements
        return copy[n // 2]
    else:
        return (copy[n // 2 - 1] + copy[n // 2]) / 2.0


def textsim(x, y):
    sm = SequenceMatcher(lambda x: x in ". -", x, y)
    return 1 - sm.ratio()

# sim = textsim
sim = lambda x, y: abs(x-y)


def single(a, b):
    return min([sim(ex, ey) for ex in a for ey in b])


def complete(a, b):
    return max([sim(ex, ey) for ex in a for ey in b])


def uclus(a, b):
    return median([sim(ex, ey) for ex in a for ey in b])


def average(a, b):
    return mean([sim(ex, ey) for ex in a for ey in b])


linkage = average


data = [['Lorem'],
        ['ipsum'],
        ['dolor'],
        ['sit'],
        ['amet'],
        ['consectetuer'],
        ['adipiscing'],
        ['elit'],
        ['Ut'],
        ['elit'],
        ['Phasellus'],
        ['consequat'],
        ['ultricies'],
        ['mi'],
        ['Sed'],
        ['congue'],
        ['leo'],
        ['at'],
        ['neque'],
        ['Nullam']]


data = [[_] for _ in [791, 956, 676, 124, 564, 84, 24, 365, 594, 940, 398, 971,
                      131, 365, 542, 336, 518, 835, 134, 391]]


def matrix(data):
    for i, row in enumerate(data):
        for j, cell in enumerate(data[:i]):
            minsim = linkage(row, cell)
            yield (minsim, (i, j))


def step(data):
    while len(data) > 1:
        sorted_matrix = sorted(matrix(data), key=lambda x: x[0])
        closest_items = sorted_matrix[0]
        a, b = closest_items[1]
        new_element = data.pop(max(a, b)) + data.pop(min(a, b))
        data.append(new_element)
        return data


def print_matrix2(data, iteration):
    values = []
    for i, row in enumerate(data):
        simdata = [linkage(row, x) for x in data[:i]]
        values.extend(simdata)
    if values:
        smallest = min(values)

    print('.. csv-table:: Matrix #{}'.format(iteration))
    print('    :header-rows: 1')
    print('    :stub-columns: 1')
    print('    :delim: :\n')
    print('    :' + ': '.join([', '.join([str(x) for x in _]) for _ in data]))
    for i, row in enumerate(data):
        simdata = [linkage(row, x) for x in data[:i]]
        strsimdata = ['**{:.3f}**'.format(_)
                      if _ == smallest else '{:.3f}'.format(_)
                      for _ in simdata]
        foo = ','.join([str(_) for _ in row])
        bar = ': '.join(strsimdata)
        print('    ' + foo, bar, sep=': ')


i = 1
while len(data) > 1:
    print_matrix2(data, i)
    print('\n')
    step(data)
    i += 1
print('\n')
print_matrix2(data, i)
print('\n')

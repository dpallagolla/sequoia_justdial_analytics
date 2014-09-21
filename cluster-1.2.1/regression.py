from cluster import HierarchicalClustering


def test(data, expected):
    cl = HierarchicalClustering(data, lambda x, y: abs(x-y))
    result = cl.getlevel(5)
    print(sorted(data))
    print result
    print expected
    assert result == expected
    print 'ok'


test([12, 34, 23, 32, 46, 96, 13],
     [[96], [46], [12, 13], [23], [34, 32]])


test([24, 84, 124, 131, 134, 336, 365, 365, 391, 398, 518, 542, 564, 594, 676,
      791, 835, 940, 956, 971],
     [[24], [84], [124], [131, 134], [336], [365, 365], [391], [398], [518],
      [542], [564], [594], [676], [791], [835], [940], [956], [971]]
     )

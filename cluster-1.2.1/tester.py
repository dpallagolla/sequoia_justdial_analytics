from cluster import (HierarchicalClustering, KMeansClustering, ClusteringError)
from difflib import SequenceMatcher

data = [24, 84, 124, 131, 134, 336, 365, 365, 391, 398, 518, 542, 564, 594, 676,
        791, 835, 940, 956, 971]
data2 = [791, 956, 676, 124, 564, 84, 24, 365, 594, 940, 398, 971, 131, 365, 542,
         336, 518, 835, 134, 391]

def test2():
        cl = HierarchicalClustering(data, lambda x, y: abs(x - y))
        new_data = []
        for row in cl.getlevel(40):
            print(row)
        print(data)
        #[new_data.extend(_) for _ in cl.getlevel(40)]
        #self.assertEqual(sorted(new_data), sorted(self.__data))

def run(level):
    print('Level = {}'.format(level))
    cluster = HierarchicalClustering(data, lambda x, y: abs(x-y))
    result = cluster.getlevel(level)
    for row in result:
        print(row)

print(data)
run(40)
#print(len(data))

#test2()

cl = HierarchicalClustering(data, lambda x, y: abs(x - y))
cl.getlevel(40)
print(sorted(data) == sorted(data2))

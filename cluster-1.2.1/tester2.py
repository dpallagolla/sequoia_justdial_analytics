from cluster import HierarchicalClustering
from difflib import SequenceMatcher

def sim(x, y):
    sm = SequenceMatcher(lambda x: x in ". -", x, y)
    return round(1 - sm.ratio(), 3)

data = ("Lorem ipsum dolor sit amet, consectetuer adipiscing "
        "elit. Ut elit. Phasellus consequat ultricies mi. Sed congue "
        "leo at neque. Nullam.").split()

def run(data):
    "Basic Hierachical clustering test with strings"
    cl = HierarchicalClustering(data, sim)
    print(cl.getlevel(0.5))

print(data)
print(sorted(data))
run(data)

for i, x in enumerate(data):
    sims = [sim(x, _) for _ in data[:i+1]]
    print(sims)

#
# This is part of "python-cluster". A library to group similar items together.
# Copyright (C) 2006    Michel Albert
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License
# for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

from __future__ import print_function


class Cluster(object):
    """
    A collection of items. This is internally used to detect clustered items
    in the data so we could distinguish other collection types (lists, dicts,
    ...) from the actual clusters. This means that you could also create
    clusters of lists with this class.
    """

    def __repr__(self):
        return "<Cluster@%s(%s)>" % (self.__level, self.__items)

    def __str__(self):
        return self.__str__()

    def __init__(self, level, *args):
        """
        Constructor

        :param level: The level of this cluster. This is used in hierarchical
            clustering to retrieve a specific set of clusters. The higher the
            level, the smaller the count of clusters returned. The level depends
            on the difference function used.
        :param *args: every additional argument passed following the level value
            will get added as item to the cluster. You could also pass a list as
            second parameter to initialise the cluster with that list as content
        """
        self.__level = level
        if len(args) == 0:
            self.__items = []
        else:
            self.__items = list(args)

    def append(self, item):
        """
        Appends a new item to the cluster

        :param item: The item that is to be appended.
        """
        self.__items.append(item)

    def items(self, new_items=None):
        """
        Sets or gets the items of the cluster

        :param new_items: if set, the items of the cluster will be replaced with
            that argument.
        """
        if new_items is None:
            return self.__items
        else:
            self.__items = new_items

    def fullyflatten(self, *args):
        """
        Completely flattens out this cluster and returns a one-dimensional
        list containing the cluster's items. This is useful in cases where
        some items of the cluster are clusters in their own right and you only
        want the items.

        :param *args: only used for recursion.
        """
        flattened_items = []
        if len(args) == 0:
            collection = self.__items
        else:
            collection = args[0].items()

        for item in collection:
            if isinstance(item, Cluster):
                flattened_items = flattened_items + self.fullyflatten(item)
            else:
                flattened_items.append(item)

        return flattened_items

    def level(self):
        """
        Returns the level associated with this cluster.
        """
        return self.__level

    def display(self, depth=0):
        """
        Pretty-prints this cluster. Useful for debuging.
        """
        print(depth * "    " + "[level %s]" % self.__level)
        for item in self.__items:
            if isinstance(item, Cluster):
                item.display(depth + 1)
            else:
                print(depth * "    " + "%s" % item)

    def topology(self):
        """
        Returns the structure (topology) of the cluster as tuples.

        Output from cl.data::

                [<Cluster@0.833333333333(['CVS',
                 <Cluster@0.818181818182(['34.xls',
                 <Cluster@0.789473684211([<Cluster@0.555555555556(['0.txt',
                 <Cluster@0.181818181818(['ChangeLog', 'ChangeLog.txt'])>])>,
                 <Cluster@0.684210526316(['20060730.py',
                 <Cluster@0.684210526316(['.cvsignore',
                 <Cluster@0.647058823529(['About.py', <Cluster@0.625(['.idlerc',
                 '.pylint.d'])>])>])>])>])>])>])>]

        Corresponding output from cl.topo()::

                ('CVS', ('34.xls', (('0.txt', ('ChangeLog', 'ChangeLog.txt')),
                ('20060730.py', ('.cvsignore', ('About.py',
                ('.idlerc', '.pylint.d')))))))
        """

        left = self.__items[0]
        right = self.__items[1]

        if isinstance(left, Cluster):
            first = left.topology()
        else:
            first = left

        if isinstance(right, Cluster):
            second = right.topology()
        else:
            second = right

        return first, second

    def getlevel(self, threshold):
        """
        Retrieve all clusters up to a specific level threshold. This
        level-threshold represents the maximum distance between two clusters.
        So the lower you set this threshold, the more clusters you will
        receive and the higher you set it, you will receive less but bigger
        clusters.

        :param threshold: The level threshold:

        .. note::
            It is debatable whether the value passed into this method should
            really be as strongly linked to the real cluster-levels as it is
            right now. The end-user will not know the range of this value
            unless s/he first inspects the top-level cluster. So instead you
            might argue that a value ranging from 0 to 1 might be a more
            useful approach.
        """

        left = self.__items[0]
        right = self.__items[1]

        # if this object itself is below the threshold value we only need to
        # return it's contents as a list
        if self.level() <= threshold:
            return [self.fullyflatten()]

        # if this cluster's level is higher than the threshold we will
        # investgate it's left and right part. Their level could be below the
        # threshold
        if isinstance(left, Cluster) and left.level() <= threshold:
            if isinstance(right, Cluster):
                return [left.fullyflatten()] + right.getlevel(threshold)
            else:
                return [left.fullyflatten()] + [[right]]
        elif isinstance(right, Cluster) and right.level() <= threshold:
            if isinstance(left, Cluster):
                return left.getlevel(threshold) + [right.fullyflatten()]
            else:
                return [[left]] + [right.fullyflatten()]

        # Alright. We covered the cases where one of the clusters was below
        # the threshold value. Now we'll deal with the clusters that are above
        # by recursively applying the previous cases.
        if isinstance(left, Cluster) and isinstance(right, Cluster):
            return left.getlevel(threshold) + right.getlevel(threshold)
        elif isinstance(left, Cluster):
            return left.getlevel(threshold) + [[right]]
        elif isinstance(right, Cluster):
            return [[left]] + right.getlevel(threshold)
        else:
            return [[left], [right]]

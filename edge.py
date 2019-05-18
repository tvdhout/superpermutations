class Edge:
    def __init__(self, start, end, distance, p):
        self.start_node = start
        self.end_node = end
        self.distance = distance
        self.pheromone = p

    # Sorting stuff:
    def cmp(self, other):
        """
        :type other: Edge
        """
        if self.start_node < other.start_node:
            return -1
        if self.start_node > other.start_node:
            return 1
        else:
            if self.end_node < other.end_node:
                return -1
            if self.end_node > other.end_node:
                return 1
        return 0

    def __str__(self):
        return "'{}' -> '{}' d: {}, p: {}".format(self.start_node, self.end_node, self.distance, self.pheromone)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.cmp(other) == 0

    def __ne__(self, other):
        return self.cmp(other) != 0

    def __lt__(self, other):
        return self.cmp(other) < 0

    def __le__(self, other):
        return self.cmp(other) <= 0

    def __ge__(self, other):
        return self.cmp(other) >= 0

    def __gt__(self, other):
        return self.cmp(other) > 0
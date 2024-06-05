class Relations(object):
    def __init__(self, relation_dict):
        self.relation_dict = relation_dict

    def get_relations(self):
        return self.relation_dict

    def items(self):
        return self.relation_dict.items()

    def get(self, key, default):
        return self.relation_dict.get(key, default)

    def __add__(self, other):
        new_dict = self.relation_dict.copy()
        for (k, v) in other.relation_dict.items():
            if k in self.relation_dict:
                new_dict[k] = new_dict[k].union(set(v))
            else:
                new_dict[k] = set(v)
        return Relations(new_dict)

    def __repr__(self):
        return str(self.relation_dict)


class Tags(object):
    def __init__(self, tag_list=None):
        self._tags = set()
        if tag_list:
            self._tags = set(tag_list)

    def to_list(self):
        return sorted(self._tags)

    def add(self, new_type):
        new_val = self.to_list()
        new_val.append(new_type)
        return Tags(new_val)

    def remove(self, type_):
        new_val = set(self.to_list())
        new_val.discard(type_)
        return Tags(list(new_val))

    def has(self, type_):
        return type_ in self._tags

    def copy(self):
        return Tags(self.to_list())

    def __eq__(self, other):
        if not isinstance(other, Tags):
            return False
        return self.to_list() == other.to_list()

    def __repr__(self):
        return 'Tags({})'.format(self.to_list())
from typing import Optional, List, Union

from sentences.tags.status_tag import StatusTag
from sentences.tags.wordtag import WordTag

Tag = Union[StatusTag, WordTag]


class Tags(object):
    def __init__(self, tag_list: List[Optional[Tag]]=None):
        self._tags = set()
        if tag_list:
            self._tags = set(tag_list)

    def to_list(self):
        return sorted(self._tags)

    def add(self, new_tag: Tag):
        new_val = self.to_list()
        new_val.append(new_tag)
        return Tags(new_val)

    def remove(self, candidate_tag: Tag):
        new_val = set(self.to_list())
        new_val.discard(candidate_tag)
        return Tags(list(new_val))

    def has(self, candidate_tag: Tag):
        return candidate_tag in self._tags

    def copy(self):
        return Tags(self.to_list())

    def __eq__(self, other):
        if not isinstance(other, Tags):
            return False
        return self.to_list() == other.to_list()

    def __repr__(self):
        return 'Tags({})'.format(self.to_list())

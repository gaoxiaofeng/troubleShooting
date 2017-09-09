import re

class _SingleTagPattern(object):
    def __init__(self,pattern):
        super(_SingleTagPattern,self).__init__()
        self.pattern = " " + pattern + " "
    def match(self,tags):

        match = True if re.compile(self.pattern).search(tags) else False
        return match

class _AndTagPattern(object):
    def __init__(self,patterns):
        super(_AndTagPattern,self).__init__()
        self.patterns = patterns
    def match(self,tags):
        matchs = [re.compile(" " + pattern + " ").search(tags)  for pattern in self.patterns]
        return all(matchs)
class _OrTagPattern(object):
    def __init__(self,patterns):
        super(_OrTagPattern,self).__init__()
        self.patterns = patterns
    def match(self,tags):
        matchs = [re.compile(" " + pattern + " ").search(tags)  for pattern in self.patterns]
        return any(matchs)

class TagPattern(object):
    def __init__(self,patterns):
        super(TagPattern,self).__init__()
        self.patterns = patterns
    def match(self,tags):
        tags = " %s "%tags
        if "AND" in self.patterns:
            return  _AndTagPattern(self.patterns.split("AND")).match(tags)
        elif "OR" in self.patterns:
            return _OrTagPattern(self.patterns.split("OR")).match(tags)
        else:
            return  _SingleTagPattern(self.patterns).match(tags)


if __name__ == "__main__":
    tags = "example"
    pattern = "exORexample"
    match = TagPattern(pattern).match(tags)
    print match

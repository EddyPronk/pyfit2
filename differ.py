class Differ(object):
    def __init__(self, compare, desc):
        self.compare2 = compare
        self.desc = desc
        self.missing = []
        self.surplus = []

    def match(self, expected, computed, col):
        if col >= 2:
            self.check(expected, computed)
        else:
            self.keyMap = {}

            self.ePartition(expected, col, self.keyMap, self.desc)
            self.cPartition(computed, col, self.keyMap)
            for key, value in self.keyMap.items():
                eList, cList = value
                if not eList:
                    self.surplus.extend(cList)
                elif not cList:
                    self.missing.extend(eList)
                elif (len(eList) == 1 and len(cList) == 1):
                    self.check(eList, cList)
                else:
                    self.match(eList, cList, col+1)

    def ePartition(self, rows, col, map, desc):
        for row in rows:
            target_type = desc[col]
            v = str(row[col])
            key = target_type(v)
            self.insureKeyExists(map, key)
            map[key][0].append(row)

    def cPartition(self, rows, col, map):
        for row in rows:
            key = row[col]
            self.insureKeyExists(map, key)
            map[key][1].append(row)

    def insureKeyExists(self, map, key):
        if map.has_key(key):
            return
        map[key] = [[], []]

    def check (self, eList, cList):
        for e,c in zip(eList, cList):
            self.compare2(e,c)


class CountList:
    def __init__(self, id, cname, count):
        self.id = id
        self.category = cname
        self.count = count

    def print_status(self):
        print "%s %d" % (self.category, self.count)

    def print_count(self):
        print "%d" % self.count

    def print_category(self):
        print "%s" % self.category

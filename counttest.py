from webExample import db
from webExample import Owners, Categories, Items
import os
import shutil
import uuid
from sqlalchemy import func


class CountList:
    def __init__(self, cname, count):
        self.category = cname
        self.count = count

    def print_status(self):
        print "%s %d" % (self.category, self.count)

    def print_count(self):
        print "%d" % self.count

    def print_category(self):
        print "%s" % self.category


category_count_list = []
categories = db.session.query(Categories).order_by(Categories.category_name).all()
for category in categories:
    item_count = db.session.query(Items).filter_by(category_id=category.category_id).count()
    c = CountList(category.category_name, item_count)
    category_count_list.append (c)

for cl in category_count_list:
    cl.print_status()
    cl.print_category()
    cl.print_count()
    # print
from webExample import db
from webExample import Owners, Categories, Items
import os
import shutil
import uuid


def add_sample_item(o_name, o_email, c_name, i_name, filename):
    """
    Adds an item to the catalog database for testing or creating intial data
    :param o_name: name of owner
    :param o_email: email address of owner
    :param c_name: category for item
    :param i_name: item name
    :param filename: filename for item picture
    :return: none
    """
    owner = db.session.query(Owners).filter_by(email=o_email).first()
    if not owner:
        owner = Owners(owner_name=o_name, email=o_email)
        db.session.add(owner)
        db.session.commit()

    category = db.session.query(Categories).filter_by(category_name=c_name).first()
    if not category:
        category = Categories(category_name=c_name, owner=owner)
        db.session.add(category)
        db.session.commit()

    item = Items(item_name=i_name, owner=owner, category=category)

    unique_filename = create_random_filename(filename)
    file1 = os.path.join(os.path.dirname(__file__), 'webExample/static/', filename)
    file2 = os.path.join(os.path.dirname(__file__), 'webExample/static/images/', unique_filename)
    shutil.copyfile(file1, file2)

    item.picture = os.path.join('/static/images/', unique_filename)
    db.session.add(item)
    db.session.commit()
    return


def create_random_filename(filename):
    """
    Creates a random filename in static/images for a file.  Original filename
    is used for filename extension
    :param filename: filename to use
    :return: random filename with original file extension
    """
    file_name_parts = os.path.splitext(filename)
    filename = '%s%s' % (uuid.uuid4().hex, file_name_parts[1], )
    while os.path.exists(os.path.join(os.path.dirname(__file__),
                                      'webExample/static/images/', filename)):
        filename = '%s%s' % (uuid.uuid4().hex, file_name_parts[1], )

    return filename

#creates database and tables
db.create_all()

#adding test data
# add_sample_item('Erik Arthur', 'erik@arthurweb.org', 'Skateboards',
#                 'Vanguard Loaded', 'default_item.png')
# add_sample_item('Erik Arthur', 'erik@arthurweb.org', 'Skateboards',
#                 'Sector9 Pin', 'default_item.png')
#
# add_sample_item('Erik Arthur', 'erik@arthurweb.org', 'Snowboards',
#                 'Never Summer', 'default_item.png')
# add_sample_item('Erik Arthur', 'erik@arthurweb.org', 'Snowboards',
#                 'Snow Mullet', 'default_item.png')
# add_sample_item('Erik Arthur', 'erik@arthurweb.org', 'Snowboards',
#                 'Prior Split', 'default_item.png')
# add_sample_item('Erik Arthur', 'erik@arthurweb.org', 'Snowboards',
#                 'Burton Fish', 'default_item.png')
#
# add_sample_item('E Arthur', 'erikarthur@gmail.com', 'Candles', 'Small Candle',
#                 'default_item.png')
# add_sample_item('E Arthur', 'erikarthur@gmail.com', 'Candles',
#                 'Medium Candle', 'default_item.png')
# add_sample_item('E Arthur', 'erikarthur@gmail.com', 'Candles', 'Large Candle',
#                 'default_item.png')
#
# add_sample_item('Zach Arthur', 'zmaster97@live.com', 'Instruments',
#                 'Alto Sax', 'default_item.png')
# add_sample_item('Zach Arthur', 'zmaster97@live.com', 'Instruments',
#                 'Tenor Sax', 'default_item.png')
# add_sample_item('Zach Arthur', 'zmaster97@live.com', 'Instruments', 'Bassoon',
#                 'default_item.png')
#
# add_sample_item('Zach Arthur', 'zmaster97@live.com', 'Video-Games', 'Halo V',
#                 'default_item.png')
# add_sample_item('Zach Arthur', 'zmaster97@live.com', 'Video-Games', 'PGR III',
#                 'default_item.png')
# add_sample_item('Zach Arthur', 'zmaster97@live.com', 'Video-Games', 'CoD IV',
#                 'default_item.png')
#
# add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Soccer', 'Cleats',
#                 'default_item.png')
# add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Soccer', 'Jersey',
#                 'default_item.png')
# add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Soccer', 'Shorts',
#                 'default_item.png')
# add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Soccer', 'Ball',
#                 'default_item.png')
#
# add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Recipes', 'Soup',
#                 'default_item.png')
# add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Recipes', 'Bread',
#                 'default_item.png')
# add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Recipes', 'Chicken',
#                 'default_item.png')
# add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Recipes', 'Cookies',
#                 'default_item.png')
#
# add_sample_item('Jack Arthur', 'jwa@arthurweb.org', 'TV-Programs',
#                 '60 Minutes', 'default_item.png')
# add_sample_item('Jack Arthur', 'jwa@arthurweb.org', 'TV-Programs', 'Dateline',
#                 'default_item.png')
# add_sample_item('Jack Arthur', 'jwa@arthurweb.org', 'TV-Programs',
#                 'Fox and Friends', 'default_item.png')
#
# add_sample_item('Jack Arthur', 'jwa@arthurweb.org', 'Remote-Controls', 'TV',
#                 'default_item.png')
# add_sample_item('Jack Arthur', 'jwa@arthurweb.org', 'Remote-Controls', 'VCR',
#                 'default_item.png')
# add_sample_item('Jack Arthur', 'jwa@arthurweb.org', 'Remote-Controls', 'DVD',
#                 'default_item.png')
#
# add_sample_item('Carol Arthur', 'carthur@hotmail.com', 'Quilting', 'Cloth',
#                 'default_item.png')
# add_sample_item('Carol Arthur', 'carthur@hotmail.com', 'Quilting', 'Fleece',
#                 'default_item.png')
#
# add_sample_item('Carol Arthur', 'carthur@hotmail.com', 'Sewing', 'Needles',
#                 'default_item.png')
# add_sample_item('Carol Arthur', 'carthur@hotmail.com', 'Sewing', 'Thread',
#                 'default_item.png')
# add_sample_item('Carol Arthur', 'carthur@hotmail.com', 'Sewing',
#                 'Sewing Machine', 'default_item.png')
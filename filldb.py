from webExample import db
from webExample import Owners, Categories, Items

def add_sample_item(o_name, o_email, c_name,i_name):

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
    item.picture = '/static/images/default_item.png'
    db.session.add(item)
    db.session.commit()
    return

db.create_all()

add_sample_item('Erik Arthur', 'erik@arthurweb.org', 'Skateboards', 'Vanguard Loaded')
add_sample_item('Erik Arthur', 'erik@arthurweb.org', 'Skateboards', 'Sector9 Pin')

add_sample_item('Erik Arthur', 'erik@arthurweb.org', 'Snowboards', 'Never Summer')
add_sample_item('Erik Arthur', 'erik@arthurweb.org', 'Snowboards', 'Snow Mullet')
add_sample_item('Erik Arthur', 'erik@arthurweb.org', 'Snowboards', 'Prior Split')
add_sample_item('Erik Arthur', 'erik@arthurweb.org', 'Snowboards', 'Burton Fish')

add_sample_item('E Arthur', 'erikarthur@gmail.com', 'Candles', 'Small Candle')
add_sample_item('E Arthur', 'erikarthur@gmail.com', 'Candles', 'Medium Candle')
add_sample_item('E Arthur', 'erikarthur@gmail.com', 'Candles', 'Large Candle')

add_sample_item('Zach Arthur', 'zmaster97@live.com', 'Instruments', 'Alto Sax')
add_sample_item('Zach Arthur', 'zmaster97@live.com', 'Instruments', 'Tenor Sax')
add_sample_item('Zach Arthur', 'zmaster97@live.com', 'Instruments', 'Bassoon')

add_sample_item('Zach Arthur', 'zmaster97@live.com', 'Video-Games', 'Halo V')
add_sample_item('Zach Arthur', 'zmaster97@live.com', 'Video-Games', 'PGR III')
add_sample_item('Zach Arthur', 'zmaster97@live.com', 'Video-Games', 'CoD IV')

add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Soccer', 'Cleats')
add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Soccer', 'Jersey')
add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Soccer', 'Shorts')
add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Soccer', 'Ball')

add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Recipes', 'Soup')
add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Recipes', 'Bread')
add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Recipes', 'Chicken')
add_sample_item('Maddie Arthur', 'madz1313@live.com', 'Recipes', 'Cookies')

add_sample_item('Jack Arthur', 'jwa@arthurweb.org', 'TV-Programs', '60 Minutes')
add_sample_item('Jack Arthur', 'jwa@arthurweb.org', 'TV-Programs', 'Dateline')
add_sample_item('Jack Arthur', 'jwa@arthurweb.org', 'TV-Programs', 'Fox and Friends')

add_sample_item('Jack Arthur', 'jwa@arthurweb.org', 'Remote-Controls', 'TV')
add_sample_item('Jack Arthur', 'jwa@arthurweb.org', 'Remote-Controls', 'VCR')
add_sample_item('Jack Arthur', 'jwa@arthurweb.org', 'Remote-Controls', 'DVD')

add_sample_item('Carol Arthur', 'carthur@hotmail.com', 'Quilting', 'Cloth')
add_sample_item('Carol Arthur', 'carthur@hotmail.com', 'Quilting', 'Fleece')

add_sample_item('Carol Arthur', 'carthur@hotmail.com', 'Sewing', 'Needles')
add_sample_item('Carol Arthur', 'carthur@hotmail.com', 'Sewing', 'Thread')
add_sample_item('Carol Arthur', 'carthur@hotmail.com', 'Sewing', 'Sewing Machine')
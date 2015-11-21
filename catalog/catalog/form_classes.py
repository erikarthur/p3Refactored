from wtforms import Form, StringField, IntegerField, validators

class Category(Form):
    category_name = StringField(u'CategoryName',
                                validators=[validators.input_required()])

class Catalog_Item(Form):
    id = IntegerField()
    name = StringField(u'Name', validators=[validators.input_required()])
    description = StringField(u'Description',
                              validators=[validators.input_required()])
    picture = StringField(u'Picture',
                          validators=[validators.input_required()])

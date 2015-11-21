from wtforms import Form, StringField, IntegerField, validators, HiddenField, SubmitField

class Category(Form):
    category_name = StringField(u'CategoryName',
                                validators=[validators.input_required()])
    email = HiddenField()
    submit = SubmitField("Add Category")

class Catalog_Item(Form):
    name = StringField(u'Name', validators=[validators.input_required()])
    description = StringField(u'Description')
    picture = StringField(u'Picture')
    id = HiddenField()
    category_id = HiddenField()
    submit = SubmitField("Add Item")
    #description = StringField(u'Description', validators=[validators.input_required()])
    #picture = StringField(u'Picture', validators=[validators.input_required()])

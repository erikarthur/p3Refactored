from wtforms import Form, StringField, IntegerField, validators, HiddenField
from wtforms import SubmitField, FileField, SelectField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, Optional
from markupsafe import Markup, escape


class Category(Form):
    category_name = StringField(u'CategoryName',
                                validators=[DataRequired(message="Category Name is Required"),
                                            Length(min=1, max=80, message="Category name must be between 2 and 80 characters")])
    email = HiddenField()
    submit = SubmitField("Add Category")

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)


class Delete_Category(Form):
    categories = SelectMultipleField(
        'Categories',
        coerce=int,
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Delete Categories')

    def __html__(self):
        fields = [u"%s %s" % (field.label, field) for field in self.fields]
        return Markup(u"".join(fields))


class Catalog_Item(Form):
    name = StringField(u'Name',
                       validators=[DataRequired(message="Name is required"),
                        Length(max=80, message="Max lenght is 80 characters")])
    description = StringField(u'Description',
                              validators=[Optional(),
                               Length(max=250, message="Max characters is 250")])
    picture = FileField(u'Upload Image')
    id = HiddenField()
    category_id = HiddenField()
    category_name = HiddenField()
    submit = SubmitField('Add Item')
    category_select = SelectField('Category', coerce=int)

    def __init__(self, *args, **kwargs):
        super(Catalog_Item, self).__init__(*args, **kwargs)

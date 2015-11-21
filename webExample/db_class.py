from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Owners(Base):
    __tablename__ = 'owners'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    owner_id = Column(Integer, ForeignKey('owners.id'))
    owner = relationship(Owners)


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    picture = Column(String(250))
    owner_id = Column(Integer, ForeignKey('owners.id'))
    owner = relationship(Owners)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Categories)

def add_items(o_name, o_email, c_name,i_name):

    #stmt = exists().where(email=o_email)

    owner = session.query(db_classes.Owners).filter_by(email=o_email).first()
    if not owner:
        owner = db_classes.Owners(name=o_name, email=o_email)
        session.add(owner)
        session.commit()

    category = session.query(db_classes.Categories).filter_by(name=c_name).first()
    if not category:
        category = db_classes.Categories(name=c_name, owner=owner)
        session.add(category)
        session.commit()

    item = db_classes.Items(name=i_name, owner=owner, category=category)
    session.add(item)
    session.commit()
    return

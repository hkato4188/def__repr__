

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData



convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

# https://learning.flatironschool.com/courses/6809/assignments/251881?module_item_id=594735
post_tag = db.Table('post_tags',
                    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                    db.Column('tag_id', db
                    .Integer, db.ForeignKey('tags.id'))
                    )



class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    # Add relationship
    comments = db.relationship('Comment', backref='post')
    tags = db.relationship('Tag', secondary=post_tag, backref='posts')
    # Add serialization rules
    serialize_rules = ("-tags.post","-comments.post")
    
    def __repr__(self):
        return f'<Post "{self.title}">'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return f'<Tag "{self.name}">' 


class Comment(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    serialize_rules = ("-post.comments", "-user.comments")
    def __repr__(self):
        return f'<Comment "{self.content[:20]}...">'


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    

    # Add relationshipmis
    tags = db.relationship(
        'Tag', backref='user')
    # Add serialization rules
    serialize_rules = ("-tags.user",)
    # Add validation

    @validates('name')
    def validate_name(self, db_column, value):
        if db_column == 'name':
            if type(value) == str and len(value) > 0:
                return value
            else:
                raise ValueError('A user needs a name of type string')
        

class Tag(db.Model, SerializerMixin):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # Add relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    # Add serialization rules
    serialize_rules = ("-post.tags", "-user.tags")
    # Add validation

    @validates('name')
    def validate_name(self, db_column, name):
        if name and len(name) > 0:
            return name
        else:
            raise ValueError('A tag must have a name')

    @validates('user_id')
    def validate_user_id(self, db_column, user_id):
        user = User.query.filter(User.id == user_id)
        if not user or user_id == None:
            raise ValueError('A tag must have a valid user id')
        else:
            return user_id

    @validates('post_id')
    def validate_post_id(self, db_column, post_id):
        post = Post.query.filter(Post.id == post_id)
        if not post or post_id == None:
            raise ValueError('A tag must have a valid post id')
        else:
            return post_id


# add any models you may need.

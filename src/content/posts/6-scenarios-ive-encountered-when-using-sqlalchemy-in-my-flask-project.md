---
title: "6 scenarios I’ve encountered when using SQLAlchemy in my Flask project"
seoTitle: "SQLAlchemy with Flask: 6 Real-World ORM Scenarios"
seoDescription: "Covers six practical SQLAlchemy patterns in a Flask app: many-to-many relationships, slug generation, object comparison, event-based seeding, and..."
datePublished: 2020-03-23T23:21:35.094Z
dateUpdated: 2026-03-02T10:51:02.091Z
cover: "/images/6-scenarios-ive-encountered-when-using-sqlalchemy-in-my-flask-project/cover.png"
series: "python"
hashnodeCuid: "clfmnhnz6000309jt0wxo5r8z"
---

A couple of years ago, inspired by some interesting Python courses I’ve followed online, I decided to embark on a mini-adventure — building my [blog engine](https://github.com/cnstlungu/samo-cms) from scratch for practice. I’ll delve more into the reasoning behind this choice in a later post, but let’s say for now that I wanted something common yet extensive enough so I could be exposed to as many challenges as a real project would pose.

I’ve picked [Flask](https://palletsprojects.com/projects/flask/) as my web application framework — I enjoyed its simplicity and light weight. Now, coming from a quite different background (Business Intelligence/Data Analytics) I was pleased to find out how rich the ecosystem was and how you can mix and match different components. One particular toolkit has proven a life savior: [SQLAlchemy](https://www.sqlalchemy.org/).

SQLAchemy is, in its maintainers’ own words,

> the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

In other words, it bridges the gap between Python objects and database entries, and it packs quite several features. Besides that, it integrates rather nicely with Flask using [an extension](https://flask-sqlalchemy.palletsprojects.com/en/2.x/). As always, there are alternatives and downsides to a particular choice, so please feel free to refer to [this page](https://www.fullstackpython.com/object-relational-mappers-orms.html) for more details.

Anyway, as a person with relational database experience but limited developer acumen, I found it refreshingly straightforward — just what you’d expect from a Python project. We’re now going to look at several scenarios I’ve encountered while working on my application that SQLAlchemy helped me out with.

Before we dig into the details, let’s have a look at how the data model looks for my blog engine. So a user can have several roles, based on which he or she may create and edit posts, assign tags to them or comment.

***Please note that all the code used in this article is available***[***here***](https://github.com/cnstlungu/samo-cms/blob/master/samo/models.py)***.***

#### Managing many-to-many relationships

So you have a many-to-many relationship between users and roles, just as you do with posts and tags. How do you leverage the toolkit to make it all work together?

Well, in the database world, you’d create an additional table to store these relationships — and SQL Alchemy lets you do just that. We define a secondary table that will host the relations between the posts and tags.

Thus, accessing the *tags* attribute on a *Post* object would return all the tags that a particular Post has, whereas using the *posts* one on a *Tag* would return the posts associated with that particular tag. **Very** useful particularly in Jinja2 templates.

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetimedb = SQLAlchemy(app)
TAGS = db.Table('post_tag',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')))


class Post(db.Model):
    """
    Defines the Post object.
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.UnicodeText(140))
    slug = db.Column(db.UnicodeText(200))
    content = db.Column(db.UnicodeText())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=TAGS, backref='posts')
    comments = db.relationship('Comment', backref='posts', cascade="all, delete-orphan")
    publish = db.Column(db.Boolean)

    def __repr__(self):
        return "<Post '{}': '{}'>".format(self.title, self.date)


class Tag(db.Model):
    """
    Defines the Tag object.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True, index=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
```

#### Creating a post slug

Next, for every post that is added, I needed a friendly phrase that would also be a valid URL for my post — also called a **slug**. This was solved using the *observes* decorator, which tracked my title and automatically generated a *slug* from it using a regular expression. This would take care of non-alphanumeric characters and output a nice valid URL for my post.

```python
from datetime import datetime
import re
from sqlalchemy_utils import observes
from flask_sqlalchemy import SQLAlchemydb = SQLAlchemy(app)class Post(db.Model):
    """
    Defines the Post object.
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.UnicodeText(140))
    slug = db.Column(db.UnicodeText(200))
    content = db.Column(db.UnicodeText())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=TAGS, backref='posts')
    comments = db.relationship('Comment', backref='posts', cascade="all, delete-orphan")
    publish = db.Column(db.Boolean)

    @observes('title')
    def compute_slug(self, title):
        """
        Computes the slug - shortened version of the title.
        :param title:  string, title to be shortened
        :return: string, resulting slug
        """
        self.slug = re.sub(r'[^\w]+', '-', title.lower())

    def __repr__(self):
        return "<Post '{}': '{}'>".format(self.title, self.date)
```

#### Comparing two objects

Say you need to compare two SQL Alchemy objects — in my case, I needed to tell if a user’s role is the admin role. The comparison relies on the *\_\_eq\_\_* special method to assess equality between objects, whereas the *\_\_hash\_\_* is a good addition [that should return the same value for](https://stackoverflow.com/questions/4005318/how-to-implement-a-good-hash-function-in-python) equal objects.

```python
from flask_sqlalchemy import SQLAlchemydb = SQLAlchemy(app)class Role(db.Model):
    """
    Defines the Role model
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return "<Role '{}'>".format(self.name)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return (self.name == other or
                self.name == getattr(other, 'name', None))

    def __hash__(self):
        return hash(self.name)
```

#### Inserting initial values

Another interesting scenario I’ve had to deal with is setting up the basic user roles. One way that I found elegant was to listen for an event on the Role table (in this case, it gets created) and insert the three roles I needed there automatically. This way their presence would be guaranteed.

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import eventdb = SQLAlchemy(app)@event.listens_for(Role.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    """
    Ensures the 3 basic roles required are created
    :rtype: object
    """
    db.session.add(Role(name='Admin', description='admin'))
    db.session.add(Role(name='Contributor', description='contributor'))
    db.session.add(Role(name='User', description='regular user'))
    db.session.commit()
```

#### Returning 'n' newest posts

Now, picture this scenario. You’ve got a front page that displays the *n* newest blog entries. This number can be tweaked based on the front page UI, but here’s how I chose to implement it with a static method on the *Post* class.

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import descdb = SQLAlchemy(app)class Post(db.Model):
    """
    Defines the Post object.
    """
    ...
    @staticmethod
    def newest(num):
        """
        Returns latest n posts.
        :param num: int, number of post to be returned.
        :return: n Post(s)
        """
        return Post.query.order_by(desc(Post.date)).limit(num)

    def __repr__(self):
        return "<Post '{}': '{}'>".format(self.title, self.date)
```

#### Getting-or-creating a Tag

Again, this might not be directly related to SQLAlchemy, but at one point I needed a method to provide me with a Tag and if it didn’t exist, create it. This would save the hassle of checking if it exists down the line.

I’ve done this using a static method on the *Tag* class itself.

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFounddb = SQLAlchemy(app)class Tag(db.Model):
    """
    Defines the Tag object.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True, index=True)

    @staticmethod
    def get_or_create(name):
        """
        Gets or creates a tag with a given name.
        :param name: string, name of the tag to be found or created if it doesn't exist.
        :return:  Tag
        """
        try:
            return Tag.query.filter_by(name=name).one()
        except NoResultFound:
            return Tag(name=name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
```

### Conclusion

To conclude, these were some scenarios I’ve encountered while working with SQLAlchemy. There is more to learn about it, but it’s a great addition to every Python developer’s toolbox, even for beginners.

Thank you for reading and I’m looking forward to hearing about your own experiences with SQLAlchemy or other Python ORMs.

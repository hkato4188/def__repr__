#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import User, Post, Comment, Tag, post_tag


def create_posts():
    posts = []
    for _ in range(20):
        p = Post(
            name=fake.first_name(),
            distance_from_earth=str(randint(100000, 10000000000)),
            nearest_star=fake.first_name(),
        )
        posts.append(p)

    return posts


def create_scientists():
    scientists = []
    names = []
    for _ in range(5):
        name = fake.name()
        while name in names:
            name = fake.name()
        names.append(name)

        s = Scientist(
            name=name,
            field_of_study=fake.sentence(),
        )
        scientists.append(s)

    return scientists


def create_missions(planets, scientists):
    missions = []
    for _ in range(20):
        m = Mission(
            name=fake.sentence(nb_words=3),
            planet_id=rc(planets).id,
            scientist_id=rc(scientists).id
        )
        missions.append(m)
    return missions


if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!
        print("Clearing db...")
        User.query.delete()
        Post.query.delete()
        Tag.query.delete()
        db.drop(post_tag)

        print("Seeding posts...")
        posts = create_posts()
        db.session.add_all(posts)
        db.session.commit()

        print("Seeding users...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()

        print("Seeding comments...")
        comments = create_comments(posts, users)
        db.session.add_all(comments)
        db.session.commit()

        print("Done seeding!")
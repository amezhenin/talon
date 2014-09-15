"""
Factories for models
"""

import factory
from django.core import files
from django.contrib.auth.models import User
from talon.models import Todo


class UserFactory(factory.Factory):
    """
    Factory for creating users
    """

    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'user{0}'.format(n))
    password = '123456'
    email = factory.Sequence(lambda n: 'user{0}@example.com'.format(n))


class TodoFactory(factory.Factory):
    """
    Factory for creating Todos
    """

    FACTORY_FOR = Todo

    user = factory.LazyAttribute(lambda a: UserFactory())  # factory.SubFactory(UserFactory)
    completed = False
    priority = 5
    text = "This is important task"

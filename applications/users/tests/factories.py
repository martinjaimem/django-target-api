import factory
from faker import Factory, Faker
from faker.providers import misc, person

from applications.users.models import User

fake = Faker()
fake.add_provider(person)
fake.add_provider(misc)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = fake.email()
    password = fake.password(length=8)
    name = fake.name()
    gender = factory.Iterator(User.Gender.choices, getter=lambda x: x[0])

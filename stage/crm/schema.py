from tkinter import FLAT
import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from django.contrib.auth.hashers import check_password

from crm.forms import RegisterForm
from .models import User


class UserType(DjangoObjectType):

    class Meta:
        model = User
        fields = ("id", "email", "name", "password")


class Qeury(graphene.ObjectType):
    all_Users = graphene.List(UserType)

    def resolve_all_Users(self, info, **kwargs):
        return User.objects.all()


def checkLogin(email, password):
    #returns an empty array(falsy) if it cant find the email
    user = list(User.objects.filter(email=email))
    if user:
        #compares the hashed passwords
        return check_password(password, user[0].password)

    return user


def userExists(email, name):
    #checks if user already exits in the database
    email = list(User.objects.filter(email=email))
    name = list(User.objects.filter(name=name))
    if not email and not name:
        return False
    else:
        if name:
            return name[0].name
        else:
            return email[0].email


class CreateUser(DjangoModelFormMutation):
    #gets fields from form
    class Meta:
        form_class = RegisterForm


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Qeury, mutation=Mutation)


def getAll():
    #executes query to return a dict
    return schema.execute("{ allUsers {email,name} }").data

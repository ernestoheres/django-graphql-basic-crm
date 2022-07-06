from distutils.log import error
from django.shortcuts import render, redirect
from .schema import getAll, checkLogin, userExists
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password


# Create your views here.
def index(request):

    return render(request, 'crm/index.html')


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            #hashes password and compares it with the hash in the database
            print(form.data['email'])
            authenticated = checkLogin(form.data['email'],
                                       form.data['password'])

            #Goes to homepage if the login was succesfull
            if authenticated:
                request.session['login'] = True
                return redirect('/')
            #Goes back to the loginpage
            else:
                error = "password or username is invalid"
                return render(request, 'crm/login.html', {"error": error})

    return render(request, 'crm/login.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            exists = userExists(form.data['email'], form.data['name'])
            if exists:
                error = exists + " already exists"
                return render(request, 'crm/register.html', {'error': error})

            #hashes password
            sForm = form.save(commit=False)
            sForm.password = make_password(sForm.password)
            sForm.save()
            return redirect('/')
    else:
        form = RegisterForm
        return render(request, 'crm/register.html', {'form': form})


def users(request):
    #get all users and pass it to template
    data = getAll()['allUsers']
    return render(request, 'crm/users.html', {'data': data})


def logout(request):
    #logs you out
    request.session["login"] = False
    return redirect('/')


def securepage(request):
    #if you are logged in you go the securepage otherwise to the login page
    if request.session["login"]:
        return render(request, 'crm/secure.html')
    else:
        return redirect('/login')

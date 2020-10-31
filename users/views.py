from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from  django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from tidp.models import Project


User = get_user_model()

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_active:
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect('home')

    return render(request, 'login.html', {'errors': ['Login details are wrong']})


def signout(request):
    logout(request)
    return redirect('login')


# Create your views here.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def index(request):

    users = User.objects.all()

    if request.method == 'GET':
        return render(request, 'users/index.html', {'users': users})

    email = request.POST['email']

    try:
        validate_email(email)
        password = User.objects.make_random_password()
        User.objects.create_user(email, email, password)
        _send_registration_email(email, password)
        return render(request, 'users/index.html', {'users': users})
    except ValidationError:
        return render(request, 'users/index.html', {'users': users, 'errors': ['Invalid email']})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete(request, id):
    users = User.objects.all()
    try:

        user = User.objects.get(id=id)
        user.is_active = 0
        user.save(update_fields=['is_active'])
        return redirect('/users/')
        # return render(request, 'users/index.html', {'users': users, 'success': 'User has been deleted.'})
    except Exception as e:
        print(e)
        return redirect('/users/')
        # return render(request, 'users/index.html', {'users': users, 'errors': ['Something went wrong. Please try again later.']})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def enable(request, id):
    users = User.objects.all()
    try:

        user = User.objects.get(id=id)
        user.is_active = 1
        user.save(update_fields=['is_active'])
        return redirect('/users/')
        # return render(request, 'users/index.html', {'users': users, 'success': 'User has been deleted.'})
    except Exception as e:
        return redirect('/users/')
        # return render(request, 'users/index.html', {'users': users, 'errors': ['Something went wrong. Please try again later.']})

def _send_registration_email(email, password):
    message = '''
    Hello,

    An Auto-BIM admininstrator has created an account for you on http://35.209.23.198.

    Below are your login details. You'll be requested upon login to change your password.

    Username: Your email address
    Password: {0}

    Thanks,
    Auto-BIM Team.
    '''.format(password)
    send_mail('Auto-BIM Registration', message, 'farouqzaib@gmail.com', [email], fail_silently=False)


# @login_required
def change_password(request):

    if request.method == 'GET':
        return render(request, 'users/change_password.html')

    password1 = request.POST['password1']
    password2 = request.POST['password2']

    if password1 != password2:
        return render(request, 'users/change_password.html', {'errors': ['Passwords do not match']})

    if len(password1) < 8:
        return render(request, 'users/change_password.html', {'errors': ['Password must be at least 8 characters']})

    try:

        user = request.user

        user.password = make_password(password1)
        user.save(update_fields=['password'])
        return redirect('/')
    except:
        return render(request, 'users/change_password.html', {'errors': ['Something went wrong. Please try again later']})



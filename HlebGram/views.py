import json
import os
import re
from datetime import datetime
from ast import literal_eval
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from .models import GramUser, Images


def startpage(requests):
    if requests.user.is_authenticated:
        return redirect('homepage')
    else:
        return render(requests, 'startpage.html')


def loginpage(requests):
    if requests.method == 'GET':
        return render(requests, 'loginpage.html')
    else:
        user = authenticate(
            requests, username=requests.POST['username'], password=requests.POST['password'])
        if user is None:
            data = {
                'error': 'Username or password did not match!'
            }
            return render(requests, 'loginpage.html', data)
        else:
            login(requests, user)
            return redirect('startpage')


def signuppage(requests):
    if requests.method == 'GET':
        return render(requests, 'signuppage.html')
    else:
        if re.search(r'[^a-zA-Z0-9]', requests.POST['username']):
            data = {
                'error': "You used wrong symbols"
            }
            return render(requests, 'signuppage.html', data)
        elif requests.POST['username'] == '':
            data = {
                'error': "You didn't write username"
            }
            return render(requests, 'signuppage.html', data)
        elif len(requests.POST['password1']) < 8:
            data = {
                'error': "Your password is short"
            }
            return render(requests, 'signuppage.html', data)
        elif requests.POST['password1'] != requests.POST['password2']:
            data = {
                'error': "Confirm password is wrong"
            }
            return render(requests, 'signuppage.html', data)
        else:
            try:
                user = GramUser.objects.create_user(
                    requests.POST['username'], password=requests.POST['password1'])
                user.save()
                login(requests, user)
                return redirect('startpage')
            except IntegrityError:
                data = {
                    'error': "This username is already used"
                }
                return render(requests, 'signuppage.html', data)


@login_required
def logoutpage(requests):
    if requests.method == 'GET':
        return redirect('startpage')
    else:
        logout(requests)
        return redirect('startpage')


@login_required
def homepage(requests):
    subscriptions = literal_eval(get_object_or_404(
        GramUser, pk=requests.user.pk).subscriptions)
    images = []

    for i in subscriptions:
        photos = Images.objects.filter(user=i).order_by('-name')
        for ii in photos:
            images.append(ii)
    data = {
        'images': images
    }
    return render(requests, 'homepage.html', data)


@login_required
def profilepage(requests):
    try:
        os.mkdir(f'HlebGram/media/images/{requests.user.pk}')
    except:
        pass

    images = Images.objects.filter(user=requests.user).order_by('-name')
    data = {
        'change_btn': 'Change Profile',
        'pk': requests.user.pk,
        'add_photo_btn': 'Add Photo',
        'images': images
    }
    return render(requests, 'profilepage.html', data)


@login_required
def changepage(requests):
    if requests.method == 'GET':
        return render(requests, 'changeprofilepage.html')
    else:
        try:
            user = get_object_or_404(GramUser, pk=requests.user.pk)
            user.description = requests.POST['new_description']
            user.save()
        except:
            pass
        try:
            ext = str(requests.FILES['new_photo']).split('.')[1]
            with open(f'HlebGram/media/profile_images/{requests.user.pk}.{ext}', 'wb+') as file:
                for i in requests.FILES['new_photo'].chunks():
                    file.write(i)
            user = get_object_or_404(GramUser, pk=requests.user.pk)
            user.profile_photo = f'profile_images/{requests.user.pk}.{ext}'
            user.save()

        except:
            pass

        return redirect('profilepage')


@login_required
def userpage(requests, user_pk):
    if requests.method == 'GET':
        profile_user = get_object_or_404(GramUser, pk=user_pk)

        if requests.user.username == profile_user.username:
            return redirect('profilepage')
        else:
            if requests.user.pk not in json.loads(profile_user.subscribers):
                state = 'Subscribe'
                state_value = 1
            else:
                state = 'UnSubscribe'
                state_value = 0

            images = Images.objects.filter(user=user_pk).order_by('-name')

            data = {
                'username': profile_user.username,
                'description': profile_user.description,
                'photo': profile_user.profile_photo.url,
                'state': state,
                'state_value': state_value,
                'pk': user_pk,
                'images': images
            }
            return render(requests, 'userpage.html', data)
    else:
        if requests.POST['state_value'] == '1':
            user = get_object_or_404(GramUser, pk=user_pk)
            subscribers = json.loads(user.subscribers)
            subscribers.append(requests.user.pk)
            user.subscribers = json.dumps(subscribers)
            user.save()

            user = get_object_or_404(GramUser, pk=requests.user.pk)
            subscriptions = json.loads(user.subscriptions)
            subscriptions.append(user_pk)
            user.subscriptions = json.dumps(subscriptions)
            user.save()
        elif requests.POST['state_value'] == '0':
            user = get_object_or_404(GramUser, pk=user_pk)
            subscribers = json.loads(user.subscribers)
            subscribers.remove(requests.user.pk)
            user.subscribers = json.dumps(subscribers)
            user.save()

            user = get_object_or_404(GramUser, pk=requests.user.pk)
            subscriptions = json.loads(user.subscriptions)
            subscriptions.remove(user_pk)
            user.subscriptions = json.dumps(subscriptions)
            user.save()

        return redirect('.')


@login_required
def subscriberspage(requests, user_pk):
    accounts_pk = json.loads(get_object_or_404(
        GramUser, pk=user_pk).subscribers)

    accounts = []
    for i in accounts_pk:
        accounts.append(get_object_or_404(GramUser, pk=i))

    data = {
        'accounts': accounts
    }
    return render(requests, 'subscriberspage.html', data)


@login_required
def subscriptionspage(requests, user_pk):
    accounts_pk = json.loads(get_object_or_404(
        GramUser, pk=user_pk).subscriptions)

    accounts = []
    for i in accounts_pk:
        accounts.append(get_object_or_404(GramUser, pk=i))

    data = {
        'accounts': accounts
    }
    return render(requests, 'subscriberspage.html', data)


@login_required
def searchpage(requests):
    try:
        if requests.GET['s'] == '':
            return render(requests, 'searchpage.html')
        users = GramUser.objects.all()
        search_result = []
        for i in users:
            if requests.GET['s'].upper() in i.username.upper():
                search_result.append(i)
        data = {
            'result': search_result,
            'get': requests.GET['s']
        }
        return render(requests, 'searchpage.html', data)
    except:
        return render(requests, 'searchpage.html')


def addphotopage(requests):
    if requests.method == 'GET':
        return render(requests, 'addphotopage.html')
    else:
        try:
            image = Images()
            image.user = requests.user

            ext = str(requests.FILES['add_photo']).split('.')[1]
            name = f'{datetime.now().strftime("%Y%m%w%d%H%M%S%f")}.{ext}'
            path = f'/media/images/{requests.user.pk}/'
            with open(f'HlebGram{path}{name}', 'wb+') as file:
                for i in requests.FILES['add_photo'].chunks():
                    file.write(i)

            image.path = path
            image.name = name
            image.description = requests.POST['description']
            image.save()
        except:
            pass

        return redirect('profilepage')


@login_required
def photopage(requests, pk):
    photo = get_object_or_404(Images, pk=pk)
    if photo.user == requests.user:
        data = {
            'delete_btn': 'Delete Photo',
            'photo': photo,
            'pk': pk
        }

        return render(requests, 'photopage.html', data)
    else:
        data = {
            'photo': photo,
            'pk': pk
        }

        return render(requests, 'photopage.html', data)


@login_required
def deletepage(requests):
    if requests.method == "POST":
        photo = get_object_or_404(Images, pk=int(requests.POST['delete']))
        if photo.user.pk == requests.user.pk:
            photo.delete()
            return redirect('profilepage')
        else:
            redirect('profilepage')

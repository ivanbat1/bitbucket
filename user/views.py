import random
from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import *
from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator

def home(request):
    # for i in range(10000):
    #     GeneralR.objects.create(name='Frontend{}'.format(i), position="front{}".format(i), parent_id=46613)
    template = 'home.html'
    username = auth.get_user(request).username
    contact_list = GeneralR.objects.filter(parent__isnull=True)
    paginator = Paginator(contact_list, 100)
    page = request.GET.get('page')
    all_generals = paginator.get_page(page)
    if request.is_ajax():
        template = 'filter.html'
        name = request.GET.get('name')
        position = request.GET.get('position')
        salary = request.GET.get('salary')
        if name:
            all_generals = GeneralR.objects.select_related().filter(name__icontains=name)
        elif position:
            all_generals = GeneralR.objects.select_related().filter(position__icontains=position)
        elif salary:
            all_generals = GeneralR.objects.select_related().filter(salary__icontains=salary)
    return render(request, template, {'all_generals':all_generals,'username':username})


def portfolio_user(request, id_user):
    template = 'user.html'
    username = auth.get_user(request).username
    user = GeneralR.objects.get(id=id_user.split('-')[0])
    user_children_all = user.children.all()
    paginator = Paginator(user_children_all, 100)
    page = request.GET.get('page')
    user_children = paginator.get_page(page)
    if request.is_ajax():
        user_id = request.GET.get('user_id')
        template = 'filter_worker.html'
        name = request.GET.get('name')
        position = request.GET.get('position')
        salary = request.GET.get('salary')
        try:
            if name:
                user_children = GeneralR.objects.select_related().get(id=user_id).children.filter(name__icontains=name)
            elif position:
                user_children = GeneralR.objects.select_related().get(id=user_id).children.filter(position__icontains=position)
            elif salary:
                user_children = GeneralR.objects.select_related().get(id=user_id).children.filter(salary__icontains=salary)
        except Exception:
            redirect('/{}-general/'.format(id_user))
    return render(request, template, {'user':user, "username":username, "user_children":user_children})


def adding(request, id_user):
    username = auth.get_user(request).username
    parent = GeneralR.objects.get(id=id_user)
    form = AddWorker(request.POST, request.FILES)
    if request.POST and form.is_valid():
        if 'photo' in request.FILES:
            form.photo = request.FILES['photo']
        f = form.save(commit=False)
        f.parent = parent
        f.save()
        return redirect('/')
    return render(request, 'adding_worker.html', locals())


def change_user(request, id_user):
    username = auth.get_user(request).username
    a = GeneralR.objects.get(id=id_user)
    form = ChangeWorker(request.POST, request.FILES, instance=a, initial={'name':a.name,
                                              'position':a.position,
                                              'salary':a.salary
                                              })
    if request.POST and form.is_valid():
        if 'photo' in request.FILES:
            form.photo = request.FILES['photo']
        form.save(commit=True)
        print(request.POST['parent'])
        try:
            if request.POST['parent'] == 'None':
                GeneralR.objects.filter(id=id_user).update(parent=None)
            else:
                GeneralR.objects.filter(id=id_user).update(parent_id=request.POST['parent'].split('id ')[1])
        except Exception:
            return redirect('/{}/change/'.format(id_user))
        return redirect('/')
    if request.is_ajax():
        parent = request.GET.get('parent')
        print(parent)
        count_workers = GeneralR.objects.filter(name__icontains=parent).count()
        text = ''
        if count_workers <= 22:
            filter_user = GeneralR.objects.filter(name__icontains=parent)
            for i in filter_user:
                text += '{}'.format(i.name)+" "+'{}'.format(i.position)+" "+'{}'.format(i.pk)+'\n'
            return JsonResponse({'count': '{}'.format(count_workers), 'info':text})
        else:
            return JsonResponse({'info': 'so many worker {}, please enter id'.format(count_workers)})
    return render(request, 'change_worker.html', locals())

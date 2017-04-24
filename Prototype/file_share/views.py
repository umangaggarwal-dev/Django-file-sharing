from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import *
from django.http import JsonResponse, HttpResponse
import datetime
from django.db.models import Q


def drive(request):
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        user = request.user
        folder = Folder.objects.filter(user = user)[0]
        print folder.name
        dirs = folder.get_children()
        files = newFile.objects.filter(folder = folder)
        #form = UploadForm()
        return render(request, 'file_share/drive.html', {'files':files, 'folders':dirs})


def folders(request, folder):
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        user = request.user
        email = user.email
        root = Folder.objects.get(name = "root%s" % str(email).replace('.', '_'))
        dirs = root.get_descendants()
        target = dirs.filter(name = folder)[0]
        files = newFile.objects.filter(folder = target)
        children = target.get_children()
        #form = UploadForm()
        return render(request, 'file_share/drive.html', {'files':files, 'folders':children})        


def signup(request):
    if not request.user.is_authenticated():
        form = SignupForm()
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                new_password = form.cleaned_data['password']
                user = User(username=username, email=email)
                user.set_password(new_password)
                user.save()
                auth.login(request, user)
                return redirect('drive')
            return render(request, 'file_share/signup.html', {'form':form})
        return render(request, 'file_share/signup.html', {'form':form})
    else:
        return redirect('drive')


def login(request):
    if not request.user.is_authenticated():
        form = LoginForm()
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = auth.authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    
                    auth.login(request, user)
                    return redirect('drive')
                else:
                    return render(request, 'file_share/login.html', {'form':form})
                return render(request, 'file_share/login.html', {'form':form})
            return render(request, 'file_share/login.html', {'form':form})
        return render(request, 'file_share/login.html', {'form':form})
    else:
        return redirect('drive')

def logout(request):
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        auth.logout(request)
        return redirect('login')


def handle_uploaded_file(f, destination, filename, extension):
    with open('/home/umang/mera_project/Prototype/file_share/static/file_share/uploads/%s/%s.%s' % (destination, filename, extension), 'ab+') as destiny:
        print destiny
        #for chunk in f.chunks():
        destiny.write(f)

def upload(request):
    #print 'x'
    if request.method== 'POST':
        #form = UploadForm(request.POST['file'])
        #if form.is_valid():
        file = request.POST.get('filedata')
        
        filename = request.META['HTTP_FILENAME']
        print filename
        extension = request.META.get('HTTP_EXTENSION')
        path = request.META.get('HTTP_TARGET')
        print path
        x = path.split('/')
        user = request.user
        print user
        root_folder = Folder.objects.filter(user = user)[0]
        destination = str(root_folder.name)
        if x[1] == 'drive':
            handle_uploaded_file(file, destination, filename, extension)
            if not newFile.objects.filter(filename__iexact = filename).exists():
                f = newFile(filename=(filename), folder=root_folder)
                f.save()
        elif x[1] == 'folders':
            folder = x[len(x)-2]
            print folder
            dir = root_folder.get_descendants().filter(name = folder)[0]
            print dir
            #dir = Folder.objects.filter(name = folder)[0]
            handle_uploaded_file(file, destination, filename, extension)
            if not newFile.objects.filter(filename__iexact = filename).exists():
                f = newFile(filename=filename, folder=dir)
                f.save()
    result = {
        'reload': '200'
    }
    return JsonResponse(result)


"""def getUser(request):
    targetUser = request.GET.get('targetUser', None)
    response = {
        'present': User.objects.filter(username__iexact = targetUser).exists()
    }"""

def share(request):
    if request.method == 'POST':
        file = request.POST.get('filedata')
        filename = request.META.get('HTTP_FILENAME')
        extension = request.META.get('HTTP_EXTENSION')
        targetUser = request.META.get('HTTP_TARGETUSER')
        #user = request.user
        user = User.objects.filter(username__iexact = targetUser)[0]
        root_folder = Folder.objects.filter(user=user)[0]
        destination = str(root_folder.name)
        handle_uploaded_file(file, destination, filename, extension)
        if not newFile.objects.filter(filename__iexact = filename).exists():
            f = newFile(filename=filename, folder=root_folder)
            f.save()
    result = {
        'reload': '200'
    }
    return JsonResponse(result)


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def forgot_mail(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        print username
        if(User.objects.filter(username__iexact=username).exists()):
            print 'a'
            x = PasswordChangeRequest(UserId = User.objects.get(username=username))
            print 'a'
            x.save()
            print 'b'
            data = {
                'confirm': True
            }
            return JsonResponse(data)
        else:
            data = {
                'confirm': False
            }
            return JsonResponse(data)
    else:
        return render(request, 'file_share/forgot_mail.html')

def forgot_mail_confirmation(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        instance = PasswordChangeRequest.objects.filter(ID = key)[0]
        if instance == None:
            return redirect('login')
        else:
            req_date = str(instance.time)
            req_year = req_date.split('-')[0]
            req_month = req_date.split('-')[1]
            req_day = req_date.split('-')[2]
            today = str(datetime.date.today()).split('-')
            year = today[0]
            month = today[1]
            day = today[2]
            if req_year == year:
                if req_month == month:
                    if req_day == day:
                        user = instance.UserId
                        #username = user.username
                        new_password = request.POST.get('new_password')
                        user.set_password(new_password)
        return redirect('login')

    else:
        return render(request, 'file_share/new_password.html')

def search_users(request):
    if not request.user.is_authenticated:
        return render('login') 
    else:
        query = request.GET.get('username')
        results = dict(user_list = list((User.objects.filter(Q(username__startswith = query))).values('username')))
        if results['user_list'] == []:
            results = {'user_list' : 'No such user'}
        return JsonResponse(results)
        


def make_trust(request):
    if not request.user.is_authenticated:
        return render('login')
    else:
        #form = Friendship()
        #if request.method == 'POST':
        user1 = request.user
        friends = []
        trusts = Trust.objects.filter(user1 = user1)
        for bond in trusts:
            friends.append(bond.user2)
        return render(request, 'file_share/trustedusers.html', {'friends':friends})


def pdf_download(request, filename):
    path = os.expanduser('~/files/pdf/')
    f = open(path+filename, "r")
    response = HttpResponse(FileWrapper(f), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=resume.pdf'
    f.close()
    return response
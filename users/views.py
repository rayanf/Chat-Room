from django.http import HttpResponse
from django.shortcuts import render,redirect
from users.models import Users
import uuid
from users.models import Gp
from messeges.views import chat
from users.models import Gp_messages
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout


def login_view(request):
    # if not request.user.is_authenticated:
    if request.method == "GET":
        return render(request,'login.html',context=None)

    if request.method == "POST":
        user = authenticate(request,username=request.POST['username'],password= request.POST['password'])
        if user is not None:
            # child_user = Users.objects.get(username=user.username)
            login(request,user)
            response = redirect('/chat/')
            return response
        else:
            return HttpResponse('not found',status = 404)
    # else:
        # return redirect('/chat/')



def logout_view(request):
    try:
        logout(request)
    except:
        pass
    return redirect('/users/login')


def signin(request):
    users = Users.objects.all()
    for u in users:
        if request.POST.get('username_signin') == u.username:
            return redirect('/users/login')

    new_user_signin = Users(
                    first_name = request.POST.get('first_name_signin'),
                    last_name = request.POST.get('last_name_signin'),
                    username = request.POST.get('username_signin'),
                    password = request.POST.get(''),
                    avatar = '123',
                    token = uuid.uuid4(),
                    contacts_id = [],
                )
    new_user_signin.set_password(request.POST.get('password_signin'))

    new_user_signin.save()
    new_user_signin = Users.objects.get(username = request.POST.get('username_signin'))
    login(request,new_user_signin)
    response = redirect('/chat/')

    return response







def user_list(request):
    if request.user.is_authenticated :
        selfuser = Users.objects.get(username = request.user.username)
        contacts = selfuser.contacts_id
        strreq = str(request)
        username_password_error = ""

        if "?del_contact=" in strreq:
            try:
                selfuser.contacts_id.remove(Users.objects.get(username=request.GET['del_contact']).id)
                selfuser.save()
            except:
                return redirect('/users/list')
        if "?username_add" in strreq:
            try:
                duplicate_user = 0
                for i in contacts:
                    if (Users.objects.get(username=request.GET['username_add']).id == i):
                        duplicate_user = 1
                        break
                #
                if duplicate_user == 0:
                    selfuser.contacts_id.append(Users.objects.get(username=request.GET['username_add']).id)
                    selfuser.save()
            except:
                return redirect('/users/list')
        contacts_Users = []
        for i in contacts:
            contacts_Users.append(Users.objects.get(id = i))

        return render(request, "list.html", context={
                                                    "contacts_Users" : contacts_Users,
                                                    "title" : "users list",
                                                    "h_dict" : {"name" : "Contacts"},
                                                    "shahrokhi" : "shahrokhi" ,
                                                    "error" :  username_password_error,

                                                        })
    else:
        return redirect('/users/login')





def gps(request,gp_id=None,user_id=None):
    if request.user.is_authenticated:
        self_user = Users.objects.get(username = request.user.username)
        contacts = self_user.contacts_id
        contacts_Users = []
        for i in contacts:
            contacts_Users.append(Users.objects.get(id = i))
        my_gps = Gp.objects.filter(admin=self_user)


        if gp_id != None and gp_id != 0:
            current_gp_edit = Gp.objects.get(id = gp_id)
            current_gp_members = []
            for i in current_gp_edit.members:
                current_gp_members.append(Users.objects.get(id = i))
            current_gp_edit_name = current_gp_edit.name
            current_gp_id = current_gp_edit.id
            if user_id != None:
                if Users.objects.get(id = user_id) not in current_gp_members:
                    current_gp_edit.members.append(user_id)
                    current_gp_edit.save()
                    new_member = Users.objects.get(id = user_id)
                    new_member.gps_id.append(current_gp_edit.id)
                    new_member.save()
                    current_gp_members.append(Users.objects.get(id = user_id))
        else:
            current_gp_edit_name = None
            current_gp_members = []
            current_gp_id = 0
        return render(request,'creatgp.html',context={
                                                    "contacts_Users" : contacts_Users,
                                                    "my_gps" : my_gps,
                                                    'edit_member_gp' : current_gp_edit_name,
                                                    "current_gp_members" : current_gp_members,
                                                    "current_gp_id" : current_gp_id
    })

    else:
        return redirect('/users/login')


def creat_gp(request):
    if request.user.is_authenticated:
        self_user = Users.objects.get(username = request.user.username)
        new_gp = Gp(
                name = request.POST.get('new_gp_name'),
                members = [self_user.id],
                admin = self_user
        )
        new_gp.save()
        self_user.gps_id.append(new_gp.id)
        self_user.save()
        return(gps(request))
    else:
        redirect('/users/login')

def delete_gp(request):
    if request.user.is_authenticated:
        del_gp = Gp.objects.get(id = int(request.POST.get('delgp""')))
        members = del_gp.members
        for i in members:
            u = Users.objects.get(id = i)
            u.gps_id.remove(int(del_gp.id))
            u.save()
        del_gp_pms = Gp_messages.objects.filter(gp=del_gp)
        for i in del_gp_pms:
            i.delete()
        del_gp.delete()
        return chat(request)
    else:
        redirect('/users/login')



def user_edit(request):

        return HttpResponse("edit page")

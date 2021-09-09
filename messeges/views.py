from django.shortcuts import render , redirect
from users.models import Users
from django.http import HttpResponse
from users.models import Messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from users.models import Gp_messages
from users.models import Gp

def add_messege(request):
    global send_cheker
    global receiver_name
    global receiver_id
    if request.user.is_authenticated:
        if request.POST.get('receiver_idh') != "None" :
            sender = Users.objects.get(username = request.user.username)
            m = Messages(
                text= request.POST.get("text"),
                sender=sender,
                receiver= Users.objects.get(id=request.POST.get('receiver_idh')),
            )
            m.status = 1
            m.save()
            send_cheker = 1
            return chat(request,user_id=request.POST.get('receiver_idh'))

        else:
            send_cheker = 2
            return chat(request)
    else:
        return redirect('/users/login')


def chat(request,user_id=None):
    if request.user.is_authenticated:
        masseges = Messages.objects.all()
        users = Users.objects.all()
        child_user = Users.objects.get(username=request.user.username)
        sender = child_user
        global send_cheker
        global receiver_name
        receiver_id = user_id
        if receiver_id != None:
            for u in users:
                if u.id == receiver_id:
                    receiver_name = u.get_fullname
            receiver_id = int(receiver_id)
            read_messages = Messages.objects.filter(Q(sender_id=receiver_id) & Q(status=2))
            for i in read_messages:
                i.status = 3
                i.save()
        else:
            receiver_name = receiver_id
        if request.method == "GET":
            received_messages = Messages.objects.filter(Q(receiver_id=sender.id) & Q(status=1))
            for i in received_messages:
                i.status = 2
                i.save()
            send_cheker = 0
        contacts = sender.contacts_id
        contacts_Users = []
        for i in contacts:
            contacts_Users.append(Users.objects.get(id = i))

        gps_acc =[]
        self_gps = sender.gps_id
        for i in self_gps:
            gps_acc.append(Gp.objects.get(id = i))
        return render(request,"chat.html",context={
                                                "contacts_Users" : contacts_Users,
                                                'receiver': receiver_name ,
                                                'receiver_id' : receiver_id,
                                                'send_cheker': send_cheker,
                                                "sender_id" : sender.id,
                                                "massages" : masseges,
                                                'sender_getfullname' : sender.get_fullname,
                                                'gps' : gps_acc,
                                                })
    else:
         return redirect('/users/login')



def chat_gp(request,gps_id=None):
    if request.user.is_authenticated:
        users = Users.objects.all()
        sender = Users.objects.get(username = request.user.username)
        global send_cheker
        contacts = sender.contacts_id
        contacts_Users = []
        for i in contacts:
            contacts_Users.append(Users.objects.get(id = i))
        if request.method == "GET":
            send_cheker = 0
        gps_acc =[]
        self_gps = sender.gps_id
        for i in self_gps:
            gps_acc.append(Gp.objects.get(id = i))

        if gps_id == None:
            masseges =[]
            return render(request,"chat_gp.html",context={
                                                        "contacts_Users" : contacts_Users,
                                                        'send_cheker': send_cheker,
                                                        "sender_id" : sender.id,
                                                        "massages" : masseges,
                                                        'sender_getfullname' : sender.get_fullname,
                                                        'gps' : gps_acc,
                                                        })
        else:
            masseges = Gp_messages.objects.filter(gp=Gp.objects.get(id=gps_id))
            current_gp = Gp.objects.get(id=gps_id)
            return render(request,"chat_gp.html",context={
                                                    "contacts_Users" : contacts_Users,
                                                    'send_cheker': send_cheker,
                                                    "sender_id" : sender.id,
                                                    "massages" : masseges,
                                                    'sender_getfullname' : sender.get_fullname,
                                                    'gps' : gps_acc,
                                                    'current_gp' : current_gp.name,
                                                    'current_gp_id' : current_gp.id,
                                                    'current_gp_admin' : current_gp.admin.id,
                                                    })


    else:
        return redirect('/users/login')



def add_messege_gp(request):
    if request.user.is_authenticated:
        sender = Users.objects.get(username = request.user.username)
        m = Gp_messages(
                        gp = Gp.objects.get(id = request.POST.get('current_gph')),
                        text = request.POST.get('text'),
                        sender = sender
        )
        if m.sender.id in m.gp.members:
            m.save()
        else:
            return redirect('/users/login')

        return chat_gp(request,gps_id=request.POST.get('current_gph'))

    else:
        return redirect('/users/login')

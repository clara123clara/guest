from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import Event,Guest,Consumer,Server
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging

import os,django
from django.template.context_processors import request
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guest.settings")# project_name 项目名称
django.setup()

def index(request):
    #return HttpResponse("hellp sdfsdf!!!")
    return render(request, "index.html")

#登陆签到
def login_action(request):
    
    if request.method=='POST':
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        user=auth.authenticate(username=username,password=password)
        '''
        if username=='admin' and password=='admin123':
            #return HttpResponse('登陆成功')
            response=HttpResponseRedirect("/event_manage/")
            #response.set_cookie('user',username,3600) #添加浏览器cookie
            request.session['user']=username
            return response
            '''
        if user is not None:
            auth.login(request,user)  
            request.session['username']=username
            response=HttpResponseRedirect("/event_manage/")
            return response
            
        else:
            return render(request,"index.html",{'error':'用户名和密码错误'})
            #return HttpResponse('登陆失败')
    else:
        return HttpResponse('不是post请求方式！！！')
    
    

# 发布会管理（登录之后默认页面）
@login_required #装饰，必须经过登陆
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('username', '')
    return render(request, "event_manage.html", {"user": username,"events":event_list})


# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('username', '')
    search_name = request.GET.get("name", "")
    search_name_bytes = search_name.encode(encoding="utf-8")
    event_list = Event.objects.filter(name__contains=search_name_bytes)
    return render(request, "event_manage.html", {"user": username, "events": event_list})

# 嘉宾管理
@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    username = request.session.get('username', '')

    paginator = Paginator(guest_list, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


# 嘉宾手机号的查询
@login_required
def search_phone(request):
    username = request.session.get('username', '')
    search_phone = request.GET.get("phone", "")
    search_name_bytes = search_phone.encode(encoding="utf-8")
    guest_list = Guest.objects.filter(phone__contains=search_name_bytes)
    username = request.session.get('username', '')

    paginator = Paginator(guest_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


# 签到页面
@login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)           # 签到人数
    sign_list = Guest.objects.filter(sign="1", event_id=event_id)   # 已签到数
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list))
    return render(request, 'sign_index.html', {'event': event,
                                               'guest':guest_data,'sign':sign_data})
    
    
# 签到动作
@login_required
def sign_index_action(request,event_id):

    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)
    sign_list = Guest.objects.filter(sign="1", event_id=event_id)
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list)+1)

    phone =  request.POST.get('phone','')

    result = Guest.objects.filter(phone = phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'phone error.','guest':guest_data,'sign':sign_data})

    result = Guest.objects.filter(phone = phone,event_id = event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'event id or phone error.','guest':guest_data,'sign':sign_data})

    result = Guest.objects.get(event_id = event_id,phone = phone)

    if result.sign:
        return render(request, 'sign_index.html', {'event': event,'hint': "user has sign in.",'guest':guest_data,'sign':sign_data})
    else:
        Guest.objects.filter(event_id = event_id,phone = phone).update(sign = '1')
        return render(request, 'sign_index.html', {'event': event,'hint':'sign in success!','user': result,'guest':guest_data,'sign':sign_data})



'''
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
'''    


# 前端签到页面
def sign_index2(request,event_id):
    event_name = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index2.html',{'eventId': event_id,'eventNanme': event_name})
    
 
# 退出登录
@login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/index/')
    return response   
    
#客户管理页面
@login_required
def consumer_manage(request):
    consumer_list = Consumer.objects.all()
    username = request.session.get('username', '')
    #request.session['consumer_unit']=consumer_list[0]
    return render(request, "consumer_manage.html", {"user": username,"consumers":consumer_list})  

# 客户单位名称搜索
@login_required
def search_consumer(request):
    
    username = request.session.get('username', '')
    search_name = request.GET.get("company", "")
    search_name_bytes = search_name.encode(encoding="utf-8")
    consumer_list = Consumer.objects.filter(company__contains=search_name_bytes)
    return render(request, "consumer_manage.html", {"user": username, "consumers": consumer_list}) 

#服务器管理页面
@login_required
def server_manage(request,consum_id):
    consumer = get_object_or_404(Consumer,id=consum_id)
    server_list = Server.objects.all()
    username = request.session.get('username','')
    return render(request,"server_manage.html",{"user":username,"servers":server_list,"consumer":consumer})

#跳转新增客户平台
@login_required
def add_consumer(request):

    username = request.session.get('username','')
    return render(request,"add_consumer.html",{"user":username})


#提交表单，新增客户    
@login_required    
def add_button(request):
    if request.methon == 'POST':
        if uf.is_valid():
            username = uf.cleaned_data['username']
            headImg = uf.cleaned_data['headImg']
                        #user = User()
                        #user.username = username
                        #user.headImg = headImg
                        #user.save()
            user = User.objects.create(username = username ,headImg = headImg)
            print username,headImg
            return HttpResponse('ok')
        else:
                uf = UserForm()
        return render_to_response('index.html',{'uf':uf})    
    #consumer_name,consumer_type,pl_version,pl_url,adminname,adminpassword,pl_app,consumerContact,consumerRemark):
    e1=Event(company=consumer_name,consumer_type=consumer_type,web_version=pl_version,url=pl_url,admin_name=adminname,admin_password=adminpassword,apps=pl_app,contact=consumerContact,counsumer_Remark=consumerRemark)
    e1.save()    
    
    
    
    
    
    
    
    
    
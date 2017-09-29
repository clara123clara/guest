from django.test import TestCase# 单元测试类django.test.TestCase 集成unittest.TestCsse
from sign.models import Event,Guest
import  time
from django.contrib.auth.models import  User


# Create your tests here.

#首先创建测试类
class ModelTest(TestCase):

    #初始化：分别创建一条发布会（Event）和一条嘉宾（Guest）的数据。
    def setUp(self):
        Event.objects.create(name="oneplus 3 event", status=True, limit=2000,address='shenzhen', start_time='2016-08-31 02:18:22')
        result = Event.objects.get(name='oneplus 3 event')
        Guest.objects.create(event=result, real_name='alen',phone='13711001101', email='alen@mail.com', sign=False)

    #下面开始写测试用例了
    #1.通过get的方法，查询插入的发布会数据，并根据地址判断
    def test_event_models(self):
        result = Event.objects.get(name="oneplus 3 event")
        self.assertEqual(result.address, "shenzhen")
        self.assertTrue(result.status)

    #2.通过get的方法，查询插入的嘉宾数据，并根据名字判断
    def test_guest_models(self):
         result = Guest.objects.get(phone='13711001101')
         self.assertEqual(result.real_name, "alen")
         self.assertFalse(result.sign)

    #写完测试用例后，执行测试用例。这里与unittest的运行方法也不一样
    
class LoginAction(TestCase):      
    #测试登陆动作
    def setUp(self):
        User.objects.create_user('admin', 'admin@email.com', 'admin123456')
        
    def test_add_admin(self):
        #测试添加用户
        user=User.objects.get(username="admin")
        print("----------------"+user.username)
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@email.com")
        
    def test_log_action_username_password_null(self):
        #用户名密码为空
        test_data={'username':'','password':''}
        response=self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)
        
        
    def test_log_action_username_password_null(self):
        #用户名密码错误
        test_data={'username':'abc','password':'a123'}
        response=self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)            
        
    def test_log_action_username_password_null(self):
        #用户名密码为空
        test_data={'username':'admin','password':'admin123456'}
        response=self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code, 302)
   
class EventManageTest(TestCase):
    '''发布会管理测试'''
    login_user = {}
    def setUP(self):        
        User.objects.create_user('admin', 'admin@email.com', 'admin123456')  
        Event.objects.create(name="oneplus 3 event", status=True, limit=2000,address='shenzhen', start_time='2016-08-31 02:18:22')
        self.login_user ={'username':'admin','password':'admin123456'}
    
    def test_event_manage_success(self):
        response =self.client.post('/login_action/', data=self.login_user)
        print("++++++++++++++++++"+response)
        response = self.client.post('/event_manage/')
        print("================"+response)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'oneplus 3 event', response.content)
        self.assertIn(b'shenzhen', response.content)
        
     
    def test_event_manage_sreach_sucess(self):
        response =self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_name/',{"name":"oneplus"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'oneplus 3 event', response.content)
        self.assertIn(b'beijing', response.content)
    
            
        
        
        
        
        
        
        
        
        
        
             
    
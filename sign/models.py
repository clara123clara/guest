from django.db import models

# Create your models here.

# 发布会表
class Event(models.Model):
    name = models.CharField(max_length=100)  # 发布会标题
    limit = models.CharField(max_length=100)# 参加人数
    status = models.BooleanField()  # 状态
    address = models.CharField(max_length=200)  # 地址
    start_time = models.DateTimeField('events time')  # 发布会时间
    create_time = models.DateTimeField(auto_now=True)  # 创建时间（自动获取当前时间）
 
    # __str__()方法告诉Python如何将对象以str的方式显示出来。所以，为每个模型类添加了__str__()方法
    # 如果是Python2.x的话，这里需要使用__unicode__()
    def __str__(self):
        return self.name
 
 
# 嘉宾表
class Guest(models.Model):
    event = models.ForeignKey(Event)  # 关联发布会id
    real_name = models.CharField(max_length=64)  # 姓名
    phone = models.CharField(max_length=16)  # 手机号
    email = models.EmailField()  # 邮箱
    sign = models.BooleanField()  # 签到状态
    create_time = models.DateTimeField(auto_now=True)  # 创建时间（自动获取当前时间）
 
    class Meta:
        unique_together = ("event", "phone")
 
    def __str__(self):
        return self.real_name
    
#客户版本控制表    
class Consumer(models.Model):
    company = models.CharField(max_length=500)#客户单位名称
    consumer_type = models.BooleanField() #客户类型，正式或者试用客户
    web_version = models.CharField(max_length=50)
    url = models.CharField(max_length=100) 
    admin_name = models.CharField(max_length=100) 
    admin_password = models.CharField(max_length=100) 
    apps = models.CharField(max_length=1000)
    contact = models.CharField(max_length=100)
    counsumer_Remark =  models.CharField(max_length=1000) #备注
    
    def __str__(self):
        return self.name 
    
#客户服务器详细信息表    
class  Server(models.Model): 
    consumer =models.ForeignKey(Consumer)  # 关联客户id
    server_name = models.CharField(max_length=100)
    in_ip = models.CharField(max_length=100)
    server_account = models.CharField(max_length=100) 
    server_password = models.CharField(max_length=100)   
    system = models.CharField(max_length=100)
    server_cpu = models.CharField(max_length=100)
    server_harddisk = models.CharField(max_length=100)
    server_Remark =  models.CharField(max_length=1000) #备注
    
    class Meta:
        unique_together = ("consumer", "in_ip")
    
    def __str__(self):
        return self.name 
    
    
    
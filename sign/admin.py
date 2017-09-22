from django.contrib import admin

# Register your models here.
from sign.models import Event, Guest,Consumer,Server
 
 
# Register your models here.
class EventAdmin(admin.ModelAdmin):
    # list_display，它是一个字段名称的数组，用于定义要在列表中显示哪些字段。
    # 当然，这些字段名称必须是模型中的Event()类定义的
    list_display = ['id','name', 'status', 'start_time', 'address','create_time','limit']
    # 生成搜索栏和过滤器
    search_fields = ['name']  # 搜索栏
    list_filter = ['status']  # 过滤栏
 
 
class GuestAdmin(admin.ModelAdmin):
    list_display = ['real_name', 'phone', 'email', 'sign', 'create_time', 'event']
    # 生成搜索栏和过滤器
    search_fields = ['realname','phone']  # 搜索栏
    list_filter = ['sign']  # 过滤栏
 
class ConsumerAdmin(admin.ModelAdmin):
    list_display = ['id','company', 'consumer_type', 'web_version', 'url', 'admin_name', 'admin_password','apps','contact','counsumer_Remark']
    # 生成搜索栏和过滤器
    search_fields = ['company']  # 搜索栏
    list_filter = ['consumer_type']  # 过滤栏 
 
admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(Consumer, ConsumerAdmin)
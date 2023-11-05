from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime

# Create your models here.
# Python 默认 UTF-8 编码，数字、英文字母、小数点、下划线以及空格，各占一个字节，而一个汉字可能占3个字节
# on_delete=models.CASCADE¶设置级联删除
# models.SET_NULL, blank=True, null=True设置为非级联删除，ForeignKey被删就设置为null

# 如果使用了继承的方式，要使用auth模块的话就需要在setting.py中进行配置
# 默认用户认证时使用的哪张表
# AUTH_USER_MODEL= "app.UserInfo"
class UserInfo(AbstractUser):
    """员工信息表"""
    status_CHOICES = [
        (1, "在职"),
        (2, "离职"),
    ]
    status = models.SmallIntegerField(verbose_name="status", choices=status_CHOICES, default=1)
    hr_admin_CHOICES = [
        (1, False),
        (2, True),
    ]
    hr_admin = models.SmallIntegerField(verbose_name="hr_admin", choices=hr_admin_CHOICES, default=1)
    linemgr_CHOICES = [
        (1, False),
        (2, True),
    ]
    linemgr = models.SmallIntegerField(choices=linemgr_CHOICES, default=1)
    finalCon_CHOICES = [
        (1, False),
        (2, True),
    ]
    finalCon = models.SmallIntegerField(choices=finalCon_CHOICES, default=1)
    finance_admin_CHOICES = [
        (1, False),
        (2, True),
    ]
    finance_admin = models.SmallIntegerField(verbose_name="finance_admin", choices=finance_admin_CHOICES, default=1)

    company_name = models.CharField(verbose_name="company_name", max_length=10, blank=True, null=True)
    business_unit = models.CharField(verbose_name="business_unit", max_length=30, blank=True, null=True)
    line_manager = models.CharField(verbose_name="line_manager", max_length=100, blank=True, null=True)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.username


class Expense_Type(models.Model):
    """费用类型表"""
    status_CHOICES = [
        (1, "启用"),
        (2, "冻结"),
    ]
    status = models.SmallIntegerField(verbose_name="status", choices=status_CHOICES, default=1)
    expense_type_level1 = models.CharField(max_length=100, blank=False, null=False)
    expense_type_level2 = models.CharField(max_length=100, blank=False, null=False)
    expense_type = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.expense_type


class Expense_Report(models.Model):
    """报销信息表"""

    cost_center= models.CharField(max_length=100, verbose_name='Cost Center', default='NEMM')
    report_number = models.CharField(max_length=100)
    email = models.ForeignKey(UserInfo, models.SET_NULL, null=True)
    expenseTyp = models.ForeignKey(to='Expense_Type', on_delete=models.SET_NULL, to_field='expense_type',
                                   verbose_name='Expense Type', null=True, )
    Crt_date=models.DateTimeField()
    exp_date = models.DateTimeField()
    from_location = models.CharField(max_length=100, verbose_name='From', blank=True, null=True, )
    to_location = models.CharField(max_length=100, verbose_name='To', blank=True, null=True, )
    Currency = models.CharField(max_length=3, )
    exchange_rate = models.FloatField(default=1, )
    orig_amount = models.FloatField(verbose_name='Original Amount', )
    local_amount = models.FloatField(verbose_name='Local Amount', )
    description = models.TextField(max_length=255, blank=True, null=True, )

    report_status_CHOICES = [
        (1, 'Draft'),
        (2, 'Sent'),
        (3, 'Completed'),
    ]
    report_status = models.SmallIntegerField(choices=report_status_CHOICES, default=1)
    line_manager_action_CHOICES = [
        (1, 'initial'),
        (2, 'received'),
        (3, 'reject'),
        (4, 'approved'),
    ]
    line_manager_action = models.SmallIntegerField(choices=line_manager_action_CHOICES, default=1)
    line_manager_comments = models.TextField(max_length=100, blank=True, null=True, )
    final_action_CHOICES = [
        (1, 'initial'),
        (2, 'received'),
        (3, 'reject'),
        (4, 'approved'),
    ]
    final_action = models.SmallIntegerField(choices=final_action_CHOICES, default=1)
    final_comments = models.TextField(max_length=255, blank=True, null=True, )
    finanDepart_CHOICES = [
        (1, 'initial'),
        (2, 'received'),
        (3, 'action_required'),
        (4, 'doc_required'),
        (5, 'approved'),
    ]
    finanDepart= models.SmallIntegerField(choices=finanDepart_CHOICES, default=1)
    finance_comments = models.TextField(max_length=255, blank=True, null=True, )

    def __str__(self):
        """返回模型的字符串表示"""
        return self.report_number

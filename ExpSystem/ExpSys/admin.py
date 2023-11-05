from django.contrib import admin

# Register your models here.
from .models import UserInfo,Expense_Type,Expense_Report
class Expense_ReportAdmin(admin.ModelAdmin):
    list_display = ('id','report_number','email', 'expenseTyp','report_status')

admin.site.register(UserInfo)
# admin.site.register(employee_information)
admin.site.register(Expense_Type)
admin.site.register(Expense_Report, Expense_ReportAdmin)
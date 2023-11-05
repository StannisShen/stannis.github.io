from django.urls import path

from . import views

urlpatterns = [

    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout, name="logout"),
    path("expense/", views.expensemain, name="expense"),
    path("expense/reimb", views.reimbursement, name="expense_reimbursement"),
    path("expense/leave", views.vacation, name="expense_leave"),
    path("expense/hr/", views.hr_admin, name="expense_hradmin"),
    path("expense/finance", views.finance_admin, name="expense_financeadmin"),

    # path("expense/test1", views.test1, name="expense_test1"),
    # path("expense/test2", views.test2, name="expense_test2"),

    # path("expense/test", views.test, name="test"),
    # path("expense/test/switch", views.test_switch, name="test"),

]

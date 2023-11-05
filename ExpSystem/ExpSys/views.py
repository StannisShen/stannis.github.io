import json
from django.shortcuts import render, HttpResponse, redirect
from .models import UserInfo, Expense_Type, Expense_Report
from django import forms
from ExpSys.utils.bootstrapforms import BootStrapForm
from django.views import View
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from datetime import datetime


# Create form for login
class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="username",
        widget=forms.TextInput,
        required=True,  # 必填
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(render_value=True),  # rendervalue True密码不自动清空
        required=True,  # 必填
    )


class ExpReportModelForm(forms.ModelForm):
    """ModelForm """

    class Meta:
        model = Expense_Report
        fields = ['cost_center',
                  'expenseTyp',
                  'exp_date',
                  'from_location',
                  'to_location',
                  'Currency',
                  'orig_amount',
                  'exchange_rate',
                  'local_amount',
                  'description',
                  ]
        # widgets={
        # 'exp_date': forms.DateTimeInput(attrs={"class": "form-control"})
        # 'exp_date': forms.DateInput(attrs={"class": "form-control"})
        # 'exp_date': forms.TimeInput(attrs={"class": "form-control"})
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        # 相当于"name": forms.TextInput(attrs={"class": "form-control"})
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placehoder": field.label}


class ExpTypeModelForm(forms.ModelForm):
    """ModelForm for expense_04_finance function, ExpTypeAdd ExpTypeEdit"""

    class Meta:
        model = Expense_Type
        fields = ['expense_type_level1',
                  'expense_type_level2',
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        # 相当于"name": forms.TextInput(attrs={"class": "form-control"})
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placehoder": field.label}


class UserModelForm(forms.ModelForm):
    """ModelForm for expense_03_hr function, NewUserAdd"""

    class Meta:
        model = UserInfo
        fields = ['username',
                  'password',
                  'first_name',
                  'last_name',
                  'email',
                  'status',
                  'hr_admin',
                  'finance_admin',
                  'company_name',
                  'business_unit',
                  'line_manager',
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        # 相当于"name": forms.TextInput(attrs={"class": "form-control"})
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placehoder": field.label}


class UserModelEditForm(forms.ModelForm):
    """ModelForm for expense_03_hr function, UserEdit"""

    class Meta:
        model = UserInfo
        fields = ['first_name',
                  'last_name',
                  'email',
                  'hr_admin',
                  'finance_admin',
                  'company_name',
                  'business_unit',
                  'line_manager',
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        # 相当于"name": forms.TextInput(attrs={"class": "form-control"})
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placehoder": field.label}


# Create your views here.

class Login(View):
    # 返回登录界面
    def get(self, request):
        error_info = request.session.pop('error_info', '')
        form = LoginForm()
        context = {'form': form, 'error_info': error_info}
        return render(request, "login.html", context)

    def post(self, request):
        # res_get=request.GET.get("next",'')
        # 接受用户登录信息并校验
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # user_obj = UserInfo.objects.filter(username=form.cleaned_data['username']).first()
            # user_obj<class appexp.models.UserInfo>
            # 用户填写信息规范，开始对用户名和密码校验
            user_obj = auth.authenticate(username=form.cleaned_data['username'],
                                         password=form.cleaned_data['password'])
            # 用户名和密码校验成功进入系统
            if user_obj:
                # 用户登录验证通过后，自动写入session['_auth_user_id', '_auth_user_backend', '_auth_user_hash']
                auth.login(request, user_obj)
                currentUserAuthHR = ''
                currentUserAuthFinance = ''
                currentUserAuthIsLM = False
                currentUserAuthIsFC = False
                if auth.get_user(request).hr_admin == 2:
                    currentUserAuthHR = 'HR Admin'
                if auth.get_user(request).finance_admin == 2:
                    currentUserAuthFinance = 'Finance Admin'
                if auth.get_user(request).linemgr == 2:
                    currentUserAuthIsLM = True
                if auth.get_user(request).finalCon == 2:
                    currentUserAuthIsFC = True

                currentUserInfo = {'tagUser': auth.get_user(request).username,
                                   'tagAuthHR': currentUserAuthHR,
                                   'tagAuthFinance': currentUserAuthFinance,
                                   'tagAuthIsLM': currentUserAuthIsLM,
                                   'tagAuthIsFC': currentUserAuthIsFC, }
                # print(currentUserInfo)
                # 自定义session信息，设置session有效期
                request.session['currentUserInfo'] = currentUserInfo
                request.session.set_expiry(60 * 60 * 24)
                # print(request.session.get('_auth_user_id'))
                # print(request.session.get('_auth_user_backend'))
                # print(request.session.get('_auth_user_hash'))
                # print(request.session.get('username'))
                # print(type(auth.get_user(request)))
                # print(type(auth.get_user(request).username))
                # print(auth.get_user(request).email)
                # print(type(user_obj))
                # print(user_obj.username)
                # print(user_obj.email)
                # context = {'authority': authority, 'currentUser': currentUser}
                return render(request, "expense_00_noticeboard.html")
                # return redirect("/index/expense")

            # 用户名和密码校验不成功返回错误提示
            else:
                request.session["error_info"] = "user is not exist or password not match"
                return redirect("/index/login")
        else:
            # 用户填写信息不规范返回错误提示
            context = {'form': form}
            return render(request, "login.html", context)


def Logout(request):
    auth.logout(request)
    return redirect("/index/login")


@login_required()
def expensemain(request):
    return render(request, "expense_00_noticeboard.html")


@csrf_exempt
@login_required()
def reimbursement(request):
    """根据用户操作判断执行"""
    # region POST request
    if request.method == "POST":
        print('1-1')
        OperateRole = request.POST.get('OperateRole')
        ReportOperate = request.POST.get('ReportOperate')
        ReportNumberOperate = request.POST.get('ReportNumber')
        if OperateRole == 'LineMgr':
            # region LineMgr action
            ReportOperate = ReportOperate.replace("\n", "")
            ReportOperate = ReportOperate.replace(" ", "")
            if ReportOperate == 'Approve':
                # print("==" + ReportOperate + "===")
                # print("==" + ReportNumberOperate + "===")
                Expense_Report.objects.filter(report_number=ReportNumberOperate).update(line_manager_action=4)
                Expense_Report.objects.filter(report_number=ReportNumberOperate).update(final_action=2)
                context = {'status': True, }
                return JsonResponse(context)
            elif ReportOperate == 'Reject':
                Expense_Report.objects.filter(report_number=ReportNumberOperate).update(line_manager_action=3)
                # Expense_Report.objects.filter(report_number=ReportNumberOperate).update(line_manager_action=2)
                context = {'status': True, }
                return JsonResponse(context)
            # endregion
        else:
            # region BtnNewExpReportSave Save report function
            if ReportOperate == 'BtnNewExpReportSave':
                # region GetData by User
                dataform = request.POST
                csrfmiddlewaretoken = dataform.getlist('csrfmiddlewaretoken')
                cost_center = dataform.getlist('cost_center')
                expenseTyp = dataform.getlist('expenseTyp')
                exp_date = dataform.getlist('exp_date')
                from_location = dataform.getlist('from_location')
                to_location = dataform.getlist('to_location')
                Currency = dataform.getlist('Currency')
                exchange_rate = dataform.getlist('exchange_rate')
                orig_amount = dataform.getlist('orig_amount')
                local_amount = dataform.getlist('local_amount')
                description = dataform.getlist('description')
                NewReport = []
                # endregion

                # region extract Data by line and attach report_number email
                for i in range(len(expenseTyp)):
                    QueryDicStr = ('csrfmiddlewaretoken=' + csrfmiddlewaretoken[i] +
                                   '&cost_center=' + cost_center[i] +
                                   '&expenseTyp=' + expenseTyp[i] +
                                   '&exp_date=' + exp_date[i] +
                                   '&from_location=' + from_location[i] +
                                   '&to_location=' + to_location[i] +
                                   '&Currency=' + Currency[i] +
                                   '&exchange_rate=' + exchange_rate[i] +
                                   '&orig_amount=' + orig_amount[i] +
                                   '&local_amount=' + local_amount[i] +
                                   '&description=' + description[i]
                                   )
                    NewReport.append(QueryDict(QueryDicStr))
                # endregion

                # region validate Data by line
                errorlist = []
                formReport = []
                ErrNum = 0
                for i in range(len(NewReport)):
                    formReport.append(ExpReportModelForm(data=NewReport[i]))
                    if formReport[i].is_valid():
                        errorlist.append({})
                    else:
                        errorlist.append(formReport[i].errors)
                    if errorlist[i]:
                        ErrNum += 1
                # endregion

                # region save or update report or return error message
                if ErrNum == 0:
                    # region if update, delete the old report and keep the report number
                    if ReportNumberOperate == 'undefined':
                        ReportQtDict = (Expense_Report.objects.filter(email=auth.get_user(request))
                                        .values_list('report_number', flat=True).distinct())
                        ReportQtExist = len(ReportQtDict)
                        NumberUnique = True
                        while NumberUnique:
                            ReportNumber = auth.get_user(request).username + str(1000 + ReportQtExist + 1)
                            if ReportNumber in ReportQtDict:
                                ReportQtExist += 1
                            else:
                                NumberUnique = False
                    else:
                        Expense_Report.objects.filter(email=auth.get_user(request),
                                                      report_number=ReportNumberOperate).delete()
                        ReportNumber = ReportNumberOperate
                    # endregion

                    # region save new report
                    for i in range(len(formReport)):
                        formReport[i].instance.email = auth.get_user(request)
                        formReport[i].instance.Crt_date = datetime.now()
                        formReport[i].instance.report_number = ReportNumber
                        formReport[i].save()
                    context = {'status': True, }
                    return JsonResponse(context)
                    # endregion
                else:
                    # region return error message
                    context = {'status': False, 'errorlist': errorlist, }
                    return JsonResponse(context)
                    # endregion
                # endregion
            # endregion

            # region BtnSend/BtnEdit/BtnDelete Edit function
            elif ReportOperate == 'BtnSend':
                Expense_Report.objects.filter(email=auth.get_user(request),
                                              report_number=ReportNumberOperate).update(report_status=2)
                Expense_Report.objects.filter(email=auth.get_user(request),
                                              report_number=ReportNumberOperate).update(line_manager_action=2)
                context = {'status': True, }
                return JsonResponse(context)
            elif ReportOperate == 'BtnEdit':
                EditReport = serializers.serialize(
                    'json', queryset=Expense_Report.objects.filter(
                        email=auth.get_user(request), report_number=ReportNumberOperate).all())
                context = {'status': True, 'EditReport': EditReport, }
                return JsonResponse(context)
            elif ReportOperate == 'BtnDelete':
                Expense_Report.objects.filter(email=auth.get_user(request), report_number=ReportNumberOperate).delete()
                context = {'status': True, }
                return JsonResponse(context)
            # endregion
    # endregion

    # region GET request
    if request.method == "GET":
        print('2-1')
        # region ReportData composition for ReportList
        ReportAll = Expense_Report.objects.filter(email=auth.get_user(request)).values_list('report_number',
                                                                                            flat=True).distinct()
        ReportData = []
        i = 0
        for RepNum in ReportAll:
            ReportData.append([])
            ReportData[i].append(str(i + 1))
            ReportData[i].append(RepNum)
            ReportObject = Expense_Report.objects.filter(report_number=RepNum)
            ReportData[i].append(ReportObject[0].Crt_date.strftime("%Y%m%d"))
            ReportData[i].append(ReportObject[0].get_report_status_display())
            ReportData[i].append([])
            j = 0
            for obj in ReportObject:
                ReportData[i][4].append([])
                ReportLineQuerySet = Expense_Report.objects.filter(report_number=RepNum, id=obj.pk)
                ReportLineObj = Expense_Report.objects.filter(report_number=RepNum, id=obj.pk).first()
                ReportExpTypI = Expense_Type.objects.filter(
                    expense_type=ReportLineObj.expenseTyp).first().expense_type_level1
                ReportExpTypII = Expense_Type.objects.filter(
                    expense_type=ReportLineObj.expenseTyp).first().expense_type_level2
                ReportData[i][4][j].append(ReportExpTypI)
                ReportData[i][4][j].append(ReportExpTypII)
                ReportData[i][4][j].append(ReportLineQuerySet)
                j += 1
            i += 1
            # ReportStatus = ReportObject.get_report_status_display()

        # [['1', '1101', [['Transport', 'Train', <QuerySet [<Expense_Report: 1101>]>],
        #               ['Transport', 'Train', <QuerySet [<Expense_Report: 1101>]>],
        #               ['Transport', 'Train', <QuerySet [<Expense# _Report: 1101>]>],
        #               ['Accommodation', 'Hotel', <QuerySet [<Expense_Report: 1101>]>]]],
        # ['2', '1102', [['Transport', 'Online_taxi', <QuerySet [<Expense_Report: 1102>]>],
        #               ['Transport', 'Online_taxi', <QuerySet [<Expense_Report: 1102>]>],
        #               ['Transport', 'Online_taxi', <QuerySet [<Expense_Report: 1102>]>],
        #               ['Transport', 'Online_taxi', <QuerySet [<Expense_Report: 1102>]>]]],
        # ['3', '1103', [['Accommodation', 'Hotel', <QuerySet [<Expense_Report: 1103>]>],
        #               ['Accommodation', 'Hotel', <QuerySet [<Expense_Report: 1103>]>],
        #               ['Accommodation', 'Hotel', <QuerySet [<Expense_Report: 1103>]>],
        #               ['Accommodation', 'Hotel', <QuerySet [<Expense_Report: 1103>]>]]],'
        # ['4', '1105', [['Accommodation', 'Hotel', <QuerySet [<Expense_Report: 1105>]>],
        #               ['Accommodation', 'Hotel', <QuerySet [<Expense_Report: 1105>]>],
        #               ['Accommodation', 'Hotel', <QuerySet [<Expense_Report: 1105>]>],
        #               ['Accommodation', 'Hotel', <QuerySet [<Expense_Report: 1105>]>],
        #               ['Accommodation', 'Hotel', <QuerySet [<Expense_Report: 1105>]>]]]]

        # endregion

        # region TaskData composition for LM
        DirectReportList = UserInfo.objects.filter(line_manager=auth.get_user(request)).values_list('pk', flat=True)
        TaskData = []
        i = 0
        for obj in DirectReportList:
            ReportAll = Expense_Report.objects.filter(email=obj, line_manager_action__gt=1).values_list('report_number',
                                                                                                        flat=True).distinct()
            for RepNum in ReportAll:
                TaskData.append([])
                TaskData[i].append(str(i + 1))
                TaskData[i].append(RepNum)
                ReportObject = Expense_Report.objects.filter(report_number=RepNum)
                TaskData[i].append(ReportObject[0].Crt_date.strftime("%Y%m%d"))
                TaskData[i].append(ReportObject[0].get_line_manager_action_display())
                TaskData[i].append([])
                j = 0
                for obj in ReportObject:
                    TaskData[i][4].append([])
                    ReportLineQuerySet = Expense_Report.objects.filter(report_number=RepNum, id=obj.pk)
                    ReportLineObj = Expense_Report.objects.filter(report_number=RepNum, id=obj.pk).first()
                    ReportExpTypI = Expense_Type.objects.filter(
                        expense_type=ReportLineObj.expenseTyp).first().expense_type_level1
                    ReportExpTypII = Expense_Type.objects.filter(
                        expense_type=ReportLineObj.expenseTyp).first().expense_type_level2
                    TaskData[i][4][j].append(ReportExpTypI)
                    TaskData[i][4][j].append(ReportExpTypII)
                    TaskData[i][4][j].append(ReportLineQuerySet)
                    j += 1
                i += 1
        # endregion

        # region NewReport setting for NewReportAdd
        ExpReportForm = ExpReportModelForm()
        ExpTypeOpt = {}
        ExpTypeLI = Expense_Type.objects.values_list('expense_type_level1', flat=True).distinct()
        for objI in ExpTypeLI:
            ExpTypeOpt[objI] = []
            ExpTypeLII = Expense_Type.objects.filter(expense_type_level1=objI).values_list('expense_type_level2',
                                                                                           flat=True).distinct()
            for objII in ExpTypeLII:
                ExpTypeOpt[objI].append(objII)
        # endregion

        # region initial data and render
        context = {'status': True,
                   'ReportData': ReportData,
                   'TaskData': TaskData,
                   'ExpReportForm': ExpReportForm,
                   'ExpTypOpt': ExpTypeOpt,
                   "CityOpt": ['Shanghai', 'Beijing', 'Guangzhou', 'Tangshan', 'Wuhan', 'Chongqing', ],
                   "CurrOpt": ['CNY', 'USD', 'EUR', ], }
        return render(request, "expense_01_reimb.html", context)
        # endregion
    # endregion


@login_required()
def vacation(request):
    return render(request, "expense_02_TA.html")


@csrf_exempt
@login_required()
def hr_admin(request):
    """根据用户操作判断执行"""
    # request.GET和request.POST返回一个<QueryDict: {}>对象
    # request.GET.dict()获取QueryDict对象中的字典
    # region GET request
    # print("1")
    if request.method == "GET":
        # GET请求，初始用户信息展示
        # 得到空字典为请求用户信息，获取数据库所有User并展示
        # region Initial GET request
        if not request.GET.dict():
            # print("2")
            # 从models找到UserInfo数据库中所有用户，返回一个包括所有用户的QuerySet对象
            user_list = UserInfo.objects.all()
            formSave = UserModelForm()
            formEdit = UserModelEditForm()
            context = {"queryset": user_list, 'formSave': formSave, 'formEdit': formEdit}
            return render(request, "expense_03_hr.html", context)
        # endregion

        # region Switch GET request
        # GET请求，（编辑用户_路径1_展示数据）和（Switch用户_路径1）
        # 得到非空字典的Ajax请求，根据字典信息（用户操作）变更数据库，最终刷新所有User并展示
        typeID = request.GET.get('typeIDJS')
        uid = request.GET.get('uid')
        # GET请求，（Switch用户_路径1）
        if typeID == 'Switch':
            # print("3")
            exists = UserInfo.objects.filter(id=uid).exists()
            if not exists:
                return JsonResponse({'status': False, 'error': 'User not exist'})

            status_now = UserInfo.objects.filter(id=uid).first().status
            if status_now == 1:
                status_now = 2
            else:
                status_now = 1
            UserInfo.objects.filter(id=uid).update(status=status_now)
            context = {'status': True}
            return JsonResponse(context)
        # endregion

        # region Edit GET request
        # GET请求，（编辑用户_路径1_展示数据）
        if typeID == 'EditDataGet':
            # print("4")
            row_dict = UserInfo.objects.filter(id=uid).values('first_name',
                                                              'last_name',
                                                              'email',
                                                              'hr_admin',
                                                              'finance_admin',
                                                              'company_name',
                                                              'business_unit',
                                                              'line_manager',
                                                              ).first()

            if not row_dict:
                # print('5')
                context = {'status': False, 'error': 'User not exist'}
                return JsonResponse(context)

            # print('6')
            context = {'status': True, 'data': row_dict}
            return JsonResponse(context)
        # endregion
    # endregion

    # region POST request
    # POST请求，新增 和 编辑用户保存_路径1 收到添加信息，验证通过后添加进数据库后返回展示
    if request.method == "POST":
        # 获取前端数据，并校验
        # print('7')
        form = UserModelForm(data=request.POST)
        EditID = request.POST.get("EditID")
        # print(EditID)

        # region Save POST request
        if form.is_valid():
            # 因为存在必填字段，只有save路径过来的数据才会校验通过form.is_valid()=True，新增用户保存_路径1
            # 编辑用户过来的数据校验永远不成功，因此不用判断
            # if EditID == "Save":
            # print('8')
            # print(form.cleaned_data)
            # form.save()
            UserInfo.objects.create_user(**form.cleaned_data)
            # print(user1)
            context = {'status': True, }
            return JsonResponse(context)

        # 数据校验不通过，新增用户返回错误提示_路径1
        edit_data = form.cleaned_data
        # print(edit_data)
        if EditID == "Save":
            # print('9')
            # print(form.errors)
            context = {'status': False, 'errors': form.errors}
            return JsonResponse(context)
        # endregion

        # region Edit POST request
        # 如果是编辑，前端没有获取username等必要字段，因此数据校验不通过
        # 因为可编辑字段，都是非必要字段，所以直接保存这些数据
        # print('10')
        UserInfo.objects.filter(id=int(EditID)).update(first_name=edit_data['first_name'],
                                                       last_name=edit_data['last_name'],
                                                       email=edit_data['email'],
                                                       hr_admin=edit_data['hr_admin'],
                                                       finance_admin=edit_data['finance_admin'],
                                                       company_name=edit_data['company_name'],
                                                       business_unit=edit_data['business_unit'],
                                                       line_manager=edit_data['line_manager'])
        context = {'status': True, }
        return JsonResponse(context)
        # endregion

    # print("=====")
    # context = {'status': False, }
    # return JsonResponse(context)
    # endregion


@csrf_exempt
@login_required()
def finance_admin(request):
    """根据用户操作判断执行"""
    # region POST request
    print('1')
    if request.method == "POST":
        print('====')
        formExpType = ExpTypeModelForm(data=request.POST)  # formExpType 从前端传过来的用户填写信息
        OperateRole = request.POST.get("OperateRole")
        ReportOperate = request.POST.get("ReportOperate")
        ReportNumberOperate = request.POST.get("ReportNumber")

        TaskFunc = request.POST.get("TaskFunc")
        ExpMainTaskTyp = request.POST.get("ExpMainTaskTyp")
        ExpTypeID = request.POST.get("ExpTypeID")

        if OperateRole == 'FinalCon':
            # region FinalCOn action
            ReportOperate = ReportOperate.replace("\n", "")
            ReportOperate = ReportOperate.replace(" ", "")
            if ReportOperate == 'Approve':
                Expense_Report.objects.filter(report_number=ReportNumberOperate).update(final_action=4)
                Expense_Report.objects.filter(report_number=ReportNumberOperate).update(finanDepart=2)
                context = {'status': True, }
                return JsonResponse(context)
            elif ReportOperate == 'Reject':
                Expense_Report.objects.filter(report_number=ReportNumberOperate).update(final_action=3)
                # Expense_Report.objects.filter(report_number=ReportNumberOperate).update(line_manager_action=2)
                context = {'status': True, }
                return JsonResponse(context)
            # endregion
        elif OperateRole == 'FinDepart':
            # region ComplianceCheck action
            ReportOperate = ReportOperate.replace("\n", "")
            ReportOperate = ReportOperate.replace(" ", "")
            if ReportOperate == 'Approve':
                Expense_Report.objects.filter(report_number=ReportNumberOperate).update(finanDepart=5)
                Expense_Report.objects.filter(report_number=ReportNumberOperate).update(report_status=3)
                context = {'status': True, }
                return JsonResponse(context)
            elif ReportOperate == 'ActionRequired':
                Expense_Report.objects.filter(report_number=ReportNumberOperate).update(finanDepart=1,
                                                                                        report_status=1,
                                                                                        line_manager_action=1,
                                                                                        final_action=1,
                                                                                        )
                context = {'status': True, }
                return JsonResponse(context)
            elif ReportOperate == 'DocRequired':
                Expense_Report.objects.filter(report_number=ReportNumberOperate).update(finanDepart=4)
                context = {'status': True, }
                return JsonResponse(context)
            # endregion
        else:
            if TaskFunc == 'ExpMainTask':
                #  region ExpMainTask Switch
                if ExpMainTaskTyp == 'Switch':
                    print("1-2")
                    exists = Expense_Type.objects.filter(id=ExpTypeID).exists()
                    if not exists:
                        return JsonResponse({'status': False, 'error': 'ExpenseType not exist'})

                    status_now = Expense_Type.objects.filter(id=ExpTypeID).first().status
                    if status_now == 1:
                        status_now = 2
                    else:
                        status_now = 1
                    Expense_Type.objects.filter(id=ExpTypeID).update(status=status_now)
                    JsonSeriExpType = json.loads(serializers.serialize('json', Expense_Type.objects.all()))
                    # JsonSeri = serializers.serialize('json', Expense_Type.objects.all())
                    # JsonSeri = json.loads(JsonSeri)
                    context = {'status': True, "JsonSeriExpType": JsonSeriExpType}
                    return JsonResponse(context)
                    # return JsonResponse(JsonSeri, safe=False)
                # endregion

                if formExpType.is_valid():
                    # region data process
                    # {'expense_type_level1': '1', 'expense_type_level2': '2'}
                    print('1-3')
                    expenseType = formExpType.cleaned_data
                    expenseType['expense_type'] = expenseType['expense_type_level1'] + '_' + expenseType[
                        'expense_type_level2']
                    expenseType_obj = Expense_Type.objects.filter(**expenseType)
                    # endregion

                    # region validate the unique data by usr for add and edit
                    if expenseType_obj:
                        print('1-4')
                        context = {'status': True, 'exist': True, }
                        return JsonResponse(context)
                    # endregion

                    #  region ExpMainTask Add Save
                    if ExpTypeID == '':
                        print('1-5')
                        Expense_Type.objects.create(**expenseType)
                        JsonSeriExpType = json.loads(serializers.serialize('json', Expense_Type.objects.all()))
                        print(JsonSeriExpType)
                        context = {'status': True, 'exist': False, "JsonSeriExpType": JsonSeriExpType}
                        return JsonResponse(context)
                    # endregion

                    #  region ExpMainTask Edit Save
                    print('1-6')
                    Expense_Type.objects.filter(id=int(ExpTypeID)).update(**expenseType)
                    JsonSeriExpType = json.loads(serializers.serialize('json', Expense_Type.objects.all()))
                    context = {'status': True, 'exist': False, "JsonSeriExpType": JsonSeriExpType}
                    return JsonResponse(context)
                    # endregion

                # region data not valid，return errors
                print('1-7')
                # print(formExpType.errors)
                context = {'status': False, "errors": formExpType.errors, }
                return JsonResponse(context)
                # endregion
    # endregion

    # region GET request
    print('2-1')
    TaskFunc = request.GET.get("TaskFunc")
    ExpMainTaskTyp = request.GET.get("ExpMainTaskTyp")
    ExpTypeID = request.GET.get("ExpTypeID")
    if TaskFunc == 'ExpMainTask':

        #  region ExpMainTask EditDataGet
        print("2-4")
        row_dict = Expense_Type.objects.filter(id=ExpTypeID).values('expense_type_level1',
                                                                    'expense_type_level2', ).first()
        if not row_dict:
            context = {'status': False, 'error': 'User not exist'}
            return JsonResponse(context)
        context = {'status': True, 'data': row_dict}
        return JsonResponse(context)
        # endregion

    # region initial request

    if not ExpTypeID:
        print("2-4")
        # region TaskData composition for FA
        ReportAllFA = Expense_Report.objects.filter(final_action__gt=1).values_list('report_number', flat=True).distinct()
        FATaskData = []
        i = 0
        for RepNum in ReportAllFA:
            FATaskData.append([])
            FATaskData[i].append(str(i + 1))
            FATaskData[i].append(RepNum)
            ReportObject = Expense_Report.objects.filter(report_number=RepNum)
            FATaskData[i].append(ReportObject[0].Crt_date.strftime("%Y%m%d"))
            FATaskData[i].append(ReportObject[0].get_final_action_display())
            FATaskData[i].append([])
            j = 0
            for obj in ReportObject:
                FATaskData[i][4].append([])
                ReportLineQuerySet = Expense_Report.objects.filter(report_number=RepNum, id=obj.pk)
                ReportLineObj = Expense_Report.objects.filter(report_number=RepNum, id=obj.pk).first()
                ReportExpTypI = Expense_Type.objects.filter(
                    expense_type=ReportLineObj.expenseTyp).first().expense_type_level1
                ReportExpTypII = Expense_Type.objects.filter(
                    expense_type=ReportLineObj.expenseTyp).first().expense_type_level2
                FATaskData[i][4][j].append(ReportExpTypI)
                FATaskData[i][4][j].append(ReportExpTypII)
                FATaskData[i][4][j].append(ReportLineQuerySet)
                j += 1
            i += 1
        # endregion

        # region TaskData composition for ComplianceCheck
        ReportAllCC = Expense_Report.objects.filter(finanDepart__gt=1).values_list('report_number', flat=True).distinct()
        CCTaskData = []
        i = 0
        for RepNum in ReportAllCC:
            CCTaskData.append([])
            CCTaskData[i].append(str(i + 1))
            CCTaskData[i].append(RepNum)
            ReportObject = Expense_Report.objects.filter(report_number=RepNum)
            CCTaskData[i].append(ReportObject[0].Crt_date.strftime("%Y%m%d"))
            CCTaskData[i].append(ReportObject[0].get_finanDepart_display())
            CCTaskData[i].append([])
            j = 0
            for obj in ReportObject:
                CCTaskData[i][4].append([])
                ReportLineQuerySet = Expense_Report.objects.filter(report_number=RepNum, id=obj.pk)
                ReportLineObj = Expense_Report.objects.filter(report_number=RepNum, id=obj.pk).first()
                ReportExpTypI = Expense_Type.objects.filter(
                    expense_type=ReportLineObj.expenseTyp).first().expense_type_level1
                ReportExpTypII = Expense_Type.objects.filter(
                    expense_type=ReportLineObj.expenseTyp).first().expense_type_level2
                CCTaskData[i][4][j].append(ReportExpTypI)
                CCTaskData[i][4][j].append(ReportExpTypII)
                CCTaskData[i][4][j].append(ReportLineQuerySet)
                j += 1
            i += 1
        # endregion

        # JsonSeriExpType = json.loads(serializers.serialize('json', Expense_Type.objects.all()))
        querySet = Expense_Type.objects.all()
        ExpTypeForm = ExpTypeModelForm()
        # list_result = [entry for entry in exptyp_list]
        context = {'status': True,
                   "querySet": querySet,
                   'FATaskData': FATaskData,
                   'CCTaskData': CCTaskData,
                   'ExpTypeForm': ExpTypeForm, }
        return render(request, "expense_04_finance.html", context)
    # endregion
    # endregion

    # endregion


def test(request):
    user_list = UserInfo.objects.all()
    form = UserModelForm()
    context = {"queryset": user_list, 'form': form}
    return render(request, "test.html", context)


def test_switch(request):
    uid = request.GET.get('uid')
    print("===========")
    print(request.GET.dict())
    print(request.GET.get('uid'))
    print(uid)
    return HttpResponse(uid)


def test1(request):
    """根据用户操作判断执行"""
    # region POST request

    return render(request, "xxx.html")

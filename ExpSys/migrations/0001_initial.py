# Generated by Django 4.2.6 on 2023-10-29 10:07

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(1, '启用'), (2, '冻结')], default=1, verbose_name='status')),
                ('expense_type_level1', models.CharField(max_length=100)),
                ('expense_type_level2', models.CharField(max_length=100)),
                ('expense_type', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('status', models.SmallIntegerField(choices=[(1, '在职'), (2, '离职')], default=1, verbose_name='status')),
                ('hr_admin', models.SmallIntegerField(choices=[(1, False), (2, True)], default=1, verbose_name='hr_admin')),
                ('finance_admin', models.SmallIntegerField(choices=[(1, False), (2, True)], default=1, verbose_name='finance_admin')),
                ('company_name', models.CharField(blank=True, max_length=10, null=True, verbose_name='company_name')),
                ('business_unit', models.CharField(blank=True, max_length=30, null=True, verbose_name='business_unit')),
                ('line_manager', models.CharField(blank=True, max_length=100, null=True, verbose_name='line_manager')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Expense_Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_number', models.CharField(max_length=100)),
                ('Crt_date', models.DateTimeField()),
                ('exp_date', models.DateTimeField()),
                ('from_location', models.CharField(blank=True, max_length=100, null=True, verbose_name='From')),
                ('to_location', models.CharField(blank=True, max_length=100, null=True, verbose_name='To')),
                ('Currency', models.CharField(max_length=3)),
                ('exchange_rate', models.FloatField(default=1)),
                ('orig_amount', models.FloatField(verbose_name='Original Amount')),
                ('local_amount', models.FloatField(verbose_name='Local Amount')),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('line_manager_comments', models.CharField(blank=True, max_length=100, null=True)),
                ('final_comments', models.TextField(blank=True, max_length=255, null=True)),
                ('finance_comments', models.TextField(blank=True, max_length=255, null=True)),
                ('report_status', models.SmallIntegerField(choices=[(1, 'Draft'), (2, 'Sent'), (3, 'Completed')], default=1)),
                ('email', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('expenseTyp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ExpSys.expense_type', to_field='expense_type', verbose_name='Expense Type')),
            ],
        ),
    ]
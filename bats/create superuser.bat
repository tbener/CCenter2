:: First run migration to create the db file
%~dp0run_command createsuperuser
::%~dp0run_command shell "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', '123')"
::echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', '123')" | "%python3%" "%~dp0..\manage.py" shell
::pause
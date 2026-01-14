import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartfirm_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# 检查是否已存在 admin 用户
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@smartfirm.com',
        password='admin123456'
    )
    print("Superuser created successfully!")
    print("Username: admin")
    print("Password: admin123456")
    print("Email: admin@smartfirm.com")
else:
    print("User 'admin' already exists")

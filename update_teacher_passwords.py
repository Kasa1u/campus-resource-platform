"""
批量更新老师密码为与账号名一致，t1保持为t123
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_platform.settings')
django.setup()

from users.models import User

def update_teacher_passwords():
    print("开始更新老师账号密码...")
    
    # 更新所有老师账号
    teachers = User.objects.filter(role='teacher')
    for teacher in teachers:
        # t1保持密码为t123，其他老师密码设置为与用户名相同
        if teacher.username == 't1':
            teacher.set_password('t123')
            teacher.save()
            print(f"  ✓ 保持 {teacher.name} ({teacher.username}) 密码为：t123")
        else:
            teacher.set_password(teacher.username)
            teacher.save()
            print(f"  ✓ 更新 {teacher.name} ({teacher.username}) 密码为：{teacher.username}")
    
    print("\n✅ 所有老师账号密码已更新！")
    print("\n📋 老师账号列表:")
    for teacher in teachers:
        if teacher.username == 't1':
            print(f"  - {teacher.username} / t123 ({teacher.name})")
        else:
            print(f"  - {teacher.username} / {teacher.username} ({teacher.name})")

if __name__ == '__main__':
    update_teacher_passwords()
"""
批量更新学生密码为与账号名一致
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_platform.settings')
django.setup()

from users.models import User

def update_student_passwords():
    print("开始更新学生账号密码...")
    
    # 更新所有学生账号
    students = User.objects.filter(role='student')
    for student in students:
        # s1保持密码为s123，其他学生密码设置为与用户名相同
        if student.username == 's1':
            student.set_password('s123')
            student.save()
            print(f"  ✓ 保持 {student.name} ({student.username}) 密码为：s123")
        else:
            student.set_password(student.username)
            student.save()
            print(f"  ✓ 更新 {student.name} ({student.username}) 密码为：{student.username}")
    
    print("\n✅ 所有学生账号密码已更新！")
    print("\n📋 学生账号列表:")
    for student in students:
        if student.username == 's1':
            print(f"  - {student.username} / s123 ({student.name})")
        else:
            print(f"  - {student.username} / {student.username} ({student.name})")

if __name__ == '__main__':
    update_student_passwords()

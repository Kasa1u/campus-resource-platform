"""
更新学生导师关系脚本
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_platform.settings')
django.setup()

from users.models import User

def update_supervisors():
    print("开始更新学生导师关系...")
    
    # 获取老师
    t101 = User.objects.get(username='t101')  # 张伟
    t102 = User.objects.get(username='t102')  # 李娜
    t103 = User.objects.get(username='t103')  # 王强
    
    # 学生与导师的对应关系
    updates = {
        # 张伟 (t101) 的学生 - 计算机科学专业
        's1001': t101,  # 刘一
        's1003': t101,  # 张三
        's1005': t101,  # 王五
        's1008': t101,  # 周八
        
        # 李娜 (t102) 的学生 - 软件工程专业
        's1002': t102,  # 陈二
        's1006': t102,  # 赵六
        's1009': t102,  # 吴九
        
        # 王强 (t103) 的学生 - 网络工程专业
        's1004': t103,  # 李四
        's1007': t103,  # 孙七
        's1010': t103,  # 郑十
    }
    
    for username, supervisor in updates.items():
        try:
            student = User.objects.get(username=username)
            student.supervisor = supervisor
            student.save()
            print(f"  ✓ 更新 {student.name} ({username}) 的导师为 {supervisor.name}")
        except User.DoesNotExist:
            print(f"  ✗ 学生 {username} 不存在")
    
    print("\n✅ 导师关系更新完成！")
    
    # 显示每位老师的学生
    print("\n📋 导师 - 学生关系：")
    for teacher in [t101, t102, t103]:
        students = teacher.students.all()
        print(f"\n{teacher.name} ({teacher.username}) 的学生:")
        for student in students:
            print(f"  - {student.name} ({student.username}) - {student.major} - {student.grade}级")

if __name__ == '__main__':
    update_supervisors()

"""
示例数据初始化脚本
用于创建丰富的测试数据，包括：
- 测试账号（重命名）
- 真实感的老师账号（101-103）
- 真实感的学生账号（1001-1010）
- 课程资源
- 论坛帖子
- 公告等
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_platform.settings')
django.setup()

from users.models import User
from courses.models import Resource, ResourceType, ResourceComment
from forum.models import ForumPost, ForumComment
from announcements.models import Announcement
from points.models import PointsRecord
from django.utils import timezone
from datetime import timedelta

def create_sample_data():
    print("=" * 60)
    print("开始创建示例数据...")
    print("=" * 60)
    
    # ========== 1. 修改测试账号名称 ==========
    print("\n📝 修改测试账号名称...")
    
    # 修改学生测试账号
    try:
        student_test = User.objects.get(username='s1', role='student')
        student_test.name = '测试账号_学生'
        student_test.save()
        print("  ✓ 学生测试账号已更新：s1 -> 测试账号_学生")
    except User.DoesNotExist:
        print("  ✗ 学生测试账号不存在")
    
    # 修改老师测试账号
    try:
        teacher_test = User.objects.get(username='t1', role='teacher')
        teacher_test.name = '测试账号_老师'
        teacher_test.student_id = 'TEST001'
        teacher_test.major = '计算机科学'
        teacher_test.save()
        print("  ✓ 老师测试账号已更新：t1 -> 测试账号_老师")
    except User.DoesNotExist:
        print("  ✗ 老师测试账号不存在")
    
    # ========== 2. 创建真实的老师账号 ==========
    print("\n👨‍🏫 创建老师账号...")
    
    teachers_data = [
        {
            'username': 't101',
            'password': 't101',
            'name': '张伟',
            'gender': 'male',
            'email': 'zhangwei@campus.edu',
            'phone': '13800138001',
            'major': '计算机科学与技术',
            'title': '教授',
            'bio': '计算机科学博士，主要研究方向为人工智能和机器学习。'
        },
        {
            'username': 't102',
            'password': 't102',
            'name': '李娜',
            'gender': 'female',
            'email': 'lina@campus.edu',
            'phone': '13800138002',
            'major': '软件工程',
            'title': '副教授',
            'bio': '软件工程专业，专注于 Web 开发和数据库系统教学。'
        },
        {
            'username': 't103',
            'password': 't103',
            'name': '王强',
            'gender': 'male',
            'email': 'wangqiang@campus.edu',
            'phone': '13800138003',
            'major': '网络工程',
            'title': '讲师',
            'bio': '网络工程专家，擅长网络安全和云计算。'
        },
    ]
    
    # 更新测试老师账号密码
    try:
        teacher_test = User.objects.get(username='t1')
        teacher_test.set_password('t1')
        teacher_test.save()
        print("  ✓ 更新测试老师账号密码：t1/t1")
    except User.DoesNotExist:
        print("  ✗ 测试老师账号不存在")
    
    teachers = []
    for teacher_data in teachers_data:
        teacher, created = User.objects.get_or_create(
            username=teacher_data['username'],
            defaults={
                'name': teacher_data['name'],
                'role': 'teacher',
                'gender': teacher_data['gender'],
                'email': teacher_data['email'],
                'phone': teacher_data['phone'],
            }
        )
        if created:
            teacher.set_password(teacher_data['password'])
            teacher.student_id = teacher_data['username'][1:]  # 去掉't'
            teacher.major = teacher_data['major']
            teacher.title = teacher_data['title']
            teacher.bio = teacher_data['bio']
            teacher.save()
            print(f"  ✓ 创建老师账号：{teacher.name} ({teacher.username})")
        else:
            print(f"  - 老师账号已存在：{teacher.name} ({teacher.username})")
        teachers.append(teacher)
    
    # ========== 3. 创建学生账号 ==========
    print("\n👨‍🎓 创建学生账号...")
    
    # 更新测试学生账号密码
    try:
        student_test = User.objects.get(username='s1')
        student_test.set_password('s1')
        student_test.save()
        print("  ✓ 更新测试学生账号密码：s1/s1")
    except User.DoesNotExist:
        print("  ✗ 测试学生账号不存在")
    
    # 学生与导师的对应关系
    student_supervisor_map = {
        # 张伟 (t101) 的学生 - 计算机科学专业
        's1001': teachers[0],  # 刘一
        's1003': teachers[0],  # 张三
        's1005': teachers[0],  # 王五
        's1008': teachers[0],  # 周八
        
        # 李娜 (t102) 的学生 - 软件工程专业
        's1002': teachers[1],  # 陈二
        's1006': teachers[1],  # 赵六
        's1009': teachers[1],  # 吴九
        
        # 王强 (t103) 的学生 - 网络工程专业
        's1004': teachers[2],  # 李四
        's1007': teachers[2],  # 孙七
        's1010': teachers[2],  # 郑十
    }
    
    students_data = [
        {'username': 's1001', 'password': 's1001', 'name': '刘一', 'gender': 'male', 'major': '计算机科学', 'grade': '2022'},
        {'username': 's1002', 'password': 's1002', 'name': '陈二', 'gender': 'female', 'major': '软件工程', 'grade': '2022'},
        {'username': 's1003', 'password': 's1003', 'name': '张三', 'gender': 'male', 'major': '计算机科学', 'grade': '2023'},
        {'username': 's1004', 'password': 's1004', 'name': '李四', 'gender': 'female', 'major': '网络工程', 'grade': '2023'},
        {'username': 's1005', 'password': 's1005', 'name': '王五', 'gender': 'male', 'major': '计算机科学', 'grade': '2022'},
        {'username': 's1006', 'password': 's1006', 'name': '赵六', 'gender': 'female', 'major': '软件工程', 'grade': '2023'},
        {'username': 's1007', 'password': 's1007', 'name': '孙七', 'gender': 'male', 'major': '网络工程', 'grade': '2022'},
        {'username': 's1008', 'password': 's1008', 'name': '周八', 'gender': 'female', 'major': '计算机科学', 'grade': '2023'},
        {'username': 's1009', 'password': 's1009', 'name': '吴九', 'gender': 'male', 'major': '软件工程', 'grade': '2022'},
        {'username': 's1010', 'password': 's1010', 'name': '郑十', 'gender': 'female', 'major': '网络工程', 'grade': '2023'},
    ]
    
    students = []
    for student_data in students_data:
        student, created = User.objects.get_or_create(
            username=student_data['username'],
            defaults={
                'name': student_data['name'],
                'role': 'student',
                'gender': student_data['gender'],
                'major': student_data['major'],
                'grade': student_data['grade'],
                'email': f"{student_data['username']}@student.edu",
            }
        )
        if created:
            student.set_password(student_data['password'])  # 使用独立密码
            student.student_id = student_data['username'][1:]  # 去掉's'
            # 分配导师
            supervisor = student_supervisor_map.get(student_data['username'])
            if supervisor:
                student.supervisor = supervisor
            student.save()
            supervisor_name = f" (导师：{supervisor.name})" if supervisor else ""
            print(f"  ✓ 创建学生账号：{student.name} ({student.username}/{student_data['password']}){supervisor_name}")
        else:
            print(f"  - 学生账号已存在：{student.name} ({student.username})")
        students.append(student)
    
    # ========== 4. 创建资源类型 ==========
    print("\n📚 创建资源类型...")
    
    resource_types = ['课件', '作业', '视频', '文档', '代码']
    for rt_name in resource_types:
        rt, created = ResourceType.objects.get_or_create(name=rt_name)
        if created:
            print(f"  ✓ 创建资源类型：{rt.name}")
    
    # ========== 5. 创建课程资源示例 ==========
    print("\n📚 创建资源示例...")
    
    resources_data = [
        # 校内课程（课件、作业）
        {
            'title': 'Python 编程基础教程',
            'type_name': '课件',
            'uploader': teachers[0],  # 张伟
            'description': 'Python 语言入门教程，包含 PPT 和示例代码',
            'points_required': 10,
            'category': 'campus'  # 校内课程
        },
        {
            'title': 'Web 开发实战项目',
            'type_name': '作业',
            'uploader': teachers[1],  # 李娜
            'description': '完整的 Web 开发项目实战练习',
            'points_required': 20,
            'category': 'campus'  # 校内课程
        },
        # 网络课程（视频）
        {
            'title': '计算机网络教学视频',
            'type_name': '视频',
            'uploader': teachers[2],  # 王强
            'description': '网络协议详解视频课程',
            'points_required': 30,
            'category': 'online'  # 网络课程
        },
        # 书籍资源（文档）
        {
            'title': 'Python 编程电子书',
            'type_name': '文档',
            'uploader': teachers[0],  # 张伟
            'description': 'Python 编程从入门到精通完整电子书',
            'points_required': 15,
            'category': 'books'  # 书籍资源
        },
        {
            'title': 'Web 前端开发指南',
            'type_name': '文档',
            'uploader': teachers[1],  # 李娜
            'description': 'HTML/CSS/JavaScript 完整教程文档',
            'points_required': 20,
            'category': 'books'  # 书籍资源
        },
    ]
    
    for res_data in resources_data:
        resource_type = ResourceType.objects.get(name=res_data['type_name'])
        resource, created = Resource.objects.get_or_create(
            title=res_data['title'],
            defaults={
                'type': resource_type,
                'uploader': res_data['uploader'],
                'description': res_data['description'],
                'points_required': res_data['points_required'],
                'status': 'active'
            }
        )
        if created:
            print(f"  ✓ 创建资源：{resource.title}")
        else:
            print(f"  - 资源已存在：{resource.title}")
    
    # ========== 6. 创建论坛帖子 ==========
    print("\n💬 创建论坛帖子...")
    
    posts_data = [
        {
            'title': 'Python 学习心得分享',
            'author': students[0],  # 刘一
            'content': '大家好，我学习 Python 已经三个月了，分享一些学习心得。Python 真的是一门非常友好的语言...'
        },
        {
            'title': 'Web 开发中遇到的问题',
            'author': students[1],  # 陈二
            'content': '在学习 Web 开发的过程中，遇到了很多有趣的问题，大家一起来讨论一下吧...'
        },
        {
            'title': '网络协议详解',
            'author': teachers[0],  # 张伟
            'content': '今天给大家详细讲解一下 TCP/IP 协议，这是网络编程的基础...'
        },
    ]
    
    posts = []
    for post_data in posts_data:
        post, created = ForumPost.objects.get_or_create(
            title=post_data['title'],
            defaults={
                'author': post_data['author'],
                'content': post_data['content'],
            }
        )
        if created:
            print(f"  ✓ 创建帖子：{post.title}")
        else:
            print(f"  - 帖子已存在：{post.title}")
        posts.append(post)
    
    # ========== 7. 创建公告 ==========
    print("\n📢 创建公告...")
    
    announcements_data = [
        {
            'title': '2024 年春季学期选课通知',
            'content': '各位同学请注意，2024 年春季学期选课将于 3 月 1 日开始...',
            'author': teachers[0]
        },
        {
            'title': '关于举办编程比赛的通知',
            'content': '为激发同学们的编程兴趣，学校将举办年度编程比赛...',
            'author': teachers[1]
        },
    ]
    
    for ann_data in announcements_data:
        announcement, created = Announcement.objects.get_or_create(
            title=ann_data['title'],
            defaults={
                'content': ann_data['content'],
                'author': ann_data['author'],
            }
        )
        if created:
            print(f"  ✓ 创建公告：{announcement.title}")
        else:
            print(f"  - 公告已存在：{announcement.title}")
    
    # ========== 8. 创建积分记录 ==========
    print("\n💰 创建积分记录...")
    
    for student in students[:5]:  # 给前 5 个学生创建积分记录
        points, created = PointsRecord.objects.get_or_create(
            user=student,
            points=100,  # 初始积分
            defaults={
                'type': 'add',
                'reason': '注册奖励',
            }
        )
        if created:
            print(f"  ✓ 为 {student.name} 创建积分记录")
    
    print("\n" + "=" * 60)
    print("✅ 示例数据创建完成！")
    print("=" * 60)
    print("\n📋 账号汇总:")
    print("\n🔹 测试账号:")
    print("  - 学生：s1 / s123 (测试账号_学生)")
    print("  - 老师：t1 / t123 (测试账号_老师)")
    print("  - 管理员：admin / admin123")
    print("\n🔹 真实老师账号:")
    for teacher in teachers:
        print(f"  - {teacher.username} / t{teacher.username[1:]} ({teacher.name} - {teacher.major})")
    print("\n🔹 学生账号 (10 个):")
    for student in students:
        print(f"  - {student.username} / s123 ({student.name} - {student.major} - {student.grade}级)")
    print("\n💡 提示：所有学生的默认密码都是 s123")
    print("=" * 60)

if __name__ == '__main__':
    create_sample_data()

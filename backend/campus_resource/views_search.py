"""
搜索相关的 API 视图
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from campus_resource.models import Resource, ForumPost

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_resources(request):
    """
    搜索资源
    GET /api/resources/search/?q=关键词
    """
    query = request.GET.get('q', '').strip()
    
    if not query:
        return Response([])
    
    # 搜索资源标题和描述
    resources = Resource.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query)
    ).select_related('uploader')[:10]  # 限制返回 10 条
    
    results = [
        {
            'id': r.id,
            'title': r.title,
            'description': r.description[:100] if r.description else '',
            'type': r.category,
            'uploader': r.uploader.username,
            'download_count': r.download_count
        }
        for r in resources
    ]
    
    return Response(results)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_forum(request):
    """
    搜索论坛帖子
    GET /api/forum/search/?q=关键词
    """
    query = request.GET.get('q', '').strip()
    
    if not query:
        return Response([])
    
    # 搜索帖子标题和内容
    posts = ForumPost.objects.filter(
        Q(title__icontains=query) | 
        Q(content__icontains=query)
    ).select_related('author')[:10]  # 限制返回 10 条
    
    results = [
        {
            'id': post.id,
            'title': post.title,
            'description': post.content[:100] if post.content else '',
            'type': 'forum',
            'author': post.author.username,
            'views': post.views,
            'replies': post.replies
        }
        for post in posts
    ]
    
    return Response(results)

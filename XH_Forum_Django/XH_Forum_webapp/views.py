from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.models import User
from XH_Forum_webapp.models import Post
import json
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db.models import Q
# class HelloWorldView(View):
#     template_name = 'HelloWorld'
# Create your views here.
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            request.session["info"] = username
            #print(request.session.get('info'))
            return HttpResponse('http://localhost:8080//HelloWorld')
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')       
        user = User.objects.create_user(username=username, password=password,email=email)
        if user is not None:
         return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': false})

class PostEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Post):
            # 将 Post 对象转换为字典形式
            return {
                'id': obj.id,
                'title': obj.title,
                'content': obj.content,
                'description': obj.description,
                'created_at': obj.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'likeCount': obj.likeCount,
                'comments': obj.comments,
                'author_id': obj.author_id,
            }
        return super().default(obj)

@csrf_exempt
def show_post(request):
    if not request.session.get('info'):
        return JsonResponse({'success': 'false'})
    else:
        posts = Post.objects.all()
        serialized_posts = json.dumps(list(posts), cls=PostEncoder)
        return JsonResponse({'posts': serialized_posts}, safe=False)

@csrf_exempt
def show_user_post(request):
    if not request.session.get('info'):
        return JsonResponse({'success': 'error'})
    else:
        username = request.session.get('info')  # 获取特定用户名
        print(username)
        user = User.objects.get(username=username)  # 获取用户对象
        posts = Post.objects.filter(author=user)  # 筛选特定用户的帖子
        serialized_posts = json.dumps(list(posts), cls=PostEncoder)
        return JsonResponse({'posts': serialized_posts}, safe=False)

@csrf_exempt
def show_user_message(request):
    if not request.session.get('info'):
        return JsonResponse({'success': 'error'})
    else:
        username = request.session.get('info')
        print(username)  # 获取特定用户名
        user = User.objects.get(username=username)
        print(user)  # 获取用户对象
        message = {
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined
        }
        print(message)
        return JsonResponse(message)

@csrf_exempt
def search(request):
    keyword = request.GET.get('keyword', '')
    print(keyword)
    search_results = Post.objects.filter(
        Q(title=keyword) |  # 标题包含关键词
        Q(content=keyword) |  # 内容包含关键词
        Q(description=keyword)  # 摘要包含关键词)
    )
    # 构造搜索结果的数据结构
    results_data = []
    for result in search_results:
        results_data.append({
            'id': result.id,
            'title': result.title,
            'description':result.description,
            'content':result.content,
            'created_at':result.created_at,
            'likeCount': result.likeCount,
            'comments': result.comments,
            'author_id': result.author_id,
            # 其他字段...
        })
    print(results_data)
    return JsonResponse(results_data, safe=False)

@csrf_exempt
def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('postId')
        try:
            post = Post.objects.get(id=post_id)
            post.likeCount += 1
            post.save()
            return JsonResponse({'likeCount': post.likeCount})
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



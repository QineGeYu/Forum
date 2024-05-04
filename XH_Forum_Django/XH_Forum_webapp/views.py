from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.models import User
from XH_Forum_webapp.models import Post
from XH_Forum_webapp.models import Comment
from XH_Forum_webapp.models import Contact
from XH_Forum_webapp.models import Notification
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
        return JsonResponse({'posts': serialized_posts}, safe=False)#特殊字符过滤，数据传输加密，特殊区域访问，DDOS，

@csrf_exempt
def show_user_post(request):
    if not request.session.get('info'):
        return JsonResponse({'success': 'error'})
    else:
        username = request.session.get('info')  # 获取特定用户名
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
        user = User.objects.get(username=username)
        message = {
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined
        }
        return JsonResponse(message)
@csrf_exempt
def show_user_post2(request):
    if not request.session.get('info'):
        return JsonResponse({'success': 'error'})
    else:
        username = request.GET.get('username') # 获取特定用户名
        user = User.objects.get(username=username)  # 获取用户对象
        posts = Post.objects.filter(author=user)  # 筛选特定用户的帖子
        serialized_posts = json.dumps(list(posts), cls=PostEncoder)
        return JsonResponse({'posts': serialized_posts}, safe=False)

@csrf_exempt
def show_user_message2(request):
    if not request.session.get('info'):
        return JsonResponse({'success': 'error'})
    else:
        username = request.GET.get('username') # 获取特定用户名
        user = User.objects.get(username=username)
        message = {
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined
        }
        return JsonResponse(message)

@csrf_exempt
def search(request):
    keyword = request.GET.get('keyword', '')
    search_results = Post.objects.filter(
        Q(title__icontains=keyword) |  # 标题包含关键词
        Q(content__icontains=keyword) |  # 内容包含关键词
        Q(description__icontains=keyword)  # 摘要包含关键词)
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

    return JsonResponse(results_data, safe=False)

@csrf_exempt
def like_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('postId')
        try:
            post = Post.objects.get(id=post_id)
            post.likeCount += 1
            post.save()
            return JsonResponse({'likeCount': post.likeCount})
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=480)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=481)

@csrf_exempt
def like_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        comment_id = data.get('commentId')
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.like_count += 1
            comment.save()
            return JsonResponse({'like_count': comment.like_count})
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Comment not found'}, status=480)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=481)

@csrf_exempt
def publish_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description')
            content = data.get('content')
            author_username = data.get('user')
            post = Post.objects.create(
                title=title,
                description=description,
                content=content,
                author_id=author_username,
                # created_at=time,
                likeCount=0,
                comments=0,
            )
            return JsonResponse({'message': '帖子发布成功'})
        except Exception as e:
            return JsonResponse({'message': '帖子发布失败', 'error': str(e)}, status=400)
    else:
        return JsonResponse({'message': '无效的请求方法'}, status=405)

@csrf_exempt
def get_post_detail(request, post_id):
    if request.session.get('info'):
        try:
          post = Post.objects.get(id=post_id)
        # 根据需要选择返回的数据字段
          data = {
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'content': post.content,
            'time': post.created_at,
            'author_id': post.author_id
            # 其他帖子详情字段
          }
          return JsonResponse(data)
        except Post.DoesNotExist:
          return JsonResponse({'error': 'Post not found'}, status=404)
    else:
        return JsonResponse({'message': '请登录后再访问'}, status=405)

@csrf_exempt
def get_post_comments(request, post_id):
    if request.session.get('info'):
            comments = Comment.objects.filter(post_id=post_id)
            serialized_comments = []
            for comment in comments:
              serialized_comment = {
               'content': comment.content,
               'author': comment.author.username,
               'created_at': comment.created_at,
               'like_count': comment.like_count,
               'id': comment.id
              }
              serialized_comments.append(serialized_comment)
            return JsonResponse({'comments': serialized_comments}, safe=False)
    else:
        return JsonResponse({'message': '请登录后再访问'}, status=405)

@csrf_exempt
def publish_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')
            author_username = data.get('user')
            postId = data.get('postId')
            comment = Comment.objects.create(
                content=content,
                author_id=author_username,
                post_id=postId,
                like_count=0,
            )
            return JsonResponse({'message': '评论发布成功'})
        except Exception as e:
            return JsonResponse({'message': '评论发布失败', 'error': str(e)}, status=400)
    else:
        return JsonResponse({'message': '无效的请求方法'}, status=405)

@csrf_exempt
def save_contact(request):
    if not request.session.get('info'):
        return JsonResponse({'success': 'error'})
    else:
        data = json.loads(request.body)
        main_users = request.session.get('info')
        main_user = User.objects.get(username=main_users)
        contacted_users = data.get('contacted_users')
        contacted_user = User.objects.get(username=contacted_users)
        existing_contact = Contact.objects.filter(main_user=main_user, contacted_user=contacted_user).exists()
        if existing_contact:
            return JsonResponse({'success': 'Contact already exists'})
        contact = Contact.objects.create(main_user=main_user, contacted_user=contacted_user)
        return JsonResponse({'success': 'Contact saved successfully'})

def get_contacts(request):
    if not request.session.get('info'):
        return JsonResponse({'success': 'error'})
    # 获取当前用户的联系人列表
    main_user = request.session.get('info')
    contacts = Contact.objects.filter(main_user__username=main_user)
    contact_usernames = [contact.contacted_user.username for contact in contacts]
    
    return JsonResponse({'contacts': contact_usernames})
@csrf_exempt
def get_chat_messages(request):
    if not request.session.get('info'):
        return JsonResponse({'success': 'error'})
    else:
        if request.method == 'POST':
            sender = request.session.get('info')
            data = json.loads(request.body)
            receiver = data.get('receiver')
            messages = Notification.objects.filter(
                Q(sender_id=sender, receiver_id=receiver) | Q(sender_id=receiver, receiver_id=sender)
            ).order_by('created_at')
            message_list = [
                {
                    'sender_id': msg.sender_id,
                    'content': msg.message,
                    'created_at': msg.created_at
                }
                for msg in messages
            ]
            return JsonResponse(message_list, safe=False)
        return JsonResponse({'error': 'Invalid request method'})
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.core import mail
from django.contrib.auth.models import User
from XH_Forum_webapp.models import Post
from XH_Forum_webapp.models import Comment
from XH_Forum_webapp.models import Contact
from XH_Forum_webapp.models import Notification
from XH_Forum_webapp.models import UserPublicKey
from XH_Forum_webapp.models import VerificationCode
import json
import random
import os
import string
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render, redirect
from XH_Forum_webapp.forms import ProfileForm
from XH_Forum_webapp.models import Profile
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
    
@csrf_exempt
def getEmail(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')  # 从请求中获取用户名
        try:
            user = User.objects.get(username=username)  # 根据用户名查找用户
            email = user.email  # 获取用户的邮箱
            # 返回邮箱作为JSON响应
            verification_code = generate_verification_code() #生成验证码
            verification_code_object, created = VerificationCode.objects.get_or_create(
                user=user,
                defaults={'code': verification_code}
                )
            if not created:
                # 如果验证码对象已存在，则进行更新
                verification_code_object.code = verification_code
                verification_code_object.save()
            subject = '重置密码验证码'
            message = f'您的验证码是：{verification_code}'
            from_email = '2928476510@qq.com'
            recipient_list = [user.email]
            mail.send_mail(subject, message, from_email, recipient_list)
            return JsonResponse({'email': email})
        except User.DoesNotExist:
            # 用户不存在的情况
            return JsonResponse({'error': 'User does not exist'}, status=404)
    else:
        # 非POST请求的情况
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
def generate_verification_code(length=6):
    # 生成指定长度的随机验证码
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@csrf_exempt
def verifyCode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')
        try:
            verification_code = VerificationCode.objects.get(code=code)
            return JsonResponse({'message': '验证码验证成功！'})
        except VerificationCode.DoesNotExist:
             return JsonResponse({'message': '验证码验证失败'}, status=400)
    else:
        # 非POST请求的情况
        return JsonResponse({'error': 'Invalid request method'}, status=400)
@csrf_exempt
def resetPassword(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        new_password = data.get('password')      
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)
    
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
                'is_private': obj.is_private,
                'tag': obj.tag,
            }
        return super().default(obj)

@csrf_exempt
def show_post(request):
    if not request.session.get('info'):
        return JsonResponse({'success': 'false'})
    else:
        posts = Post.objects.filter(is_private=False)
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
def update_post_privacy(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('post_id')  # 获取请求中的post_id参数
        is_private = data.get('is_private')  # 获取请求中的is_private参数
        # 根据post_id获取对应的Post对象
        try:
            post = Post.objects.get(id=post_id)
            post.is_private = is_private
            post.save()
            return JsonResponse({'success': True})
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def show_user_message(request):
    if not request.session.get('info'):
        return JsonResponse({'success': 'error'})
    else:
        username = request.session.get('info')
        user = User.objects.get(username=username)
        message = {
            'PersonalSignature': user.last_name,
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined,
            'name': user.first_name,
        }
        return JsonResponse(message)
@csrf_exempt
def show_user_post2(request):
    if not request.session.get('info'):
        return JsonResponse({'success': 'error'})
    else:
        username = request.GET.get('username') # 获取特定用户名
        user = User.objects.get(username=username)  # 获取用户对象
        posts = Post.objects.filter(author=user, is_private=False)  # 筛选特定用户的帖子
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
        Q(description__icontains=keyword),  # 摘要包含关键词)
        is_private=False
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
            isPrivate = data.get('isPrivate')
            post = Post.objects.create(
                title=title,
                description=description,
                content=content,
                author_id=author_username,
                # created_at=time,
                likeCount=0,
                comments=0,
                is_private=isPrivate,
                tag=tag,
            )
            return JsonResponse({'message': '帖子发布成功'})
        except Exception as e:
            return JsonResponse({'message': '帖子发布失败', 'error': str(e)}, status=400)
    else:
        return JsonResponse({'message': '无效的请求方法'}, status=405)
@csrf_exempt
def publish_singleMessage(request):
    if request.method == 'POST':
        try:
            username = request.session.get('info')
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            PersonalSignature = data.get('PersonalSignature')
            
            user = User.objects.get(username=username)
            user.first_name = name
            user.email = email
            user.last_name = PersonalSignature
            user.save()
            
            return HttpResponse('User fields updated successfully')
        except User.DoesNotExist:
            return HttpResponse('User not found')
        except Exception as e:
            return HttpResponse(f'Error: {str(e)}')
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
@csrf_exempt
def get_server_public_key(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        try:
            user_public_key = UserPublicKey.objects.get(user=username)
            public_key = user_public_key.public_key
            return JsonResponse({'publicKey': public_key})
        except UserPublicKey.DoesNotExist:
            return JsonResponse({'error': 'Public key not found for the user.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})
@csrf_exempt
def get_server_private_key(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        try:
            user_private_key = UserPublicKey.objects.get(user=username)
            private_key = user_private_key.private_key
            print(private_key)
            return JsonResponse({'private': private_key})
        except UserPublicKey.DoesNotExist:
            return JsonResponse({'error': 'private key not found for the user.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})
@csrf_exempt
def savePublicKey(request):
    try:
        # data = json.loads(request.body)
        # encrypted_message = data.get('encryptedMessage')
        # print(encrypted_message)
        # encrypted_message = encrypted_message.encode('utf-8')
        # print(encrypted_message)
        # private_key_str = getattr(settings, 'PRIVATE_KEY')
        # print(private_key_str)
        # private_key_bytes = private_key_str.encode()
        # print(private_key_bytes)
        # private_key = rsa.PrivateKey.load_pkcs1(private_key_bytes)
        # decrypted_data = rsa.decrypt(encrypted_message, private_key)
        #private_key = private_key_str.encode()
        data = json.loads(request.body)
        private_key = data.get('privateKey')
        public_key = data.get('publicKey')
        user = request.session.get('info')
        if private_key and public_key:
            try:
                user_public_key = UserPublicKey.objects.get(user=user)
            except UserPublicKey.DoesNotExist:
                user_public_key = UserPublicKey(user=user)
                
            user_public_key.private_key = private_key
            user_public_key.public_key = public_key
            user_public_key.save()
            return HttpResponse('key saved successfully')
    except Exception as e:
        print("error: {}".format(e))
        return JsonResponse({'error': 'save false'}, status=555)
    
@csrf_exempt
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if profile is None:
                # 如果用户没有相关联的 Profile 对象，则创建一个新的
                profile = form.save(commit=False)
                profile.user = request.user
                username = request.user.username
                print(username)
                file_extension = request.FILES['avatar'].name.split('.')[-1]
                new_filename = f"{username}.{file_extension}"
                profile.avatar.save(new_filename, request.FILES['avatar'])
                profile.save()
            else:
                # 如果用户已经有相关联的 Profile 对象，则更新它
                form.save()
            return JsonResponse({'message': '修改成功'})
    else:
        form = ProfileForm(instance=profile)

    return JsonResponse({'message': '修改成功'})

@csrf_exempt
def get_avatar(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Profile does not exist'}, status=404)

    avatar_url = profile.avatar.url if profile and profile.avatar else None
    avatar_path = 'C:\\Users\\29284\\Desktop\\XHforum\\XH_Forum_Django' + avatar_url
    if os.path.exists(avatar_path):
        # 读取文件内容
        with open(avatar_path, 'rb') as f:
            avatar_content = f.read()  
        # 构建HTTP响应，将头像文件内容作为响应主体
        response = HttpResponse(avatar_content, content_type='image/png')
        return response
    #if avatar_url:
    #    return JsonResponse({'avatar_url': avatar_url})
    else:
        return JsonResponse({'error': 'Avatar not found'}, status=500)
    
@csrf_exempt
def get_avatar2(request, username):
    try:
        # 通过用户名获取用户对象
        user = User.objects.get(username=username)
        # 尝试获取用户的 profile
        profile = Profile.objects.get(user=user)
        if profile and profile.avatar:
            # 获取用户头像的路径
            avatar_url = profile.avatar.url
            avatar_path = 'C:\\Users\\29284\\Desktop\\XHforum\\XH_Forum_Django' + avatar_url

            # 检查头像文件是否存在
            if os.path.exists(avatar_path):
                # 读取文件内容
                with open(avatar_path, 'rb') as f:
                    avatar_content = f.read()
                
                # 构建HTTP响应，将头像文件内容作为响应主体
                response = HttpResponse(avatar_content, content_type='image/png')
                return response
            else:
                return JsonResponse({'error': 'Avatar not found'}, status=500)
        else:
            return JsonResponse({'error': 'User has no avatar'}, status=501)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=502)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Profile does not exist'}, status=503)
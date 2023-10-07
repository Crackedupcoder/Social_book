from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Profile, Post, LikePost, FollowerCount
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from . forms import ProfileUpdateForm
from itertools import chain
from django.db.models import Q


def home(request):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)

    user_following_list = []
    feed = []

    user_following = FollowerCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for username in user_following_list:
        feed_lists = Post.objects.filter(user=username)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))
    

    cxt = {'profile': profile, 'user': user,'posts':feed_list}
    return render(request,'base/index.html', cxt)



def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(
        Q(caption__icontains=q)|
        Q(user__icontains=q)
    )

    return render(request, 'base/search.html', {'posts': posts, 'profile': profile})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already exists")
                return redirect('signup')  
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Already exists")
                return redirect('signup')  
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                login(request, user)
                return redirect('settings')
        else:
            messages.error(request, "Passwords Don't Match")

    else:
        return render(request, 'base/signup.html')


@login_required(login_url=('signin')) 
def settings(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('avatar') == None:
            avatar = profile.avatar
            email = request.POST.get('email')
            name = request.POST['name']
            bio = request.POST['bio']
            location = request.POST['location']

            profile.avatar = avatar
            request.user.email = email
            profile.name = name
            profile.bio = bio
            profile.location = location
            profile.save()
            messages.success(request, 'User successfully Updated')
            return redirect('home')
        elif request.FILES.get('avatar') != None:
            avatar = request.FILES.get('avatar')
            email = request.POST.get('email')
            name = request.POST['name']
            bio = request.POST['bio']
            location = request.POST['location']

            profile.avatar = avatar
            request.user.email = email
            profile.name = name
            profile.bio = bio
            profile.location = location
            profile.save()
            messages.success(request, 'User successfully Updated')
            return redirect('home')
        else:
            ProfileUpdateForm()
            messages.error(request, 'An error Occured')
    cxt = {'profile': profile}
    return render(request, 'base/setting.html', cxt)

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does NOT exist')
            
        user = authenticate(username=username,password=password)

        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password does NOT exist')


    else:
        return render(request, 'base/signin.html')


@login_required(login_url=('signin'))   
def signout(request):
    logout(request)
    return redirect('signin')


@login_required(login_url=('signin'))
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')
        post = Post.objects.create(user=user, image=image, caption=caption)
        post.save()
        return redirect('home')
    else:
        return render(request, 'base/index.html')
    

@login_required(login_url=('signin'))
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')


@login_required(login_url=('signin'))
def profile(request, pk):
    user_profile = User.objects.get(username=pk)
    profile = Profile.objects.get(user=user_profile)
    posts = Post.objects.filter(user=pk)
    no_posts = posts.count()

    follower = request.user.username
    user = pk
    if FollowerCount.objects.filter(follower=follower, user=user):
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    followers_count = FollowerCount.objects.filter(user=pk)
    followers = followers_count.count()

    following_count = FollowerCount.objects.filter(follower=pk)
    following = following_count.count()


    cxt = {'user_profile': user_profile, 'profile': profile, 'following': following,
           'no_posts': no_posts, 'posts':posts, 'button_text': button_text, 'followers': followers}
    return render(request, 'base/profile.html', cxt)


@login_required(login_url=('signin'))
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowerCount.objects.filter(follower=follower, user=user).first():
            follower = FollowerCount.objects.get(follower=follower, user=user)
            follower.delete()
            return redirect('/profile/'+user)
        else:
            follower = FollowerCount.objects.create(follower=follower, user=user)
            follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')




from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
import json
from .models import User, LikesUnlikes, Profile, Following
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from collections import Counter
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage

def index(request):
    data = Profile.objects.order_by('-timestamp')
    reCount = LikesUnlikes.objects.values_list('postId')
    userNam = LikesUnlikes.objects.all()
    onlyUserLikes = []
    for x in userNam:
        if request.user == x.userNameOnLU:
            onlyUserLikes.append(x.postId)
    coutin = Counter(reCount)
    idPost = []
    totalLiked = []
    dic = {}
    for x, y in coutin.items():
        idPost.append(x[0])
        totalLiked.append(y)
        dic[x[0]] = y

    p = Paginator(data, 10)
    page_num = request.GET.get('page', 1)
    
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    final = {'item': page,'data':data, 'userLikes':onlyUserLikes,  'userRequest':str(request.user), 'dic':dic, 'idPost':idPost, 'totalLiked':totalLiked, 'idUser':request.user.id}
    return render(request, "network/index.html", final)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='login')
def getPost(request):
    obj = Profile()
    if request.method == "POST":
        form = request.POST['userPost']
        if form == "":
            return redirect("index")
        obj.userName = request.user
        obj.userBio = form
        obj.save()
    return redirect('index')

@login_required(login_url='login')
def userInfo(request, userId):
    userPost = Profile.objects.filter(userName=userId).order_by('-timestamp')
    cout = Profile.objects.filter(userName=userId).count()
    totalFollowers = Following.objects.filter(following=userId).count()
    totalFollowing = Following.objects.filter(follStatu=userId).count()
    check = Following.objects.filter(follStatu=request.user, following=userId).exists()

    reCount = LikesUnlikes.objects.values_list('postId')
    userNam = LikesUnlikes.objects.all()
    onlyUserLikes = []
    for x in userNam:
        if request.user == x.userNameOnLU:
            onlyUserLikes.append(x.postId)
    coutin = Counter(reCount)
    idPost = []
    totalLiked = []
    dic = {}
    for x, y in coutin.items():
        idPost.append(x[0])
        totalLiked.append(y)
        dic[x[0]] = y
    
    p = Paginator(userPost, 10)
    page_num = request.GET.get('page', 1)
    
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    finalData = {'show':'hello', 'item':page, 'idUser':request.user.id, 'dic':dic, 'idPost':idPost, 
                 'totalLiked':totalLiked, 'userLikes':onlyUserLikes, 'following':totalFollowing, 
                 'follower': totalFollowers, 'userPost':userPost, 'userN':userId,
                  'requestUser':str(request.user), 'post':cout, 'check':check}
    return render(request, 'network/index.html',finalData)

@login_required(login_url='login')
def followIngo(request, userFollow, userFoller):

    if request.method == "POST":
        if 'following' in request.POST:
            deleteItem = Following.objects.filter(follStatu=userFollow, following=userFoller)
            getData = deleteItem.get()
            getData.delete()
        elif 'follow' in request.POST:
            print("follow", request.user.id)
            item_to_save = get_object_or_404(Profile, pk=request.user.id)
            check = Following.objects.filter(follStatu=userFollow, following=userFoller).exists()
            print("Check ", check)
            if Following.objects.filter(follStatu=userFollow, following=userFoller).exists():
                return render(request, 'network/index.html')
            user_list = Following(user=request.user, follStatu=userFollow, following=userFoller)
            user_list.save()
            user_list.follower.add(item_to_save)
    return redirect('userInfo', userId=userFoller)

@login_required(login_url='login')
def followingPost(request):
    userNameData = []
    checkLikes = LikesUnlikes.objects.all()
    totalFollowing = Following.objects.filter(follStatu=request.user)

    for x in totalFollowing:
        userNameData.append(x.following)

    follwingPost = Profile.objects.order_by('-timestamp')
    reCount = LikesUnlikes.objects.values_list('postId')
    userNam = LikesUnlikes.objects.all()
    onlyUserLikes = []

    for x in userNam:
        if request.user == x.userNameOnLU:
            onlyUserLikes.append(x.postId)
    coutin = Counter(reCount)
    idPost = []
    totalLiked = []
    dic = {}
    for x, y in coutin.items():
        idPost.append(x[0])
        totalLiked.append(y)
        dic[x[0]] = y

    postByFollowers = []
    for x in follwingPost:
        if x.userName in userNameData:
            postByFollowers.append(x)

    p = Paginator(postByFollowers, 10)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    final = {'userLikes':onlyUserLikes, 'item':page, 'userPostt': follwingPost,
             'userRequest':str(request.user), 'dic':dic,
             'idPost':idPost, 'totalLiked':totalLiked, 'idUser':request.user.id}

    return render(request, "network/index.html", final)

@csrf_exempt
def updatepost(request, post_id):
    try:
        post = Profile.objects.get(pk=post_id)
    except Profile.DoesNotExist:
        return JsonResponse({"error": "Error."}, status=404)
    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get('userBio') is not None:
            post.userBio = data['userBio']
        post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
            }, status=400)


@csrf_exempt
@login_required(login_url='login')
def checkLikes(request, likes_id):
    count = LikesUnlikes.objects.filter(userNameOnLU=request.user, postId=likes_id).count()
    dataCount = LikesUnlikes.objects.values_list('postId', 'userNameOnLU')
    reCount = LikesUnlikes.objects.values_list('postId')
    data = Counter(dataCount)
    coutin = Counter(reCount)
    
    if count == 0:
        obj = LikesUnlikes()
        obj.userNameOnLU = request.user
        obj.postId = likes_id
        obj.countLikes = True;
        obj.save()
        totalCount = LikesUnlikes.objects.filter(postId=likes_id).count()
        return JsonResponse({'Liked': 'Post Liked', 'totalLiked': totalCount}, status=201)
    else:
        deleteData = LikesUnlikes.objects.filter(userNameOnLU=request.user, postId=likes_id)
        getData = deleteData.get()
        getData.delete()
        totalCount = LikesUnlikes.objects.filter(postId=likes_id).count()
        return JsonResponse({'Unliked': 'Post Unliked', 'totalLiked': totalCount}, status=201)




























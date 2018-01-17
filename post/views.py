from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Like, Comment
from .forms import PostForm, UserSignupForm, UserLoginForm, CommentForm
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q



def likes(request, post_id):
	post = Post.objects.get(id=post_id)
	impressed, created = Like.objects.get_or_create(user=request.user, post=post)
	if created:
		action = "like"
	else:
		action = "unlike"
		impressed.delete()

	post_like_count = Like.objects.filter(post=post).count()

	context = {
	"action": action,
	"count": post_like_count
	}

	return JsonResponse(context, safe=False)


def user_signup(request):
	form = UserSignupForm()
	if request.method == 'POST':
		form = UserSignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			username = user.username
			password = user.password

			user.set_password(password)
			form.save()

			login(request, user)

			return redirect('list')

	context = {
		'form': form,
	}
	return render(request, 'signup.html', context)


def user_login(request):
	form = UserLoginForm()
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect('list')
	context = {
	'form': form
	}
	return render(request, 'login.html', context)





def user_logout(request):
	logout(request)
	return redirect('list')



def post_list(request):
	object_list = Post.objects.all().order_by('-updated')

	query = request.GET.get('q')
	if query:
		object_list = object_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(author__first_name__icontains=query) |
			Q(author__last_name__icontains=query) |
			Q(author__username__icontains=query) 
			).distinct()

	context = {
	
	"posts" : object_list
	}
	return render(request, 'list.html', context)

def post_detail(request, post_id):
	post = Post.objects.get(id= post_id)
	form = CommentForm()

	liked = False
	if request.user.is_authenticated:
		if Like.objects.filter(post=post, user=request.user).exists():
			liked = True

	post_like_count = Like.objects.filter(post=post).count()

	if request.method =="POST":
		form = CommentForm(request.POST or None)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post=post
			comment.user=request.user
			comment.save()
			return redirect("detail", post_id=post.id)

	comments = Comment.objects.filter(post=post).order_by("timestamp")

	context = {

	"form": form,
	"post" : post,
	"liked" : liked,
	"count" : post_like_count,
	"comments": comments,
	}
	return render(request, 'detail.html', context)

def post_delete(request,post_id):
	Post.objects.get(id=post_id).delete()

	return redirect("list")

def no_access(request):
	return render (request, 'no_access.html', {})

def post_create(request):
	if not (request.user.is_staff or request.user.is_superuser):
		return redirect ('no_access')

	form =PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		post = form.save(commit=False)
		post.author= request.user
		post.save()

		return redirect("list")
	context = {

	"form" : form 
	}

	return render(request, "create.html", context)

		

def post_update(request,post_id):

	item = Post.objects.get(id= post_id)
	form = PostForm(instance = item)

	if request.method == "POST":

		form = PostForm(request.POST or None,request.FILES or None, instance = item)

		
		if form.is_valid():
			form.save()
			return redirect("list")

	context = {

	"form": form,
	"item": item,	

	}

	return render(request, "update.html", context)
	



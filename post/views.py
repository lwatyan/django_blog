from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post
from .forms import PostForm


def post_list(request):
	object_list = Post.objects.all()

	context = {
	
	"posts" : object_list
	}
	return render(request, 'list.html', context)

def post_detail(request, post_id):
	article = Post.objects.get(id= post_id)

	context = {
	
	"title" : article
	}
	return render(request, 'detail.html', context)

def post_delete(request,post_id):
	Post.objects.get(id=post_id).delete()

	return redirect("list")

def post_create(request):
	form =PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():

		form.save()

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
	



from django.shortcuts import render , redirect
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,

	)
from .forms import UserLoginForm , UserRegisterForm
import MySQLdb
from django import forms

# Create your views here.


def login_view(request):
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username,password=password)
		# if username and password:
		# 	user = authenticate(username=username,password=password)
		# 	if not user or user == 'AnonymousUser':
		# 		raise forms.ValidationError("the user does not exits")
		# 	if not user.check_password(password):
		# 		raise forms.ValidationError("Incorrect password")
		# 	if not user.is_active:
		# 		raise forms.ValidationError("This user is no longer active")
		login(request,user)
		return redirect("/")
	return render(request,'neoyoutube/login.html',{"form":form, "title":title})

def register_view(request):
	title = "Register"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username,password=password)
		login(request,new_user)
		return redirect("/history")
	context = {
		"form": form,
		"title":title
	}
	return render(request,'neoyoutube/register.html',context)

def logout_view(request):
	logout(request)
	return redirect("/")

def history_view(request):
	db = MySQLdb.connect('localhost', 'root','vegeta','neoyoutube')
	cursor  = db.cursor()
	# sql = "Create table "+ request.user+"_" + request.user.id + "( )"
	# print cursor.execute(sql)
	db.close()
	return redirect("/")

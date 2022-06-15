from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.

class RecentMatches(View):
  
  def get(self, request, *args, **kwargs):
    print("hi")
  
  def post(self, request, *args, **kwargs):
    print("hi")

class Match(View):
  
  def get(self, match_id, request, *args, **kwargs):
    print("hi")
  
  def post(self, match_id, request, *args, **kwargs):
    print("hi")

class Player(View):

  def get(self, match_id, hero_id, request, *args, **kwargs):
    print("hi")
  
  def post(self, match_id, hero_id, request, *args, **kwargs):
    print("hi")

class Rivals(View):

  def get(self, match_id, hero_id, request, *args, **kwargs):
    print("hi")
  
  def post(self, match_id, hero_id, request, *args, **kwargs):
    print("hi")
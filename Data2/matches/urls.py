from django.urls import path
from .views import RecentMatches, Match, Player, Rivals, Items, GraphData


urlpatterns = [
    path('', RecentMatches.as_view()),
    path('<int:match_id>', Match.as_view()),
    path('<int:match_id>/<int:hero_id>', Player.as_view()),
    path('<int:match_id>/rivals/<int:hero_id>', Rivals.as_view()),
    path('<int:match_id>/items', Items.as_view()),
    path('<int:match_id>/graphdata', GraphData.as_view()),
]
from django.urls import path
from . import views
urlpatterns = [
    path("updateLeaderDailyBoard",views.updateLeaderDailyBoard,),
    path("updateLeaderWeeklyBoard",views.updateLeaderWeeklyBoard,),
    path("updateLeaderMonthlyBoard",views.updateLeaderMonthlyBoard,),
    path("getLeaderDailyBoard",views.getLeaderDailyBoard,),
    path("getLeaderWeeklyBoard",views.getLeaderWeeklyBoard,),
    path("getLeaderMonthlyBoard",views.getLeaderMonthlyBoard,),
]
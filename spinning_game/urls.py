from django.urls import path,include
from . import views
urlpatterns = [
    path("getOrCreateAndGetSpinning/",views.getOrCreateAndGetSpinning,name="getOrCreateAndGetSpinning"),
    path("bidInSpin/",views.bidInSpin,name="bidInSpin"),
    path("addWinningCoin/",views.addWinningCoin,name="addWinningCoin"),
    path("getWinner/",views.getWinner,name="getWinner"),
]
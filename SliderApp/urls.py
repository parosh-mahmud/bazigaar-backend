from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('add-new-slider/',AddNewSlider.as_view(),name='add-new-slider'),
    path('update-slider/<int:pk>/',UpdateSliderAPIView.as_view(),name='update-slider'),
    path('list-slider/',SliderListView.as_view(),name='list-slider'),
    path('details-slider/', SliderDetailsView.as_view(), name='get-slider'),
    path('admin-list-slider/',SliderListViewByAdmin.as_view(),name='admin-list-slider'),
    path('admin-slider-active/<int:pk>/',ActiveSlider,name='admin-active-slider'),
    path('admin-slider-DeActive/<int:pk>/',DeActiveSlider,name='admin-Deactive-slider'),
    path('delete/<int:pk>/', delete_slider, name='delete-slider'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
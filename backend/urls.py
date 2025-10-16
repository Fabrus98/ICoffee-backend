from django.contrib import admin
from django.urls import path
from bookings.views import GetSession, BookingList, BookingDetail, ItemList, CustomAuthToken

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/login/", CustomAuthToken.as_view()),
    path("api/session/", GetSession.as_view()),
    path("api/items/", ItemList.as_view()),
    path("api/bookings/", BookingList.as_view()),
	path("api/bookings/<int:booking_id>/", BookingDetail.as_view()),
]

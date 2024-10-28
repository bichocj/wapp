from django.urls import path, include
from .views import views

app_name = "dashboard"

urlpatterns = [
    #path("", view=views.home_view, name="home"),
    path("", views.upload_xls_view, name="home"),
    path("send-whatsapp-message/", view=views.send_whatsapp_message, name="send_whatsapp_message"),
    path(r"api/", include(views.router.urls)),
]

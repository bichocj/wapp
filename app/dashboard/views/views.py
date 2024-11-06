from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from .apis.people import PersonViewSet, PersonPathSerializer
from .apis.users import UserViewSet, UserPathSerializer
from django.http import JsonResponse
import pywhatkit as kit
#import pyautogui
import datetime
import time
import webbrowser

from core.models import Browser
from django.shortcuts import render
from .forms import XLSUploadForm
import pandas as pd

def upload_xls_view(request):
    if request.method == "POST":
        form = XLSUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            
            # Leer el archivo usando pandas
            try:
                df = pd.read_excel(file)
                # Puedes realizar alguna lógica aquí, como procesar o guardar los datos
                data = df.to_dict(orient="records")  # Convertir a una lista de diccionarios para renderizar
                browsers = Browser.objects.all()
                for b in browsers:
                    webbrowser.register(b.name, None, webbrowser.BackgroundBrowser(b.path))

                i = 0
                for d in data:
                    if i + 1 > len(browsers):
                        i = 0
                    d['browser'] = browsers[i].name
                    i += 1                               

                return render(request, "dashboard/display_data.html", {"data": data})
            
            except Exception as e:
                return render(request, "dashboard/upload.html", {"form": form, "error": str(e)})
    
    else:
        form = XLSUploadForm()
    return render(request, "dashboard/upload.html", {"form": form})


# @login_required
def home_view(request):
    message = "hello low"
    return render(request, "dashboard/home.html", locals())


def send_whatsapp_message(request):
    phone_number = "+" + request.GET.get("phone_number")
    message = request.GET.get("message")
    browser = request.GET.get("browser")
    try:        
        kit.sendwhatmsg_instantly(phone_number, message, 15, True, 3, browser)
        return JsonResponse({"status": "success", "message": "Message sent successfully"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

people_path = PersonPathSerializer.get_path()
user_path = UserPathSerializer.get_path()
router = routers.DefaultRouter()
router.register(r"%s" % user_path, UserViewSet, basename=user_path)
router.register(r"%s" % people_path, PersonViewSet, basename=people_path)

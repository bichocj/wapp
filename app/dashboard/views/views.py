from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from .apis.people import PersonViewSet, PersonPathSerializer
from .apis.users import UserViewSet, UserPathSerializer
from django.http import JsonResponse
import pywhatkit as kit
import pyautogui
import datetime
import time

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
    # Get parameters from the request
    phone_number = "+" + request.GET.get("phone_number")
    message = request.GET.get("message")
    #send_hour = request.GET.get("hour")
    #send_minute = request.GET.get("minute")

    
    # Set default time if hour and minute are not provided
    # now = datetime.datetime.now()
    #if send_hour is None:
    #    send_hour = now.hour
    #else:
    #    send_hour = int(send_hour)
        
    #if send_minute is None:
    #    send_minute = (now.minute + 2) % 60
    #else:
    #    send_minute = int(send_minute) + 1
    
    try:
        # kit.sendwhatmsg(phone_number, message, send_hour, send_minute, 15, True, 3)
        kit.sendwhatmsg_instantly(phone_number, message, 15, True, 3)
        return JsonResponse({"status": "success", "message": "Message sent successfully"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

people_path = PersonPathSerializer.get_path()
user_path = UserPathSerializer.get_path()
router = routers.DefaultRouter()
router.register(r"%s" % user_path, UserViewSet, basename=user_path)
router.register(r"%s" % people_path, PersonViewSet, basename=people_path)

from unicodedata import name
from urllib import response
from urllib.request import Request
from django.shortcuts import render

from django.http import JsonResponse

from datetime import timedelta
from django.utils import timezone

from api.serializers import alert_typeSerializer,cameraSerializer,capture_videoSerializer,guardSerializer,camera_alertsSerializer,camera_settingsSerializer,camera_alert_flagSerializer

from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework import viewsets



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from app1.models import alert_types,camera,capture_video,guard,camera_alerts,camera_settings



class alert_typesClassBassedView(APIView):
    
    def get(self, request, id=None, format=None):
        if id is not None:
            try:
                tt = alert_types.objects.get(id=id)
            except:
                return Response('no data found', status=status.HTTP_404_NOT_FOUND)

            s = alert_typeSerializer(tt, many=False)

            return Response(s.data, status=status.HTTP_200_OK)
        
        
        
        tt = alert_types.objects.all()
        

        s = alert_typeSerializer(tt, many=True)

      

        return Response(s.data, status=status.HTTP_200_OK)

    
    def post(self, request, id=None ,format=None):
        s = alert_typeSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)

        return Response(s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    
    def put(self, request, id=None ,format=None):
        try:
            tt=alert_types.objects.get(id=id)
        except:
            return Response("no data found ", status=status.HTTP_404_NOT_FOUND)
        s = alert_typeSerializer(instance=tt, data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    
    def delete(self, request, id=None ,format=None):
        try:
            tt= alert_types.objects.get(id=id)
        except:
            return Response("no data found ", status=status.HTTP_404_NOT_FOUND)
        tt.delete()
        return Response("deleted", status=status.HTTP_201_CREATED)
    


 

class cameraClassBassedView(APIView):
    


    def get(self, request, id=None ,format=None):
        if id is not None:
            
            try:
                tt = camera.objects.get(id=id)
            except:
                return Response('no data found', status=status.HTTP_404_NOT_FOUND)

            s = cameraSerializer(tt,many=False)

            return Response(s.data, status=status.HTTP_200_OK)
        tt= camera.objects.all()
        s = cameraSerializer(tt, many=True)
        return Response(s.data, status=status.HTTP_200_OK)

    def post(self, request, id=None ,format=None):
        s = cameraSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)

        return Response(s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    
    def put(self, request, id=None ,format=None):
        try:
            tt=camera.objects.get(id=id)
        except:
            return Response("no data found ", status=status.HTTP_404_NOT_FOUND)
        s = camera_alertsSerializer(instance=tt, data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    
    def delete(self, request, id=None ,format=None):
        try:
            tt= camera.objects.get(id=id)
        except:
            return Response("no data found ", status=status.HTTP_404_NOT_FOUND)
        tt.delete()
        return Response("deleted", status=status.HTTP_201_CREATED)

class capture_videoClassBassedView(APIView):
    


    def get(self, request, id=None ,format=None):
        if id is not None:
            
            try:
                tt = capture_video.objects.get(id=id)
            except:
                return Response('no data found', status=status.HTTP_404_NOT_FOUND)

            s = capture_videoSerializer(tt,many=False)

            return Response(s.data, status=status.HTTP_200_OK)
        tt= capture_video.objects.all()
        s = capture_videoSerializer(tt, many=True)
        return Response(s.data, status=status.HTTP_200_OK)

    def post(self, request, id=None ,format=None):
        s = capture_videoSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)

        return Response(s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    
    def put(self, request, id=None ,format=None):
        try:
            tt=capture_video.objects.get(id=id)
        except:
            return Response("no data found ", status=status.HTTP_404_NOT_FOUND)
        s = capture_videoSerializer(instance=tt, data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    
    def delete(self, request, id=None ,format=None):
        try:
            tt= capture_video.objects.get(id=id)
        except:
            return Response("no data found ", status=status.HTTP_404_NOT_FOUND)
        tt.delete()
        return Response("deleted", status=status.HTTP_201_CREATED)

class guardClassBassedView(APIView):
    


    def get(self, request, id=None ,format=None):
        if id is not None:
            
            try:
                tt = guard.objects.get(id=id)
            except:
                return Response('no data found', status=status.HTTP_404_NOT_FOUND)

            s = guardSerializer(tt,many=False)

            return Response(s.data, status=status.HTTP_200_OK)
        tt= guard.objects.all()
        s = guardSerializer(tt, many=True)
        return Response(s.data, status=status.HTTP_200_OK)

    def post(self, request, id=None ,format=None):
        s = guardSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)

        return Response(s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    
    def put(self, request, id=None ,format=None):
        try:
            tt=guard.objects.get(id=id)
        except:
            return Response("no data found ", status=status.HTTP_404_NOT_FOUND)
        s = guardSerializer(instance=tt, data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    
    def delete(self, request, id=None ,format=None):
        try:
            tt= guard.objects.get(id=id)
        except:
            return Response("no data found ", status=status.HTTP_404_NOT_FOUND)
        tt.delete()
        return Response("deleted", status=status.HTTP_201_CREATED)
    


class camera_alertsClassBassedView(APIView):
    


    def get(self, request, id=None, format=None):
        if id is not None:
            try:
                tt = camera_alerts.objects.filter(camera_id=id)
            except:
                return Response('no data found', status=status.HTTP_404_NOT_FOUND)

            s = camera_alertsSerializer(tt, many=True)

            return Response(s.data, status=status.HTTP_200_OK)
        
        
        
        tt = camera_alerts.objects.all()
        

        # tf = camera_alerts.objects.all().order_by('-date_time')[:2]  # Retrieve last two objects
        # if len(tf) < 2:
        #     return Response('Insufficient data to calculate difference', status=status.HTTP_200_OK)

        # last_object_time = tf[0].date_time
        # second_last_object_time = tf[1].date_time
        # time_difference = last_object_time - second_last_object_time

        # # Calculate time difference in hours
        # time_difference_hours = time_difference.total_seconds() / 3600

        # # Check if time difference is greater than 1 hour
        # alert_flag = True if time_difference_hours > 1 else False

        s = camera_alertsSerializer(tt, many=True)

       

        return Response(s.data, status=status.HTTP_200_OK)

    
    
    def post(self, request, id=None ,format=None):
        s = camera_alertsSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)

        return Response(s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    
    # def put(self, request, id=None ,format=None):
    #     print(id)
    #     try:
    #         tt=camera_alerts.objects.get(camera_id=id)
    #     except:
    #         return Response("no data found ", status=status.HTTP_404_NOT_FOUND)
    #     s = camera_alertsSerializer(instance=tt, data=request.data)
    #     if s.is_valid():
    #         s.save()
    #         return Response(s.data, status=status.HTTP_201_CREATED)
    #     return Response(s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def put(self, request, id=None, format=None):
        print(id)
        try:
            alert = camera_alerts.objects.get(camera_id=id)
        except camera_alerts.DoesNotExist:
            return Response({"error": "No data found for the given camera ID"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = camera_alertsSerializer(instance=alert, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, id=None ,format=None):
        try:
            tt= camera_alerts.objects.get(camera_id=id)
        except:
            return Response("no data found ", status=status.HTTP_404_NOT_FOUND)
        tt.delete()
        return Response("deleted", status=status.HTTP_201_CREATED)



class camera_settingsClassBassedView(APIView):
    


    def get(self, request, id=None ,format=None):
        if id is not None:
            
            try:
                tt = camera_settings.objects.get(id=id)
            except:
                return Response('no data found', status=status.HTTP_404_NOT_FOUND)

            s = camera_settingsSerializer(tt,many=False)

            return Response(s.data, status=status.HTTP_200_OK)
        tt= camera_settings.objects.all()
        s = camera_settingsSerializer(tt, many=True)
        return Response(s.data, status=status.HTTP_200_OK)

    def post(self, request, id=None ,format=None):
        s = camera_settingsSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)

        return Response(s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    
    def put(self, request, id=None ,format=None):
        try:
            tt=camera_settings.objects.get(id=id)
        except:
            return Response("no data found ", status=status.HTTP_404_NOT_FOUND)
        s = camera_settingsSerializer(instance=tt, data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    
    def delete(self, request, id=None ,format=None):
        try:
            tt= camera_settings.objects.get(id=id)
        except:
            return Response("no data found ", status=status.HTTP_404_NOT_FOUND)
        tt.delete()
        return Response("deleted", status=status.HTTP_201_CREATED)


class camera_alert_flagClassBassedView(APIView):
    
    def get(self, request, alert_type_id=None, camera_id=None, format=None):
        if alert_type_id and camera_id is not None:
            try:
                tf = camera_alerts.objects.filter(camera_id=camera_id, alert_type=alert_type_id).order_by('-date_time')[:2]  
            except camera_alerts.DoesNotExist:
                return Response('no data found', status=status.HTTP_404_NOT_FOUND)
            
            
            # tf = camera_alerts.objects.all().order_by('-date_time')[:2]  # Retrieve last two objects
            
            if len(tf) < 2:
                response_data_def = {
                        'alert_flag': False
                    }
                return Response(response_data_def, status=status.HTTP_200_OK)

            last_object_time = tf[0].date_time
            second_last_object_time = tf[1].date_time
            time_difference = last_object_time - second_last_object_time

            # Calculate time difference in hours
            time_difference_hours = time_difference.total_seconds() / 10

            # Check if time difference is greater than 1 hour
            alert_flag = True if time_difference_hours > 1 else False

            # s = camera_alertsSerializer(tf, many=True)

            response_data = {
                'alert_flag': alert_flag
            }

            return Response(response_data, status=status.HTTP_200_OK)
        
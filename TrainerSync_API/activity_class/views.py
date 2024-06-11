from django.shortcuts import render



class AtivityRoomViewSet(viewsets.ModelViewSet):
    queryset = ActivityClass.objects.all()
    serializer_class = ActivityClassSerializer
from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class IsRoomOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'perform_create']:
            room_id = view.kwargs.get('room_pk')
            room = Room.objects.get(pk=room_id)
            return room.owner == request.user
        return True


class ActivityClassViewSet(viewsets.ModelViewSet):
    queryset = ActivityClass.objects.none()
    serializer_class = ActivityClassSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        room_id = self.kwargs['room_pk']
        return ActivityClass.objects.filter(room_id=room_id)

    def create(self, request, *args, **kwargs):
        room_id = self.kwargs.get('room_pk')
        request.data['room'] = room_id
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        room_id = self.kwargs.get('room_pk')
        room = get_object_or_404(Room, pk=room_id)
        
        instance = serializer.save(room=room)
        instance.create_attendance()
        return instance
    
    @action(detail=True, methods=['GET'])
    def payment_present_users_list(self, request, pk=None, **kwargs):
        activity_class = self.get_object()
        balance_users = BalanceForActivityClass.objects.filter(activity_class=activity_class)
        
        result = []
        
        for balance in balance_users:
            user_data = None
            sub_user_data = None
            
            if balance.user:
                user_data = {
                    'user': balance.user.get_full_name() if balance.user else None,
                    'amount_due': balance.amount_due,
                    'amount_paid': balance.amount_paid,  
                    'paid': balance.paid 
                }
                result.append(user_data)
            elif balance.subuser:     
                sub_user_data = {             
                    'subuser': f'{balance.subuser.name} opiekunem jest: {balance.subuser.parent}' if balance.subuser else None,
                    'amount_due': balance.amount_due,
                    'amount_paid': balance.amount_paid, 
                    'paid': balance.paid 
                }
                result.append(sub_user_data)

        return Response(result, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['POST'])
    def acceptance_payment_outside_system(self, request, pk=None, **kwargs):
        activity_class = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        balance_user = BalanceForActivityClass.objects.filter(
            activity_class=activity_class,
            user_id=user_id,
            paid=False
        ).first()

        if not balance_user:
            return Response({'error': 'No unpaid balance found for the specified user'}, status=status.HTTP_404_NOT_FOUND)

        balance_user.paid = True
        balance_user.amount_paid = balance_user.amount_due
        balance_user.save()

        return Response({'status': 'User Payment Accepted'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["POST"])
    def check_attendance_set_true(self, request, pk=None, **kwargs):
        activity_class = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        attendance, created = Attendance.objects.get_or_create(
            user_id=user_id,
            activity_class=activity_class,
            room=activity_class.room,
            defaults={'present': True}
        )
        if not created:
            attendance.present = True
            attendance.save()
        
        balance, created = BalanceForActivityClass.objects.get_or_create(
            user_id=user_id,
            activity_class=activity_class,
            room=activity_class.room,
            defaults={'amount_due': activity_class.cost, 'amount_paid': 0, 'paid': False}
        )
        if not created:
            balance.amount_due = activity_class.cost
            balance.save()
            
        
        return Response({'status': 'Attendance marked and balance updated'}, status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=["POST"])
    def check_attendance_set_false(self, request, pk=None, **kwargs):
        activity_class = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        attendance, created = Attendance.objects.get_or_create(
            user_id=user_id,
            activity_class=activity_class,
            room=activity_class.room,
            defaults={'present': False}
        )
        if not created:
            attendance.present = False
            attendance.save()
        
        BalanceForActivityClass.objects.filter(
            user_id=user_id,
            activity_class=activity_class,
            room=activity_class.room
        ).delete()
            
        
        return Response({'status': 'Attendance marked and balance updated'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["POST"], permission_classes=[permissions.IsAuthenticated])
    def set_presence(self, request, pk=None):
        activity_class = self.get_object()
        user = request.user

        attendance, created = Attendance.objects.get_or_create(
            user=user,
            activity_class=activity_class,
            defaults={'present': True, 'room': activity_class.room}  
        )

        if not created:
            attendance.present = not attendance.present
            attendance.save()

        serializer = AttendanceForActivityClassSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
class BalanceForActivityClassViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
       
    @extend_schema(
        description="user_id taking from the url"
    )
    @action(detail=False, methods=['GET'])
    def history_of_user_payments(self, request, pk=None, **kwargs):
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        user_balances = BalanceForActivityClass.objects.filter(user_id=user_id)
        subuser_balances = BalanceForActivityClass.objects.filter(subuser__parent_id=user_id)
        
        result = []

        for balance in user_balances:
            result.append({
                'activity_class': balance.activity_class.name,
                'paid': balance.paid,
                'amount_due': balance.amount_due,
                'amount_paid': balance.amount_paid,
                'date': balance.date,
                'name': balance.user.get_full_name() if balance.user else None,
            })

        for balance in subuser_balances:
            result.append({
                'activity_class': balance.activity_class.name,
                'paid': balance.paid,
                'amount_due': balance.amount_due,
                'amount_paid': balance.amount_paid,
                'date': balance.date,
                'type': 'Subuser',
                'name': f'{balance.subuser.name} {balance.subuser.last_name}' if balance.subuser else None,
            })

        return Response(result, status=status.HTTP_200_OK)

    

class AttendanceForActivityClassViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    def list(self, request, room_pk=None, activity_class_pk=None):
        queryset = Attendance.objects.filter(room_id=room_pk, activity_class_id=activity_class_pk)
        serializer = AttendanceForActivityClassSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, room_pk=None, activity_class_pk=None):
        queryset = Attendance.objects.filter(room_id=room_pk, activity_class_id=activity_class_pk)
        attendance = get_object_or_404(queryset, pk=pk)
        serializer = AttendanceForActivityClassSerializer(attendance, many=False)
        return Response(serializer.data)

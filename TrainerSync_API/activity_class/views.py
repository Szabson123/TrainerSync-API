from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q


class ActivityClassViewSet(viewsets.ModelViewSet):
    queryset = ActivityClass.objects.all()
    serializer_class = ActivityClassSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.create_balances()
        return instance

    @action(detail=True, methods=['POST'])
    def create_balances(self, request, pk=None):
        activity_class = self.get_object()
        activity_class.create_balances()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'])
    def payment_users_list(self, request, pk=None):
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
    
    @action(detail=False, methods=['GET'])
    def history_of_user_peyments(self, request, pk=None):
        user_id = request.data.get('user_id')
        balance_user = BalanceForActivityClass.objects.filter(user_id=user_id)
        
        result = []
        
        for balance in balance_user:
            user_data = {
                'activity_class': balance.activity_class.name,
                'paid': balance.paid,
                'amount_due': balance.amount_due,
                'amount_paid': balance.amount_paid,
                'data': balance.date
            }
            result.append(user_data)
        return Response(result, status=status.HTTP_200_OK)
        
    
    @action(detail=True, methods=['POST'])
    def payment_accepted_by_trainer_manager(self, request, pk=None):
        activity_class = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Find the balance for the given user and activity class
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
       

class BalanceForActivityClassViewSet(viewsets.ModelViewSet):
    queryset = BalanceForActivityClass.objects.all()
    serializer_class = BalanceForActivityClassSerializer
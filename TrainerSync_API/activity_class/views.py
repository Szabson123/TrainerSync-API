from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action



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
        

class BalanceForActivityClassViewSet(viewsets.ModelViewSet):
    queryset = BalanceForActivityClass.objects.all()
    serializer_class = BalanceForActivityClassSerializer
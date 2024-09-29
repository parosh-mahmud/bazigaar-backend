from rest_framework.response import Response
from rest_framework.views import APIView
from unicodedata import decimal
from level_and_achievement.models import UserAchievement,Achievement
from .models import *
from user_app.models import *
from . import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from django.contrib.auth import get_user_model, login

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from django.db.models import Q
from rest_framework import generics, viewsets
from rest_framework import status
from notifications.models import RequestNotification
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import *

from .serializers import ResellerSerializer, TopUpRequestHistorySaveSerializer, \
    ResellerCoinReqSerializer
from Lottery.views import UserLoginView


# class ResellerLoginView(UserLoginView):
#     permission_classes = (AllowAny,)
    
#     def post(self, request, format=None):
#         try:
#             email=request.data["email"]
#             password=request.data["password"]
#             if email == '':
#                 return Response({"type":"error","msg":"email not found."})
#             if password == '':
#                 return Response({"type":"error","msg":"password not found."})
#         except:
#             return Response({"type":"error","msg":"email or password not found."})
        
#         if get_user_model().objects.filter(email=email).exists():
#             user_obj = get_user_model().objects.get(email=email)
#         elif User.objects.filter(username=email).exists():
#             user_obj = get_user_model().objects.get(username=email)
#         else:
#             return Response({"type":"error","msg":"Registered user not found."})
        

#         if models. Reseller.objects.filter(user=user_obj).exists():
#             if models.Reseller.objects.filter(user=user_obj,active=False).exists():

#                 return Response({"type":"error","msg":"This reseller account is blocked"})
#         else:
#             return Response({"type":"error","msg":"No reseller account found."})
            
        
#         if user_obj:
#             if user_obj.check_password(password) == False:
#                 return Response({"type":"error","msg":"Password Incorrect."})
#         else:
#             return Response({"type":"error","msg":"username or email not found."})
        
        
#         credentials = {
#             'username': user_obj.username,
#             'password': password
#         }
#         serializer = AuthTokenSerializer(data=credentials)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
        
        
#         login(request, user)
#         dd= super(ResellerLoginView, self).post(request, format=None)

#         dd["username"] = user_obj.username
#         dd["email"] = user_obj.email
#         dd["token"] = AuthToken.objects.create(user)

#         return dd

# class CreateReseller(generics.CreateAPIView):
#     # serializer_class = serializers.CreateResellerSerializer
#     # serializer_class2 = serializers.CreateResellerSerializerHistory
    
#     def post(self, request):
#         try:
#             user=request.data["user"]
            
#             if user == '':
#                 return Response({"type":"error","msg":"user id or email or username not found."})
#             else:
            
#                 if User.objects.filter(email=user).exists():
#                     user_obj = User.objects.get(email=user)
#                 elif User.objects.filter(username=user).exists():
#                     user_obj = User.objects.get(username=user)
#                 elif User.objects.filter(id=int(user)).exists():
#                     user_obj = User.objects.get(id=int(user))
#                 else:
#                     return Response({"type":"error","msg":"Registered user not found."})
#         except:
#             return Response({"type":"error","msg":"Either user not sent with request or not valid."})

        
#         if Reseller.objects.filter(user=user_obj).exists():
#             print(user)
#             # print(Reseller.objects.all())
#             return Response({"type":"error","msg":"This user registered as a reseller before."})
#         else:
#             # user = {}
#             # user['user'] = user_obj
#             # serializer = self.serializer_class(data=user)
#             # serializer.is_valid(raise_exception=True)
#             res=Reseller()
#             res.user=user_obj
#             # res.save()
            
#             if res.save():
                
#                 history = []
#                 history['resellerUserId'] = user_obj.id
#                 history['createdBy'] = request.user
#                 se2 = self.serializer_class2(data=history)
#                 se2.is_valid(raise_exception=True)
#                 # user_obj.isReseller = True
#                 user_obj.save()
#                 se2.save()
                
#                 return Response({"type":"success","msg":"You Created a new Reseller","data":True})
#             else:
#                 return Response({"type":"error","msg":"Reseller Account not created"})


# class ResellerList(generics.ListAPIView):

#     queryset = Reseller.objects.all()
    # serializer_class = serializers.ResellerSerializer
from user_app.serializers import UserSerializer
from django.db.models import Q

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # IsAdminUser
def resellers_list(request):
    data = request.data
    # contrycode = data["contrycode"]

    queryset = User.objects.filter(Q(isReseller=True)).all().order_by('-id')
    serializer_class = UserSerializer(queryset, many=True)
    j = 0
    arr = []
    for i in serializer_class.data:
        j = j + 1
        i["id2"] = j
        arr.append(i)

    return Response(arr)

class CreateTopUpRequest(generics.CreateAPIView):
    queryset = TopUpRequest.objects.all()
    serializer_class = serializers.TopUpRequestSaveSerializer

    def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        data=request.data
        seri=serializers.TopUpRequestSaveSerializer(
            data=data
        )
        if seri.is_valid():
            topup=seri.save()
            
            return Response(seri.data)
        else:
            return Response(seri.errors)
        # topup=TopUpRequest.objects.create(
        #      reseller=User.objects.get(id=data["reseller"]) ,
        #      requestFrom=User.objects.get(id=data["requestFrom"]),
        #      amount=data["amount"],
        #      equalBgCoin=data["equalBgCoin"],
        #      transactionId=data["transactionId"],
        #      transactionMedium=data["transactionMedium"],
        #      screenshot=data.get("ss"),

        # )
        print (request.data)
        print()
        # serializer.is_valid(raise_exception=True)

        # topup:TopUpRequest= serializer.save()


        # headers = self.get_success_headers(serializer.data)

        return Response({}, status=status.HTTP_201_CREATED,)


class TopUpRequestById(generics.RetrieveAPIView):
    serializer_class= serializers.TopUpRequestSerializerDetails
    queryset = TopUpRequest.objects.all()

class TopUpRequestList(generics.ListAPIView):
    queryset= TopUpRequest.objects.all()
    serializer_class= serializers.TopUpRequestSerializer
    def get_queryset(self):
        user=self.request.user
        return TopUpRequest.objects.filter(requestFrom=user).order_by('-created_at')
    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@api_view(["POST"])
def topUpRequestStatusUpdate(request):

    any=TopUpRequest.objects.filter(id=request.data["id"])
    if any.exists():
        topUprequest=any[0]
        topUprequest.status=request.data["status"]
        topUprequest.save()
        if topUprequest.status=="accepted":
            reseller=topUprequest.reseller
            if reseller.bgcoin<topUprequest.equalBgCoin:
                return Response({"error":"You do not have enough balance to accept."},status=400)
            client=topUprequest.requestFrom
            client.bgcoin=client.bgcoin+topUprequest.equalBgCoin
            client.save()
            reseller.bgcoin=reseller.bgcoin-topUprequest.equalBgCoin
            reseller.save()
            a=Achievement.objects.filter(name="Buy BGcoin any amount").first()
            ua=UserAchievement.objects.filter(
                achievement=a
                ).filter(user=client).first()
            if a and client and not ua:
                ua=UserAchievement()
                ua.achievement=a
                ua.user=client
                ua.save()
            return Response({"type":"success","msg":"Topup Request Accepted"})
    return Response({"type":"success","msg":"Topup Request denied"})


@api_view(["POST"])
def acceptTopupRequest(request):
    
    any=TopUpRequest.objects.filter(id=request.data["id"])
    if any.exists():
        topUprequest=any[0]
        topUprequest.status="accepted"
        topUprequest.save()
        
        client=topUprequest.requestFrom
        client.bgcoin=client.bgcoin+topUprequest.equalBgCoin
        client.save()
        
        MTUPH = TopUpRequestHistory()
        MTUPH.TopUpRequest = topUprequest
        MTUPH.status = "accepted"
        
        MTUPH.save()

    return Response({"type":"success","msg":"Topup Request Accepted Successfully"})

@api_view(["POST"])
def cancelTopupRequest(request):
    
    any=TopUpRequest.objects.filter(id=request.data["id"])
    if any.exists():
        topUprequest=any[0]
        topUprequest.status="denied"
        topUprequest.save()
        
        MTUPH = TopUpRequestHistory()
        MTUPH.TopUpRequest = topUprequest
        MTUPH.status = "denied"
        
        MTUPH.save()

    return Response({"type":"success","msg":"Topup Request Denied Successfully"})




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def coin_request(request):
    serializer =serializers. CoinReqSerializer(data=request.data)
    if serializer.is_valid():
        coin_req = serializer.save(reseller=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_coin_requests(request, status):
    if status not in ['pending', 'accepted', 'rejected']:
        return Response({'message': 'Invalid status'}, status=400)

    coin_requests = CoinReq.objects.filter(status=status)
    serializer =serializers. CoinReqSerializer(coin_requests, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_coin_request(request, request_id):
    try:
        coin_req = CoinReq.objects.get(request_id=request_id, reseller=request.user)
        coin_req.status = 'rejected'
        coin_req.save()
        return Response({'message': 'Coin request marked as rejected'}, status=200)
    except CoinReq.DoesNotExist:
        return Response({'message': 'Coin request not found'}, status=404)

from decimal import Decimal
@api_view(['POST'])
@permission_classes([AllowAny])
def accept_coin_request(request, request_id,reseller_id):
    try:
        coin_req = CoinReq.objects.get(request_id=request_id)
        coin_req.status = 'accepted'
        coin_req.save()
        reseller = get_user_model().objects.get(isReseller=True, id=reseller_id)
        amount = Decimal(coin_req.amount_req)
        reseller.bgcoin += amount
        reseller.save()
        return Response({'message': 'Coin request marked as accepted and amount added to reseller'}, status=200)
    except CoinReq.DoesNotExist:
        return Response({'message': 'Coin request not found'}, status=404)
    except User.DoesNotExist:
        return Response({'message': 'Reseller not found'}, status=404)



@api_view(['GET'])
@permission_classes([AllowAny])
def current_reseller(request):
    user = request.user  # Get the current user making the request
    if user.is_authenticated:
        reseller = User.objects.get(user=user)  # Retrieve the Reseller object associated with the user
        reseller_id = reseller.resellerId
        active = reseller.active
        amount = reseller.amount
        return Response({
            'reseller_id': reseller_id,
            'active': active,
            'amount': amount,
            'message': 'Reseller found',
        })
    else:
        # User is not authenticated
        return Response({'message': 'User not found'})




def reseller_serializer(reseller):
    return {
        'id': reseller.id,
        'username': reseller.username,
        'email': reseller.email,
        # Add other fields as needed
    }
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_resellers(request):
    user = request.user  # Get the current user making the request
    if user.is_authenticated:
        reseller = User.objects.get(user=user)  # Retrieve the Reseller object associated with the user
        reseller_id = reseller.resellerId
        active = reseller.active
        amount = reseller.amount
        return Response({
            'reseller_id': reseller_id,
            'active': active,
            'amount': amount,
            'message': 'Reseller found',
        })
    else:
        # User is not authenticated
        return Response({'message': 'User not found'})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_topup_history(request):
    topUps = TopUpRequestHistory.objects.all()
    serializer = TopUpRequestHistorySaveSerializer(topUps, many =True)
    return Response(serializer.data)


class ResellerCoinReqListAPIView(APIView):
    def get(self, request, format=None):
        reseller_coin_reqs = ResellerCoinRequest.objects.all()
        serializer = ResellerCoinReqSerializer(reseller_coin_reqs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ResellerCoinReqCreateAPIView(APIView):
    def post(self, request, format=None):
        # Set the resellerId and reseller_name fields based on the authenticated user
        request.data['resellerId'] = request.user.id
        request.data['reseller_name'] = request.user.username

        serializer = ResellerCoinReqSerializer(data=request.data)
        if serializer.is_valid():
            # Perform the API call and file handling here
            doc_file = request.FILES.get('document', None)
            if doc_file:
                instance:ResellerCoinRequest = serializer.save()
                instance.doc_url = instance.document.url
                instance.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








# create

@api_view(['POST'])
def create_reseller_coin_request(request):
    if request.method == 'POST':
        # Modify the request data before deserializing it
        request.data['resellerId'] = request.user.id
        request.data['reseller_name'] = request.user.username
        request.data['status'] = 'pending'

        # Deserialize the modified request data
        serializer =serializers.ResellerCoinRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Create the object
            reseller_coin_request = serializer.save()
            return Response(serializers.ResellerCoinRequestSerializer(reseller_coin_request).data)
        return Response(serializer.errors, status=400)


#details view
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_requests_by_doc_url(request):
    id = request.query_params.get('id')

    try:
        reseller_req = ResellerCoinRequest.objects.get(id= id)
    except ResellerCoinRequest.DoesNotExist:
        return Response({'error': 'No matching document found.'}, status=404)

    serializer =serializers. ResellerCoinRequestSerializer(reseller_req)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def accept_status_by_doc_url(request):
    id = request.query_params.get('id')
    try:
        reseller_req = ResellerCoinRequest.objects.get(id=id)
    except ResellerCoinRequest.DoesNotExist:
        return Response({'error': 'No matching document found.'}, status=404)

    reseller_req.status = 'accepted'
    user=get_user_model().objects.get(id=reseller_req.resellerId)
    user.bgcoin+=reseller_req.bgcoin
    user.save()
    reseller_req.save()
    serializer =serializers. ResellerCoinRequestSerializer(reseller_req)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAdminUser])
def reject_status_by_doc_url(request):
    id = request.query_params.get('id')
    try:
        reseller_req = ResellerCoinRequest.objects.get(id=id)
    except ResellerCoinRequest.DoesNotExist:
        return Response({'error': 'No matching document found.'}, status=404)
    reseller_req.status = 'rejected'
    reseller_req.save()
    serializer =serializers. ResellerCoinRequestSerializer(reseller_req)
    return Response(serializer.data)
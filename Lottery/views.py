import random
import json
import string
from websocket import create_connection
from datetime import datetime
from django.conf import settings

from rest_framework import generics

from notifications.models import EventNotification
from notifications.serializers import EventNotificationSerializer
from django.http import JsonResponse
from SuperAdminPanel.serializers import CreateTicketSerializer
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from ticket_draw_app.models import Ticket
from wallet_app.models import Wallet
from .models import Lottery, LotteryTicket, Winner

from .serializers import (
    LotteryListSerializer,
    LotterySerializer, 
    LotteryTicketSerializer, 
    WinnerTicketSerializer,
)

from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from rest_framework import serializers
from knox.views import LogoutView as KnoxLogoutView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from base.ws_send_data import ws_send_model_to_data

class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        User = get_user_model()
        try:
            email = request.data["email"]
            password = request.data["password"]
            if email == '':
                return Response({"type": "error", "msg": "email not found."})
            if password == '':
                return Response({"type": "error", "msg": "password not found."})
        except:
            return Response({"type": "error", "msg": "email or password not found."})

        if get_user_model().objects.filter(email=email).exists():
            user_obj = get_user_model().objects.get(email=email)
        elif User.objects.filter(username=email).exists():
            user_obj = get_user_model().objects.get(username=email)
        else:
            return Response({"type": "error", "msg": "Registered user not found."})

        if user_obj:
            if user_obj.check_password(password) == False:
                return Response({"type": "error", "msg": "Password Incorrect."})
        else:
            return Response({"type": "error", "msg": "username or email not found."})

        credentials = {
            'username': user_obj.username,
            'password': password
        }
        serializer = AuthTokenSerializer(data=credentials)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(type(user))

        login(request, user)
        print(user_obj)
        # dd = super(UserLoginView, self).post(request, format=None)
        dd = {}
        dd["username"] = user_obj.username
        dd["email"] = user_obj.email
        # dd["profile_picture"] = user_obj.profile_picture.url

        # Check if the user has a wallet
        try:
            wallet = Wallet.objects.get(user=user_obj)
            dd["wallet_id"] = wallet.wallet_id
        except Wallet.DoesNotExist:
            pass
        try:
            Token.objects.get(user=user).delete()
        except:
            pass
        dd["token"] = Token.objects.create(user=user).key
        dd["id"] = user.id
        if user.profile_picture:
            dd["profile_picture"] = user.profile_picture.url
        dd["is_admin"] = user.is_staff
        print(dd)

        return Response(data=dd,)


class UserLogoutView(APIView):
    permission_classes = ([IsAuthenticated])

    # def post(self, request, format=None):
    #     # Perform logout for the authenticated user
    #     super(UserLogoutView, self).post(request, format=None)

    #     # Return a response to indicate successful logout
    #     return Response({"detail": "User successfully logged out."})

    def post(self, request, format=None):
        # Get the user's token
        print(request.user)
        try:
            token = Token.objects.get(user=request.user)
            print(token)
            token.delete()  # Delete the user's token
        except Token.DoesNotExist:
            pass  # Handle the case when the token does not exist (optional)

        return Response({"detail": "User successfully logged out."})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lottery_list(request):
    print("-------hi--i am here!")
    lotteries = Lottery.objects.all()
    serializer = LotterySerializer(lotteries, many=True)
    return Response(serializer.data)


#================== Draw Lottery List ========= RM =====
class DrawLotteryListAPIView(APIView):
    """
    API view to retrieve a list of lotteries.
    Supports filtering by 'type' (Regular, Special, Other).
    If no 'type' query parameter is provided, returns all lotteries.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get 'type' from query parameters
            lottery_type = request.query_params.get('type', None)

            # Fetch all lotteries by default
            queryset = Lottery.objects.all()

            # Filter by lottery type if provided
            if lottery_type:
                if lottery_type not in ['Regular', 'Special', 'Other']:
                    return Response(
                        {"error": "Invalid type parameter. Valid options are 'Regular', 'Special', 'Other'."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                queryset = queryset.filter(type=lottery_type)

            # Serialize the data
            serializer = LotterySerializer(queryset, many=True)

            # Return response with serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle unexpected exceptions and provide a professional error response
            return Response(
                {"error": "An unexpected error occurred. Please try again later.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    return Response({
        'status': 'ok',
        'message': 'logged out'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def open_lottery_list(request):
    lotteries = Lottery.objects.filter(isOpen=True)
    serializer = LotterySerializer(lotteries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def closed_lottery_list(request):
    lotteries = Lottery.objects.filter(isOpen=False)
    serializer = LotterySerializer(lotteries, many=True)
    return Response(serializer.data)


class jsonencode():
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def make_reseller(request):
    UserRepository = get_user_model()
    user = request.query_params.get('user', None)
    return Response(user)


def convert_lottery_to_ticket(lottery_obj, lottery):
    ticket_obj = Ticket()
    ticket_obj.LotteryName = lottery_obj["LotteryName"]
    ticket_obj.lotteryuuid = str(lottery.LotteryId)
    ticket_obj.price = lottery_obj["Price"]
    ticket_obj.drawPriceAmount = lottery_obj["PriceAmount"]
    ticket_obj.numberOfWinner = lottery_obj["NumberOfWinners"]
    ticket_obj.totalNumberOfTickets = lottery_obj["NumberOfTickets"]
    ticket_obj.type = lottery_obj["type"]
    ticket_obj.firstPrizeName = lottery_obj["FirstPrizeName"]
    ticket_obj.secondPrizeName = lottery_obj["SecondPrizeName"]
    ticket_obj.thirdPrizeName = lottery_obj["ThirdPrizeName"]
    ticket_obj.numberOfFirstWinner = lottery_obj["TotalFirstPrizeWinner"]
    ticket_obj.numberOfSecondWinner = lottery_obj["TotalSecondPrizeWinner"]
    ticket_obj.numberOfThirdWinner = lottery_obj["TotalThirdPrizeWinner"]
    ticket_obj.bannerColor = lottery_obj["banner_color"]
    ticket_obj.ticketSellOpeningTime = str(lottery_obj["OpeningTime"])
    ticket_obj.ticketSellClosingTime = str(lottery_obj["ClosingTime"])
    # ticket_obj.ticketSellClosingTime =

    # Check if the draw is complete in the Lottery object and set draw status accordingly in the Ticket object
    if lottery_obj["isDrawComplete"]:
        ticket_obj.drawStatus = "Draw Complete"
        ticket_obj.firstPrizeDrawIsComplete = True
        ticket_obj.secondPrizeDrawIsComplete = True
        ticket_obj.thirdPrizeDrawIsComplete = True
    else:
        ticket_obj.drawStatus = "Draw Incomplete"

    # Validate and set other fields, e.g., images and coverImage
    # ticket_obj.prizeImage = lottery_obj["image_prizes"]
    # ticket_obj.firstPrize = lottery_obj["image_first"]
    # ticket_obj.secondPrize = lottery_obj["image_second"]
    # ticket_obj.thirdPrize = lottery_obj["image_third"]
    # ticket_obj.coverImage = lottery_obj["image_banner"]

    ticket_obj.prizeImage = lottery_obj["image_prizes"]
    ticket_obj.firstPrize = lottery_obj["image_first"]
    ticket_obj.secondPrize = lottery_obj["image_second"]
    ticket_obj.thirdPrize = lottery_obj["image_third"]
    ticket_obj.coverImage = lottery_obj["image_banner"]

    ticket_obj.created_at = str(datetime.now())
    ticket_obj.update_at = str(datetime.now())
    ticket_obj.bannerColor = lottery_obj["banner_color"]
    ticket_obj.active = True

    return json.loads(jsonencode.toJSON(ticket_obj))
    # return ticket_obj


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_lottery(request):
    print(request.data)
    serializer = LotterySerializer(data=request.data)
    # print(serializer.data.ClosingTime)
    # print(serializer)
    if serializer.is_valid():
        lottery = serializer.save()
        print("lottery")
        print(lottery.LotteryId)
        test = convert_lottery_to_ticket(serializer.data, lottery)
        print("test")
        print(test)
        # print("hi")
        lotteryTicketSerializer = CreateTicketSerializer(data=test)
        # print(lotteryTicketSerializer)
        # print(lotteryTicketSerializer.is_valid())
        # print(lotteryTicketSerializer)
        if lotteryTicketSerializer.is_valid():
            print("hello")
            lotteryTicketSerializer.save()
            print(lotteryTicketSerializer.data)
            return Response(lotteryTicketSerializer.data, status=200)
        else:
            return Response(lotteryTicketSerializer.errors, status=400)

        # return Response({
        #     'status':'error',
        #     'message':serializer.errors
        # }, status=200)
        # print(convert_lottery_to_ticket(serializer.data))
        # return Response(convert_lottery_to_ticket(serializer.data))
    else:
        return Response(serializer.errors)

    # if serializer.is_valid():
    #     serializer.save()
    #     return Response({
    #     'status':'ok',
    #     'message':'Lottery Created'
    # }, status=200)
    # return Response({
    #     'status':'error',
    #     'message':serializer.errors
    # }, status=200)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_lottery_form(request):
    serializer = LotterySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
    # return Response(convert_lottery_to_ticket(serializer))


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_lottery(request):
    lottery_id = request.query_params.get('LotteryId', None)
    try:
        lottery = Lottery.objects.get(LotteryId=lottery_id)
    except Lottery.DoesNotExist:
        return Response({'message': 'Lottery not found'}, status=404)

    serializer = LotterySerializer(lottery)
    print(serializer.data)
    return Response(serializer.data)


def convert_edit_lottery_to_ticket(lottery_obj, lottery):
    ticket = Ticket.objects.get(lotteryuuid=str(lottery.LotteryId))
    ticket.LotteryName = lottery_obj["LotteryName"]
    ticket.lotteryuuid = str(lottery.LotteryId)
    ticket.price = lottery_obj["Price"]
    ticket.drawPriceAmount = lottery_obj["PriceAmount"]
    ticket.numberOfWinner = lottery_obj["NumberOfWinners"]
    ticket.totalNumberOfTickets = lottery_obj["NumberOfTickets"]
    ticket.type = lottery_obj["type"]
    ticket.firstPrizeName = lottery_obj["FirstPrizeName"]
    ticket.secondPrizeName = lottery_obj["SecondPrizeName"]
    ticket.thirdPrizeName = lottery_obj["ThirdPrizeName"]
    ticket.numberOfFirstWinner = lottery_obj["TotalFirstPrizeWinner"]
    ticket.numberOfSecondWinner = lottery_obj["TotalSecondPrizeWinner"]
    ticket.numberOfThirdWinner = lottery_obj["TotalThirdPrizeWinner"]
    ticket.bannerColor = lottery_obj["banner_color"]
    ticket.ticketSellOpeningTime = str(lottery_obj["OpeningTime"])
    ticket.ticketSellClosingTime = str(lottery_obj["ClosingTime"])
    # ticket_obj.ticketSellClosingTime =

    # Check if the draw is complete in the Lottery object and set draw status accordingly in the Ticket object
    if lottery_obj["isDrawComplete"]:
        ticket.drawStatus = "Draw Complete"
        ticket.firstPrizeDrawIsComplete = True
        ticket.secondPrizeDrawIsComplete = True
        ticket.thirdPrizeDrawIsComplete = True
    else:
        ticket.drawStatus = "Draw Incomplete"

    # Validate and set other fields, e.g., images and coverImage
    # ticket_obj.prizeImage = lottery_obj["image_prizes"]
    # ticket_obj.firstPrize = lottery_obj["image_first"]
    # ticket_obj.secondPrize = lottery_obj["image_second"]
    # ticket_obj.thirdPrize = lottery_obj["image_third"]
    # ticket_obj.coverImage = lottery_obj["image_banner"]

    ticket.prizeImage = lottery_obj["image_prizes"]
    ticket.firstPrize = lottery_obj["image_first"]
    ticket.secondPrize = lottery_obj["image_second"]
    ticket.thirdPrize = lottery_obj["image_third"]
    ticket.coverImage = lottery_obj["image_banner"]

    ticket.created_at = str(datetime.now())
    ticket.update_at = str(datetime.now())
    ticket.bannerColor = lottery_obj["banner_color"]

    ticket.save()
    # print(ticket.data)
    return ticket


@api_view(['POST'])
@permission_classes([IsAdminUser])
def edit_lottery(request):
    print(request)
    lottery_id = request.query_params.get('LotteryId', None)

    print(request.data)
    print(lottery_id)
    try:
        lottery = Lottery.objects.get(LotteryId=lottery_id)
        print(lottery)
    except Lottery.DoesNotExist:
        return Response({
            'status': 'ok',
            'message': 'Not Found'
        }, status=301)

    serializer = LotterySerializer(lottery, data=request.data, partial=True)
    print("--------test")
    print(serializer)
    if serializer.is_valid():
        print("test--------------------------")

        lottery = serializer.save()
        print(serializer.data)

        print(lottery.image_first)

        test = convert_edit_lottery_to_ticket(serializer.data, lottery)
        # ticket.firstPrize
        print("test printing")
        print(serializer.data["image_first"])
        print(test.firstPrize)
        return Response({
            'status': 'ok',
            'message': 'Lottery Edit'
        }, status=200)
    return Response({
        'status': 'error',
        'message': 'could not edit'
    }, status=500)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_lottery(request):
    lottery_id = request.query_params.get('LotteryId', None)
    try:
        lottery = Lottery.objects.get(LotteryId=lottery_id)
        ticket = Ticket.objects.get(lotteryuuid=str(lottery_id))

        ticket.active = False
        ticket.save()
        lottery.delete()
        # ticket.active = False

    except Lottery.DoesNotExist:
        return Response({'status': 'error', 'message': 'Lottery not found'}, status=400)

    return Response({'status': 'ok', 'message': 'Lottery deleted'}, status=200)


#==================RM ================ Develop



from rest_framework import generics, status
from rest_framework.response import Response


class LotteryListAPIView(generics.ListAPIView):
    serializer_class = LotteryListSerializer

    def get_queryset(self):
        """
        Optionally filter the Lotteries by `type` passed in query parameters.
        Returns error if an invalid type is provided.
        """
        print("I am Here--for Lottery List!")
        queryset = Lottery.objects.all()
        lottery_type = self.request.query_params.get('type', None)  # 'type' is the query parameter

        # Validate the lottery_type
        valid_types = ['Regular', 'Special', 'Other']
        if lottery_type and lottery_type not in valid_types:
            # Raise an error for invalid type
            raise ValueError(f"Invalid type '{lottery_type}'. Must be one of {valid_types}.")

        if lottery_type in valid_types:
            queryset = queryset.filter(type=lottery_type)

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Override the list method to handle errors gracefully.
        """
        try:
            return super().list(request, *args, **kwargs)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  # Assuming you have imported the User model from Django
        fields = '__all__'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Test(request):
    user = request.user
    if isinstance(user, AnonymousUser):
        return Response({'detail': 'User is not authenticated'}, status=401)

    user_details = {
        'username': user.username,
        'email': user.email,
        'id': user.id
        # Add more user details as needed
    }
    return Response(user_details)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def user_purchase_lottery_ticket(request):
#     user = request.user
#     if isinstance(user, AnonymousUser):
#         return Response({'detail': 'User is not authenticated'}, status=401)
#     user_id=user.id
#     lottery_id = request.query_params.get('LotteryId', None)
#     try:
#         lottery = Lottery.objects.get(LotteryId=lottery_id)
#     except Lottery.DoesNotExist:
#         return Response({'message': 'Lottery not found'}, status=404)
#     if(lottery.isOpen== False):
#         return Response({
#             'Status':'Error',
#        'Message ': 'Lottery Closed'}
#         )
#     user_input = request.data.get('userInput', None)
#     quantity = request.data.get('quantity', 1)
#     if not user_input:
#         return Response({'message': 'Please provide a user input'}, status=400)
#     estimated_cost = quantity * lottery.Price
#     balance = user.bgtoken
#     if balance >= estimated_cost:
#         balance = balance - estimated_cost
#     else:
#         return Response(
#             {
#                 'message':'Not enough tokens',
#                 'cost': str(estimated_cost) + ' bg tokens',
#                 'balance': str(balance) + ' bg tokens',
#             },
#         status =201
#         )
#     tickets=[]
#     itr = 0
#     while (itr < quantity):
#         ticket = LotteryTicket(userLuckyNumber='', userInput=user_input, lotteryId=lottery.LotteryId, userId=user_id,
#                                quantity=quantity)
#         random_digits_start = ''.join(random.choices(string.digits, k=4))
#         random_digits_end = ''.join(random.choices(string.digits, k=4))
#         ticket.userLuckyNumber = f"{random_digits_start}{user_input}{random_digits_end}"
#         tickets.append(ticket)
#         itr+=1
#         ticket.save()
#         user.bgtoken -= lottery.Price
#         user.save()

#     result =[]
#     for ticket in tickets:
#         serialized_ticket = LotteryTicketSerializer(ticket)
#         result.append(serialized_ticket.data)


#     return Response(
#         {
#             'message': 'Lottery ticket purchased successfully',
#             'cost': str(estimated_cost) + ' bg tokens',
#             'new balance': str(balance) + ' bg tokens',
#             'ticket data': result
#         },
#         status=201
#     )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_tickets_in_lottery(request):
    user = request.user
    if isinstance(user, AnonymousUser):
        return Response({'detail': 'User is not authenticated'}, status=401)

    user_id = user.id
    lottery_id = request.query_params.get('LotteryId', None)
    try:
        lottery = Lottery.objects.get(LotteryId=lottery_id)
    except Lottery.DoesNotExist:
        return Response({'message': 'Lottery not found'}, status=404)

    tickets = LotteryTicket.objects.filter(
        userId=user_id, lotteryId=lottery_id)
    serialized_tickets = LotteryTicketSerializer(tickets, many=True)

    return Response(serialized_tickets.data, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_tickets_in_lottery(request):
    lottery_id = request.query_params.get('LotteryId', None)
    try:
        lottery = Lottery.objects.get(LotteryId=lottery_id)
    except Lottery.DoesNotExist:
        return Response({'message': 'Lottery not found'}, status=404)
    tickets = LotteryTicket.objects.filter(lotteryId=lottery_id)
    serialized_tickets = LotteryTicketSerializer(tickets, many=True)
    return Response(
        serialized_tickets.data, status=200)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def draw_ticket(request):
    lottery_id = request.query_params.get('LotteryId', None)
    try:
        lottery = Lottery.objects.get(LotteryId=lottery_id)
        ticket = Ticket.objects.get(lotteryuuid=str(lottery_id))
    except Lottery.DoesNotExist and ticket.DoesNotExist:
        return Response({'message': 'Lottery not found'}, status=404)
    if (lottery.isDrawComplete == True):
        return Response({
            'Status': 'Error',
            'Message ': 'Lottery Closed'}
        )
    tickets = LotteryTicket.objects.filter(lotteryId=lottery_id)
    size = lottery.TotalFirstPrizeWinner + \
        lottery.TotalSecondPrizeWinner + lottery.TotalThirdPrizeWinner
    if size > tickets.count():
        return Response({'message': 'Not enough tickets available'}, status=400)

    random_tickets = random.sample(list(tickets), size)
    first_winners = []
    second_winners = []
    third_winners = []
    for i in range(size):
        user_ticket: LotteryTicket = random_tickets[i]
        user = get_user_model().objects.get(id=user_ticket.userId)
        winner_data = {
            'ticketId': user_ticket.userLuckyNumber,
            'userId': user_ticket.userId,
            'prizeType': '',
            'username': user.username
        }
        evn_notific = EventNotification()
        if i < lottery.TotalFirstPrizeWinner:
            winner_data['prizeType'] = '1st Prize Winner'
            first_winners.append(winner_data)
            evn_notific.title = f"Congratulations! You have won {lottery.FirstPrizeName}."
            evn_notific.notification_to = user
            evn_notific.type = "type2"
            evn_notific.thumbnail = lottery.image_first
            evn_notific.save()
        elif i < (lottery.TotalFirstPrizeWinner + lottery.TotalSecondPrizeWinner):
            winner_data['prizeType'] = '2nd Prize Winner'
            second_winners.append(winner_data)
            evn_notific.title = f"Congratulations! You have won {lottery.SecondPrizeName}."
            evn_notific.notification_to = user
            evn_notific.type = "type2"
            evn_notific.thumbnail = lottery.image_second
            evn_notific.save()
        else:
            winner_data['prizeType'] = '3rd Prize Winner'
            third_winners.append(winner_data)
            evn_notific.title = f"Congratulations! You have won {lottery.ThirdPrizeName}."
            evn_notific.notification_to = user
            evn_notific.type = "type2"
            evn_notific.thumbnail = lottery.image_third
            evn_notific.save()

        # Save winner in the Winner model
        Winner.objects.create(
            ticketId=user_ticket.userLuckyNumber,
            userId=user_ticket.userId,
            prizeType=winner_data['prizeType'],
            username=user.username,
            lotteryId=lottery_id
        )
        ws_send_model_to_data(userid=user.id,model=evn_notific)
        
    data = [
        {
            'First_Prize_Winners': first_winners,
            'Second_Prize_Winners': second_winners,
            'Third_Prize_Winners': third_winners,
        }
    ]
    try:
        lottery.isOpen = False
        ticket.active = False
        ticket.drawStatus = "Draw Complete"
        ticket.firstPrizeDrawIsComplete = True
        ticket.secondPrizeDrawIsComplete = True
        ticket.thirdPrizeDrawIsComplete = True
        lottery.isDrawComplete = True
        lottery.save()
        return Response(data, status=200)
    except RuntimeError as e:
        return Response(e, status=500)

    # return Response(data, status=200)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def winner_list(request):
    lottery_id = request.query_params.get('LotteryId', None)
    try:
        lottery = Lottery.objects.get(LotteryId=lottery_id)
    except Lottery.DoesNotExist:
        return Response({'message': 'Lottery not found'}, status=404)

    winner_list = Winner.objects.filter(lotteryId=lottery_id)

    winner_data = []
    for winner in winner_list:
        winner_data.append({
            'ticketId': winner.ticketId,
            'userId': winner.userId,
            'prizeType': winner.prizeType,
            'username': winner.username,
        })

    return Response(winner_data, status=200)

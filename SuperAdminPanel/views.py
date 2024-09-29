from datetime import timedelta, date
from django.utils import timezone
from decimal import Decimal
# from datetime import timezone

from django.contrib.auth.models import AnonymousUser
from django.db.models import Sum
from django.shortcuts import render
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import get_user_model, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
# from AdminPanel.serializers import *
from Lottery.models import Lottery
from .serializers import *
from reseller_app.models import ResellerCoinRequest
from reseller_app.serializers import ResellerSerializer
from django.shortcuts import get_object_or_404
from Lottery.views import *
from user_app.serializers import UserSerializer

# Create your views here.


class SuperAdminLoginView(UserLoginView):
    permission_classes = (AllowAny)

    def post(self, request, format=None):
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
            user_obj: User = get_user_model().objects.get(email=email)
        elif User.objects.filter(username=email).exists():
            user_obj = get_user_model().objects.get(username=email)
        else:
            return Response({"type": "error", "msg": "Registered user not found."})

        if user_obj.is_superuser == False:
            return Response({"type": "error", "msg": "No super admin record found."})

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

        login(request, user)
        dd = {}
        dd["username"] = user_obj.username
        dd["email"] = user_obj.email
        dd["profile_picture"] = user_obj.profile_picture.url
        dd["is_admin"] = user_obj.is_staff
        dd["token"] = AuthToken.objects.create(user)
        print(dd)

        return dd


@api_view(['GET'])
@permission_classes([IsAdminUser])
def AllUserData(request):
    queryset = User.objects.filter(
        is_staff=False, is_superuser=False).all().order_by('-id')
    serializer_class = UserSerializer(queryset, many=True)
    j = 0
    arr = []
    for i in serializer_class.data:
        j = j+1
        i["id2"] = j
        arr.append(i)

    return Response(arr)


@api_view(['GET'])
@permission_classes([IsAdminUser])  # IsAdminUser
def all_resellers(request):
    queryset = User.objects.filter(isReseller=True).all().order_by('-id')
    serializer_class = UserSerializer(queryset, many=True)
    j = 0
    arr = []
    for i in serializer_class.data:
        j = j + 1
        i["id2"] = j
        arr.append(i)

    return Response(arr)


@api_view(['GET'])
@permission_classes([IsAdminUser])  # IsAdminUser
def all_general_user(request):
    queryset = User.objects.filter(isReseller=False).all().order_by('-id')
    serializer_class = UserSerializer(queryset, many=True)
    j = 0
    arr = []
    for i in serializer_class.data:
        j = j + 1
        i["id2"] = j
        arr.append(i)

    return Response(arr)


@api_view(['GET'])
@permission_classes([IsAdminUser])  # IsAdminUser
def all_blocked_user(request):
    queryset = User.objects.filter(is_active=False).all().order_by('-id')
    serializer_class = UserSerializer(queryset, many=True)
    j = 0
    arr = []
    for i in serializer_class.data:
        j = j + 1
        i["id2"] = j
        arr.append(i)

    return Response(arr)


@api_view(['GET'])
@permission_classes([IsAdminUser])  # IsAdminUser
def AllActiveUser(request):
    queryset = User.objects.filter(
        is_active=True, is_agent=False, is_superuser=False, is_staff=False).all().order_by('-id')
    serializer_class = UserSerializer(queryset, many=True)
    j = 0
    arr = []
    for i in serializer_class.data:
        j = j+1
        i["id2"] = j
        arr.append(i)

    return Response(arr)


@api_view(['GET'])
@permission_classes([IsAdminUser])  # IsAdminUser
def AllBlockUser(request):
    queryset = User.objects.filter(
        is_active=False, is_agent=False, is_superuser=False, is_staff=False).all().order_by('-id')
    serializer_class = UserSerializer(queryset, many=True)
    j = 0
    arr = []
    for i in serializer_class.data:
        j = j+1
        i["id2"] = j
        arr.append(i)

    return Response(arr)
# ****************************************   block a user   ****************************


@api_view(['POST'])
@permission_classes([IsAdminUser])
def BlockUserView(request, user_id):
    print(user_id)
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return Response({'message': 'User blocked successfully'})


# ************************** CONVERT COIN TO TOKEN*************


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def convert_coin_to_token(request):
    amount = request.query_params.get('amount')
    if amount is None:
        return Response({'error': 'Amount parameter is missing'}, status=400)

    user = request.user
    if isinstance(user, AnonymousUser):
        return Response({'detail': 'User is not authenticated'}, status=401)
    amount = Decimal(amount)

    if (user.bgcoin >= amount):
        try:
            user.bgcoin -= amount
            user.bgtoken += amount
            user.save()
            return Response('Coins converted')
        except ValueError:
            return Response({'error': 'Invalid amount value'}, status=400)
    else:
        return Response('Not enough coins to convert')

# ***********************-- ADD COIN*******************************


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddBGCoin(request, user_id):
    amount = request.query_params.get('amount')
    if amount is None:
        return Response({'error': 'Amount parameter is missing'}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'No user found with the given user_id'}, status=404)

    try:
        amount = Decimal(amount)
        user.bgcoin += amount
        user.save()
        return Response({'success': 'BGCoin added successfully'})
    except ValueError:
        return Response({'error': 'Invalid amount value'}, status=400)


# ***********************-- ADD COIN*******************************
@api_view(['POST'])
@permission_classes([IsAdminUser])
def SubBGCoin(request, user_id):
    amount = request.query_params.get('amount')
    if amount is None:
        return Response({'error': 'Amount parameter is missing'}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'No user found with the given user_id'}, status=404)

    try:
        amount = Decimal(amount)
        user.bgcoin -= amount
        if (user.bgcoin < 0):
            return Response({'User does not have enough coins'})
        user.save()
        return Response({'success': 'BGCoin substracted successfully'})
    except ValueError:
        return Response({'error': 'Invalid amount value'}, status=400)


@api_view(['GET'])
@permission_classes([IsAdminUser])  # IsAdminUser
def SingleUserData(request, pk):
    try:
        id = pk
    except:
        return Response({"type": "error", "msg": "user id is not found in request"})

    if User.objects.filter(is_staff=False, is_superuser=False, id=id).exists():
        queryset = User.objects.get(is_staff=False, is_superuser=False, id=id)
        serializer_class = UserSerializer(queryset, many=False)
        return Response(serializer_class.data)
    else:
        return Response({"type": "error", "msg": "user id is not valid in our system"})


@api_view(['GET'])
@permission_classes([IsAdminUser])  # IsAdminUser
def AllAgentsData(request):
    queryset = User.objects.filter(is_agent=True).all().order_by('-id')
    serializer_class = UserSerializer(queryset, many=True)
    j = 0
    arr = []
    for i in serializer_class.data:
        j = j+1
        i["id2"] = j
        arr.append(i)

    return Response(arr)


@api_view(['GET'])
@permission_classes([IsAdminUser])  # IsAdminUser
def SingleAgentsData(request, pk):
    try:
        id = pk
    except:
        return Response({"type": "error", "msg": "Agent id is not found in request"})

    if User.objects.filter(is_agent=True, id=id).exists():
        queryset = User.objects.get(is_agent=True, id=id)
        serializer_class = UserSerializer(queryset, many=False)
        return Response(serializer_class.data)
    else:
        return Response({"type": "error", "msg": "Agent id is not valid in our system"})


@api_view(['GET'])
@permission_classes([IsAdminUser])  # IsAdminUser
def AllUnverifiedEmailUser(request):
    queryset = User.objects.filter(
        is_verified=False, is_staff=False, is_superuser=False).all().order_by('-id')
    serializer_class = UserSerializer(queryset, many=True)
    j = 0
    arr = []
    for i in serializer_class.data:
        j = j+1
        i["id2"] = j
        arr.append(i)

    return Response(arr)


@api_view(['GET'])
def DashboardInfo(request):
    arr = {}
    arr['totalUser'] = User.objects.filter(
        is_agent=False, is_superuser=False, is_staff=False).count()
    arr['totalActiveUser'] = User.objects.filter(
        is_active=True, is_agent=False, is_superuser=False, is_staff=False).count()
    arr['totalInActiveUser'] = User.objects.filter(
        is_active=False, is_agent=False, is_superuser=False, is_staff=False).count()
    arr['totalVerifiedUser'] = User.objects.filter(
        is_verified=False, is_agent=False, is_superuser=False, is_staff=False).count()
    arr['totalUnVerifiedUser'] = User.objects.filter(
        is_verified=False, is_agent=False, is_superuser=False, is_staff=False).count()
    arr['totalHost'] = User.objects.filter(isHost=True).count()
    arr['totalActiveHost'] = User.objects.filter(
        is_active=True, isHost=True).count()
    arr['totalInActiveHost'] = User.objects.filter(
        is_active=False, isHost=True).count()

    arr['totalAgent'] = User.objects.filter(is_agent=True).count()
    arr['totalActiveAgent'] = User.objects.filter(
        is_agent=True, is_active=True).count()

    arr['totalActiveSuperuser'] = User.objects.filter(
        is_superuser=True, is_active=True).count()

    return Response(arr)


def get_pending_payment():
    pending_amount_sum = ResellerCoinRequest.objects.filter(
        status='pending').aggregate(Sum('amount'))['amount__sum']

    # If there are no 'pending' records, the sum will be None, so handle that case
    if pending_amount_sum is None:
        pending_amount_sum = 0
    return pending_amount_sum


def get_total_payment_received():
    # Calculate the sum of 'amount' for all 'accepted' rows using aggregation
    pending_amount_sum = ResellerCoinRequest.objects.filter(
        status='accepted').aggregate(Sum('amount'))['amount__sum']

    # If there are no 'accepted' records, the sum will be None, so handle that case
    if pending_amount_sum is None:
        pending_amount_sum = 0

    return pending_amount_sum


def get_pending_payment():
    pending_amount_sum = ResellerCoinRequest.objects.filter(
        status='pending').count()

    # If there are no 'pending' records, the sum will be None, so handle that case
    if pending_amount_sum is None:
        pending_amount_sum = 0
    return pending_amount_sum


def get_total_order():
    pending_amount_sum = ResellerCoinRequest.objects.all().count()

    # If there are no 'pending' records, the sum will be None, so handle that case
    if pending_amount_sum is None:
        pending_amount_sum = 0
    return pending_amount_sum


def get_new_users():
    current_date = timezone.now().date()

    # Filter users who joined on the current date
    users_joined_today = User.objects.filter(date_joined__date=current_date)

    # Get the count of users who joined today
    num_users_joined_today = users_joined_today.count()
    return num_users_joined_today

# Function to find the sum of 'amount' for 'ResellerCoinReq' objects
# with 'status' as 'accepted' for the last week


def sum_amount_last_week_accepted():
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=7)

    total_amount = ResellerCoinRequest.objects.filter(status='accepted', date__range=[
                                                      start_date, end_date]).aggregate(total_amount_last_week_accepted=models.Sum('amount'))
    return total_amount['total_amount_last_week_accepted'] or get_total_payment_received()

# Function to find the sum of 'amount' for 'ResellerCoinReq' objects
# with 'status' as 'accepted' for the last month


def sum_amount_last_month_accepted():
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)

    total_amount = ResellerCoinRequest.objects.filter(status='accepted', date__range=[
                                                      start_date, end_date]).aggregate(total_amount_last_month_accepted=models.Sum('amount'))
    return total_amount['total_amount_last_month_accepted'] or get_total_payment_received()

# Function to find the sum of 'amount' for 'ResellerCoinReq' objects
# with 'status' as 'accepted' for the last year


def sum_amount_last_year_accepted():
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=365)

    total_amount = ResellerCoinRequest.objects.filter(status='accepted', date__range=[
                                                      start_date, end_date]).aggregate(total_amount_last_year_accepted=models.Sum('amount'))
    return total_amount['total_amount_last_year_accepted'] or get_total_payment_received()

# Function to find the sum of 'amount' for 'ResellerCoinReq' objects
# with 'status' as 'accepted' for today


def sum_amount_today_accepted():
    current_date = timezone.now().date()

    total_amount = ResellerCoinRequest.objects.filter(status='accepted', date__date=current_date).aggregate(
        total_amount_today_accepted=models.Sum('amount'))
    return total_amount['total_amount_today_accepted'] or get_total_payment_received()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Test(request):
    HeaderData = [
        {
            "name": "Total Earning",
            "value": get_total_payment_received(),
            "url": "some url",
        },]
    UserData = [
        {
            "name": "Total Users",
            "value": User.objects.filter(is_agent=False, is_superuser=False, is_staff=False).count(),
            "url": "https://drive.google.com/file/d/1eTQYr_3BI_wxS7kb0EJ7DkOjR5LdX5cZ/view?usp=drive_link",
            "hover-url": "https://drive.google.com/file/d/1cvT9IUBzmKZS2TX1QwTrjyx2L-LINBS-/view?usp=drive_link"
        },
        {
            "name": "Total Active Users",
            "value": User.objects.filter(is_active=True, is_agent=False, is_superuser=False, is_staff=False).count(),
            "url": "https://drive.google.com/file/d/1i1xdB5ZB6aHN6lVVKhad57dTVni9HSKN/view?usp=drive_link",
            "hover-url": "https://drive.google.com/file/d/1JfSa9q0RfMuYtQPXlPvMw-d8343BgiJx/view?usp=drive_link"
        },
        {
            "name": "New Users",
            "value": int(get_new_users()),
            "url": "add later ",
            "hover-url": ""
        },
        {
            "name": "Total Products",
            "value": int(Lottery.objects.all().count()),
            "url": "https://drive.google.com/file/d/1i1xdB5ZB6aHN6lVVKhad57dTVni9HSKN/view?usp=drive_link",
            "hover-url": "https://drive.google.com/file/d/1JfSa9q0RfMuYtQPXlPvMw-d8343BgiJx/view?usp=drive_link"
        },
        {
            "name": "Total Site Visitors",
            "value": User.objects.filter(is_active=True, is_agent=False, is_superuser=False, is_staff=False).count(),
            "url": "https://drive.google.com/file/d/1i1xdB5ZB6aHN6lVVKhad57dTVni9HSKN/view?usp=drive_link",
            "hover-url": "https://drive.google.com/file/d/1i1xdB5ZB6aHN6lVVKhad57dTVni9HSKN/view?usp=drive_link"
        },
        {
            "name": "Orders Received",
            "value": int(get_total_order()),
            "url": "https://drive.google.com/file/d/1i1xdB5ZB6aHN6lVVKhad57dTVni9HSKN/view?usp=drive_link",
            "hover-url": "https://drive.google.com/file/d/1i1xdB5ZB6aHN6lVVKhad57dTVni9HSKN/view?usp=drive_link"
        },
        {
            "name": "Orders Pending",
            "value": int(get_pending_payment()),
            "url": "https://drive.google.com/file/d/1i1xdB5ZB6aHN6lVVKhad57dTVni9HSKN/view?usp=drive_link",
            "hover-url": "https://drive.google.com/file/d/1i1xdB5ZB6aHN6lVVKhad57dTVni9HSKN/view?usp=drive_link"
        },
        {
            "name": "Total Events",
            "value": 0,
            "url": "https://drive.google.com/file/d/1i1xdB5ZB6aHN6lVVKhad57dTVni9HSKN/view?usp=drive_link",
            "hover-url": "https://drive.google.com/file/d/1i1xdB5ZB6aHN6lVVKhad57dTVni9HSKN/view?usp=drive_link"
        },

        {
            "name": "Payment Received",
            "value": int(get_total_payment_received()),
            "url": "https://drive.google.com/file/d/1i1xdB5ZB6aHN6lVVKhad57dTVni9HSKN/view?usp=drive_link",
            "hover-url": "https://drive.google.com/file/d/1i1xdB5ZB6aHN6lVVKhad57dTVni9HSKN/view?usp=drive_link"
        },

        # response
        # extra data starts here
    ]
    EarningData = [
        {
            "name": "Today Earning",
            "value": sum_amount_today_accepted(),
            "url": "some url"
        },
        {
            "name": "Last Week Earning",
            "value": sum_amount_last_week_accepted(),
            "url": "some url"
        },
        {
            "name": "Last Month Earning",
            "value": sum_amount_last_month_accepted(),
            "url": "some url"
        },
        {
            "name": "Last Year Earning",
            "value": sum_amount_last_year_accepted(),
            "url": "some url"
        }
    ]
    res = {
        'HeaderData': HeaderData,
        'UserData': UserData,
        'EarningData': EarningData
    }
    return Response(res)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chart(request):
    total = {'Period': 'This Week', 'Total_Earnings': '123,000',        "curve": "up",
             "week": "+3.2%"}
    data_earn = [
        {'Month': 'Jan', 'Earnings': 1200, 'TicketSold': 239},
        {'Month': 'Feb', 'Earnings': 1300, 'TicketSold': 239},
        {'Month': 'Mar', 'Earnings': 1400, 'TicketSold': 335},
        {'Month': 'Apr', 'Earnings': 1500, 'TicketSold': 189},
        {'Month': 'May', 'Earnings': 1600, 'TicketSold': 334},
        {'Month': 'Jun', 'Earnings': 1700, 'TicketSold': 361},
        {'Month': 'Jul', 'Earnings': 1800, 'TicketSold': 389},
        {'Month': 'Aug', 'Earnings': 1900, 'TicketSold': 423},
        {'Month': 'Sep', 'Earnings': 2000, 'TicketSold': 438},
        {'Month': 'Oct', 'Earnings': 2100, 'TicketSold': 478},
        {'Month': 'Nov', 'Earnings': 2200, 'TicketSold': 498},
        {'Month': 'Dec', 'Earnings': 2300, 'TicketSold': 517}
    ]

    compare = {'Period': 'This Week',         "curve": "up",
               "week": "+13.32%",
               "Total_Site_Visitor": 0
               }
    data_login = [
        {'Month': 'Jan', 'Login': 413},
        {'Month': 'Feb', 'Login': 480},
        {'Month': 'Mar', 'Login': 555},
        {'Month': 'Apr', 'Login': 624},
        {'Month': 'May', 'Login': 711},
        {'Month': 'Jun', 'Login': 805},
        {'Month': 'Jul', 'Login': 888},
        {'Month': 'Aug', 'Login': 970},
        {'Month': 'Sep', 'Login': 1052},
        {'Month': 'Oct', 'Login': 1139},
        {'Month': 'Nov', 'Login': 1225},
        {'Month': 'Dec', 'Login': 1300}
    ]

    res = {
        'finance_total': total,
        'finance_chart': data_earn,
        'login_total': compare,
        'login_chart': data_login
    }

    return Response(res)


@api_view(['GET'])
@permission_classes([IsAdminUser])  # IsAdminUser
def AllReseller(request):

    queryset = get_user_model().objects.all().order_by('-id')
    serializer_class = ResellerSerializer(queryset, many=True)
    j = 0
    arr = []
    for i in serializer_class.data:
        j = j+1
        i["id2"] = j
        arr.append(i)

    return Response(arr)


@api_view(['GET'])
@permission_classes([IsAdminUser])  # IsAdminUser
def SingleReseller(request, pk):

    try:
        id = pk
    except:
        return Response({"type": "error", "msg": "Reseller id is not found in request"})

    if get_user_model().objects.filter(id=id).exists():
        queryset = get_user_model().objects.get(id=id)
        serializer_class = ResellerSerializer(queryset, many=False)
        return Response(serializer_class.data)
    else:
        return Response({"type": "error", "msg": "Reseller id is not valid in our system"})


@api_view(['POST'])
@permission_classes([IsAdminUser])  # IsAdminUser
def Active_Host(request):
    try:
        email = request.data["email"]
        if email == '':
            return Response({"type": "error", "msg": "email not found."})
    except:
        return Response({"type": "error", "msg": "email not sent."})

    User.objects.filter(email=email).update(isHost=True)
    return Response({"type": "success", "msg": "You Created a user as a host."})


@api_view(['POST'])
@permission_classes([IsAdminUser])  # IsAdminUser
def DeActive_Host(request):
    try:
        email = request.data["email"]
        if email == '':
            return Response({"type": "error", "msg": "email not found."})
    except:
        return Response({"type": "error", "msg": "email or password not found."})

    User.objects.filter(email=email).update(isHost=False)
    return Response({"type": "success", "msg": "You De-active a host."})


@api_view(['POST'])
@permission_classes([IsAdminUser])  # IsAdminUser
def userDataUpdate(request):
    try:
        email = request.data["email"]
        if email == '':
            return Response({"type": "error", "msg": "email not found."})
    except:
        return Response({"type": "error", "msg": "email or password not found."})


class userDataUpdate(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    http_method_names = ['patch']
    queryset = User.objects.all()
    serializer_class = AdminUserUpdateSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response({"type": "success", "msg": "user data updated successfully"})

        else:
            return Response({"type": "error", "msg": "Update failed"})


@api_view(['GET'])
@permission_classes([IsAdminUser])  # IsAdminUser
def AllHostList(request):
    queryset = User.objects.filter(isHost=True).all().order_by('-id')
    serializer_class = UserSerializer(queryset, many=True)
    j = 0
    arr = []
    for i in serializer_class.data:
        j = j+1
        i["id2"] = j
        arr.append(i)

    return Response(arr)


@api_view(['GET'])
@permission_classes([IsAdminUser])  # IsAdminUser
def SingleHostList(request, pk):
    try:
        id = pk
    except:
        return Response({"type": "error", "msg": "user id is not found in request"})

    if User.objects.filter(isHost=True, id=id).exists():
        queryset = User.objects.get(isHost=True, id=id)
        serializer_class = UserSerializer(queryset, many=False)
        return Response(serializer_class.data)
    else:
        return Response({"type": "error", "msg": "user id is not valid in our system"})

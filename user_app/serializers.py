from wallet_app.serializers import BankAccountModelSerializer, CryptoModelSerializer, MobileBankModelSerializer
from . import models
from rest_framework import serializers
from follow.models import Follow
from follow.serializers import FollowSerializer
from django.db.models import Q
from level_and_achievement.models import UserLevel
from level_and_achievement.serializers import UserLevelSerializer
from wallet_app.models import BankAccount, Crypto, MobileBank, User, Wallet
from reseller_app.models import TopUpRequest, CoinReq


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_picture', 'isHost', 'is_active', 'is_verified', 'is_agent', 'is_superuser', 'first_name', 'last_name',
                  'is_premium', 'nickname', 'GENDER_CHOICES', 'online', 'isReseller', 'gender', 'date_of_birth',
                  'last_online', 'countryCode', 'phoneNumber', 'address', 'city', 'state', 'postal_code',
                  'country', 'device_name', 'ip_address', 'operating_system', 'src', 'ref']

    # def validate(self, data):
    #     """
    #     Validate the entire serializer data.
    #     Ensure profile_picture is removed if not a valid image file.
    #     """
    #     profile_picture = data.get('profile_picture')
    #     if profile_picture:
    #         if not isinstance(profile_picture, serializers.ImageField):
    #             # Remove profile_picture if not an ImageField
    #             data.pop('profile_picture', None)

    #     return data

    # def update(self, instance, validated_data):
    #     # Update each field in the instance
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance


class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField("getfollowers")
    followings = serializers.SerializerMethodField("getfollowings")
    friends = serializers.SerializerMethodField("getfriends")
    userLevel = serializers.SerializerMethodField("getUserLevel")
    referredBy = serializers.SerializerMethodField("getReferredBy")
    mobileBanks = serializers.SerializerMethodField("getMobileBanks")
    cryptoBanks = serializers.SerializerMethodField("getCryptoBanks")
    bigBanks = serializers.SerializerMethodField("getBigBanks")
    walletId = serializers.SerializerMethodField("getwalletId")

    class Meta:
        model = models.User
        exclude = ['password']
    def getMobileBanks(self,model):
        wallet = getattr(model,"wallet",None)
        if not wallet:
            return []
        qs=MobileBank.objects.filter(wallet=wallet)
        return MobileBankModelSerializer(qs,many=True).data
    def getwalletId(self,model):
        wallet = getattr(model,"wallet",None)
        if not wallet:
            wallet=Wallet.objects.create(user=model)
        return wallet.wallet_id
    def getCryptoBanks(self,model):
        wallet = getattr(model,"wallet",None)
        if not wallet:
            return []
        qs=Crypto.objects.filter(wallet=wallet)
        return CryptoModelSerializer(qs,many=True).data
    def getBigBanks(self,model):
        wallet = getattr(model,"wallet",None)
        if not wallet:
            return []
        qs=BankAccount.objects.filter(wallet=wallet)
        return BankAccountModelSerializer(qs,many=True).data

    def getReferredBy(self, model: models.User):
        referral = models.Referral.objects.filter(referred_user=model).first()
        if not referral:
            return None
        return referral.referrer

    def getfollowers(self, model: models.User):
        followers = Follow.objects.filter(
            Q(active=True) & Q(follow_to=model)
        )
        return FollowSerializer(followers, many=True).data

    def getfollowings(self, model: models.User):
        followings = Follow.objects.filter(
            Q(active=True) & Q(user=model)
        )
        return FollowSerializer(followings, many=True).data

    def getUserLevel(self, model):
        try:
            return UserLevelSerializer(model.user_level).data
        except:
            return None

    def getfriends(self, model: models.User):
        followings = Follow.objects.filter(
            Q(active=True) & Q(user=model)
        )
        followers = Follow.objects.filter(
            Q(active=True) & Q(follow_to=model)
        )
        friends = []
        if (followings.exists() and followers.exists()):
            for f in followers:
                any = followings.filter(follow_to=f.user)
                if any.exists():
                    friends.append(any[0])
        return FollowSerializer(friends, many=True).data


class UserSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ['password']


class UserPictureSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = models.User
        fields = ['profile_picture']
        expandable_fields = {
            'profile_picture': ('reviews.ImageSerializer', {'many': True}),
        }

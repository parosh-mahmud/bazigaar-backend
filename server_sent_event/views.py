from django.http import StreamingHttpResponse
import time
from django.views.decorators.csrf import csrf_exempt
import time
from asgiref.sync import async_to_sync
from rest_framework.authentication import TokenAuthentication
import json
from notifications import models as nfModels
from notifications import serializers as nfSerializers
from livestream import models as LVmodels
from livestream import serializers as LVserializers
from django.db.models import Q
from django.utils.timezone import now
from chat_with_friend import models as cwfModels
from chat_in_group import models as cgModels

from chat_with_friend import serializers as cwfSerializers
from chat_in_group import serializers as cgSerializers

from calling_app2.models import Call
from calling_app2.serializers import CallSerializer
from group_call.models import GroupCall, GroupCallMember
from group_call.serializers import GroupCallSerializer


@csrf_exempt
@async_to_sync
async def notification_stream(request):
    def stream():
        if request.method == "GET":
            token = request.GET["token"]
            if token:
                request.META['HTTP_AUTHORIZATION'] = f'Token {token}'
            lastRequestNotificationCheck = lastCommentUpdate = lastPromotionNotificationCheck = lastGameNotificationCheck = lastEventNotificationCheck = last2v2messageCheck = last2v2callCheck = lastGroupCallCgeck = lastComMessageCheck = now()
            while True:
                user = get_user_from_token(request)
                if user:
                    try:
                        user.online = True
                        user.save()
                        # Sent RequestNotification
                        any = nfModels.RequestNotification.objects.filter(
                            Q(notification_to=user) & Q(updated_at__gt=lastRequestNotificationCheck))
                        if any.exists():
                            for x in any:
                                message = {
                                    "type": "RequestNotification",
                                    "data": nfSerializers.RequestNotificationSerializer(x).data
                                }
                                yield 'data: {}\n\n'.format(json.dumps(message))
                            lastRequestNotificationCheck = any.latest(
                                'updated_at').updated_at

                        # Sent  EventNotification
                        any = nfModels.EventNotification.objects.filter(Q(Q(notification_to=user) | Q(
                            to_all=True)) & Q(updated_at__gt=lastEventNotificationCheck))
                        if any.exists():
                            for x in any:
                                message = {
                                    "type": "EventNotification",
                                    "data": nfSerializers.EventNotificationSerializer(x).data
                                }
                                yield 'data: {}\n\n'.format(json.dumps(message))
                            lastEventNotificationCheck = any.latest(
                                'updated_at').updated_at

                        # Sent  GameNotification
                        any = nfModels.GameNotification.objects.filter(Q(Q(notification_to=user) | Q(
                            to_all=True)) & Q(updated_at__gt=lastGameNotificationCheck))
                        if any.exists():
                            for x in any:
                                message = {
                                    "type": "GameNotification",
                                    "data": nfSerializers.GameNotificationSerializer(x).data
                                }
                                yield 'data: {}\n\n'.format(json.dumps(message))
                            lastGameNotificationCheck = any.latest(
                                'updated_at').updated_at

                        # Sent  PromotionNotification
                        any = nfModels.PromotionNotification.objects.filter(Q(Q(notification_to=user) | Q(
                            to_all=True)) & Q(updated_at__gt=lastPromotionNotificationCheck))
                        if any.exists():
                            for x in any:
                                message = {
                                    "type": "PromotionNotification",
                                    "data": nfSerializers.PromotionNotificationSerializer(x).data
                                }
                                yield 'data: {}\n\n'.format(json.dumps(message))
                            lastPromotionNotificationCheck = any.latest(
                                'updated_at').updated_at

                        chats = cwfModels.ChatWithFriend.objects.filter(
                            Q(message_req_from=user) | Q(message_req_to=user))
                        # Listen 2v2 Message
                        for chat in chats:
                            any = cwfModels.Message.objects.filter(
                                Q(chat_with_friend=chat) & Q(updated_at__gt=last2v2messageCheck))
                            if any.exists():
                                for x in any:
                                    message = {
                                        "type": "2v2Message",
                                        "data": cwfSerializers.MessageSerializer(x).data
                                    }
                                    yield 'data: {}\n\n'.format(json.dumps(message))

                                last2v2messageCheck = any.latest(
                                    'updated_at').updated_at
                        # Listen to Call
                        calls = Call.objects.filter(Q(Q(callee=user) | Q(
                            caller=user)) & Q(updated_at__gt=last2v2callCheck))
                        if calls.exists():
                            for call in calls:
                                message = {
                                    "type": "2v2Call",
                                    "data": CallSerializer(call).data
                                }
                                yield 'data: {}\n\n'.format(json.dumps(message))
                            last2v2callCheck = calls.latest(
                                'updated_at').updated_at

                        comChats = cgModels.CommunityChat.objects.filter(
                            Q(member__member=user))
                        # Listen Community Message
                        for chat in comChats:
                            any = cgModels.Message.objects.filter(
                                Q(chat_in_community=chat) & Q(updated_at__gt=lastComMessageCheck))
                            if any.exists():
                                for x in any:
                                    message = {
                                        "type": "CommunityMessage",
                                        "data": cgSerializers.MessageSerializer(x).data
                                    }
                                    yield 'data: {}\n\n'.format(json.dumps(message))

                                lastComMessageCheck = any.latest(
                                    'updated_at').updated_at
                        # Listen to group Call
                        groupCalls = GroupCall.objects.filter(
                            Q(member__member=user) & Q(updated_at__gt=lastGroupCallCgeck))
                        if groupCalls.exists():
                            for call in groupCalls:
                                message = {
                                    "type": "GroupCall",
                                    "data": GroupCallSerializer(call).data
                                }
                                yield 'data: {}\n\n'.format(json.dumps(message))
                            lastGroupCallCgeck = calls.latest(
                                'updated_at').updated_at

                        # Live Stream Comment
                        any = LVmodels.Comment.objects.filter(
                            Q(created_at__gt=lastCommentUpdate))
                        if any.exists():
                            for x in any:
                                print("comment added")
                                message = {
                                    "type": "Comment",
                                    "data": LVserializers.CommentSerializer(x).data
                                }
                                yield 'data: {}\n\n'.format(json.dumps(message))
                            lastCommentUpdate = any.latest(
                                'created_at').created_at

                    except GeneratorExit:
                        user.online = False
                        user.save()
                        print(str(user)+" has gone offline")
                        break
                else:
                    break
                time.sleep(1)
    response = StreamingHttpResponse(
        stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response


def get_user_from_token(request):
    try:
        user, token = TokenAuthentication().authenticate(request=request)
    except:
        return None
    if user is not None:
        return user
    else:
        return None

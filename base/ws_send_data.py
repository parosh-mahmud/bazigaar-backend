from base.ws_constants import *
from base.ws import *
import json
from notifications import models as nfModels
from notifications import serializers as nfSerializers
from livestream import models as LVmodels
from livestream import serializers as LVserializers
from chat_with_friend import models as cwfModels
from chat_in_group import models as cgModels
from chat_with_friend import serializers as cwfSerializers
from chat_in_group import serializers as cgSerializers
from calling_app2.models import Call
from calling_app2.serializers import CallSerializer
from group_call.models import GroupCall, GroupCallMember
from group_call.serializers import GroupCallSerializer

def ws_send_model_to_data(userid,model):
    serializer=None
    _type=None
    if model.__class__==nfModels.RequestNotification:
        _type=WS_REQUEST_NOTIFICATION
        serializer=nfSerializers.RequestNotificationSerializer
    elif model.__class__==nfModels.EventNotification:
        _type=WS_EVENT_NOTIFICATION
        serializer=nfSerializers.EventNotificationSerializer
    elif model.__class__==nfModels.GameNotification:
        _type=WS_GAME_NOTIFICATION
        serializer=nfSerializers.GameNotificationSerializer
    elif model.__class__==nfModels.PromotionNotification:
        _type=WS_PROMOTION_NOTIFICATION
        serializer=nfSerializers.PromotionNotificationSerializer
    elif model.__class__==Call:
        _type=WS_2v2_CALL
        serializer=CallSerializer
    elif model.__class__==cgModels.Message:
        _type=WS_COMMUNITY_MESSAGE
        serializer=cgSerializers.MessageSerializer
    elif model.__class__==cwfModels.Message:
        _type=WS_2V2_MESSAGE
        serializer=cwfSerializers.MessageSerializer
    elif model.__class__==GroupCall:
        _type=WS_GROUP_CALL
        serializer=GroupCallSerializer
    elif model.__class__==LVmodels.Comment:
        _type=WS_LIVESTREAM_COMMENT
        serializer=LVserializers.CommentSerializer
    else:
        return
    data=serializer(model).data
    message=json.dumps({
            "type": _type,
            "data":data})
    wsMessageToUser(userid,message)
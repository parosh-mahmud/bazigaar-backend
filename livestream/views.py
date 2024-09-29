from django.http import StreamingHttpResponse
import time
from django.views.decorators.csrf import csrf_exempt
import time
from asgiref.sync import async_to_sync
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models, serializers
from django.utils.timezone import datetime
from django.utils.timezone import now
from django.contrib.auth import  get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
import json

@api_view(["POST"])
def getLiveStreams(request):
    liveStreams=models.LiveStream.objects.all().filter(isLive=True)
    serializer=serializers.LiveStreamMiniSerializers(liveStreams,many=True)
    return Response(serializer.data)


@api_view(["POST"])
def createALiveStream(request):
    user :get_user_model()= request.user
    data=request.data.dict()
    data["host"]=request.user
    print(data)
    if(user.isHost):
        try:
            ls=models.LiveStream()
            ls.host=request.user
            ls.name=request.data["name"]
            ls.thumbnail=request.data["thumbnail"]
            ls.save()
            seri=serializers.LiveStreamMiniSerializers(ls,many=False)
            return Response(seri.data)
        except Exception as e:
            print(e)
            return Response({"msg":str(e)},status=404)
    else:
        return Response({"msg":"You are not host"},status=403)
    return

@api_view(["PUT"])
def updateALiveStream(request):
    user :get_user_model()= request.user
    if(user.isHost):
        data=request.data.dict()
        any=models.LiveStream.objects.filter(id=data["id"])
        if any.exists():
            ls=any[0]
            isLive=data["isLive"]
            ls.isLive=False if isLive=="false" else True
            ls.save()
            seri=serializers.LiveStreamMiniSerializers(ls)
            return Response(seri.data,status=200)
            
        else:
            return Response({
                "Error":"not found"},status=404)
            
    else:
        return Response({"msg":"You are not host"},status=403)
    return


@api_view(["POST"])
def getSingleLiveStream(request):
    liveStream=get_object_or_404(models.LiveStream,id=request.data["id"])
    return Response( serializers.LiveStreamSerializers(liveStream,many=False).data)

@api_view(["POST"])
def commentHere(request):
    data={"live_stream":request.data["id"],
     "user":request.user.id,
     "text":request.data["text"]}
    # print(data)
    serializer=serializers.CommentSaveSerializer(data=data,partial=True)
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"msg":"Comment successful"},status=201)
    return Response({"msg":"Comment not successful"},status=404)

@api_view(["POST"])
def abc(request):
    return



@csrf_exempt
@async_to_sync
async def getLiveStreamSSE(request):
    def stream():
        if request.method=="GET":
            token=request.GET["token"]
            id=request.GET["id"]
            if token:
                request.META['HTTP_AUTHORIZATION'] = f'Token {token}'
            lastUpdate=lastCommentUpdate=now()
            while True:
                user=get_user_from_token(request)
                if user:
                    try:
                        user.online=True
                        user.save()
                        # LiveStream
                        any=models.LiveStream.objects.filter(updated_at__gt=lastUpdate)
                        if any.exists():
                            for x in any:
                                message={
                                    "type":"LiveStream",
                                    "data":serializers.LiveStreamSerializers(x).data
                                }
                                yield 'data: {}\n\n'.format(json.dumps(message))
                            lastUpdate=any.latest('updated_at').updated_at
                        
                        any=models.Comment.objects.filter(Q(live_stream__id=id)&Q(created_at__gt=lastCommentUpdate))
                        if any.exists():
                            for x in any:
                                print("comment added")
                                message={
                                    "type":"Comment",
                                    "data":serializers.CommentSerializer(x).data
                                }
                                yield 'data: {}\n\n'.format(json.dumps(message))
                            lastCommentUpdate=any.latest('created_at').created_at
                        
                            
                    except GeneratorExit:
                        user.online=False
                        user.save()
                        print(str(user)+" has left the livestream,id:"+str(id))
                        break
                else:
                    break
                time.sleep(1)
    response = StreamingHttpResponse(stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response


def get_user_from_token(request):
    try:
        user, token = TokenAuthentication().authenticate(request=request)
    except :
        return None
    if user is not None:
        return user
    else:
        return None
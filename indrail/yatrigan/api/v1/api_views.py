from rest_framework import status, generics, viewsets
from rest_framework.response import Response

from indrail import models as IrMdl
from indrail import serializers as IrSrl
from indrail.yatrigan.api.v1 import api_msg as IrApiV1Msg
from indrail.yatrigan.api.v1.railapi import pnr_status

def response_200(response_data):
    return Response(response_data, status=status.HTTP_200_OK)

def response_400(response_data):
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class ShopListApi(generics.ListAPIView):
    serializer_class = IrSrl.ShopList_YatriganSrl

    def get(self, request, *args, **kwargs):
        response_data = {}
        response_data['station'] = kwargs['station']
        shops = IrMdl.Shop.objects.filter(station__code=kwargs['station'])
        if shops.filter(is_active=True, is_verified=True).count() != 0:
            serializer = self.get_serializer(shops.filter(is_active=True, is_verified=True), many=True)
            response_data['shops'] = serializer.data
            return response_200(response_data)
        elif shops.filter(is_active=False).count() != 0 or shops.filter(is_verified=False).count() != 0:
            response_data.update(IrApiV1Msg.ShopListMsg.irShopListInActiveNotVerified(shops[0].station.name, shops[0].station.code))
            return response_400(response_data)
        else:
            station = IrMdl.Station.objects.get(code = kwargs['station'])
            response_data.update(IrApiV1Msg.ShopListMsg.irShopListEmpty(station.name, station.code))
            return response_400(response_data)


class ShopInfoApi(generics.RetrieveAPIView):
    serializer_class = IrSrl.ShopInfo_YatriganSrl

    def get(self, request, *args, **kwargs):
        response_data = {}
        response_data['shopId'] = kwargs['shopId']
        try:
          shop = IrMdl.Shop.objects.get(station__code=kwargs['station'], id=kwargs['shopId'], is_active=True, is_verified=True)
        except IrMdl.Shop.DoesNotExist:
            station = IrMdl.Station.objects.get(code = kwargs['station'])
            response_data.update(IrApiV1Msg.ShopListMsg.irShopListEmpty(station.name, station.code))
            return response_400(response_data)      
        serializer = self.get_serializer(shop)
        response_data['info'] = serializer.data
        return response_200(response_data)


class TrainListApi(generics.ListAPIView):
    serializer_class = IrSrl.TrainList_YatriganSrl

    def get(self, request, *args, **kwargs):
        trains = IrMdl.Train.objects.all()
        serializer = self.get_serializer(trains, many=True)
        trains = []
        for station in serializer.data:
            trains.append(station['train'])
        return response_200({
            "total" : len(trains),
            "trains" : trains,
        })


class TrainScheduleApi(generics.GenericAPIView):
    serializer_class = IrSrl.TrainSchedule_YatriganSrl

    def get(self, request, *args, **kwargs):
        response_data = {}
        response_data['trainNo'] = request.headers['train']
        try:
            train = IrMdl.Train.objects.get(train_no=request.headers['train'])
        except IrMdl.Train.DoesNotExist:
            response_data.update(IrApiV1Msg.TrainMsg.irTrainNotFound())
            return response_400(response_data)  
        serializers = self.get_serializer(train)
        response_data['trainSchedule'] = serializers.data
        return response_200(response_data)
       

class PnrStatusApi(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        return response_200(pnr_status.getPnrStatusApi(request.data['pnr']))
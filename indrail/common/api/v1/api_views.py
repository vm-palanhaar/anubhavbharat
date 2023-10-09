from rest_framework import generics, status
from rest_framework.response import Response

from indrail import models as IrMdl
from indrail import serializers as IrSrl


def response_200(response_data):
    return Response(response_data, status=status.HTTP_200_OK)

def response_201(response_data):
    return Response(response_data, status=status.HTTP_201_CREATED)

def response_400(response_data):
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

def response_401(response_data):
    return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

def response_403(response_data):
    return Response(response_data, status=status.HTTP_403_FORBIDDEN)

def response_409(response_data):
    return Response(response_data, status=status.HTTP_409_CONFLICT)


class RailStationListApi(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        stations = IrMdl.Station.objects.all()
        serializer = IrSrl.RailStationListSrl(stations, many=True)
        stations = []
        for station in serializer.data:
            stations.append(station['station'])
        return response_200({
            'total' : len(stations),
            "stations" : stations,
        })

"""
Copyright 2020 ООО «Верме»
"""

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from orgunits.api_v1.serializers import OrganizationSerializer
from orgunits.models import Organization
from wfm.views import TokenAuthMixin


class OrganizationViewSet(TokenAuthMixin, ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()

    @action(methods=["GET"], detail=True)
    def parents(self, request, *args, **kwargs):
        """
        Возвращает родителей запрашиваемой организации
        """
        
        parents = self.get_object().parents()
        serializer = self.get_serializer(parents, many=True)

        return Response(serializer.data)

    @action(methods=["GET"], detail=True)
    def children(self, request, *args, **kwargs):
        """
        Возвращает детей запрашиваемой организации
        """

        childrens = self.get_object().childrens()
        serializer = self.get_serializer(childrens, many=True)

        return Response(serializer.data)

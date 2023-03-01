from rest_framework import generics #importante o uso do genercis, pois facilita na escrita, e o get e post ja funcionamd por default
from rest_framework.generics import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import action #alterar acoes dentro do model view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import permissions

from .models import Curso, Avaliacao
from .serializers import CursoSerializer, AvaliacaoSerializer
from .permissions import SuperUserClass

"""API version 1"""


class CursosAPIView(generics.ListCreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class CursoAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class AvaliacoesAPIView(generics.ListCreateAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

    def get_queryset(self):
        if self.kwargs.get('curso_pk'):
            return self.queryset.filter(curso_id=self.kwargs.get('curso_pk'))
        return self.queryset.all()


class AvaliacaoAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

    def get_object(self):
        if self.kwargs.get("curso_pk"):
            return get_object_or_404(self.get_queryset(),
                                     curso_id=self.kwargs.get("curso_pk"),
                                     pk=self.kwargs.get("avaliacao_pk"))
        return get_object_or_404(self.get_queryset(),
                                 pk=self.kwargs.get("avaliacao_pk"))



"""API version 2"""


class CursoViewSet(viewsets.ModelViewSet):
    permission_classes = (
        SuperUserClass,
        permissions.DjangoModelPermissions,)
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    
    @action(detail=True, methods=['get'])
    def avaliacoes(self, request, pk=None):
        
        self.pagination_class.page_size = 2
        avaliacoes = Avaliacao.objects.filter(curso_id=pk)
        page = self.paginate_queryset(avaliacoes)
        
        if page is not None: 
            serializer = AvaliacaoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        # curso = self.get_object()
        # serializer = AvaliacaoSerializer(curso.avaliacoes.all(), many=True)
        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        return Response(serializer.data)

# paginacao global feita no arquivo settings nao influencia na paginacao deste model viewset pois foi feito por funcao sobrescrita

"""
class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
"""

# aqui posso colocar os metodos que eu quero atraves do mixins. se eu quiser tirar o get, ou o post, ou o destroy, ou qualquer dos metodos, posso fazer desta forma: 

class AvaliacaoViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
    ):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

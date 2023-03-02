from rest_framework import serializers
from django.db.models import Avg

from .models import Curso, Avaliacao


class AvaliacaoSerializer(serializers.ModelSerializer):

    class Meta:
        extra_kwargs = { # para nao comprometer a privacidade do usurio, campo sensivel
          "email": {"write_only": True}
        }
        model = Avaliacao
        fields = (
          "id",
          "curso",
          "nome",
          "email",
          "comentario",
          "avaliacao",
          "criacao",
          "ativo",
        )
        
    def validate_avaliacao(self, valor):
        if valor in range(1, 6): # 1, 2, 3, 4, 5
          return valor
        raise serializers.ValidationError("The avaliation must be between 1 e 5")

class CursoSerializer(serializers.ModelSerializer):
  # nested relationships
  # a lista pode ficar grande, este metodo deve ser pensado se vale a pen ou nao a depender do projeto:
    # avaliacoes = AvaliacaoSerializer(many=True, read_only=True)
    # HyperLinked related field: 
  """
    avaliacoes = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="avaliacao-detail")
  """
  # primary key related field: 
  # avaliacoes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
  
  # abordagem escolhida: hyperlinked related field
  avaliacoes = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="avaliacao-detail")
  media_avaliacoes = serializers.SerializerMethodField() # o serializerMethodField requer que criemos um metodo. Este metodo deve iniciar, por padrao, com o nome def get_nome_do_atributo_que_vai_atualizar. Recebe o self e o obj. Sendo o obj o curso especifico
    
  class Meta:
        model = Curso
        fields = (
          "id",
          "titulo",
          "url",
          "criacao",
          "ativo",
          "avaliacoes",
          "media_avaliacoes",
        )
        
        
  def get_media_avaliacoes(self, obj):
    media = obj.avaliacoes.aggregate(Avg("avaliacao")).get("avaliacao__avg")

    if media is None:
      return 0
    return round(media * 2) / 2 # o round retorna sempre um valor com 0.5 
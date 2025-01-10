from rest_framework import serializers

from user.models import User
from paper.models import Paper
from heart.models import Heart

class HeartSerializer(serializers.ModelSerializer):

    userName = serializers.CharField(source='userFK.name')
    rollingPaperName = serializers.CharField(source='paperFK.title')
    createdAt = serializers.DateTimeField(format='%Y.%m.%d')

    class Meta:
        model = Heart
        fields = ('id', 'userName', 'rollingPaperName', 'context', 'danger', 'createdAt')
    

class HeartWriteSerializer(serializers.ModelSerializer):
    
    userFK = serializers.IntegerField()
    paperFK = serializers.IntegerField()
    
    class Meta:
        model = Heart
        fields = ('userFK', 'paperFK', 'context')
        
    def create(self, validated_data):
        
        user_id = validated_data['userFK']
        paper_id = validated_data['paperFK']
        context = validated_data['context']
        
        heart_instance = Heart.objects.create(
            userFK=User.objects.get(pk=user_id),
            paperFK=Paper.objects.get(pk=paper_id),
            context=context
        )
        
        return heart_instance
    
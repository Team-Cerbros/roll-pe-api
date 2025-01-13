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
    
    def __init__(self, *args, **kwargs):
        self.method = kwargs.pop('method', 'post')
        super().__init__(*args, **kwargs)
        
        self.fields['userFK'] = serializers.IntegerField()
        self.fields['paperFK'] = serializers.IntegerField()
        self.fields['context'] = serializers.CharField()
        
        if self.method == 'patch': 
            self.fields['hcode'] = serializers.CharField()            
    
    class Meta:
        model = Heart
        fields = ()
        
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
    
    def update(self, validated_data):
        
        user_id = validated_data['userFK']
        paper_id = validated_data['paperFK']
        context = validated_data['context']
        hcode = validated_data['hcode']
        
        heart_instance = Heart.objects.filter(code=hcode).update(context=context)
        
        return heart_instance
        
    
from rest_framework import serializers

from user.models import User
from paper.models import Paper
from heart.models import Heart

class HeartReadSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        self.is_public = kwargs.pop('is_public', True)
        self.my_pk = kwargs.pop('my_pk', 0)
        super().__init__(*args, **kwargs)

    userName = serializers.CharField(source='userFK.name')
    rollingPaperName = serializers.CharField(source='paperFK.title')
    createdAt = serializers.DateTimeField(format='%Y.%m.%d')
    blur=serializers.SerializerMethodField()

    class Meta:
        model = Heart
        fields = ('id', 'userName', 'rollingPaperName', 'context', 'danger', 'createdAt', 'index', 'blur', 'code')
        
    def get_blur(self, obj):
        if self.is_public or self.my_pk == 0 or self.my_pk >= obj.id:
            return False
        return True
                    
    
class HeartWriteSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        self.method = kwargs.pop('method', 'post')
        super().__init__(*args, **kwargs)
        
        self.fields['paperFK'] = serializers.IntegerField()
        self.fields['context'] = serializers.CharField()
        self.fields['index'] = serializers.IntegerField()
        
        if self.method == 'patch': 
            self.fields['hcode'] = serializers.CharField()            
    
    class Meta:
        model = Heart
        fields = ()
        
        
    def create(self, validated_data):
        
        heart_instance = Heart.objects.create(
            userFK=User.objects.get(pk=validated_data['userFK']),
            paperFK=Paper.objects.get(pk=validated_data['paperFK']),
            context=validated_data['context'],
            index=validated_data['index']
        )
        return heart_instance
    
    
    # def update(self, validated_data):
        
    #     user_id = validated_data['userFK']
    #     paper_id = validated_data['paperFK']
    #     context = validated_data['context']
    #     hcode = validated_data['hcode']
        
    #     heart_instance = Heart.objects.filter(code=hcode).update(context=context)
        
    #     return heart_instance
        
    
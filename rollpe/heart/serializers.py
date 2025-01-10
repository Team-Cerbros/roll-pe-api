from rest_framework import serializers

from heart.models import Heart

class HeartSerializer(serializers.ModelSerializer):

    userName = serializers.CharField(source='userFK.name')
    rollingPaperName = serializers.CharField(source='paperFK.title')
    createdAt = serializers.DateTimeField(format='%Y.%m.%d')

    class Meta:
        model = Heart
        fields = ('id', 'userName', 'rollingPaperName', 'context', 'danger', 'createdAt')
    
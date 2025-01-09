from rest_framework import serializers

from paper.models import Paper


class UserShowPaperSerializer(serializers.ModelSerializer):
	hostName = serializers.SerializerMethodField()
	class Meta:
		model = Paper
		fields = ["id", "title", "viewStat", "receivingStat", "receivingDate", "hostName"]
	def get_hostName(self, paper):
		return paper.hostFK.name


class PaperCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Paper
		fields = [
			'hostFK', 'receiverFK', 'receiverName',
			'receiverTel', 'receivingDate', 'receivingStat',
			'viewStat', 'title', 'description', 'password',
			]
		read_only_fields = ("id", "createdAt", "updatedAt", "code")

	def validate_receiverTel(self, receiverTel):
		if not receiverTel.isdigit():
			raise serializers.ValidationError("receiverTel 영역의 값은 int로 이루어져야 합니다.")

		if len(receiverTel) != 11:
			raise serializers.ValidationError("receiverTel 영역의 값은 11자리여야 합니다. 010XXXXXXXX 형식")

		return receiverTel

	def validate(self, attrs):
		receiverFK = attrs.get('receiverFK')
		receiverName = attrs.get('receiverName')
		receiverTel = attrs.get('receiverTel')

		if not receiverFK and (not receiverName or not receiverTel):
			raise serializers.ValidationError(
				"수신자 정보를 위해 receiverFK 또는 receiverName, receiverTel 중 최소 하나는 반드시 전달되어야 합니다."
				)
		return attrs

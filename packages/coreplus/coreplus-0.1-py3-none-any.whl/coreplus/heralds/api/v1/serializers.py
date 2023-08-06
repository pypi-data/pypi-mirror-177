from rest_framework import serializers

from coreplus.reactions.api.v1.serializers import ReactionableModelSerializer

from ...models import DirectMessage, DirectMessageAttachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessageAttachment
        fields = "__all__"


class DirectMessageSerializer(ReactionableModelSerializer, serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = DirectMessage
        fields = "__all__"


class DirectMessageCreateSerializer(serializers.ModelSerializer):
    attachment_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )

    class Meta:
        model = DirectMessage
        fields = ["content", "recipient", "attachment_ids"]

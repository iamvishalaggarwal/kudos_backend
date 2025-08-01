from rest_framework import serializers
from .models import User, Kudo


class UserSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "organization"]

    def get_organization(self, obj):
        return obj.organization.name


class CurrentUserSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    rem_kudos = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "organization", "rem_kudos"]

    def get_organization(self, obj):
        return obj.organization.name

    def get_rem_kudos(self, obj):
        return obj.kudos_remaining()


class KudosSummarySerializer(serializers.Serializer):
    given = serializers.SerializerMethodField()
    receive = serializers.SerializerMethodField()

    def get_given(self, obj):
        kudos_given = obj["kudos_given"]
        return [
            {
                "id": k.recipient.id,
                "username": k.recipient.username,
                "message": k.message,
                "timestamp": k.timestamp,
            }
            for k in kudos_given
        ]

    def get_receive(self, obj):
        kudos_received = obj["kudos_received"]
        return [
            {
                "id": k.sender.id,
                "username": k.sender.username,
                "message": k.message,
                "timestamp": k.timestamp,
            }
            for k in kudos_received
        ]


class GiveKudoSerializer(serializers.ModelSerializer):
    recipient_id = serializers.IntegerField()

    class Meta:
        model = Kudo
        fields = ["recipient_id", "message"]

    def validate(self, data):
        sender = self.context["request"].user
        if sender.kudos_remaining() <= 0:
            raise serializers.ValidationError(
                {"non_field_errors": ["You have no kudos left this week."]}
            )
        return data

    def create(self, validated_data):
        sender = self.context["request"].user

        try:
            recipient = User.objects.get(id=validated_data["recipient_id"])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"non_field_errors": ["Recipient does not exist."]}
            )

        if sender.organization != recipient.organization:
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        "You can only give kudos within your organization."
                    ]
                }
            )

        if sender.id == recipient.id:
            raise serializers.ValidationError(
                {"non_field_errors": ["You can only give kudos to others."]}
            )

        return Kudo.objects.create(
            sender=sender, recipient=recipient, message=validated_data["message"]
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from kudos.serializers import KudosSummarySerializer, GiveKudoSerializer
from kudos.models import Kudo


class KudosSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        kudos_given = Kudo.objects.filter(sender=user).order_by("-timestamp")
        kudos_received = Kudo.objects.filter(recipient=user).order_by("-timestamp")

        context = {
            "user": user,
            "kudos_given": kudos_given,
            "kudos_received": kudos_received
        }

        serializer = KudosSummarySerializer(context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GiveKudoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GiveKudoSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": f"Kudos sent to {request.user.username}!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KudosRemainingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"remaining": request.user.kudos_remaining()}, status=status.HTTP_200_OK
        )

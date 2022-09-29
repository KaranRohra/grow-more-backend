from accounts import models
from accounts import serializers
from rest_framework import authentication
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import views
from rest_framework import status


class RegisterAPI(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

    def post(self, request):
        response = self.create(request)
        return response
    

class UserAPI(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        new_email = request.data.get("new_email")
        if current_password and new_password:
            if request.user.check_password(current_password):
                request.user.set_password(new_password)
                request.user.save()
                return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    data={
                        "current_password": "wrong password",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        elif new_email:
            user = models.User.objects.filter(email=new_email).first()
            if user:
                return Response(
                    data={
                        "new_email": "Email already exists",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                request.user.email = new_email
                request.user.save()
                return Response({"message": "Email changed successfully"}, status=status.HTTP_200_OK)
        else:
            user = serializers.UserSerializer(instance=request.user, data=request.data, partial=True)
            if user.is_valid():
                user.save()
                return self.get(request)
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
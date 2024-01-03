from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import MyTokenObtainPairSerializer
  
class HomeView(APIView):
    permission_classes = (IsAuthenticated, )
  
    def get(self, request):
        content = {'message': 'Welcome to the JWT Authentification page using React Js and Django!'}
        return Response(content)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            print("Se ha cerrado sesión correctamente")
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print("Ha ocurrido un error:", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
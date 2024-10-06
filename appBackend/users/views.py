# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
# from .models import CustomUser
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from rest_framework.permissions import IsAuthenticated
# # from rest_framework.decorators import api_view, permission_classes

# from django.db.models import Q



# class RegisterView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user)

#             # Create an access token and include the username
#             access_token = refresh.access_token
#             access_token['username'] = user.username  # Add username to token claims

#             return Response({
#                 "user": user.to_json(),  # Assuming to_json() returns user details
#                 "refresh": str(refresh),
#                 "access": str(access_token),
#             }, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginView(APIView):
    
#     def post(self, request):
#         print("Login request data:", request.data)  # Log incoming request data
#         serializer = LoginSerializer(data=request.data)
        
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']

#             # Retrieve the user object
#             try:
#                 user = CustomUser.objects.get(username=username)
                
#                 if user.check_password(password):
#                     refresh = RefreshToken.for_user(user)
#                     # Add custom claims to the access token
#                     access_token = refresh.access_token
#                     access_token['username'] = user.username  # Include the username in the token
                    
#                     return Response({
#                         "user": user.to_json(),
#                         "refresh": str(refresh),
#                         "access": str(access_token),
#                     }, status=status.HTTP_200_OK)
#                 else:
#                     return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
#             except CustomUser.DoesNotExist:
#                 return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class DashboardView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response({"message": f"Hello, {request.user.username}! Welcome to the dashboard."}, status=status.HTTP_200_OK)


# # class SearchUsersView(APIView):
# #     permission_classes = [IsAuthenticated]

# #     def get(self, request):
# #         query = request.GET.get('query', '').strip()
# #         if not query:
# #             return Response({"error": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

# #         # Perform case-insensitive search on username and phone_number
# #         users = CustomUser.objects(
# #             username__icontains=query
# #         ) | CustomUser.objects(
# #             phone_number__icontains=query
# #         )

# #         # Serialize the results
# #         serializer = UserSerializer(users, many=True)
# #         return Response(serializer.data, status=status.HTTP_200_OK)
    

# # class SearchUsersView(APIView):
# #     permission_classes = [IsAuthenticated]

# #     def get(self, request):
# #         query = request.GET.get('query', '').strip()
        
# #         if not query:
# #             return Response({"error": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

# #         # Perform a case-insensitive search on username and phone_number
# #         users = CustomUser.objects.filter(
# #             Q(username__icontains=query) | Q(phone_number__icontains=query)
# #         )

# #         # Serialize the results
# #         serializer = UserSerializer(users, many=True)
# #         return Response(serializer.data, status=status.HTTP_200_OK)


# class SearchUsersView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         query = request.GET.get('query', '').strip()
        
#         if not query:
#             return Response({"error": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

#         # Perform a case-insensitive search on username and phone_number
#         users_by_username = CustomUser.objects.filter(username__icontains=query)
#         users_by_phone = CustomUser.objects.filter(phone_number__icontains=query)

#         # Combine the querysets
#         users = list(users_by_username) + list(users_by_phone)
#         users = list(set(users))

#         # Serialize the results
#         serializer = UserSerializer(users, many=True)
        
#         if not serializer.data:
#             return Response({"message": "No users found."}, status=status.HTTP_404_NOT_FOUND)

#         return Response(serializer.data, status=status.HTTP_200_OK)




from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, CurrentUserSerializer
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            # Create an access token and include the username
            access_token = refresh.access_token
            access_token['username'] = user.username  # Add username to token claims

            return Response({
                "user": user.to_json(),  # Assuming to_json() returns user details
                "refresh": str(refresh),
                "access": str(access_token),
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        print("Login request data:", request.data)  # Log incoming request data
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Retrieve the user object
            try:
                user = CustomUser.objects.get(username=username)
                
                if user.check_password(password):
                    # Update last_seen and is_online on successful login
                    user.last_seen = timezone.now()  # Update last_seen to current time
                    user.is_online = True  # Set user as online
                    user.save()

                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token
                    access_token['username'] = user.username  # Include the username in the token
                    
                    return Response({
                        "user": user.to_json(),
                        "refresh": str(refresh),
                        "access": str(access_token),
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
            except CustomUser.DoesNotExist:
                return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = CurrentUserSerializer(user)
        # return Response({"message": f"Hello, {request.user.username}! Welcome to the dashboard."}, status=status.HTTP_200_OK)
        return Response(serializer.data)


class SearchUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get('query', '').strip()
        
        if not query:
            return Response({"error": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Perform a case-insensitive search on username and phone_number
        users_by_username = CustomUser.objects.filter(username__icontains=query)
        users_by_phone = CustomUser.objects.filter(phone_number__icontains=query)

        # Combine the querysets
        users = list(users_by_username) + list(users_by_phone)
        users = list(set(users))

        # Serialize the results
        serializer = UserSerializer(users, many=True)
        
        if not serializer.data:
            return Response({"message": "No users found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CurrentUserView(APIView):
    """
    API view to retrieve the current authenticated user's information.
    """
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Assuming request.user is correctly set via JWT
        serializer = CurrentUserSerializer(user)
        return Response(serializer.data)
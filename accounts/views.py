from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer, UserSearchSerializer
from .models import User
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.authtoken.models import Token


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class SearchView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = UserSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        search_keyword = serializer.validated_data["search_keyword"].strip()

        try:
            # Search by email, if there is a match return the user.
            user = User.objects.get(email=search_keyword)
            return Response(
                {"users": [UserSerializer(user).data], "total_pages": 1},
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            # Search by first name and last name if the email search failed.
            users = User.objects.filter(
                Q(first_name__icontains=search_keyword)
                | Q(last_name__icontains=search_keyword)
            )

            # Paginate the results
            paginator = Paginator(users, 10)
            page_number = request.query_params.get("page", 1)
            page_obj = paginator.get_page(page_number)
            serialized_users = [UserSerializer(user).data for user in page_obj]
            return Response(
                {"users": serialized_users, "total_pages": paginator.num_pages},
                status=status.HTTP_200_OK,
            )

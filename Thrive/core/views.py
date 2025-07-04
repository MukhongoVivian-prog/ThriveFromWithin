# core/views.py
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from rest_framework.generics import ListAPIView

from .models import Affirmation, Scene, Sound, User, Material
from .serializers import AffirmationSerializer, MaterialSerializer, RegisterSerializer, CustomTokenObtainPairSerializer, SceneSerializer, SoundSerializer, TherapistSerializer, UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

"""
- [*]  Register normal user
- [*]  Register Company admin
- [*]  login
- [*]  company profile update
- [*]  user profile update
- [*]  user mood and info
- [ ]  employees overview / see all employees

buggy : work on permissions and fields required
user should not be able to update their role
"""

"""
- [*]  create  and get webinars, guides and company materials
"""

class ManageCompanyMaterial(ViewSet):
    """
    create and get webinars, guides and company materials for the authenticated user's company.

    list:
        - Returns a list of materials for the user's company.
        - Authentication required.
        - Response: 200 OK, list of materials (title, description, file, etc.)
    create:
        - Allows company admin/manager to upload a new material.
        - Request: multipart/form-data with 'file_name', 'description', and 'file'.
        - Response: 201 CREATED on success, 401 UNAUTHORIZED if not allowed.
    retrieve:
        - Get a single material by ID for the user's company.
        - Response: 200 OK with material data, 404 if not found.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List all materials for the authenticated user's company",
        responses={200: MaterialSerializer(many=True)}
    )
    def list(self,request):
        """
        Get all materials for the authenticated user's company.
        Response: 200 OK, list of materials.
        """
        user = request.user
        materials = Material.objects.filter(company=user.company)

        return Response(MaterialSerializer(materials, many=True).data)

    @swagger_auto_schema(
        operation_summary="Upload a new material for the user's company",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'file_name': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'file': openapi.Schema(type=openapi.TYPE_FILE),
            }
        ),
        responses={201: 'Created', 401: 'Unauthorized'}
    )
    def create(self,request):
        """
        Upload a new material for the user's company.
        Request: multipart/form-data with 'file_name', 'description', 'file'.
        Response: 201 CREATED or 401 UNAUTHORIZED.
        """
        user = request.user

        if user.role == "employee" or user.role == "therapist":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.POST
        file_name = data['file_name']
        description = data['description']
        file = request.FILES['file']

        material = Material()

        material.company = user.company
        material.title = file_name
        material.description = description
        material.file = file

        material.save()
        return Response(status=status.HTTP_201_CREATED)


    @swagger_auto_schema(
        operation_summary="Retrieve a single material by ID",
        responses={200: MaterialSerializer()}
    )
    def retrieve(self,request,pk=None):
        """
        Get a single material by ID for the user's company.
        Response: 200 OK with material data, 404 if not found.
        """
        user = request.user
        materials = Material.objects.filter(company=user.company)
        material = materials.objects.get(id=pk)

        return Response(MaterialSerializer(material).data)

class SetUserEnvironmentAndChallenges(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Set user's environment and challenges",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'environment': openapi.Schema(type=openapi.TYPE_STRING),
                # 'challenges': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={200: 'Success'}
    )
    def post(self,request,format=None):
        data = request.POST
        user = request.user
        environment = data['environment']
        # challenges = data['challenges']

        user.environment = environment
        # user.challenges = challenges
        user.save()

        return Response({},status=200)

class ManageUser(ViewSet):
    """
    Manage user registration, listing, retrieval, and update.

    list:
        - List all employees in the authenticated user's company.
        - Only accessible by admin/manager.
        - Query params: staff-metric (optional), name (optional)
        - Response: 200 OK, list of users.
    create:
        - Register a new user.
        - Request: JSON body with user fields (see RegisterSerializer).
        - Response: 201 CREATED with user data, 400 BAD REQUEST on error.
    retrieve:
        - Get a user by ID.
        - Response: 200 OK with user data, 404 if not found.
    update:
        - Update a user by ID.
        - Request: JSON body with updatable fields.
        - Response: 200 OK with updated user, 400/404 on error.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # 🔐 Make this public
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_summary="List all employees in the authenticated user's company",
        manual_parameters=[
            openapi.Parameter('staff-metric', openapi.IN_QUERY, description="Optional staff metric", type=openapi.TYPE_STRING),
            openapi.Parameter('name', openapi.IN_QUERY, description="Optional name filter", type=openapi.TYPE_STRING),
        ],
        responses={200: UserSerializer(many=True)}
    )
    def list(self,request):
        """
        List all employees in the authenticated user's company.
        Query params: staff-metric (optional), name (optional)
        Response: 200 OK, list of users.
        """
        # see all employees
        metric = request.query_params.get("staff-metric")
        name = request.query_params.get("name")

        user = request.user
        
        if user.role == "employee" or user.role == "therapist":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        employees = User.objects.filter(company=user.company)
        employees = employees.aaggregate

        return Response(UserSerializer(employees, many=True).data)

    @swagger_auto_schema(
        operation_summary="Register a new user",
        request_body=RegisterSerializer,
        responses={201: RegisterSerializer(), 400: 'Bad Request'}
    )
    def create(self, request):
        """
        Register a new user.
        Request: JSON body with user fields (see RegisterSerializer).
        Response: 201 CREATED with user data, 400 BAD REQUEST on error.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token,_ = Token.objects.get_or_create(user=user)

            return Response({
                'message': 'User registered successfully',
                'user': self.serializer_class(user).data,
                'token':token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Get a user by ID",
        responses={200: RegisterSerializer(), 404: 'Not Found'}
    )
    def retrieve(self, request, pk=None):
        """
        Get a user by ID.
        Response: 200 OK with user data, 404 if not found.
        """
        try:
            user = request.user
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Update a user by ID",
        request_body=RegisterSerializer,
        responses={200: RegisterSerializer(), 400: 'Bad Request', 404: 'Not Found'}
    )
    def update(self, request, pk=None):
        """
        Update a user by ID.
        Request: JSON body with updatable fields.
        Response: 200 OK with updated user, 400/404 on error.
        """
        try:
            user = request.user
            serializer = self.serializer_class(user, data=request.data, partial=True)
            if serializer.is_valid():
                updated_user = serializer.save()
                return Response({
                    'message': 'User and/or company updated successfully',
                    'user': self.serializer_class(updated_user).data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        

class CustomTokenView(APIView):
    """
    Obtain authentication token for a user.
    POST: username, password (form-data or JSON)
    Response: 200 OK with token, 401 if invalid credentials.
    """
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary="Obtain authentication token for a user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={200: openapi.Response('Token', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING),
            'employee': openapi.Schema(type=openapi.TYPE_BOOLEAN)
        })), 401: 'Invalid credentials'}
    )
    def post(self,request, format=None):
        """
        Authenticate user and return token.
        Request: username, password (form-data or JSON)
        Response: 200 OK with token, 401 if invalid credentials.
        """
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            token,_ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, "employee":user.role == "employee"})
        return Response({'error': 'Invalid credentials'}, status=401)
    
"""
[*] get scenes
[*] get and filter sounds
[*] get affirmations
"""

class ManageSounds(APIView):
    """
    Get and filter sounds.
    GET: Optional query param 'title' to filter by sound title.
    Response: 200 OK, list of sounds (title, tag, picture, audio).
    """
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary="Get and filter sounds",
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, description="Filter by sound title", type=openapi.TYPE_STRING)
        ],
        responses={200: SoundSerializer(many=True)}
    )
    def get(self,request,format=None):
        """
        Get all sounds or filter by title.
        Query param: title (optional)
        Response: 200 OK, list of sounds.
        """
        title = request.query_params.get("title")

        sounds = Sound.objects.all()
        if title is not None:
            sounds = sounds.filter(title__icontains=title)

        return Response(SoundSerializer(sounds, many=True).data)

class GetScenes(ListAPIView):
    """
    List all scenes.
    GET: No params.
    Response: 200 OK, list of scenes (title, description, file).
    """
    permission_classes = [AllowAny]
    serializer_class = SceneSerializer
    queryset = Scene.objects.all()

    @swagger_auto_schema(
        operation_summary="List all scenes",
        responses={200: SceneSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class GetAffirmations(ListAPIView):
    """
    List all affirmations.
    GET: No params.
    Response: 200 OK, list of affirmations (quote, by).
    """
    permission_classes = [AllowAny]
    queryset = Affirmation.objects.all()
    serializer_class = AffirmationSerializer

    @swagger_auto_schema(
        operation_summary="List all affirmations",
        responses={200: AffirmationSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ManageTherapist(ViewSet):
    """
    List and manage therapists.
    list:
        - List all therapists, optionally filter by name.
        - Query param: name (optional, filters by first or last name)
        - Response: 200 OK, list of therapists.
    """
    queryset = User.objects.filter(role="therapist")
    serializer_class = ""

    @swagger_auto_schema(
        operation_summary="List all therapists, optionally filter by name",
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Filter by therapist name", type=openapi.TYPE_STRING)
        ],
        responses={200: TherapistSerializer(many=True)}
    )
    def list(self,request,format=None):
        """
        List all therapists, optionally filter by name.
        Query param: name (optional)
        Response: 200 OK, list of therapists.
        """
        name = request.query_params.get("name")
        data = self.queryset

        if name is not None:
            data = data.filter(Q(first_name__icontains=name)|Q(last_name__icontains=name))

        return Response(TherapistSerializer(data, many=True).data)
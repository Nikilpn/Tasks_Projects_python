from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from blogapp.serializers import RegisterSerializer,LoginSerializer,BlogSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from blogapp.models import Blog
from rest_framework.exceptions import PermissionDenied


class RegisterApiView(GenericAPIView):
    permission_classes=[AllowAny]
    serializer_class=RegisterSerializer
    
    
    def post(self,request,*args,**kwargs):
        serializer_instance=self.get_serializer(data=request.data)
        if serializer_instance.is_valid():
            user=serializer_instance.save()
            return Response(
                {
                "user_id":user.id,
                "user_name":user.email,
                'token': user.token,
                'message': 'User created successfully'
            
                }
            )
        return Response(
            serializer_instance.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UserLoginApiView(GenericAPIView):
    permission_classes=[AllowAny]
    serializer_class=LoginSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']    
        
        token= Token.objects.get(user=user)

        return Response({
            'user_id': user.id,
            'username': user.email,
            'token': token.key,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    
        
        return Response(
            data=serializer_instance.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
        
class AddBlogApiView(GenericAPIView):
    serializer_class=BlogSerializer
    permission_classes=[IsAuthenticated]
    
    def post(self,request,*args,**kwargs):
        serializer_instance=self.get_serializer(data=request.data)
        authenticated_user=request.user

        if serializer_instance.is_valid(raise_exception=True):
            blog = serializer_instance.save(owner=request.user)
            if authenticated_user:
                return Response(
                    {
                        'user_id':authenticated_user.id,
                        'user_email':authenticated_user.email,
                        'user_data':serializer_instance.data

                    }
                )
        return Response(
            {'message':'invalid user'}
        )
        
    
class ListAllBlog(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=BlogSerializer
    def get(self,request,*args,**kwargs):
        qs=Blog.objects.all()
        serializer=self.get_serializer(qs,many=True)
        return Response(
            {  
                'user':serializer.data,

             }
        )
        
class BlogUpdateApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    
    def put(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        
        try:
            blog_object = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return Response(
                {'error': 'Blog not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer_instance = self.get_serializer(
            instance=blog_object,  # instance first
            data=request.data      # data second
        )
        
        if serializer_instance.is_valid():
            authenticated_user = request.user
            owner = blog_object.owner  # Get owner from instance, not serializer
            
            if authenticated_user == owner:
                serializer_instance.save()
                return Response(
                    serializer_instance.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'You are not authorized to update this blog'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                serializer_instance.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )

class DeleteBlogApiView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    
    def perform_destroy(self, instance):
        try:
        # Check if the authenticated user is the owner
            if self.request.user != instance.owner:
                raise PermissionDenied("You are not authorized to delete this blog")
        except:
            
            # Proceed with deletion (this is automatic, but you can be explicit)
            instance.delete()
            return Response(
                    {'message': 'Blog deleted successfully'}, 
                     status=status.HTTP_200_OK
                     )
            
#for black-listing
class ReportBlogApiView(generics.GenericAPIView):
    # serializer_class=BlogReportSerializer
    def post(self,request,*args,**kwargs):
        
        pass
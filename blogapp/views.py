from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from blogapp.serializers import RegisterSerializer,LoginSerializer,BlogSerializer,BlogReportSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from blogapp.models import Blog,BlogReport,BlacklistedUser
from rest_framework.exceptions import PermissionDenied
from django.db import IntegrityError
from rest_framework.response import Response



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
        
    # class ListAllBlog(generics.ListAPIView):
#     # permission_classes=[IsAuthenticated]
#     serializer_class=BlogSerializer
#     def get(self,request,*args,**kwargs):
#         qs=Blog.objects.all()
#         serializer=self.get_serializer(qs,many=True)
#         return Response(
#             {  
#                 'user':serializer.data,

#              }
#         )


class ListAllBlog(generics.ListAPIView):
        # permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()  # ഇത് മാത്രം മതി!
    
    # get() method വേണ്ടാ - automatic pagination work ചെയ്യും
    
    
class BlogUpdateApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()  # Add this line
    
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
            instance=blog_object,
            data=request.data
        )
        if serializer_instance.is_valid():
            authenticated_user = request.user
            owner = blog_object.owner
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
    
            if self.request.user != instance.owner:
                raise PermissionDenied("You are not authorized to delete this blog")
        except:
            
          
            instance.delete()
            return Response(
                    {'message': 'Blog deleted successfully'}, 
                     status=status.HTTP_200_OK
                     )
            
#for black-listing
# class ReportBlogApiView(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = BlogReportSerializer
#     report_count = 0
    
#     def post(self, request, *args, **kwargs):
#         serializer_instance = self.get_serializer(data=request.data)
#         serializer_instance.is_valid(raise_exception=True)
#         blog = serializer_instance.validated_data['blog']
#         description = serializer_instance.validated_data['description']
#         reported_by = request.user
#         reported_to = blog.owner
        
#         if reported_to == reported_by:
#             return Response({
#                 'error': 'You cannot report your own blog'
#             }, status=400),
            
        
#         try:
#             report = serializer_instance.save(reported_by=reported_by)
#             return Response({
#                 'message': 'Report successfully created',
#                 'report_id': report.id
#             }, status=201)
#         except IntegrityError:
#             return Response({
#                 'error': 'You have already reported this blog'
#             }, status=400)
   
class ReportBlogApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogReportSerializer
    report_count = 0
    
    def post(self, request, *args, **kwargs):
        serializer_instance = self.get_serializer(data=request.data)
        serializer_instance.is_valid(raise_exception=True)
        blog = serializer_instance.validated_data['blog']
        description = serializer_instance.validated_data['description']
        reason = serializer_instance.validated_data['reason']
        reported_by = request.user
        reported_to = blog.owner
        
        if reported_to == reported_by:
            return Response({
                'error': 'You cannot report your own blog'
            }, status=400)
        
        try:
            # Save the report
            report = serializer_instance.save(reported_by=reported_by)
            
           
            blog.is_active = False
            blog.save()
            
            return Response({
                'message': 'Report successfully created and blog deactivated',
                'report_details': {
                    'report_id': report.id,
                    'blog_id': blog.id,
                    'blog_title': blog.title,
                    'reported_to': reported_to.email,
                    'reason': reason
                },
                'action_taken': {
                    'blog_deactivated': True,
                    'blog_is_now_active': False,
                    'deactivation_reason': 'report received'
                }
            }, status=201)
            
        except IntegrityError:
            return Response({
                'error': 'You have already reported this blog'
            }, status=400)
            
            
class GetReportListView(generics.GenericAPIView):
    # permission_classes = [IsAdminUser]
    serializer_class=BlogReportSerializer
    
    
    def get(self, request, *args, **kwargs):

        qs = BlogReport.objects.select_related(   #its a good appproach nallath
            'blog', 'blog__owner', 'reported_by'
        ).order_by('-created_at')
        
        reports_data = []
        for report in qs:
            report_data = {
                'report_id': report.id,
                'blog_title': report.blog.title,
                'report_to':report.blog.owner.id,
                'blog_owner_email': report.blog.owner.email,   
                
                'report_by_id':report.reported_by.id,
                'reported_by_email': report.reported_by.email,  
                'reason': report.reason,
                'description': report.description,
                'created_at': report.created_at.isoformat(),
  
            }
            reports_data.append(report_data)
        
        return Response({
            'total_reports': len(reports_data),
            'reports': reports_data
        })
        
# class GetReportListView(generics.GenericAPIView):
#     permission_classes = []
#     serializer_class=[BlogReportSerializer]
    
#     def get(self, request, *args, **kwargs):
#         qs=BlogReport.objects.all()
#         serializer_instance=self.get_serializer(qs,many=True)
#         if serializer_instance.is_valid:
#             return Response(
#                 data=serializer_instance.data
#             )
#         else:
#             return Response(
#                 {'message':'cant view'}
#             )

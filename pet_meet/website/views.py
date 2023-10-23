from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import Http404

from rest_framework.generics import (
    GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User, Meeting, Group, Post, Comment, Animal
from .serializers import (
    AnimalDetailSerializer, AnimalIndexSerializer, 
    CommentDetailSerializer, CommentIndexSerializer,
    GroupDetailSerializer, GroupIndexSerializer, 
    MeetingDetailSerializer, MeetingIndexSerializer, 
    PostDetailSerializer, PostIndexSerializer, 
    UserDetailSerializer, UserIndexSerializer 
)


def find_or_404(model, pk):
    record = model.objects.filter(id=pk).first()
    if record == None:
        raise Http404
    
    return record


def paginate(request, queryset, serializer_class):
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(queryset, request=request)
    serializer = serializer_class(page, many=True)
    return paginator.get_paginated_response(serializer.data)


class SignUpAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserIndexSerializer

    def post(self, request):
        user = User(
            email=request.data['email'], #request.data is a dict with 'email' as a field (dynamic parameters)
            #password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            address_street=request.data['address_street'],
            address_city=request.data['address_city'],
            address_country=request.data['address_country'],
            phone_number=request.data['phone_number'],
            bio=request.data['bio']
        )
        user.set_password(request.data['password'])
        try:
            user.save() #ORM saving in to the database
            serializer = UserDetailSerializer(user)
            return Response(serializer.data)
        except IntegrityError:
            return Response({
                'success': False,
                'error': f'User with email {user.email} already exists'
            })


class UserIndexAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserIndexSerializer
    pagination_class = PageNumberPagination


class UserDetailAPIView(GenericAPIView):
    serializer_class = UserDetailSerializer

    def get(self, request, user_id):
        user = find_or_404(User, user_id)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    
    # we don't need to create user using post method cause we have already created him using sign up methon above 

    def put(self, request, user_id):
        user = find_or_404(User, user_id)
        if user != request.user:
            return Response({
                'success': False,
                'error': 'forbidden'
            })

        user.set_password(request.data['password'])
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.address_street = request.data['address_street']
        user.address_city = request.data['address_city']
        user.address_country = request.data['address_country']
        user.phone_number = request.data['phone_number']
        user.bio = request.data['bio']
        user.save()
        serializer = UserDetailSerializer(user)
        login(request, user)
        return Response(serializer.data)


class GroupIndexAPIView(ListAPIView):  # cause of ListCreateAPIView we have get
    serializer_class = GroupIndexSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Group.objects.all()
        city = self.request.query_params.get('city')
        if city is not None:
            queryset = queryset.filter(city=city)

        return queryset

    def post(self, request):
        group = Group(
            name=request.data['name'],
            city=request.user.address_city,
            creator=request.user
        )
        group.save()
        serializer = GroupIndexSerializer(group)
        return Response(serializer.data)


class GroupDetailAPIView(GenericAPIView):
    serializer_class = GroupDetailSerializer

    def get(self, request, group_id): 
        group = find_or_404(Group, group_id)
        serializer = GroupDetailSerializer(group)
        return Response(serializer.data)
    
    def put(self, request, group_id):
        group = find_or_404(Group, group_id)
        if group.creator != request.user: #if the current user is not the creator of the group, they can not update it
            return Response({
                'success' : False,
                'message' : 'You are not the owner of the group'
            })

        group.name = request.data['name']
        group.save()
        serializer = GroupDetailSerializer(group)
        return Response({
            'success' : True,
            'group' : serializer.data
        })
    
    def delete(self, request, group_id):
        group = find_or_404(Group, group_id)
        if group.creator != request.user:
            return Response({
                'success': False,
                'message': 'You are not the owner of the group'
            })

        group.delete()
        return Response({'success' : True})


class PostIndexAPIView(GenericAPIView):
    serializer_class = PostIndexSerializer

    def get(self, request, group_id):
        group = find_or_404(Group, group_id)
        posts = group.posts.all() #one to many
        return paginate(request, posts, PostIndexSerializer)

    def post(self, request, group_id):
        group = find_or_404(Group, group_id)
        post = Post(
            title=request.data['title'],
            text=request.data['text'],
            user=request.user,
            group=group
        )
        post.save()
        serializer = PostIndexSerializer(post)
        return Response(serializer.data)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class MeetingIndexAPIView(GenericAPIView):
    serializer_class = MeetingIndexSerializer

    def get(self, request, group_id):
        group = find_or_404(Group, group_id)
        meetings = group.meetings.all() #one to many
        return paginate(request, meetings, MeetingIndexSerializer)

    def post(self, request, group_id):
        group = find_or_404(Group, group_id)

        meeting = Meeting(
            title=request.data['title'],
            time=request.data['time'],
            location=request.data['location'],
            group=group,
            creator=request.user
        )
        meeting.save()
        serializer = MeetingIndexSerializer(meeting)
        return Response(serializer.data)


class MeetingDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingDetailSerializer


class MeetingAttendAPIView(GenericAPIView):
    serializer_class = MeetingDetailSerializer

    def post(self, request, meeting_id):
        meeting = find_or_404(Meeting, meeting_id)
        already_attending = meeting.attendees.filter(id=request.user.id).first()

        if already_attending:
            return Response({
                'success': False,
                'message': 'You are already attending this meeting'
            })
        
        meeting.attendees.add(request.user)
        meeting.save()
        serializer = MeetingDetailSerializer(meeting)
        return Response(serializer.data)


class MeetingUnattendAPIView(GenericAPIView):
    serializer_class = MeetingDetailSerializer

    def post(self, request, meeting_id):
        meeting = find_or_404(Meeting, meeting_id)
        already_attending = meeting.attendees.filter(id=request.user.id).first()

        if not already_attending:
            return Response({
                'success': False,
                'message': 'You are already not attending this meeting'
            })
        
        meeting.attendees.remove(request.user)
        meeting.save()
        serializer = MeetingDetailSerializer(meeting)
        return Response(serializer.data)


class CommentIndexAPIView(GenericAPIView):
    serializer_class = CommentIndexSerializer

    def get(self, request, post_id):
        post = find_or_404(Post, post_id)
        comments = post.comments.all() #one to many
        return paginate(request, comments, CommentIndexSerializer)

    def post(self, request, post_id):
        post = find_or_404(Post, post_id)

        comment = Comment(
            text=request.data['text'],
            rating=request.data['rating'],
            post=post,
            user=request.user
        )
        comment.save()
        serializer = CommentIndexSerializer(comment)
        return Response(serializer.data)
    

class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer


class AnimalIndexAPIView(GenericAPIView):
    serializer_class = AnimalIndexSerializer

    def get(self, request, user_id):
        user = find_or_404(User, user_id)
        animals = user.animals.all() #one to many
        return paginate(request, animals, AnimalIndexSerializer)


class AnimalCreateAPIView(GenericAPIView):
    serializer_class = AnimalDetailSerializer

    def post(self, request):
        animal = Animal(
            name=request.data['name'],
            type=request.data['type'],
            breed=request.data['breed'],
            user=request.user
        )
        animal.save()
        serializer = AnimalDetailSerializer(animal)
        return Response(serializer.data)
    

class AnimalDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalDetailSerializer
from rest_framework import serializers

from .models import User, Meeting, Group, Post, Comment, Animal


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name'
        )


class GroupNestedSerializer(serializers.ModelSerializer):
    creator = UserNestedSerializer(read_only=True)
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'creator',
            'city'
        )


class MeetingNestedSerializer(serializers.ModelSerializer):
    creator = UserNestedSerializer(read_only=True)

    class Meta:
        model = Meeting
        fields = (
            'id',
            'title',
            'location',
            'time',
            'creator'
        )


class PostNestedSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'user'
        )


class CommentNestedSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'rating',
            'user'
        )


class AnimalNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = (
            'id',
            'name',
            'breed',
            'type'
        )


class UserIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 
            'id',
            'email',
            'first_name', 
            'last_name'
        )


class UserDetailSerializer(serializers.ModelSerializer):
    animals = AnimalNestedSerializer(many=True, read_only=True)
    created_groups = GroupNestedSerializer(many=True, read_only=True)
    attending_meetings = MeetingNestedSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'address_street',
            'address_city',
            'address_country',
            'phone_number',
            'bio',
            'created_at',
            'updated_at',
            'animals',
            'created_groups',
            'attending_meetings'
        )


class GroupIndexSerializer(serializers.ModelSerializer):
    creator = UserNestedSerializer(read_only=True)

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'creator',
            'city'
        )


class GroupDetailSerializer(serializers.ModelSerializer):
    creator = UserNestedSerializer(read_only=True)
    posts = PostNestedSerializer(many=True, read_only=True)
    meetings = MeetingNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'


class MeetingIndexSerializer(serializers.ModelSerializer):
    creator = UserNestedSerializer(read_only=True)

    class Meta:
        model = Meeting
        fields = (
            'title',
            'time',
            'location',
            'creator'
        )


class MeetingDetailSerializer(serializers.ModelSerializer):
    creator = UserNestedSerializer(read_only=True)
    attendees = UserNestedSerializer(many=True, read_only=True)
    group = GroupNestedSerializer(read_only=True)

    class Meta:
        model = Meeting
        fields = '__all__'


class PostIndexSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'text',
            'user'
        )


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)
    group = GroupNestedSerializer(read_only=True)
    comments = CommentNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class CommentIndexSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'rating',
            'user'
        )


class CommentDetailSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)
    group = GroupNestedSerializer(read_only=True)
    post = PostNestedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class AnimalIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = (
            'id',
            'name',
            'breed',
            'type'
        )


class AnimalDetailSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)

    class Meta:
        model = Animal
        fields = '__all__'
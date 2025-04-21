from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self , username , email , password=None,**extra_fields):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    

class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_initiated')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_received')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        unique_together = (('user', 'friend'),)

    def __str__(self):
        return f"{self.user.username} have friendship with {self.friend.username}"
    
    def save(self, *args, **kwargs):
        if self.user == self.friend:
            raise ValueError("User cannot be friends with themselves.")

        if not Friendship.objects.filter(user=self.friend, friend=self.user).exists():
            super().save(*args, **kwargs)
            Friendship.objects.create(user=self.friend, friend=self.user)
        else:
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        Friendship.objects.filter(user=self.friend, friend=self.user).delete()
        super().delete(*args, **kwargs)


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True) 
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id} between {', '.join(user.username for user in self.participants.all())}"

    class Meta:
        ordering = ['-created_at']

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content} ({self.timestamp})"

    class Meta:
        ordering = ['timestamp']
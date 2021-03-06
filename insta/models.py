from pickle import TRUE
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import uuid

from django.db.models.signals import post_save
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name_plural='Tags'
    

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug= slugify(self.title)
        return super().save(*args, **kwargs)

class Post(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture=models.ImageField(upload_to=user_directory_path, verbose_name='Picture', null=False)
    caption=models.TextField(max_length=300, verbose_name='Caption')
    posted = models.DateTimeField(auto_now_add=True)
    tags=models.ManyToManyField(Tag,related_name='tags')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)


    def __str__(self):
        return self.caption

    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()
    
    def update_post(self):
        self.new_caption.save()

    def get_absolute_url(self):
        return reverse('postdetails', args=[self.id])

class Follow (models.Model):
    follower=models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following=models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

class Stream(models.Model):
    following=models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    date=models.DateTimeField()

    def add_post(sender,instance,*args, **kwargs):
        post=instance
        user=post.user
        followers=Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date = post.posted, following=user)
            stream.save()

class Likes (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')


post_save.connect(Stream.add_post, sender=Post)

       
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(default='default.png', upload_to='profile_pics')
    bio = models.TextField()

        
    def __str__(self):
        return f'{self.user.username} Profile'
        

    def delete_profile(self):
        self.delete()
    
    def update_profile(self):
        self.new_username.save()


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
        img = Image.open(self.profile_photo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_photo.path)   


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.TextField()
	date = models.DateTimeField(auto_now_add=True)



    

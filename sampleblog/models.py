from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid
# Create your models here.

class Category(models.Model):
     categories = (
     ('Economics', 'Economics'),
     ('Finance', 'Finance'),
     ('Pet', 'Pet'),
     ('Gaming', 'Gaming'),
     ('Nature', 'Nature'),
     ('Medical', 'Medical'),
     ('Social Media', 'Social Media'),
     ('Sports', 'Sports'),
     ('Science', 'Science'),
     ('Technology', 'Technology'),
     ('History', 'History'),
     ('Travel', 'Travel'),
     ('Fashion', 'Fashion'),
     ('Music', 'Music'),
     ('Movie', 'Movie'),
     ('Education', 'Education'),
     ('Health', 'Health'),
     )
     category = models.CharField(max_length=50,choices=categories,)
     slug = models.SlugField()
     def __str__(self):
             return self.category

     def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(Category, self).save(*args, **kwargs)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    likes = models.IntegerField(null=True,blank=True,default = 0)
    dislikes = models.IntegerField(null=True,blank=True,default = 0)
    title = models.CharField(max_length=200,unique=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField()
    published_date = models.DateTimeField(blank=True, null=True)
    # # category = models.CharField(max_length=50)
    #
    # def publish(self):
    #     self.published_date = timezone.now()
    #     self.save()

    def __str__(self):
            return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.title = self.title.title()
        super(Post, self).save(*args, **kwargs)

    def current_comments_count(self):
        return Comment.objects.filter(post = self).count()


class Comment(models.Model):
   post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments', )
   user = models.ForeignKey(User,on_delete=models.CASCADE,)
   parent = models.ForeignKey('self', null=True,blank=True)
   likes = models.IntegerField(null=True,blank=True,default = 0)
   dislikes = models.IntegerField(null=True,blank=True,default = 0)
   text = models.TextField()
   created_date = models.DateTimeField(default=timezone.now,)
   slug = models.SlugField()
   comment_id = models.UUIDField(default=uuid.uuid4, editable=False)
   # approved_comment = models.BooleanField(default=False, )
   #
   # def approve(self):
   #     self.approved_comment = True
   #     self.save()

   def __str__(self):
       return self.text


   def save(self, *args, **kwargs):
       self.slug = slugify(self.comment_id)
       super(Comment, self).save(*args, **kwargs)

   def replies(self):
       return Comment.objects.filter(parent = self).order_by('-created_date')

   def latest_two_replies(self):
       return Comment.objects.filter(parent = self).order_by('-created_date')[:2]

   def current_replies_count(self):
       return Comment.objects.filter(parent = self).count()

class Profile(models.Model):

   user = models.OneToOneField(User,on_delete=models.CASCADE,)
   first_name = models.CharField(max_length=200,)
   last_name = models.CharField(max_length=200,)
   text = models.TextField()
   avatar = models.ImageField() # or whatever
   created_date = models.DateTimeField(default=timezone.now)


   def __str__(self):
       return self.text

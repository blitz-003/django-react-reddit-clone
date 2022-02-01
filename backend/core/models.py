from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.

class Category(models.Model):
    id = models.TextField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    id = models.TextField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    num_upvotes = models.IntegerField(default=0)
    num_downvotes = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.id

    @property
    def username(self):
        return self.user.username

    @property
    def category_name(self):
        return self.category.name

class Comment(models.Model):
    id = models.TextField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # We do nothing when parent post gets deleted because we still want to see the comment replies.
    parent_post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)

    content = models.CharField(max_length=1000)
    num_upvotes = models.IntegerField(default=0)
    num_downvotes = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)

    # Note, this will be null for comments that do not have parents i.e. top level comments.
    parent_comment = models.ForeignKey("self", on_delete=models.DO_NOTHING, related_name="replies", blank=True, null=True)

    def __str__(self):
        return self.id

    @property
    def username(self):
        return self.user.username

    # TODO: Add constraint to make sure that parent post of comment reply samea as parent comment.

class PostVotes(models.Model):
    id = models.TextField(primary_key=True)

    # We do not want to lose votes of users that delete their accounts.
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="vote_once_constraint"),
            models.CheckConstraint(check= (~Q(upvote=True) | ~Q(downvote=True)),
            name="cant_upvote_and_downvote")
        ]
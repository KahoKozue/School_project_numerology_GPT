from django.db import models
from django.contrib.auth.models import User




class book(models.Model):
    bookname = models.CharField(max_length=20,verbose_name="書名")
    bookID = models.CharField(max_length=20, unique=True, default='bookID',verbose_name="編號")
    author = models.CharField(max_length=10, default='author',verbose_name="作者")

    def __str__(self):
        return self.bookname
    
    class Meta:
        ordering = ("bookname",)   
        verbose_name_plural = "書籍"

class chapter(models.Model):#
    chapterID = models.CharField(max_length=20, unique=True,verbose_name="章節編號")
    title = models.CharField(max_length=50,verbose_name="章節名稱")
    content = models.TextField(default='content',null=False,verbose_name="內文")
    book = models.ForeignKey(book, on_delete=models.CASCADE)#定義了一個外鍵
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ("title",)   
        verbose_name_plural = "章節名稱"
    
class Chatroom2(models.Model):
    name = models.CharField(max_length=100,default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_chatrooms')

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Conversation_history')
    chatroom = models.ForeignKey(Chatroom2, on_delete=models.CASCADE)
    user_question = models.TextField()
    ai_answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='birthday')
    birthday = models.DateField(default='2000-01-01')
    birthday_time = models.TimeField(default='00:00')
    sex = models.CharField(max_length=1, null=False, blank=False)

class Daily(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    health = models.TextField(null=True, blank=True)
    love = models.TextField(null=True, blank=True)
    work = models.TextField(null=True, blank=True)
    finance = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Yearly(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    january = models.TextField(null=True, blank=True)
    february = models.TextField(null=True, blank=True)
    march = models.TextField(null=True, blank=True)
    april = models.TextField(null=True, blank=True)
    may = models.TextField(null=True, blank=True)
    june = models.TextField(null=True, blank=True)
    july = models.TextField(null=True, blank=True)
    august = models.TextField(null=True, blank=True)
    september = models.TextField(null=True, blank=True)
    october = models.TextField(null=True, blank=True)
    november = models.TextField(null=True, blank=True)
    december = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'year')
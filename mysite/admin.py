from django.contrib import admin

from mysite.models import book
from mysite.models import chapter

from mysite.models import Chatroom2,Conversation,Daily,Yearly
from mysite.models import Customer

# Register your models here.
 
class bookAdmin(admin.ModelAdmin):
  list_display=('id','bookname','bookID','author',)#指定欄位
  list_filter=('author',)#過濾器
  search_fields=('bookname','author',)#搜尋欄位s
  ordering=('-id',)#排序
 
class chapterAdmin(admin.ModelAdmin):
  list_display=('id','chapterID','title','content','book',)#指定欄位
  list_filter=('title',)#過濾器
  search_fields=('chapterID','title',)#搜尋欄位s
  list_per_page = 5
  ordering=('-id',)#排序
 



#測試內聯
# 定義內聯模型 (Inline model)，這個模型將用於在書籍詳細信息頁面上直接管理章節
class ChapterInline(admin.TabularInline):
  model = chapter  # 設定內聯模型的目標為 Chapter 模型
  extra = 1  # 定義額外的空白章節表單，這允許在一次編輯中添加多個章節
  ordering=('chapterID',)#排序


# 定義書籍管理類別，這將用於後台管理
class BookAdmin(admin.ModelAdmin):
  inlines = [ChapterInline]  # 將章節內聯模型添加到書籍管理中，以便在書籍詳細信息頁面上管理章節




# 註冊 Book 模型和 BookAdmin 管理類別
admin.site.register(book, BookAdmin)
#admin.site.register(book,bookAdmin)
admin.site.register(chapter,chapterAdmin)
admin.site.register(Chatroom2)
admin.site.register(Conversation)
admin.site.register(Customer)
admin.site.register(Daily)
admin.site.register(Yearly)
from django.contrib import admin
from .models import RegisteredUser,Post,Comment,CommentLike 


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    exclude = ('author',) 
    fields = ('title', 'content', 'image', 'is_published')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        if not change or not obj.author:
            obj.author = request.user  
        obj.save()

admin.site.register(Post, PostAdmin)
admin.site.register(RegisteredUser)
admin.site.register(Comment)
admin.site.register(CommentLike)




from django.contrib import admin

from .models import Question,Choice,Category,Post,Comentario,videos,userProfile

class QuestionAdmin(admin.ModelAdmin):
	fields=['pud_date','question_text']

admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comentario)
admin.site.register(videos)
admin.site.register(userProfile)




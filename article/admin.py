from django.contrib import admin
from .models import ArticleColumn, ArticlePost
from .models import Question,  Answer

# Register your models here.


class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('column', 'created', )
    list_filter = ("column", 'created', )


admin.site.register(ArticleColumn, ArticleColumnAdmin)


class ArticlePostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'column', 'created', 'updated', 'voteanonymousornot')
    list_filter = ('author__username', 'title', 'column', 'article_tag', 'created', 'updated', 'users_like__username')
    search_fields = ['author__username', 'title',   'body', ]
    readonly_fields = ['author', 'created', 'updated', ]


admin.site.register(ArticlePost, ArticlePostAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'required', 'question_type', 'choices', 'survey')


admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'survey', 'interviewer', 'interviewee', 'created', 'updated')
    readonly_fields = ('question', 'answer', 'survey', 'interviewer', 'interviewee', 'created', 'updated')
    extra = 0


admin.site.register(Answer, AnswerAdmin)


from .models import ArticleProcessFlow, ProcessStateRecord


class ArticleProcessFlowAdmin(admin.ModelAdmin):
    list_display = [
        "applicant", "article", "approved", "application_time",
                    ]


admin.site.register(ArticleProcessFlow, ArticleProcessFlowAdmin)


class ProcessStateRecordAdmin(admin.ModelAdmin):
    list_display = [
        "process",  "this_step_user", "this_step_state", "this_step_handle", "this_step_opinion", "this_step_time",
                    ]


admin.site.register(ProcessStateRecord, ProcessStateRecordAdmin)


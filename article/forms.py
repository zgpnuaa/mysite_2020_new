from django import forms
from .models import ArticleColumn, ArticlePost, Comment, ArticleTag, CommentMulti, ArticleProcessFlow, ProcessStateRecord
from.models import Question, Answer


class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ("column",)


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ("title", "body", "voteanonymousornot", "usercanvote", "votedeadline", "approved")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("commentator", "body",)


class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ('tag',)


class CommentMultiForm(forms.ModelForm):
    class Meta:
        model = CommentMulti
        fields = ("comment_content", )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'required', 'question_type', 'choices', 'survey')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('question', 'answer', 'survey', 'interviewer', 'interviewee')


class ArticleProcessFlowForm(forms.ModelForm):
    class Meta:
        model = ArticleProcessFlow
        fields = '__all__'


class ProcessStateRecordForm(forms.ModelForm):
    class Meta:
        model = ProcessStateRecord
        fields = '__all__'


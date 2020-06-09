from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from slugify import slugify
from django.core.exceptions import ValidationError


# Create your models here.


class ArticleColumn(models.Model):
    user = models.ForeignKey(User, related_name='article_column', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='栏目作者')
    column = models.CharField('栏目名称', max_length=200)
    created = models.DateField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '栏目信息'
        verbose_name_plural = '栏目信息'

    def __str__(self):
        return self.column


class ArticleTag(models.Model):
    author = models.ForeignKey(User, related_name="tag", blank=True, null=True, on_delete=models.SET_NULL, verbose_name='标签作者')
    tag = models.CharField(max_length=500)

    def __str__(self):
        return self.tag
# default=datetime.datetime.now() + datetime.timedelta(days=15))
import datetime
class ArticlePost(models.Model):
    author = models.ForeignKey(User, related_name="article", blank=True, null=True, on_delete=models.SET_NULL, verbose_name='作者')
    title = models.CharField('题目', max_length=200)
    slug = models.SlugField(max_length=500)
    # on_delete=models.CASCADE ： 主外关系键中，级联删除，也就是当删除主表的数据时候从表中的数据也随着一起删除
    # on_delete=models.PROTECT : 保护模式，如果采用该选项，删除的时候，会抛出ProtectedError错误
    # on_delete=models.SET_NULL : 置空模式，删除的时候，外键字段被设置为空，前提就是blank=True, null=True,定义该字段的时候，允许为空
    # on_delete=models.SET_DEFAULT: 置默认值，删除的时候，外键字段设置为默认值，所以定义外键的时候注意加上一个默认值
    # on_delete=models.SET(): 自定义一个值，该值当然只能是对应的实体了
    # column = models.ForeignKey(ArticleColumn, related_name="article_column", on_delete=models.CASCADE)
    column = models.ForeignKey(ArticleColumn, related_name="article_column", blank=True, null=True, on_delete=models.SET_NULL, verbose_name='栏目')
    body = models.TextField('内容')
    created = models.DateTimeField('发布时间', default=timezone.now)
    updated = models.DateTimeField('更新时间', auto_now=True)
    users_like = models.ManyToManyField(User, related_name="articles_like", blank=True, verbose_name='点赞用户')
    article_tag = models.ManyToManyField(ArticleTag, related_name='article_tag', blank=True, verbose_name='标签')
    voteanonymousornot = models.BooleanField(blank=True, verbose_name="投票/问卷是否匿名制", default=True)
    usercanvote = models.ManyToManyField(User, related_name="user_canvote", blank=True, verbose_name='问卷/投票范围')
    userhasvoted = models.ManyToManyField(User, related_name="user_hasvoted", blank=True, verbose_name='已投票')
    votedeadline = models.DateTimeField(verbose_name='问卷投票截止时间', blank=True,  default=timezone.now)
    approved = models.BooleanField(default=False)
    state = models.CharField('当前状态', max_length=200, default="草稿")

    class Meta:
        ordering = ("-updated",)
        index_together = (('id', 'slug'),)
        verbose_name = '文章信息'
        verbose_name_plural = '文章信息'

    def __str__(self):
        return self.title

    def save(self, *args, **kargs):
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kargs)

    def get_absolute_url(self):
        return reverse("article:article_detail", args=[self.id, self.slug])

    def get_url_path(self):
        return reverse("article:list_article_detail", args=[self.id, self.slug])

    def questions(self):
        if self.pk:
            return Question.objects.filter(survey=self.pk)
        else:
            return None


class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, related_name="comments", blank=True, null=True, on_delete=models.SET_NULL)
    commentator = models.CharField(max_length=90)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator, self.article)


class CommentMulti(models.Model):
    comment_article = models.ForeignKey(ArticlePost,  related_name="comment_article", blank=True, null=True, on_delete=models.SET_NULL)
    comment_user = models.ForeignKey(User, related_name="commentmulti_user", on_delete=models.CASCADE, null="true",)
    comment_like = models.ManyToManyField(User, related_name="commentmulti_like", blank=True)
    comment_time = models.DateTimeField(default=timezone.now)
    comment_content = models.TextField(null="true",)
    comment_parent_id = models.CharField(max_length=300, null="true",)


def validate_list(value):
    """takes a text value and verifies that there is at least one comma"""
    values = value.split(',')
    if len(values) < 2:
        raise ValidationError("The selected field requires an associated list of choices. Choices must contain more than one item.")


class Question(models.Model):
    TEXT = 'text'
    RADIO = 'radio'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select-multiple'
    INTEGER = 'integer'
    FLOAT = 'float'

    QUESTION_TYPES = (
        (TEXT, '文本'),
        (RADIO, '单选按钮'),
        (SELECT, '单选下拉列表'),
        (SELECT_MULTIPLE, '多选框'),
        (INTEGER, '整数'),
        (FLOAT, '实数')
    )

    text = models.TextField(verbose_name='问题')
    required = models.BooleanField(verbose_name='是否必填')
    survey = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, null=True,  blank=True, verbose_name='关联文章')
    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT, verbose_name='问题类型')
    # the choices field is only used if the question type
    choices = models.TextField(blank=True, null=True,
        help_text='如果问题类型为单选按钮、单选下拉列表或多选框，请提供用英文逗号分隔的问题选项！', verbose_name='问题选项')

    class Meta:
        verbose_name = '投票问卷题目'
        verbose_name_plural = '投票问卷题目'

    def save(self, *args, **kwargs):
        if (self.question_type == Question.RADIO or self.question_type == Question.SELECT or self.question_type == Question.SELECT_MULTIPLE):
            validate_list(self.choices)
        super(Question, self).save(*args, **kwargs)

    def get_choices(self):
        ''' parse the choices field and return a tuple formatted appropriately
        for the 'choices' argument of a form widget.'''
        choices = self.choices.split(',')
        choices_list = []
        for c in choices:
            c = c.strip()
            choices_list.append(c)
        choices_tuple = tuple(choices_list)
        return choices_tuple

    def __unicode__(self):
        return (self.text)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,  null=True,  blank=True)
    answer = models.TextField(blank=True, null=True)
    survey = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, null=True, blank=True)
    interviewer = models.ForeignKey(User, related_name="interviewer", blank=True, null=True, on_delete=models.SET_NULL,
                                    verbose_name='邀请者')
    interviewee = models.ForeignKey(User, related_name="interviewee", blank=True, null=True, on_delete=models.SET_NULL,
                                    verbose_name='被邀请者')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '投票问卷结果'
        verbose_name_plural = '投票问卷结果'



class ArticleProcessFlow(models.Model):
    applicant = models.ForeignKey(User, related_name="applicant", blank=False, null=True, on_delete=models.SET_NULL,
                              verbose_name='申请人')
    approvers = models.ManyToManyField(User, related_name="approver", blank=False,  verbose_name='审批人')
    article = models.ForeignKey(ArticlePost, related_name="approvearticle",  blank=False, null=True, on_delete=models.CASCADE,
                              verbose_name='审批文章')
    application_time = models.DateTimeField(verbose_name='发起时间', default=timezone.now)
    approved = models.BooleanField(verbose_name='是否批准', default=False)

    class Meta:
        verbose_name = '审批流程'
        verbose_name_plural = '审批流程'

    def approve_article(self):
        self.article.approved = True
        self.article.save(update_fields=['approved'])


class ProcessStateRecord(models.Model):
    process = models.ForeignKey(ArticleProcessFlow, related_name="state_process", blank=False, null=True, on_delete=models.CASCADE, verbose_name='流程')
    this_step_user = models.ForeignKey(User, related_name="this_step_user", blank=False, null=True, on_delete=models.CASCADE,
                              verbose_name='当前处理人')
    next_step_user = models.ManyToManyField(User, default="", related_name="next_step_user",   blank=False,
                              verbose_name='下一步处理人')
    this_step_handle = models.IntegerField(verbose_name='当前处理', default=0, help_text="0：草稿制作；1：发起审批；2：同意；3：驳回；4：撤回；5：删除")
    this_step_state = models.IntegerField(verbose_name='当前状态', default=0, help_text="0：草稿；1：审批中；2：已发布；3：被驳回；4：已撤回；5：已删除")
    this_step_opinion = models.TextField(verbose_name='处理意见', default="")
    this_step_time = models.DateTimeField(verbose_name='处理时间', auto_now=True)

    class Meta:
        verbose_name = '审批记录'
        verbose_name_plural = '审批记录'


















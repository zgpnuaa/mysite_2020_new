from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ArticlePost, CommentMulti, ArticleColumn, ArticleTag, Question, Answer
from .forms import CommentForm, CommentMultiForm, AnswerForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
import redis
from django.conf import settings
from django.db.models import Count
import collections
import json
from account.models import UserInfo
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import Iterable
from django.db.models.query import QuerySet
from notifications.signals import notify


r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def column_filter(request, column_filter=None):
    if column_filter:
        column_obj = ArticleColumn.objects.filter(column__contains=column_filter)
        articles_title = ArticlePost.objects.filter(column__in=[col for col in column_obj]).filter(approved=True)
        articles_count = articles_title.count()
    else:
        articles_title = ArticlePost.objects.all()

    all_views = {}
    all_comments = {}
    for article in articles_title:
        comment_list1 = list(CommentMulti.objects.values().filter(comment_article=article))
        all_comments[article] = len(comment_list1)
        if r.get("article:{}:views".format(article.id)):
            total_views = int(r.get("article:{}:views".format(article.id)))
        else:
            total_views = 0
        all_views[article] = total_views
    paginator = Paginator(articles_title, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))

    user_request = request.user
    print(column_filter)
    if column_filter:
        return render(request, "article/list/column_articles.html",  {"articles": articles, "page": current_page,"all_views": all_views, "all_comments": all_comments, "column_filter": column_filter, "articles_count": articles_count, "user_request": user_request})
    return render(request, "article/list/article_titles.html",
                  {"articles": articles, "page": current_page, "all_views": all_views, "all_comments": all_comments,
                   "most_viewed": most_viewed})


def tag_filter(request, tag_filter=None):
    if tag_filter:
        print(tag_filter)
        print(ArticleTag.objects.get(tag__contains=tag_filter))
        tag_obj = ArticleTag.objects.get(tag__contains=tag_filter)
        print(tag_obj)
        articles_title = ArticlePost.objects.filter(article_tag=tag_obj).filter(approved=True)
        articles_count = articles_title.count()
    else:
        articles_title = ArticlePost.objects.all()

    all_views = {}
    all_comments = {}
    for article in articles_title:
        comment_list1 = list(CommentMulti.objects.values().filter(comment_article=article))
        all_comments[article] = len(comment_list1)
        if r.get("article:{}:views".format(article.id)):
            total_views = int(r.get("article:{}:views".format(article.id)))
        else:
            total_views = 0
        all_views[article] = total_views
    paginator = Paginator(articles_title, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))

    user_request = request.user

    if column_filter:
        return render(request, "article/list/tag_articles.html",
                      {"articles": articles, "page": current_page,
                       "all_views": all_views, "all_comments": all_comments, "tag_filter": tag_filter, "articles_count": articles_count, "user_request": user_request})
    return render(request, "article/list/article_titles.html",
                  {"articles": articles, "page": current_page, "all_views": all_views, "all_comments": all_comments,
                   "most_viewed": most_viewed})


def article_titles(request, username=None):
    num_views = {}
    if username:
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user).filter(approved=True)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        articles_title = ArticlePost.objects.filter(approved=True)
    all_views = {}
    all_comments = {}
    for article in articles_title:
        comment_list1 = list(CommentMulti.objects.values().filter(comment_article=article))
        all_comments[article] = len(comment_list1)
        if r.get("article:{}:views".format(article.id)):
            total_views = int(r.get("article:{}:views".format(article.id)))
        else:
            total_views = 0
        all_views[article] = total_views
    paginator = Paginator(articles_title, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list

    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))

    user_request = request.user

    if username:
        return render(request, "article/list/author_articles.html", {"articles": articles, "page": current_page, "userinfo": userinfo, "user": user, "all_views": all_views, "all_comments": all_comments, "user_request": user_request, 'recipient': user.username})
    return render(request, "article/list/article_titles.html", {"articles": articles, "page": current_page, "all_views": all_views, "all_comments": all_comments, "most_viewed": most_viewed})


def tree_search(d_dic, comment_obj):
    for k, v_dic in d_dic.items():
        if k[0] == int(comment_obj[2]):
            d_dic[k][comment_obj] = collections.OrderedDict()
            return
        else:
            tree_search(d_dic[k], comment_obj)


comment_list = [
    (1, ('com1', 'com2', 'content', 'c_time', 'like'), None),
    (2, ('com1', 'com2', 'content', 'c_time', 'like'), None),
    (3, ('com1', 'com2', 'content', 'c_time', 'like'), None),
    (9, ('com1', 'com2', 'content', 'c_time', 'like'), 5),
    (4, ('com1', 'com2', 'content', 'c_time', 'like'), 2),
    (5, ('com1', 'com2', 'content', 'c_time', 'like'), 1),
    (6, ('com1', 'com2', 'content', 'c_time', 'like'), 4),
    (7, ('com1', 'com2', 'content', 'c_time', 'like'), 2),
    (8, ('com1', 'com2', 'content', 'c_time', 'like'), 4),
]

# list-> ordereddict
def build_tree(comment_list):
    comment_dic = collections.OrderedDict()

    for comment_obj in comment_list:
        if comment_obj[2] == "None":
            comment_dic[comment_obj] = collections.OrderedDict()
        else:
            tree_search(comment_dic, comment_obj)
    #print(comment_dic)
    return comment_dic


from ast import literal_eval
from django.contrib.auth.models import AnonymousUser
from wxtoken.wx_token import getSignPackage
import datetime
import pytz

@csrf_exempt
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    total_views = r.incr("article:{}:views".format(article.id))
    r.zincrby('article_ranking',  1, article.id)

    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
    print(article.votedeadline)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        commentmulti_form = CommentMultiForm()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
        if request.is_ajax():
            comment = json.loads(request.POST.get("comment"))
            new_commentmulti = commentmulti_form.save(commit=False)
            new_commentmulti.comment_article = article
            new_commentmulti.comment_parent_id = comment["comment_parent_id"]
            new_commentmulti.comment_content = comment["comment_content"]
            new_commentmulti.comment_user = request.user
            new_commentmulti.save()

            if comment['comment_parent_id'] == "None":
                parent_comment_user_obj = article.author
                notify.send(request.user, recipient=parent_comment_user_obj, verb='评论了你的文章', target=article, action_object=new_commentmulti)
            if comment['comment_parent_id'] != "None":
                parent_comment = list(CommentMulti.objects.values().filter(id=comment['comment_parent_id']))
                parent_comment_user_obj = User.objects.get(id=parent_comment[0]['comment_user_id'])
                notify.send(request.user, recipient=parent_comment_user_obj, verb='回复了你的评论', target=article,
                            action_object=new_commentmulti)
        return HttpResponse(json.dumps({"success": "1"}))
    else:
        comment_list1 = list(CommentMulti.objects.values().filter(comment_article=article))
        comment_lst = []
        for comment in comment_list1:
            comment_id = comment['id']
            comment_user = User.objects.get(id=comment['comment_user_id'])
            if comment['comment_parent_id'] == "None":
                parent_comment_user = None
                parent_comment_user_obj = None
            if comment['comment_parent_id'] != "None":
                parent_comment = list(CommentMulti.objects.values().filter(id=comment['comment_parent_id']))
                parent_comment_user = str(User.objects.get(id=parent_comment[0]['comment_user_id']))
                parent_comment_user_obj = User.objects.get(id=parent_comment[0]['comment_user_id'])
            comment_content = comment['comment_content']
            comment_time = int(round(time.mktime(comment['comment_time'].timetuple())*1000))
            comment_obj = CommentMulti.objects.get(id=comment_id)
            # count后记得加括号->count(),不加括号调用方法本身，带括号调用方法的返回值
            comment_like = int(comment_obj.comment_like.count())
            try:
                comment_user_info = UserInfo.objects.filter(user=comment_user)[0]
            except:
                comment_user_info = None
            print(comment_user_info)
            try:
                if comment_user_info.photo:
                    comment_user_photo = comment_user_info.photo.url
                    print(comment_user_photo)
                else:
                    comment_user_photo = ''
            except:
                comment_user_photo = ''
            try:
                parent_comment_user_info = UserInfo.objects.filter(user=parent_comment_user_obj)[0]
            except:
                parent_comment_user_info = None
            try:
                if parent_comment_user_info.photo:
                    parent_comment_user_photo = parent_comment_user_info.photo.url
                    print(parent_comment_user_photo)
                else:
                    parent_comment_user_photo = None
            except:
                parent_comment_user_photo = None
            comment_tup = (comment_id, (comment_user_photo, comment_user, parent_comment_user_photo, parent_comment_user, comment_content, comment_time, comment_like), comment['comment_parent_id'])
            comment_lst.append(comment_tup)

        comment_dic = build_tree(comment_lst)
        # 有序字典按父评论发表时间进行倒序排列，即最新发布的评论排在前面
        comment_dic_reverse = collections.OrderedDict(sorted(comment_dic.items(), key=lambda t: t[0][1][5], reverse=True))
        # 评论分页
        num_per = 5
        paginator = Paginator(list(comment_dic_reverse.items()), num_per)
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
            comment_dic_reverse_lst = current_page.object_list
            comment_dic_reverse_p = collections.OrderedDict()
            for sub_list in comment_dic_reverse_lst:
                comment_dic_reverse_p[sub_list[0]] = sub_list[1]

        except PageNotAnInteger:
            current_page = paginator.page(1)
            comment_dic_reverse_lst = current_page.object_list
            comment_dic_reverse_p = collections.OrderedDict()
            for sub_list in comment_dic_reverse_lst:
                comment_dic_reverse_p[sub_list[0]] = sub_list[1]
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)
            comment_dic_reverse_lst = current_page.object_list
            comment_dic_reverse_p = collections.OrderedDict()
            for sub_list in comment_dic_reverse_lst:
                comment_dic_reverse_p[sub_list[0]] = sub_list[1]

        comment_form = CommentForm()

        article_tags_ids = article.article_tag.values_list("id", flat=True)
        similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
        similar_articles = similar_articles.annotate(same_tags=Count("article_tag")).order_by('-same_tags', '-created')[:4]
        survey = []
        data = []
        questions = Question.objects.filter(survey=article)
        dt = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
        print(dt)
        print(article.votedeadline)
        expire = False
        if dt > article.votedeadline:
            expire = True
        else:
            expire = False
        if isinstance(request.user, AnonymousUser):
            print("游客")
            canvote = False
            hasvoted = False
            anonymoususer = True
        else:
            anonymoususer = False
            canvote = True
            if article.voteanonymousornot == False:
                answers = Answer.objects.filter(survey=article).filter(interviewee=request.user)
            else:
                answers = Answer.objects.filter(survey=article)
            print("mmmmmmm")
            print(answers)
            print(expire)
            hasvoted = True
            if request.user in article.userhasvoted.all():
                hasvoted = True
                print("777")
            else:
                hasvoted = False
                print("666")
            if hasvoted == True or expire == True:
                print("answers is:")
                print(answers)
                for question in questions:
                    survey.append([question.text, question.question_type, question.choices, question.required])
                    answer = Answer.objects.filter(question=question).filter(interviewee=request.user)
                    if (question.question_type == "radio"):
                        choices = question.get_choices()
                        print(choices)
                        num_choices = len(choices)
                        num_vote = []
                        ratio_vote = []
                        sum_vote = 0
                        for option in range(num_choices):
                            print(option)
                            num_temp = len(Answer.objects.filter(question=question).filter(answer=option))
                            num_vote.append(num_temp)
                            print(Answer.objects.filter(question=question).filter(answer=option))
                            sum_vote += num_temp
                        print('vote:')
                        print(num_vote)

                        for temp in num_vote:
                            if sum_vote > 0:
                                ratio_vote.append(round(temp / sum_vote * 100, 2))
                            else:
                                ratio_vote.append(0)
                        print(ratio_vote)
                        if answer.count() > 0:
                            response = (num_vote, ratio_vote, answer[0].answer)
                        else:
                            response = (num_vote, ratio_vote, -1)
                        print(response)
                        data.append(response)
                    elif (question.question_type == "select-multiple"):
                        choices = question.get_choices()
                        print(choices)
                        num_choices = len(choices)
                        num_vote = [0] * num_choices
                        ratio_vote = []
                        sum_vote = 0
                        for answer_obj in Answer.objects.filter(question=question):
                            for select in literal_eval(answer_obj.answer):
                                print(literal_eval(answer_obj.answer))
                                for option in range(num_choices):
                                    if select == option:
                                        num_vote[option] += 1
                        for temp in num_vote:
                            sum_vote += temp
                        print('vote:')
                        print(num_vote)

                        for temp in num_vote:
                            if sum_vote > 0:
                                ratio_vote.append(round(temp / sum_vote * 100, 2))
                            else:
                                ratio_vote.append(0)
                        print(ratio_vote)
                        if answer.count() > 0:
                            response = (num_vote, ratio_vote, literal_eval(answer[0].answer))
                        else:
                            response = (num_vote, ratio_vote, -1)
                        print(response)
                        data.append(response)
                    elif (question.question_type == "select"):
                        choices = question.get_choices()
                        print(choices)
                        num_choices = len(choices)
                        num_vote = []
                        ratio_vote = []
                        sum_vote = 0
                        for option in range(num_choices):
                            print(option)
                            num_temp = len(Answer.objects.filter(question=question).filter(answer=option))
                            num_vote.append(num_temp)
                            print(Answer.objects.filter(question=question).filter(answer=option))
                            sum_vote += num_temp
                        print('vote:')
                        print(num_vote)

                        for temp in num_vote:
                            if sum_vote > 0:
                                ratio_vote.append(round(temp / sum_vote * 100, 2))
                            else:
                                ratio_vote.append(0)
                        print(ratio_vote)
                        if answer.count() > 0:
                            response = (num_vote, ratio_vote, answer[0].answer)
                        else:
                            response = (num_vote, ratio_vote, -1)
                        print(response)
                        data.append(response)
                    elif (question.question_type == "integer"):
                        choices = question.choices
                        print(choices)
                        if answer.count() > 0:
                            response = (answer[0].answer)
                        else:
                            response = ''
                        print(response)
                        data.append(response)
                    elif (question.question_type == "real"):
                        choices = question.choices
                        print(choices)
                        if answer.count() > 0:
                            response = (answer[0].answer)
                        else:
                            response = ''
                        print(response)
                        data.append(response)
                    elif (question.question_type == "textarea"):
                        choices = question.choices
                        print(choices)
                        if answer.count() > 0:
                            response = (answer[0].answer)
                        else:
                            response = ''
                        print(response)
                        data.append(response)
                print(data)
            else:
                print(questions)
                print(article.usercanvote.all())
                print(request.user in article.usercanvote.all())
                if request.user in article.usercanvote.all():
                    canvote = True
                    print("nnnnnnnn")
                    for question in questions:
                        survey.append([question.text, question.question_type, question.choices, question.required])
                else:
                    canvote = False
                    print("answers is:")
                    print(answers)
                    for question in questions:
                        survey.append([question.text, question.question_type, question.choices, question.required])
                        answer = Answer.objects.filter(question=question).filter(interviewee=request.user)
                        if (question.question_type == "radio"):
                            choices = question.get_choices()
                            print(choices)
                            num_choices = len(choices)
                            num_vote = []
                            ratio_vote = []
                            sum_vote = 0
                            for option in range(num_choices):
                                print(option)
                                num_temp = len(Answer.objects.filter(question=question).filter(answer=option))
                                num_vote.append(num_temp)
                                print(Answer.objects.filter(question=question).filter(answer=option))
                                sum_vote += num_temp
                            print('vote:')
                            print(num_vote)
                            for temp in num_vote:
                                if sum_vote > 0:
                                    ratio_vote.append(round(temp / sum_vote * 100, 2))
                                else:
                                    ratio_vote.append(0)
                            print(ratio_vote)
                            if answer.count() > 0:
                                response = (num_vote, ratio_vote, answer[0].answer)
                            else:
                                response = (num_vote, ratio_vote, -1)
                            print(response)
                            data.append(response)
                        elif (question.question_type == "select-multiple"):
                            choices = question.get_choices()
                            print(choices)
                            num_choices = len(choices)
                            num_vote = [0] * num_choices
                            ratio_vote = []
                            sum_vote = 0
                            for answer_obj in Answer.objects.filter(question=question):
                                for select in literal_eval(answer_obj.answer):
                                    print(literal_eval(answer_obj.answer))
                                    for option in range(num_choices):
                                        if select == option:
                                            num_vote[option] += 1
                            for temp in num_vote:
                                sum_vote += temp
                            print('vote:')
                            print(num_vote)

                            for temp in num_vote:
                                if sum_vote > 0:
                                    ratio_vote.append(round(temp / sum_vote * 100, 2))
                                else:
                                    ratio_vote.append(0)
                            print(ratio_vote)
                            if answer.count() > 0:
                                response = (num_vote, ratio_vote, literal_eval(answer[0].answer))
                            else:
                                response = (num_vote, ratio_vote, -1)
                            print(response)
                            data.append(response)
                        elif (question.question_type == "select"):
                            choices = question.get_choices()
                            print(choices)
                            num_choices = len(choices)
                            num_vote = []
                            ratio_vote = []
                            sum_vote = 0
                            for option in range(num_choices):
                                print(option)
                                num_temp = len(Answer.objects.filter(question=question).filter(answer=option))
                                num_vote.append(num_temp)
                                print(Answer.objects.filter(question=question).filter(answer=option))
                                sum_vote += num_temp
                            print('vote:')
                            print(num_vote)

                            for temp in num_vote:
                                if sum_vote > 0:
                                    ratio_vote.append(round(temp / sum_vote * 100, 2))
                                else:
                                    ratio_vote.append(0)
                            print(ratio_vote)
                            if answer.count() > 0:
                                response = (num_vote, ratio_vote, answer[0].answer)
                            else:
                                response = (num_vote, ratio_vote, -1)
                            print(response)
                            data.append(response)
                        elif (question.question_type == "integer"):
                            choices = question.choices
                            print(choices)
                            if answer.count() > 0:
                                response = (answer[0].answer)
                            else:
                                response = ''
                            print(response)
                            data.append(response)
                        elif (question.question_type == "real"):
                            choices = question.choices
                            print(choices)
                            if answer.count() > 0:
                                response = (answer[0].answer)
                            else:
                                response = ''
                            print(response)
                            data.append(response)
                        elif (question.question_type == "textarea"):
                            choices = question.choices
                            print(choices)
                            if answer.count() > 0:
                                response = (answer[0].answer)
                            else:
                                response = ''
                            print(response)
                            data.append(response)
                    print(data)
                print("canvote:" + str(canvote))

        #SignPackage = getSignPackage(request)
        #return render(request, "article/list/article_detail.html", {"article": article, "total_views": total_views, "most_viewed": most_viewed, "comment_form": comment_form, "similar_articles": similar_articles, "comment_dic": comment_dic_reverse_p, "num_comments": len(comment_lst), "page": current_page, "expire": expire, "survey": json.dumps(survey), "data": json.dumps(data), "SignPackage": SignPackage})
        print("999")
        print(data)
        print("999")
        print(len(survey))
        len_survey = len(survey)
        if len(survey) > 0:
            print("777888")
        else:
            print("666555")
        return render(request, "article/list/article_detail.html",
                      {"article": article, "total_views": total_views, "most_viewed": most_viewed,
                       "comment_form": comment_form, "similar_articles": similar_articles,
                       "comment_dic": comment_dic_reverse_p, "num_comments": len(comment_lst), "page": current_page,
                       "anonymoususer": anonymoususer,
                       "expire": expire, "canvote": canvote, "hasvoted": hasvoted, "len_survey":len_survey, "survey": json.dumps(survey), "data": json.dumps(data),
                       })


@login_required(login_url='/account/new-login/')
@require_POST
@csrf_exempt
def like_article(request):
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "like":
                article.users_like.add(request.user)
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")


@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def like_comment(request):
    comment_id = request.POST.get('comment_id')
    action = request.POST.get('action')
    if comment_id and action:
        try:
            comment = CommentMulti.objects.get(id=comment_id)
            if action == "like":
                comment.comment_like.add(request.user)
                return HttpResponse("1")
            else:
                comment.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")


# 投票调查系统
@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def answer_submit(request):
    if request.is_ajax():
        dic_answer = json.loads(request.POST.get("dic_answer"))
        article_id = dic_answer['article_id']
        answer = dic_answer['answer']
        article = ArticlePost.objects.get(id=article_id)
        questions = Question.objects.filter(survey=article)
        print(article.id)
        data = []
        i = 0
        for question in questions:
            print(question.question_type)
            answer_form = AnswerForm()
            print("question:  " + question.text)
            print("answer:   ")
            print(answer[i])
            new_answer_form = answer_form.save(commit=False)
            new_answer_form.question = question
            new_answer_form.answer = answer[i]
            new_answer_form.survey = article
            new_answer_form.interviewer = article.author
            if article.voteanonymousornot == True:
                new_answer_form.interviewee = None
            else:
                new_answer_form.interviewee = request.user
            new_answer_form.save()
            print(len(Answer.objects.filter(question=question)))
            if(question.question_type == "radio"):
                choices = question.get_choices()
                print(choices)
                num_choices = len(choices)
                num_vote = []
                ratio_vote = []
                sum_vote = 0
                for option in range(num_choices):
                    print(option)
                    num_temp = len(Answer.objects.filter(question=question).filter(answer=option))
                    num_vote.append(num_temp)
                    print(Answer.objects.filter(question=question).filter(answer=option))
                    sum_vote += num_temp
                print('vote:')
                print(num_vote)
                for temp in num_vote:
                    ratio_vote.append(round(temp/sum_vote*100, 2))
                print(ratio_vote)
                response = (num_vote, ratio_vote, answer[i])
                print(response)
                data.append(response)
            elif(question.question_type == "select-multiple"):
                choices = question.get_choices()
                print(choices)
                num_choices = len(choices)
                num_vote = [0]*num_choices
                ratio_vote = []
                sum_vote = 0
                for answer_obj in Answer.objects.filter(question=question):
                    for select in literal_eval(answer_obj.answer):
                        print(literal_eval(answer_obj.answer))
                        for option in range(num_choices):
                            if select == option:
                                num_vote[option] += 1
                for temp in num_vote:
                    sum_vote += temp
                print('vote:')
                print(num_vote)
                for temp in num_vote:
                    ratio_vote.append(round(temp / sum_vote * 100, 2))
                print(ratio_vote)
                response = (num_vote, ratio_vote, answer[i])
                print(response)
                data.append(response)
            elif(question.question_type == "select"):
                choices = question.get_choices()
                print(choices)
                num_choices = len(choices)
                num_vote = []
                ratio_vote = []
                sum_vote = 0
                for option in range(num_choices):
                    print(option)
                    num_temp = len(Answer.objects.filter(question=question).filter(answer=option))
                    num_vote.append(num_temp)
                    print(Answer.objects.filter(question=question).filter(answer=option))
                    sum_vote += num_temp
                print('vote:')
                print(num_vote)
                for temp in num_vote:
                    ratio_vote.append(round(temp / sum_vote * 100, 2))
                print(ratio_vote)
                response = (num_vote, ratio_vote, answer[i])
                print(response)
                data.append(response)
            elif (question.question_type == "integer"):
                choices = question.choices
                print(choices)
                response = (answer[i])
                print(response)
                data.append(response)
            elif (question.question_type == "real"):
                choices = question.choices
                print(choices)
                response = (answer[i])
                print(response)
                data.append(response)
            elif (question.question_type == "textarea"):
                choices = question.choices
                print(choices)
                response = (answer[i])
                print(response)
                data.append(response)
            i += 1
        print(data)
        user_obj = User.objects.filter(username=request.user)
        print(user_obj[0])
        if user_obj:
            article.userhasvoted.add(user_obj[0])
        return HttpResponse(json.dumps(data))




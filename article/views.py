from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn, ArticlePost, ArticleTag
from .forms import ArticleColumnForm, ArticlePostForm, ArticleTagForm, QuestionForm, AnswerForm, ArticleProcessFlowForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from PIL import Image
from mysite.settings import MEDIA_ROOT
import os
import random
from slugify import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from .models import CommentMulti
from haystack.views import SearchView
from django.conf import settings
from django.template import Context, Template
from django.utils import timezone
from django.contrib.auth.models import User
from .models import ArticleProcessFlow, ProcessStateRecord


# Create your views here.


@login_required(login_url='/account/new-login')
@csrf_exempt
def article_column(request):
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        print(columns.count())
        for column in columns:
            print(column.column)
        user_request = request.user
        articles_list = ArticlePost.objects.filter(author=request.user, approved=False)
        articles_list_published = ArticlePost.objects.filter(author=request.user, approved=True)
        list_draft = []
        list_processed = []
        for art in articles_list:
            process = ArticleProcessFlow.objects.filter(article=art)
            if process.count() == 0:
                list_draft.append(art)
            else:
                list_processed.append(art)
        num_draft = len(list_draft)
        num_processed = len(list_processed)
        num_published = len(articles_list_published)

        processes_list_ori = ArticleProcessFlow.objects.filter(approvers=request.user)
        processes_list = []
        for process in processes_list_ori:
            if process.state_process.last().this_step_state == 1:
                if user_request in process.state_process.last().next_step_user.all():
                    processes_list.append(process)
        num_process = len(processes_list)
        num_all = [num_draft, num_processed, num_published, num_process]
        return render(request, "article/column/article_column.html", {"columns": columns, "column_form": column_form, "user_request": user_request, "num_all": num_all})
    if request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)
        if len(column_name) == 0:

            return HttpResponse(3)
        elif columns:

            return HttpResponse(2)
        else:
            newcolumn = ArticleColumn.objects.create(user=request.user, column=column_name)
            dict_id = {"newcolumn_id": newcolumn.id}
            return HttpResponse(json.dumps(dict_id), content_type='application/json')


@login_required(login_url='/account/new-login')
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


@login_required(login_url='/account/new-login')
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/account/new-login')
@csrf_exempt
def article_tag(request):
    if request.method == "GET":
        article_tags = ArticleTag.objects.filter(author=request.user)
        article_tag_form = ArticleTagForm()
        user_request = request.user
        articles_list = ArticlePost.objects.filter(author=request.user, approved=False)
        articles_list_published = ArticlePost.objects.filter(author=request.user, approved=True)
        list_draft = []
        list_processed = []
        for art in articles_list:
            process = ArticleProcessFlow.objects.filter(article=art)
            if process.count() == 0:
                list_draft.append(art)
            else:
                list_processed.append(art)
        num_draft = len(list_draft)
        num_processed = len(list_processed)
        num_published = len(articles_list_published)

        processes_list_ori = ArticleProcessFlow.objects.filter(approvers=request.user)
        processes_list = []
        for process in processes_list_ori:
            if process.state_process.last().this_step_state == 1:
                if user_request in process.state_process.last().next_step_user.all():
                    processes_list.append(process)
        num_process = len(processes_list)
        num_all = [num_draft, num_processed, num_published, num_process]
        return render(request, "article/tag/tag_list.html", {"article_tags": article_tags, "article_tag_form": article_tag_form, "user_request": user_request, "num_all": num_all})
    if request.method == "POST":
        tag_post_form = ArticleTagForm(data=request.POST)
        tag_name = request.POST['tag']
        tags = ArticleTag.objects.filter(author_id=request.user.id, tag=tag_name)
        if len(tag_name) == 0:
            return HttpResponse(3)
        if tag_post_form.is_valid():
            if tags:
                return HttpResponse(2)
            else:
                try:
                    tag_last = ArticleTag.objects.last()
                    new_tag = tag_post_form.save(commit=False)
                    new_tag.author = request.user
                    new_tag.save()
                    dict_id = {"tag_last_id": tag_last.id, "new_tag_id": new_tag.id}
                    return HttpResponse(json.dumps(dict_id), content_type='application/json')
                except:
                    return HttpResponse(4)
        else:
            return HttpResponse(3)


@login_required(login_url='/account/new-login')
@require_POST
@csrf_exempt
def del_article_tag(request):
    tag_id = request.POST['tag_id']
    print(tag_id)
    try:
        tag = ArticleTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@login_required(login_url='/account/new-login')
@require_POST
@csrf_exempt
def rename_article_tag(request):
    tag_name = request.POST["tag_name"]
    tag_id = request.POST['tag_id']
    try:
        line = ArticleTag.objects.get(id=tag_id)
        line.tag = tag_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


import sys, traceback
from django.contrib.auth.models import Group


@login_required(login_url='/account/new-login')
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        print('da')
        print(article_post_form)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            print('55')
            try:
                survey = request.POST['survey']
                print(survey)
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                print(request.POST['column_id'])
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                if survey:
                    interviewees = eval(request.POST['interviewees'])
                    deadline = request.POST['deadline']
                    anonymous = request.POST['anonymous']
                    if interviewees:
                        print(interviewees)
                        print(type(interviewees))
                        for user in interviewees:
                            print(user)
                            user_obj = User.objects.filter(username=user)
                            print(user_obj[0])
                            if user_obj:
                                new_article.usercanvote.add(user_obj[0])
                    if deadline:
                        print(deadline)
                        new_article.votedeadline = deadline
                    if anonymous:
                        print(anonymous)
                        new_article.voteanonymousornot = anonymous
                new_article.save()
                print(request.POST['tags'])
                tags = request.POST['tags']
                if tags:
                    for atag in json.loads(tags):
                        tag = request.user.tag.get(tag=atag)
                        new_article.article_tag.add(tag)
                if survey:
                    for question in json.loads(survey):
                        question_form = QuestionForm().save(commit=False)
                        question_form.text = question[0]
                        question_form.question_type = question[1]
                        question_form.choices = question[2]
                        question_form.required = question[3]
                        question_form.survey = new_article
                        question_form.save()
                return HttpResponse("1")
            except Exception as e:
                print(traceback.format_exc())
                return HttpResponse("2")
        else:
            print(traceback.format_exc())
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        article_tags = request.user.tag.all()
        user_request = request.user
        column_form = ArticleColumnForm()
        tag_form = ArticleTagForm()
        survey_form = QuestionForm()

        article_post_form['title'].field.widget.attrs['style'] = 'width:600px'
        groups = Group.objects.all()
        print(groups)
        interviewees = []
        interviewees.append({"id": 1, "pId": 0, "name": "全部",  "open": "true", "checked": "true"})
        i = 1
        for group in groups:
            print(group.name)
            parent_temp = {"id": "1" + str(i), "pId": 1, "name": group.name, "open": "false", "checked": "true"}
            interviewees.append(parent_temp)
            users = group.user_set.all()
            j = 1
            for user in users:
                print(user)
                children_temp = {"id": int("1" + str(i) + str(j)), "pId": "1" + str(i), "name": user.first_name, "checked": "true", "username": user.username}
                interviewees.append(children_temp)
                j = j+1
            i = i+1
        print(interviewees)
        articles_list = ArticlePost.objects.filter(author=request.user, approved=False)
        articles_list_published = ArticlePost.objects.filter(author=request.user, approved=True)
        list_draft = []
        list_processed = []
        for art in articles_list:
            process = ArticleProcessFlow.objects.filter(article=art)
            if process.count() == 0:
                list_draft.append(art)
            else:
                list_processed.append(art)
        num_draft = len(list_draft)
        num_processed = len(list_processed)
        num_published = len(articles_list_published)

        processes_list_ori = ArticleProcessFlow.objects.filter(approvers=request.user)
        processes_list = []
        for process in processes_list_ori:
            if process.state_process.last().this_step_state == 1:
                if user_request in process.state_process.last().next_step_user.all():
                    processes_list.append(process)
        num_process = len(processes_list)
        num_all = [num_draft, num_processed, num_published, num_process]
        return render(request, "article/column/article_post.html", {"article_post_form": article_post_form, "article_columns": article_columns, "column_form": column_form,  "article_tags": article_tags, "article_tag_form": tag_form, "survey_form": survey_form, "user_request":  user_request, "interviewees": json.dumps(interviewees, ensure_ascii=False), "num_all": num_all})


@login_required(login_url='/account/new-login')
def article_list(request):
    articles_list = ArticlePost.objects.filter(author=request.user)
    user_request = request.user
    paginator = Paginator(articles_list, 10)
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
    interviewees = []
    interviewees.append({"id": 1, "pId": 0, "name": "全部", "open": "true", "checked": "true"})
    i = 1
    groups = Group.objects.all()
    for group in groups:
        print(group.name)
        parent_temp = {"id": "1" + str(i), "pId": 1, "name": group.name, "open": "false", "checked": "true"}
        interviewees.append(parent_temp)
        users = group.user_set.all()
        j = 1
        for user in users:
            print(user)
            children_temp = {"id": int("1" + str(i) + str(j)), "pId": "1" + str(i), "name": user.first_name,
                             "checked": "true", "username": user.username}
            interviewees.append(children_temp)
            j = j + 1
        i = i + 1
    print(interviewees)
    states = []
    state = 0
    for article in articles:
        process = ArticleProcessFlow.objects.filter(article=article)
        if process.count() > 0:
            print(process[0])
            states = ProcessStateRecord.objects.filter(process=process[0]).order_by("-id")

            print(states[0])
            if states.count() > 0:
                state_t = states[0].this_step_state
                state = state_t
                if state_t == 1:
                    article.state = "审批中"
                elif state_t == 2:
                    article.state = "已发布"
                elif state_t == 3:
                    article.state = "被驳回"
                elif state_t == 4:
                    article.state = "已撤回"
                else:
                    article.state = "已删除"
        else:
            article.state = "草稿"
    return render(request, "article/column/article_list.html", {"articles": articles, "page": current_page, "user_request": user_request, "interviewees": json.dumps(interviewees, ensure_ascii=False), "state": state})


@login_required(login_url='/account/new-login')
def article_list_processed(request):
    articles_list = ArticlePost.objects.filter(author=request.user, approved=False)
    list_processed = []
    for art in articles_list:
        process = ArticleProcessFlow.objects.filter(article=art)
        if process.count() != 0:
            list_processed.append(art)
    user_request = request.user
    paginator = Paginator(list_processed, 10)
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
    interviewees = []
    interviewees.append({"id": 1, "pId": 0, "name": "全部", "open": "true", "checked": "true"})
    i = 1
    groups = Group.objects.all()
    for group in groups:
        print(group.name)
        parent_temp = {"id": "1" + str(i), "pId": 1, "name": group.name, "open": "false", "checked": "true"}
        interviewees.append(parent_temp)
        users = group.user_set.all()
        j = 1
        for user in users:
            print(user)
            children_temp = {"id": int("1" + str(i) + str(j)), "pId": "1" + str(i), "name": user.first_name,
                             "checked": "true", "username": user.username}
            interviewees.append(children_temp)
            j = j + 1
        i = i + 1
    print(interviewees)

    for article in articles:
        process = ArticleProcessFlow.objects.filter(article=article)
        if process.count() > 0:
            print(99999)
            print(process[0])
            states = ProcessStateRecord.objects.filter(process=process[0]).order_by("-id")
            print(states[0].this_step_state)
            if states.count() > 0:
                state_t = states[0].this_step_state
                if state_t == 1:
                    article.state = "审批中"
                elif state_t == 2:
                    article.state = "已发布"
                elif state_t == 3:
                    article.state = "被驳回"
                elif state_t == 4:
                    article.state = "已撤回"
                else:
                    article.state = "已删除"
        else:
            article.state = "草稿"
    classification = 1
    articles_list = ArticlePost.objects.filter(author=request.user, approved=False)
    articles_list_published = ArticlePost.objects.filter(author=request.user, approved=True)
    list_draft = []
    list_processed = []
    for art in articles_list:
        process = ArticleProcessFlow.objects.filter(article=art)
        if process.count() == 0:
            list_draft.append(art)
        else:
            list_processed.append(art)
    num_draft = len(list_draft)
    num_processed = len(list_processed)
    num_published = len(articles_list_published)

    processes_list_ori = ArticleProcessFlow.objects.filter(approvers=request.user)
    processes_list = []
    for process in processes_list_ori:
        if process.state_process.last().this_step_state == 1:
            if user_request in process.state_process.last().next_step_user.all():
                processes_list.append(process)
    num_process = len(processes_list)
    num_all = [num_draft, num_processed, num_published, num_process]
    return render(request, "article/column/article_list.html", {"articles": articles, "page": current_page, "user_request": user_request, "interviewees": json.dumps(interviewees, ensure_ascii=False), "classification": classification, "num_all":num_all})


@login_required(login_url='/account/new-login')
def article_list_published(request):
    articles_list = ArticlePost.objects.filter(author=request.user, approved=True)
    user_request = request.user
    paginator = Paginator(articles_list, 10)
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
    interviewees = []
    interviewees.append({"id": 1, "pId": 0, "name": "全部", "open": "true", "checked": "true"})
    i = 1
    groups = Group.objects.all()
    for group in groups:
        print(group.name)
        parent_temp = {"id": "1" + str(i), "pId": 1, "name": group.name, "open": "false", "checked": "true"}
        interviewees.append(parent_temp)
        users = group.user_set.all()
        j = 1
        for user in users:
            print(user)
            children_temp = {"id": int("1" + str(i) + str(j)), "pId": "1" + str(i), "name": user.first_name,
                             "checked": "true", "username": user.username}
            interviewees.append(children_temp)
            j = j + 1
        i = i + 1
    print(interviewees)
    for article in articles:
        process = ArticleProcessFlow.objects.filter(article=article)
        if process.count() > 0:
            print(process[0])
            states = ProcessStateRecord.objects.filter(process=process[0]).order_by("-id")
            print(states[0])
            if states.count() > 0:
                state_t = states[0].this_step_state

                if state_t == 1:
                    article.state = "审批中"
                elif state_t == 2:
                    article.state = "已发布"
                elif state_t == 3:
                    article.state = "被驳回"
                elif state_t == 4:
                    article.state = "已撤回"
                else:
                    article.state = "已删除"
        else:
            article.state = "草稿"
    classification = 2
    articles_list = ArticlePost.objects.filter(author=request.user, approved=False)
    articles_list_published = ArticlePost.objects.filter(author=request.user, approved=True)
    list_draft = []
    list_processed = []
    for art in articles_list:
        process = ArticleProcessFlow.objects.filter(article=art)
        if process.count() == 0:
            list_draft.append(art)
        else:
            list_processed.append(art)
    num_draft = len(list_draft)
    num_processed = len(list_processed)
    num_published = len(articles_list_published)

    processes_list_ori = ArticleProcessFlow.objects.filter(approvers=request.user)
    processes_list = []
    for process in processes_list_ori:
        if process.state_process.last().this_step_state == 1:
            if user_request in process.state_process.last().next_step_user.all():
                processes_list.append(process)
    num_process = len(processes_list)
    num_all = [num_draft, num_processed, num_published, num_process]
    return render(request, "article/column/article_list.html", {"articles": articles, "page": current_page, "user_request": user_request, "interviewees": json.dumps(interviewees, ensure_ascii=False), "classification": classification, "num_all": num_all})


@login_required(login_url='/account/new-login')
def article_list_draft(request):
    articles_list = ArticlePost.objects.filter(author=request.user)
    list_draft = []
    for art in articles_list:
        process = ArticleProcessFlow.objects.filter(article=art)
        if process.count() == 0:
            list_draft.append(art)
    user_request = request.user
    paginator = Paginator(list_draft, 10)
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
    interviewees = []
    interviewees.append({"id": 1, "pId": 0, "name": "全部", "open": "true", "checked": "true"})
    i = 1
    groups = Group.objects.all()
    for group in groups:
        print(group.name)
        parent_temp = {"id": "1" + str(i), "pId": 1, "name": group.name, "open": "false", "checked": "true"}
        interviewees.append(parent_temp)
        users = group.user_set.all()
        j = 1
        for user in users:
            print(user)
            children_temp = {"id": int("1" + str(i) + str(j)), "pId": "1" + str(i), "name": user.first_name,
                             "checked": "true", "username": user.username}
            interviewees.append(children_temp)
            j = j + 1
        i = i + 1
    print(interviewees)
    for article in articles:
        process = ArticleProcessFlow.objects.filter(article=article)
        if process.count() > 0:
            print(process[0])
            states = ProcessStateRecord.objects.filter(process=process[0]).order_by("-id")
            print(states[0])
            if states.count() > 0:
                state_t = states[0].this_step_state

                if state_t == 1:
                    article.state = "审批中"
                elif state_t == 2:
                    article.state = "已发布"
                elif state_t == 3:
                    article.state = "被驳回"
                elif state_t == 4:
                    article.state = "已撤回"
                else:
                    article.state = "已删除"
        else:
            article.state = "草稿"
    classification = 0
    articles_list = ArticlePost.objects.filter(author=request.user, approved=False)
    articles_list_published = ArticlePost.objects.filter(author=request.user, approved=True)
    list_draft = []
    list_processed = []
    for art in articles_list:
        process = ArticleProcessFlow.objects.filter(article=art)
        if process.count() == 0:
            list_draft.append(art)
        else:
            list_processed.append(art)
    num_draft = len(list_draft)
    num_processed = len(list_processed)
    num_published = len(articles_list_published)

    processes_list_ori = ArticleProcessFlow.objects.filter(approvers=request.user)
    processes_list = []
    for process in processes_list_ori:
        if process.state_process.last().this_step_state == 1:
            if user_request in process.state_process.last().next_step_user.all():
                processes_list.append(process)
    num_process = len(processes_list)
    num_all = [num_draft, num_processed, num_published, num_process]
    return render(request, "article/column/article_list.html", {"articles": articles, "page": current_page, "user_request": user_request, "interviewees": json.dumps(interviewees, ensure_ascii=False), "classification": classification, "num_all": num_all})


from .models import Question, Answer
from django.contrib.auth.models import AnonymousUser
import datetime
import pytz
from ast import literal_eval

@login_required(login_url='/account/new-login')
def article_detail(request, id, slug):
    user_request = request.user
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    print(article.votedeadline)
    if request.method == "POST":
        return HttpResponse(json.dumps({"success": "1"}))
    else:
        article_tags_ids = article.article_tag.values_list("id", flat=True)
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
        return render(request, "article/column/article_detail.html",
                      {"article": article,
                       "anonymoususer": anonymoususer,
                       "expire": expire, "canvote": canvote, "hasvoted": hasvoted, "len_survey":len_survey, "survey": json.dumps(survey), "data": json.dumps(data),
                       })


@login_required(login_url='/account/new-login')
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/account/new-login')
@csrf_exempt
def redit_article(request, article_id):
    if request.method == "GET":
        article_columns = request.user.article_column.all()
        article_tags = request.user.tag.all()
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(initial={"title": article.title})
        this_article_form['title'].field.widget.attrs['style'] = 'width:600px'
        article_tag_form = ArticleTagForm()
        this_article_column = article.column
        this_article_tags = article.article_tag
        user_request = request.user
        interviewees_obj = article.usercanvote.all()
        questions_obj = Question.objects.filter(survey=article)
        questions = []
        for question in questions_obj:
            if question.required == True:
                questions.append([question.text, question.question_type, question.choices, "true"])
            else:
                questions.append([question.text, question.question_type, question.choices, "false"])
        groups = Group.objects.all()
        print(groups)
        interviewees = []
        interviewees.append({"id": 1, "pId": 0, "name": "全部", "open": "true", "checked": "true"})
        i = 1
        for group in groups:
            print(group.name)
            parent_temp = {"id": "1" + str(i), "pId": 1, "name": group.name, "open": "false", "checked": "true"}
            interviewees.append(parent_temp)
            users = group.user_set.all()
            j = 1
            for user in users:
                print(user)
                print(interviewees_obj)
                if user in interviewees_obj:
                    children_temp = {"id": int("1" + str(i) + str(j)), "pId": "1" + str(i), "name": user.first_name,
                                 "checked": "true"}
                else:
                    children_temp = {"id": int("1" + str(i) + str(j)), "pId": "1" + str(i), "name": user.first_name,
                                     "checked": "false"}
                interviewees.append(children_temp)
                j = j + 1
            i = i + 1
        print(interviewees)
        voteanonymousornot = article.voteanonymousornot
        votedeadline = article.votedeadline
        print(voteanonymousornot)
        column_form = ArticleColumnForm()
        return render(request, "article/column/redit_article.html", {"article": article, "article_columns": article_columns, "this_article_column": this_article_column,"article_tags": article_tags, "this_article_tags": this_article_tags, "article_tag_form": article_tag_form , "this_article_form": this_article_form,"user_request": user_request, "interviewees": interviewees, "questions": questions, "column_form": column_form, "voteanonymousornot": voteanonymousornot, "votedeadline": votedeadline})
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            tags = request.POST['tags']
            if tags:
                redit_article.article_tag.clear()
                for atag in json.loads(tags):
                    tag = request.user.tag.get(tag=atag)
                    redit_article.article_tag.add(tag)
            redit_article.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")





@login_required(login_url='/account/new-login')
@csrf_exempt
def blog_img_upload(request):
    if request.method == "POST":
        data = request.FILES['editormd-image-file']
        print('222')
        print(data)
        img = Image.open(data)
        width = img.width
        height = img.height
        rate = 1.0

        if width >= 2000 or height >= 2000:
            rate = 0.3
        elif width >= 1000 or height >= 1000:
            rate = 0.5
        elif width >= 500 or height >= 500:
            rate = 0.9

        width = int(width * rate)
        height = int(height * rate)

        #img.thumbnail((width, height), Image.ANTIALIAS)

        url = 'blogimg/' + slugify(request.user.username) + '-' + data.name
        print(url)
        name = MEDIA_ROOT + '/' + url
        print(name)

        while os.path.exists(name):
            file, ext = os.path.splitext(data.name)
            file = file + str(random.randint(1, 1000))
            data.name = file + ext
            url = 'blogimg/' + slugify(request.user.username) + '-' + data.name
            name = MEDIA_ROOT + '/' + url
            print(name)

        try:
            file, ext = os.path.splitext(data.name)
            # .lower()将字符串中所有大写字母转换为小写，只对ASKII编码有效，即A-Z，其他语言需用casefold转换大小写
            print(ext.lower())
            # 如果是gif图片，保存时需设定save_all=True将多帧保存，否则只保存第一帧
            if ext.lower() == '.gif':
                img.save(name, save_all=True)
            else:
                img.save(name)
            url = '/media' + name.split('media')[-1]
            print("url="+url)
            return JsonResponse({'success': 1, 'message': '成功', 'url': url})
        except Exception as e:
            return JsonResponse({'success': 0, 'message': '上传失败'})


@login_required(login_url='/account/new-login')
@csrf_exempt
def blog_img_upload_drag(request):
    if request.method == "POST":
        data = request.FILES.get('img')
        print('222')
        print(data)
        img = Image.open(data)
        width = img.width
        height = img.height
        rate = 1.0

        if width >= 2000 or height >= 2000:
            rate = 0.3
        elif width >= 1000 or height >= 1000:
            rate = 0.5
        elif width >= 500 or height >= 500:
            rate = 0.9

        width = int(width * rate)
        height = int(height * rate)

        #img.thumbnail((width, height), Image.ANTIALIAS)

        url = 'blogimg/' + slugify(request.user.username) + '-' + data.name
        print(url)
        name = MEDIA_ROOT + '/' + url
        print(name)

        while os.path.exists(name):
            file, ext = os.path.splitext(data.name)
            file = file + str(random.randint(1, 1000))
            data.name = file + ext
            url = 'blogimg/' + slugify(request.user.username) + '-' + data.name
            name = MEDIA_ROOT + '/' + url
            print(name)

        try:
            file, ext = os.path.splitext(data.name)
            # .lower()将字符串中所有大写字母转换为小写，只对ASKII编码有效，即A-Z，其他语言需用casefold转换大小写
            print(ext.lower())
            # 如果是gif图片，保存时需设定save_all=True将多帧保存，否则只保存第一帧
            if ext.lower() == '.gif':
                img.save(name, save_all=True)
            else:
                img.save(name)
            url = '/media' + name.split('media')[-1]
            print("url="+url)
            return JsonResponse({'success': 1, 'message': '成功', 'url': url})
        except Exception as e:
            return JsonResponse({'success': 0, 'message': '上传失败'})


@login_required(login_url='/account/new-login')
@csrf_exempt
def blog_video_upload_drag(request):
    if request.method == "POST":
        data = request.FILES.get('video')
        print('222')
        print(data)
        url = 'blogvideo/' + slugify(request.user.username) + '-' + data.name
        print(url)
        name = MEDIA_ROOT + '/' + url
        print(name)

        while os.path.exists(name):
            file, ext = os.path.splitext(data.name)
            file = file + str(random.randint(1, 1000))
            data.name = file + ext
            url = 'blogvideo/' + slugify(request.user.username) + '-' + data.name
            name = MEDIA_ROOT + '/' + url
            print(name)

        try:
            file, ext = os.path.splitext(data.name)
            # .lower()将字符串中所有大写字母转换为小写，只对ASKII编码有效，即A-Z，其他语言需用casefold转换大小写
            print(ext.lower())

            f = open(name, 'wb')
            for chunk in data.chunks():
                f.write(chunk)
            f.close()
            url = '/media' + name.split('media')[-1]
            print("url="+url)
            return JsonResponse({'success': 1, 'message': '成功', 'url': url})
        except Exception as e:
            return JsonResponse({'success': 0, 'message': '上传失败'})


@login_required(login_url='/account/new-login')
@csrf_exempt
def blog_file_upload_drag(request):
    if request.method == "POST":
        data = request.FILES.get('file')
        print('222')
        print(data)
        url = 'blogfile/' + slugify(request.user.username) + '-' + data.name
        print(url)
        name = MEDIA_ROOT + '/' + url
        print(name)

        while os.path.exists(name):
            file, ext = os.path.splitext(data.name)
            file = file + str(random.randint(1, 1000))
            data.name = file + ext
            url = 'blogfile/' + slugify(request.user.username) + '-' + data.name
            name = MEDIA_ROOT + '/' + url
            print(name)

        try:
            file, ext = os.path.splitext(data.name)
            # .lower()将字符串中所有大写字母转换为小写，只对ASKII编码有效，即A-Z，其他语言需用casefold转换大小写
            print(ext.lower())

            f = open(name, 'wb')
            for chunk in data.chunks():
                f.write(chunk)
            f.close()
            url = '/media' + name.split('media')[-1]
            print("url=" + url)
            return JsonResponse({'success': 1, 'message': '成功', 'url': url})
        except Exception as e:
            return JsonResponse({'success': 0, 'message': '上传失败'})


class MySearchView(SearchView):
    template = 'article/search.html'

    def create_response(self):
        if not self.request.GET.get('q', ''):
            show_all = True
            articles = ArticlePost.objects.all()
            paginator = Paginator(articles, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
            try:
                page = paginator.page(int(self.request.GET.get('page', 1)))
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                page = paginator.page(paginator.num_pages)
            return render(self.request, self.template, locals())
        else:
            show_all = False
            qs = super(MySearchView, self).create_response()
            return qs


@csrf_exempt
def submit_approve(request):
    if request.method == "POST":
        article_id = request.POST['article_id']
        approvers = eval(request.POST['approvers'])
        opinion = request.POST['opinion']
        article = ArticlePost.objects.get(id=article_id)
        print('666')
        process_old = ArticleProcessFlow.objects.filter(article=article, applicant=request.user)
        if process_old.count() > 0:
            process = process_old[0]
            print("yicunzai")
            print(process.pk)
            state_last = process.state_process.last().this_step_state
            print(state_last)
            if state_last == 1:
                return HttpResponse("11")
            elif state_last == 2:
                return HttpResponse("22")
            elif state_last == 5:
                return HttpResponse("55")
        else:
            process = ArticleProcessFlow(article=article, applicant=request.user)
            process.save(force_insert=True)
            print("xinjian")
        for appr in approvers:
            approver = User.objects.filter(username=appr)[0]
            process.approvers.add(approver)
        process.save()
        print("777")
        state = ProcessStateRecord(process=process, this_step_user=request.user, this_step_handle=1, this_step_state=1)
        state.save(force_insert=True)
        for appr in approvers:
            approver = User.objects.filter(username=appr)[0]
            state.next_step_user.add(approver)
        state.this_step_opinion = opinion
        state.save()
        print('999')
        return HttpResponse("1")
    return HttpResponse("2")


@csrf_exempt
def queue_approve(request, article_id):
        user_request =request.user
        article = ArticlePost.objects.get(id=article_id)
        process_temp = ArticleProcessFlow.objects.filter(article=article)
        if process_temp.count() > 0:
            process = process_temp[0]
            states_list = ProcessStateRecord.objects.filter(process=process)
        else:
            states_list = []
        paginator = Paginator(states_list, 10)
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
            states = current_page.object_list
        except PageNotAnInteger:
            current_page = paginator.page(1)
            states = current_page.object_list
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)
            states = current_page.object_list
        return render(request, "article/approve/queue.html", {"article": article, "states": states, "page": current_page, "user_request":user_request})


@csrf_exempt
def list_task(request):
        user_request =request.user
        processes_list_ori = ArticleProcessFlow.objects.filter(approvers=user_request)
        processes_list = []
        for process in processes_list_ori:
            if process.state_process.last().this_step_state == 1:
                if user_request in process.state_process.last().next_step_user.all():
                    processes_list.append(process)
                    print(True)
                else:
                    print(False)
        paginator = Paginator(processes_list, 10)
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
            processes = current_page.object_list
        except PageNotAnInteger:
            current_page = paginator.page(1)
            processes = current_page.object_list
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)
            processes = current_page.object_list
        articles_list = ArticlePost.objects.filter(author=request.user, approved=False)
        articles_list_published = ArticlePost.objects.filter(author=request.user, approved=True)
        list_draft = []
        list_processed = []
        for art in articles_list:
            process = ArticleProcessFlow.objects.filter(article=art)
            if process.count() == 0:
                list_draft.append(art)
            else:
                list_processed.append(art)
        num_draft = len(list_draft)
        num_processed = len(list_processed)
        num_published = len(articles_list_published)

        processes_list_ori = ArticleProcessFlow.objects.filter(approvers=request.user)
        processes_list = []
        for process in processes_list_ori:
            if process.state_process.last().this_step_state == 1:
                if user_request in process.state_process.last().next_step_user.all():
                    processes_list.append(process)
        num_process = len(processes_list)
        num_all = [num_draft, num_processed, num_published, num_process]
        return render(request, "article/approve/task_list.html", {"processes": processes, "page": current_page, "user_request":user_request, "num_all": num_all})


@csrf_exempt
def approve_article(request):
    if request.method == "POST":
        process_id = request.POST['process_id']
        process = ArticleProcessFlow.objects.filter(id=process_id)[0]
        print(process_id)
        print(process)
        if process.state_process.last().this_step_state == 1:
            opinion = request.POST['opinion']
            approve = request.POST['approve_state']
            state = ProcessStateRecord(process=process, this_step_user=request.user)
            state.save(force_insert=True)
            print(state)
            if approve == "yes":
                process.approved = True
                process.approve_article()
                state.this_step_handle = 2
                state.this_step_state = 2
                state.this_step_opinion = opinion
                state.save()
            else:
                state.this_step_handle = 3
                state.this_step_state = 3
                state.this_step_opinion = opinion
                state.next_step_user.add(process.applicant)
                state.save()
            return HttpResponse("1")
        elif process.state_process.last().this_step_state == 4:
            return HttpResponse("4")
        elif process.state_process.last().this_step_state == 3:
            return HttpResponse("3")
        elif process.state_process.last().this_step_state == 2:
            return HttpResponse("5")
    else:
        return HttpResponse("2")


@csrf_exempt
def undo_approve(request):
    if request.method == "POST":
        article_id = request.POST['article_id']
        opinion = request.POST['opinion']
        article = ArticlePost.objects.filter(id=article_id)[0]
        process = ArticleProcessFlow.objects.filter(article=article)[0]
        print(process)
        if process.state_process.last().this_step_state == 1:
            state = ProcessStateRecord(process=process, this_step_user=request.user)
            state.save(force_insert=True)
            print(state)
            state.this_step_handle = 4
            state.this_step_state = 4
            state.this_step_opinion = opinion
            state.save()
            return HttpResponse("1")
        elif process.state_process.last().this_step_state == 3:
            return HttpResponse("3")
        elif process.state_process.last().this_step_state == 2:
            return HttpResponse("5")
    else:
        return HttpResponse("2")


from django.views.generic import TemplateView, ListView
from .models import Course
from braces.views import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from django.shortcuts import redirect
from .forms import CreateCourseForm
from django.urls import reverse_lazy
from django.http import HttpResponse
import json
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from .forms import CreateLessonForm
from .models import Lesson
from django.views.generic.base import TemplateResponseMixin

# Create your views here.


class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = 'course/course_list.html'


class UserMixin:
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)


class UserCourseMixin(UserMixin, LoginRequiredMixin):
    model = Course
    login_url = "/account/login/"


class ManageCourseListView(UserCourseMixin, ListView):
    context_object_name = "courses"
    template_name = 'course/manage/manage_course_list.html'

    def get(self, request, *args, **kwargs):
        #form = CreateCourseForm(user=self.request.user)
        courses = Course.objects.filter(user=request.user)
        user_request = request.user
        return render(request, "course/manage/manage_course_list.html", {"user_request": user_request, "courses": courses})


class CreateCourseView(UserCourseMixin, CreateView):
    fields = ['title', 'overview']
    template_name = 'course/manage/create_course.html'

    def get(self, request, *args, **kwargs):
        form = CreateCourseForm()
        user_request = request.user
        return self.render_to_response({"form": form, "user_request": user_request})

    def post(self, request, *args, **kwargs):
        user_request = request.user
        form = CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect("course:manage_course")
        return self.render_to_response({"form": form, "user_request": user_request})


class DeleteCourseView(UserCourseMixin, DeleteView):
    #template_name = 'course/manage/delete_course_confirm.html'
    success_url = reverse_lazy("course:manage_course")

    def dispatch(self, request, *args, **kwargs):
        resp = super(DeleteCourseView, self).dispatch(request, *args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return resp


class CreateLessonView(LoginRequiredMixin, View):
    model = Lesson
    login_url = "/account/login/"

    def get(self, request, *args, **kwargs):
        form = CreateLessonForm(user=self.request.user)
        user_request = request.user
        return render(request, "course/manage/create_lesson.html", {"form": form,  "user_request": user_request})

    def post(self, request, *args, **kwargs):
        form = CreateLessonForm(self.request.user, request.POST, request.FILES)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.user = self.request.user
            new_lesson.save()
            return redirect("course:manage_course")


class ListLessonsView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = "/account/login/"
    template_name = 'course/manage/list_lessons.html'

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        user_request = request.user
        return self.render_to_response({'course': course,  "user_request": user_request})


class DetailLessonView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = "/account/login/"
    template_name = "course/manage/detail_lesson.html"

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        user_request = request.user
        return self.render_to_response({"lesson": lesson, "user_request": user_request})


class StudentListLessonView(ListLessonsView):
    template_name = "course/slist_lessons.html"

    def post(self, request, *args, **kwargs):
        course = Course.objects.get(id=kwargs['course_id'])
        course.student.add(self.request.user)
        return HttpResponse("ok")




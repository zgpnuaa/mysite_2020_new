from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm
from .models import Image

# Create your views here.


@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def upload_image(request):
    form = ImageForm(data=request.POST)
    if form.is_valid():
        try:
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return JsonResponse({'status': "1"})
        except:
            return JsonResponse({'status': 0})


from article.models import ArticlePost,ArticleProcessFlow


@login_required(login_url='/account/login/')
def list_images(request):
    images = Image.objects.filter(user=request.user)
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
    return render(request, 'image/list_images.html', {"images": images, "user_request": user_request, "num_all": num_all})


@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def del_image(request):
    image_id = request.POST['image_id']
    try:
        image = Image.objects.get(id=image_id)
        image.delete()
        return JsonResponse({'status': "1"})
    except:
        return JsonResponse({'status': "2"})


def falls_images(request):
    images = Image.objects.all()
    return render(request, 'image/falls_images.html', {"images": images})



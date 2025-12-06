from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from .models import Course, MediaItem, Comment, Like, ContactInfo
from django.core.paginator import Paginator
from datetime import datetime

def home(request):
    latest_media = MediaItem.objects.order_by('-created_at')[:6]
    courses = Course.objects.order_by('-created_at')[:6]
    return render(request, "home.html", {'latest_media': latest_media, 'courses': courses})

def about(request):
    return render(request, "about.html")

def courses(request):
    all_courses = Course.objects.order_by('-created_at')
    return render(request, "courses.html", {'courses': all_courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, "course_detail.html", {'course': course})

def gallery(request):
    items = MediaItem.objects.order_by('-created_at')
    paginator = Paginator(items, 24)
    page = request.GET.get('page', 1)
    items_page = paginator.get_page(page)
    return render(request, "gallery.html", {'items': items_page})

def media_detail(request, pk):
    m = get_object_or_404(MediaItem, pk=pk)
    comments = m.comments.order_by('-created_at')

    has_liked = False
    if request.user.is_authenticated:
        has_liked = m.likes.filter(user=request.user).exists()

    return render(request, "media_detail.html", {
        'media': m,
        'comments': comments,
        'has_liked': has_liked
    })

def contact(request):
    info = ContactInfo.objects.first()
    return render(request, "contact.html", {'info': info})

# helper to check staff
def is_staff(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_staff)
def admin_dashboard(request):
    media_list = MediaItem.objects.order_by('-created_at')[:12]
    context = {
        'media_list': media_list,
        'courses_count': Course.objects.count(),
        'media_count': MediaItem.objects.count(),
        'comments_count': Comment.objects.count(),
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
@user_passes_test(is_staff)
def upload_media(request):
    """
    Handles multiple file upload from admin dashboard.
    Accepts:
      - files[] (multiple)
      - event (same for all files)
      - description (same for all files)
      - date (YYYY-MM-DD, optional)
    """
    if request.method != "POST":
        return render(request, 'upload.html')

    files = request.FILES.getlist('files')
    if not files:
        return HttpResponseBadRequest("No files uploaded")

    event = request.POST.get('event','').strip()
    description = request.POST.get('description','').strip()
    date_str = request.POST.get('date','').strip()
    date_val = None
    if date_str:
        try:
            date_val = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            date_val = None

    created = []
    for f in files:
        ft = 'video' if f.content_type.startswith('video') else 'image'
        obj = MediaItem.objects.create(file=f, type=ft, event_name=event, description=description, date=date_val)
        created.append(obj.id)

    return redirect('admin_dashboard')


@require_POST
def like_media(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error':'login required'}, status=401)

    media = get_object_or_404(MediaItem, pk=pk)
    existing = Like.objects.filter(media=media, user=request.user)
    if existing.exists():
        # toggle off
        existing.delete()
        liked = False
    else:
        Like.objects.create(media=media, user=request.user)
        liked = True

    return JsonResponse({'liked': liked, 'likes_count': media.likes.count()})


@require_POST
def comment_media(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error':'login required'}, status=401)
    text = request.POST.get('text','').strip()
    if not text:
        return JsonResponse({'error':'empty'}, status=400)
    media = get_object_or_404(MediaItem, pk=pk)
    c = Comment.objects.create(media=media, user=request.user, text=text)
    # return JSON so frontend can append without reload
    return JsonResponse({
        'ok': True,
        'comment': {
            'id': c.id,
            'user': c.user.username if c.user else 'Guest',
            'text': c.text,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M'),
        },
        'comments_count': media.comments.count()
    })

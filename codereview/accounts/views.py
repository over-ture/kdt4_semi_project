import openai
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CodeReviewForm, SignupForm
from .models import CodeReview


@login_required
def accounts_home(request):
    return render(request, 'accounts/accounts_home.html')


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('upload_code')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        # 로그인 로직
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # 인증에 성공한 경우
        if user is not None:
            login(request, user)
            return redirect('upload_code')
        else:
            # 인증 실패
            return render(request, 'accounts/login.html', {'error': '아이디나 비밀번호가 올바르지 않습니다.'})
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')


from django.shortcuts import render
from django.contrib.auth.models import User

def find_username(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            return render(request, 'accounts/username_result.html', {'username': user.username})
        except User.DoesNotExist:
            return render(request, 'accounts/find_username.html', {'error': 'Email not found!'})
    else:
        return render(request, 'accounts/find_username.html')



@login_required
def upload_code(request):
    if request.method == 'POST':
        form = CodeReviewForm(request.POST, request.FILES)
        if form.is_valid():
            code_review = form.save(commit=False)
            code_review.user = request.user

            if not code_review.code and code_review.uploaded_file:
                # 파일에서 코드를 읽어옵니다.
                code_review.code = code_review.uploaded_file.read().decode('utf-8')

            # ChatGPT API로 코드 리뷰를 받습니다.
            code_review.review_result = get_code_review(code_review.code)

            code_review.save()
            return redirect('review_result', code_review_id=code_review.id)
    else:
        form = CodeReviewForm()
    return render(request, 'accounts/upload_code.html', {'form': form})


openai.api_key = ""

def get_code_review(input_code):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo", messages = [{"role": "user", "content": f"다음 파이썬 코드를 리뷰해 주세요. 리뷰 내용은 한글로 작성하세요.:\n\n{input_code}"}]
    )
    return response.choices[0].message.content



def review_result(request, code_review_id):
    code_review = get_object_or_404(CodeReview, id=code_review_id)

    # 리뷰의 소유자가 아니면 접근을 제한합니다.
    if request.user != code_review.user:
        raise PermissionDenied

    return render(request, 'accounts/review_result.html', {'code_review': code_review})


@login_required
def my_reviews(request):
    # 현재 로그인한 사용자의 리뷰 기록을 최신 순으로 가져오기
    reviews = CodeReview.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'accounts/my_reviews.html', {'reviews': reviews})

@login_required
def delete_review(request, code_review_id):
    review = get_object_or_404(CodeReview, id=code_review_id)

    # 리뷰의 소유자가 아니면 접근을 제한합니다.
    if request.user != review.user:
        raise PermissionDenied

    review.delete()
    return redirect('my_reviews')



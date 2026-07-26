from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


User = get_user_model()


def register_view(request):
    context = {}
    if request.method == "POST":
        full_name = request.POST.get("fullName", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirmPassword", "")

        if not all((full_name, username, email, password)):
            context["server_error"] = "يرجى تعبئة جميع الحقول المطلوبة."
        elif password != confirm_password:
            context["server_error"] = "كلمتا المرور غير متطابقتين."
        elif User.objects.filter(username__iexact=username).exists():
            context["server_error"] = "اسم المستخدم مستخدم بالفعل."
        elif User.objects.filter(email__iexact=email).exists():
            context["server_error"] = "البريد الإلكتروني مستخدم بالفعل."
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=full_name,
            )
            login(request, user)
            return redirect("accounts:profile")

        context["submitted"] = request.POST

    return render(request, "accounts/register.html", context)


def login_view(request):
    context = {}
    if request.method == "POST":
        identifier = request.POST.get("loginIdentifier", "").strip()
        password = request.POST.get("loginPassword", "")
        username = identifier
        email_user = User.objects.filter(email__iexact=identifier).first()
        if email_user:
            username = email_user.get_username()

        user = authenticate(request, username=username, password=password)
        if user is None:
            context["server_error"] = "اسم المستخدم أو البريد الإلكتروني أو كلمة المرور غير صحيحة."
            context["identifier"] = identifier
        else:
            login(request, user)
            if not request.POST.get("rememberMe"):
                request.session.set_expiry(0)
            return redirect("accounts:profile")

    return render(request, "accounts/login.html", context)


@login_required(login_url="accounts:login")
def profile_view(request):
    return render(request, "accounts/profile.html")


def logout_view(request):
    logout(request)
    return redirect("accounts:login")

from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models

def index(request):
    return render(request, 'index.html')
def register(request):
    if request.method=='POST':
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        password2=request.POST.get("password2")
        calorie_goal=request.POST.get("calorie_goal")
        protein_goal=request.POST.get("protein_goal")
        image=request.FILES.get("image")
        
        if models.User.objects.filter(email=email).exists():
            return HttpResponse('email already exists')
        if password==password2:
            user=models.User(username=username,email=email,
                             password=password,calorie_goal=calorie_goal,
                             protein_goal=protein_goal,image=image)
            user.save()
            return redirect('index')
        return HttpResponse('passwords do not match')
    



    return render(request, 'register.html')

def login(request):
    if request.method=='POST':
        email=request.POST.get("email")
        password=request.POST.get("password")
        try:
            user=models.User.objects.get(email=email)
            if user.password==password:
                request.session['email']=email
                return redirect('home')
            return HttpResponse('<script> alert("invalid password");window.history.back();  </script>')
        except models.User.DoesNotExist:
            return HttpResponse('<script> alert("invalid email");window.history.back();  </script>')
    return render(request, 'login.html')   

from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import MealLog, User  # make sure User is imported

def home(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')

    user = User.objects.filter(email=email).first()
    if not user:
        return redirect('login')  # safety check

    today = now().date()

    # Fetch today's meals for this user
    mealstoday = MealLog.objects.filter(
        user=user,   # ✅ use user from session, not request.user
        date=today
    ).order_by('-date')[:2]
    meals = MealLog.objects.filter(
        user=user,   # ✅ use user from session, not request.user
        date=today
    ).order_by('-date')

    total_calories = sum(meal.total_calories for meal in meals)
    total_protein = sum(meal.total_protein for meal in meals)
    # progreebar
    # ✅ SAFE progress calculation
    calorie_percent = (
        min(100, int((total_calories / user.calorie_goal) * 100))
        if user.calorie_goal else 0
    )

    protein_percent = (
        min(100, int((total_protein / user.protein_goal) * 100))
        if user.protein_goal else 0
    )


    return render(request, 'home.html', {
        "user": user,
        "calorie_percent": calorie_percent,
        "protein_percent": protein_percent,
        "meals": meals,
        "mealstoday": mealstoday,
        "total_calories": total_calories,
        "total_protein": total_protein,
    })
    


def profile(request):
    user=models.User.objects.get(email=request.session.get('email'))
    return render(request , 'profile.html',{'user':user})
def logout(request):
    request.session.flush()
    return redirect('index')
def adminlogout(request):
    request.session.flush()
    return redirect('adminlogin')

def editprofile(request):
    if 'email' in request.session:
        user=models.User.objects.get(email=request.session.get('email'))
        if request.method=='POST':
            user.username=request.POST.get("username")
            user.email=request.POST.get("email")
            user.password=request.POST.get("password")
            user.calorie_goal=request.POST.get("calorie_goal")
            user.protein_goal=request.POST.get("protein_goal")
            if 'image' in request.FILES:
                user.image=request.FILES.get("image")
            user.save()
            return redirect('profile')
        return render(request,'editprofile.html',{'user':user})
    return redirect('login')
def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        if username == "admin" and password == "admin123":
            request.session['username'] = username
            return redirect('admindashboard')
        return HttpResponse('<script> alert("invalid password");window.history.back();  </script>')

    return render(request, 'adminlogin.html')
from django.contrib.auth import get_user_model
from .models import MealLog
User = get_user_model()
def admindashboard(request):


    total_users = User.objects.count()
    total_logs = MealLog.objects.count()
    total_foods = Food.objects.count()

    # Cap percentages at 100% to prevent invalid CSS
    user_percent = min(100, total_users)
    logs_percent = min(100, total_logs)

    context = {
        'total_users': total_users,
        'total_logs': total_logs,
        'total_foods' : total_foods,
        'user_percent': user_percent,
        'logs_percent': logs_percent,
    }
    return render(request,'admindashboard.html',context)

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Food

def adminaddfood(request):
    if not request.session.get('username'):
        return redirect('adminlogin')

    if request.method == "POST":
        name = request.POST.get("name")
        calories = request.POST.get("calories")
        protein = request.POST.get("protein")

        # Create new Food object
        Food.objects.create(
            name=name,
            calories=int(calories),
            protein=float(protein)
        )

        messages.success(request, "Food item added successfully!")
        return redirect("admindashboard")

    return render(request, "adminaddfood.html")

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Food

def adminfoodlist(request):
    if not request.session.get('username'):
        return redirect('adminlogin')

    foods = Food.objects.all()
    return render(request, "adminfoodlist.html", {"foods": foods})


def admineditfood(request, food_id):
    if not request.session.get('username'):
        return redirect('adminlogin')

    food = get_object_or_404(Food, id=food_id)

    if request.method == "POST":
        food.name = request.POST.get("name")
        food.calories = int(request.POST.get("calories"))
        food.protein = float(request.POST.get("protein"))
        

        food.save()
        messages.success(request, "Food updated successfully!")
        return redirect("adminfoodlist")

    # GET request → just render the form with current food data
    return render(request, "admineditfood.html", {"food": food})


def admindeletefood(request, food_id): 
    if not request.session.get('username'): 
        return redirect('adminlogin')
    food = get_object_or_404(Food, id=food_id)
    food.delete()
    messages.success(request, "Food deleted successfully!")

    return redirect("adminfoodlist")






def userlist(request):
    users=models.User.objects.all()
    return render(request,'userlist.html',{'users':users})
def deleteuser(request,id):
    users=models.User.objects.get(id=id)
    users.delete() 
    return redirect('userlist')


from .models import Food


from django.contrib import messages
from .models import Food, MealLog ,UserFavorite
def add_food_view(request):
    if not request.session.get('email'):
        return redirect('login')

    user = User.objects.get(email=request.session['email'])
    foods = Food.objects.all()

    favorites = UserFavorite.objects.filter(user=user)

    if request.method == "POST":
        food_id = request.POST.get("food_id")
        quantity = int(request.POST.get("quantity"))
        total_cal = int(request.POST.get("total_calories"))
        total_pro = float(request.POST.get("total_protein"))

        food = Food.objects.get(id=food_id)

        MealLog.objects.create(
            user=user,
            food=food,
            quantity=quantity,
            total_calories=total_cal,
            total_protein=total_pro
        )
        if request.POST.get("save_favorite"):
            # Check if already exists to avoid duplicates
            UserFavorite.objects.get_or_create(
                user=user,
                food=food,
                defaults={
                    'calories': food.calories,
                    'protein': food.protein
                }
            )
        return HttpResponse('<script> alert("Your food is logged successfully");window.location.href=/home/;  </script>')
    

        
        

    return render(request, "tracker/addfood.html", {"foods": foods ,"favorites": favorites})



from django.shortcuts import redirect, render
from .models import MealLog, User

def add_custom_food(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')

    user = User.objects.get(email=email)
    
    if request.method == 'POST':
        food_name = request.POST.get("food_name")
        qty = int(request.POST.get("custom_qty"))
        total_cal = int(request.POST.get("custom_total_calories"))
        total_protein = float(request.POST.get("custom_total_protein_val"))
        
        # Per unit values for favorites
        cal_per_unit = total_cal / qty
        pro_per_unit = total_protein / qty

        MealLog.objects.create(
            user=user,
            food_name=food_name,
            quantity=qty,
            total_calories=total_cal,
            total_protein=total_protein
        )
        
        # 🌟 CHECKBOX LOGIC: Save custom food to favorites
        if request.POST.get("save_favorite"):
            UserFavorite.objects.get_or_create(
                user=user,
                custom_name=food_name,
                defaults={
                    'calories': cal_per_unit,
                    'protein': pro_per_unit
                }
            )
        return HttpResponse('<script> alert("Your food is logged successfully");window.location.href=/home/;  </script>')
    

    return redirect("home")


def add_favorite_food(request):
    """Handle submission from Favorites tab"""
    email = request.session.get('email')
    if not email:
        return redirect('login')
    
    user = User.objects.get(email=email)
    
    if request.method == 'POST':
        quantity = int(request.POST.get("quantity", 1))
        total_cal = int(request.POST.get("total_calories"))
        total_pro = float(request.POST.get("total_protein"))
        food_name = request.POST.get("food_name")
        
        MealLog.objects.create(
            user=user,
            food_name=food_name,
            quantity=quantity,
            total_calories=total_cal,
            total_protein=total_pro
        )
        
    return redirect("home")





from django.utils.timezone import now
from .models import MealLog

def meals_view(request):
    if not request.session.get('email'):
        return redirect('login')

    user = User.objects.get(email=request.session['email'])
    meals = MealLog.objects.filter(
        user=user
    ).order_by("-date", "-id")
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    meals = MealLog.objects.filter(user=user).order_by('-date')

    context = {
        'today_meals': meals.filter(date=today),
        'week_meals': meals.filter(date__gte=start_of_week),
        'month_meals': meals.filter(date__gte=start_of_month),
    }

    return render(request, "tracker/meals.html", context)


def delete_meal(request, id):
    email = request.session.get("email")
    if not email:
        return redirect("login")

    user = models.User.objects.get(email=email)

    meal = MealLog.objects.filter(id=id, user=user).first()
    if meal:
        meal.delete()
        messages.success(request, "Meal deleted successfully")

    return redirect("home")  # or "meals"

from datetime import timedelta
from django.utils import timezone
from .models import MealLog


from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta

def report_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')

    user = User.objects.get(email=email)
    report_type = request.GET.get('type', 'daily')
    today = now().date()

    # Base queryset with date filtering
    if report_type == 'daily':
        meals = MealLog.objects.filter(user=user, date=today)
    elif report_type == 'weekly':
        start_date = today - timedelta(days=7)
        meals = MealLog.objects.filter(user=user, date__range=[start_date, today])
    elif report_type == 'monthly':
        meals = MealLog.objects.filter(
            user=user, 
            date__month=today.month, 
            date__year=today.year
        )
    else:
        meals = MealLog.objects.filter(user=user, date=today)

    # Use database aggregation for better performance
    aggregates = meals.aggregate(
        total_calories=Sum('total_calories'),
        total_protein=Sum('total_protein')
    )

    context = {
        'meals': meals.order_by('-date', '-id'),  # Newest first
        'total_calories': aggregates['total_calories'] or 0,
        'total_protein': round(aggregates['total_protein'] or 0, 1),
        'report_type': report_type,
        'user': user,
        'meals_json': list(meals.values('date', 'total_calories', 'total_protein'))
    }
    
    return render(request, 'report.html', context)







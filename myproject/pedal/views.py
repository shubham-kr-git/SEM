from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.images import ImageFile
import razorpay
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, CycleForm
from .models import Cycle, AppUser
from chat.models import Room
from django.contrib.auth import get_user_model

User = get_user_model()
orders = {}

cnt = 0
# class Cycle:

# 	def __init__(self,model,address,dop,price,img='cycle1.png'):
# 		global cnt
# 		cnt+=1
# 		self.model=model
# 		self.address=address
# 		self.dop=dop
# 		self.price=price
# 		self.img="http://localhost:8080/"+str(img)
# 		self.id=cnt
# 		print(f"{self.id} and {self.model}")
# 	def __str__(self):
# 		return f"cyle_id:{self.id} model {self.model} "


class Review:
    def __init__(self, cycle_id, content, user_name, img_link, date):
        self.cycle_id = cycle_id
        self.content = content
        self.user_name = user_name
        self.img_link = img_link
        self.date = date


class User:
    def __init__(self, user_name, email_id, contact):
        self.user_name = user_name
        self.email_id = email_id
        self.contact = contact


# cycles=[Cycle(model='hero Razor back',address='1102 MSA 1 ',dop='06/09/19',price='190',img='cycle2.jpg'),
# 		Cycle(model='hero Sprint',address='1201 MSA 2',dop='06/06/23',price='1000'),
# 		Cycle(model='atlas',address='1102 Malviya Bahvan',dop='06/06/23',price='2000'),
# 		Cycle(model='hercules',address='312 Ram Bhavan',dop='06/06/23',price='1000'),
# 		Cycle(model='hero Sprint',address='2321 Buddha Bhavan',dop='06/06/23',price='1000')
# 		]
img1 = "https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(26).webp"
img2 = "https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(23).webp"
cont = "Suspendisse quos? Tempus cras iure temporibus? Eu laudantium cubilia sem sem! Repudiandae et! Massa senectus enim minim sociosqu delectus posuere."
reviews = [
    Review(
        cycle_id=1, content=cont, user_name="Ramesh", img_link=img1, date="06/06/23"
    ),
    Review(
        cycle_id=1, content=cont, user_name="Suresh", img_link=img2, date="01/12/23"
    ),
    Review(
        cycle_id=1,
        content="Good cycle. well maintained",
        user_name="Ramesh",
        img_link=img1,
        date="06/06/23",
    ),
    Review(
        cycle_id=1,
        content="Good cycle. well maintained",
        user_name="Suresh",
        img_link=img2,
        date="01/12/23",
    ),
]


def index(request):
    cycles = Cycle.objects.filter(lend_or_sell="lend").all()
    context = {
        "cycles": cycles,
    }
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            messages.success(request, "You have been logged in!!!")

        else:
            messages.success(request, "There was an error logging in.Please try again")
            return redirect("/login")

    return render(request, "index.html", context=context)


def login_user(request):
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!!!")
    return render(request, "login.html")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            file_key = None
            for file_key in sorted(request.FILES):
                print(file_key)
                pass
            # wrapped_file = ImageFile(request.FILES[file_key])
            # filename = wrapped_file.name
            print(request.FILES)

            app_user = AppUser()
            app_user.authUser = user
            app_user.address = form.cleaned_data["address"]
            app_user.phone = form.cleaned_data["phone"]
            app_user.profile_img = request.FILES[file_key]
            app_user.save()

            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect("/")
    else:
        form = SignUpForm()
        return render(request, "register.html", {"form": form})

    return render(request, "register.html", {"form": form})


def buy(request):
    cycles = Cycle.objects.filter(lend_or_sell="sell").all()
    context = {
        "cycles": cycles,
    }
    return render(request, "buy.html", context=context)


def sell(request):
    form = CycleForm
    if request.method == "POST":
        # form = CycleForm(request.POST, request.FILES)
        # if form.is_valid():
        #     cycle = form.save(commit=False)
        #     cycle.owner_id = request.user.id # logged in user
        #     cycle.save()
        # 	#form.save()
        #     return redirect('/')
        file_key = None
        for file_key in sorted(request.FILES):
            pass
        wrapped_file = ImageFile(request.FILES[file_key])
        filename = wrapped_file.name
        from .models import Cycle, AppUser

        cycle = Cycle()
        appUser = AppUser.objects.get(authUser=request.user)
        cycle.owner = appUser
        print(request.POST["lendorSell"])
        cycle.model = request.POST["bikeModel"]
        cycle.lend_or_sell = request.POST["lendorSell"]
        cycle.dop = request.POST["dateOfPurchase"]
        cycle.price = request.POST["Price"]
        cycle.cycle_img = request.FILES[file_key]
        cycle.save()
        return redirect("/")

    # else:
    #     form = CycleForm

    return render(request, "sell.html", {"form": form})
    # return render(request, "sell.html")


def reports(request):
    return render(request, "reports.html")


def history(request):
    return render(request, "history.html")


def shops(request):
    return render(request, "shops.html")


def details(request, id):
    context = {"reviews": reviews}
    cycle = Cycle.objects.get(id=id)
    context["cycle"] = cycle
    if cycle.no_of_rents != 0:
        rating = int(cycle.total_stars / cycle.no_of_rents)
        rating_stars = [i for i in range(rating)]
    else:
        rating_stars = []
    context["rating"] = rating_stars
    # for cycle in cycles:
    # 	if cycle.id==id:
    # 		context["cycle"]=cycle
    return render(request, "details.html", context=context)


def your_bikes(request, id):
    print(request, id)
    context = {}
    # for cycle in cycles:
    # 	if cycle.id==id:
    # 		context["cycle"]=cycle
    cycle = Cycle.objects.get(id=id)
    context["cycle"] = cycle
    appUser = AppUser.objects.get(authUser=request.user)
    cycles = Cycle.objects.filter(owner_id=appUser.id).all()
    print("AppUser:", appUser.id)
    print("Cycles:", cycles)
    for cycle in cycles:
        print("Cycle Id:", cycle.id)
    rooms = Room.objects.filter(cycle_id__in=cycles).all()
    allRooms = Room.objects.all()
    print("all Rooms:", allRooms)
    for room in allRooms:
        user = User.objects.get(id=room.user_id)
        print(
            "Room name:",
            room.name,
            "Cycle ID:",
            room.cycle_id,
            "User Id:",
            room.user_id,
            "Firstname:",
            user.first_name,
        )
    for room in rooms:
        print("Room name:", room.name, "Cycle ID:", room.cycle_id)
    print("Rooms:", rooms)
    context["rooms"] = allRooms
    # bike=Cycle.objects.get(owner = appUser)
    return render(request, "your_bikes.html", context=context)


def checkout(request):
    data = request.POST
    print(data)
    cycle = {
        "cycle_model": data["cycle_model"],
        "cycle_price": int(data["cycle_price"]),
    }
    cyc_id = data["cycle_id"]
    user = User(
        user_name="Ramesh", email_id="gaurav.kumar@example.com", contact="9991232234"
    )

    client = razorpay.Client(
        auth=("rzp_test_hQHF0MU9H0s3HU", "4PJIN81Fhl66bGWTLmtkj2Ma")
    )

    payment_data = {
        "amount": int(data["cycle_price"]),
        "currency": "INR",
        "receipt": "order_rcptid_11",
    }
    payment = client.order.create(data=payment_data)

    orders[payment["id"]] = {
        "status": "payment requested",
        "cycle_id": data["cycle_id"],
    }
    print(f"Orders are as follows\n {orders} \n")
    context = {"payment": payment, "cycle": cycle, "user": user}
    import json

    # print(context)
    return render(request, "checkout.html", context=context)


@csrf_exempt
def payments(request):
    print(request.POST)
    payments_details = {
        "order_id": request.POST["razorpay_order_id"],
        "payment_id": request.POST["razorpay_payment_id"],
    }
    # client = razorpay.Client(auth=("rzp_test_hQHF0MU9H0s3HU", "4PJIN81Fhl66bGWTLmtkj2Ma"))

    # data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
    # payment = client.order.create(data=data)
    # #print(payment)
    cycle_id = orders[request.POST["razorpay_order_id"]]["cycle_id"]
    payments_details["cycle_id"] = cycle_id
    context = {"payments_details": payments_details}
    return render(request, "payments.html", context=context)

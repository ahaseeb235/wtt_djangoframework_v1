from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Workday
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'webapp/index.html', {'home': True})

# Register/Create user

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')

    context = {'form': form, 
               'page_title': 'Regsiter'}

    return render(request, 'webapp/register.html', context=context)

# login user

def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username or password is incorrect.')

    context = {'form': form, 
               'page_title': 'Login'}

    return render(request, 'webapp/login.html', context=context)



# - Dashboard

@login_required(login_url='login')
def dashboard(request):
    if request.user.is_superuser:
        records_list = Workday.objects.all()  # Superuser sees all records
    else:
        records_list = Workday.objects.filter(user=request.user)  # Regular users see their records only

    paginator = Paginator(records_list, 3)  # Showing 3 records per page
    page = request.GET.get('page', 1)
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        records = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        records = paginator.page(paginator.num_pages)

    context = {
        'records': records,
        'page_title': 'Dashboard'
    }

    return render(request, 'webapp/dashboard.html', context=context)

# Create a record 

@login_required(login_url='login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user  # Associate record with logged-in user
            record.save()
            messages.success(request, "Your record was created!")
            return redirect("dashboard")

    context = {'form': form, 'page_title': 'Create Record'}
    return render(request, 'webapp/create-record.html', context=context)

# Update a record 

@login_required(login_url='login')
def update_record(request, pk):
    if request.user.is_superuser:
        record = Workday.objects.filter(id=pk).first()  # Superuser can edit any record
    else:
        record = Workday.objects.filter(user=request.user, id=pk).first()  # Regular user restriction

    if not record:
        messages.error(request, "You don't have permission to update this record.")
        return redirect('dashboard')

    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect("view-record", pk=record.id)

    context = {'form': form, 'page_title': 'Update Record'}
    return render(request, 'webapp/update-record.html', context=context)




# - Read / View a singular record

@login_required(login_url='login')
def singular_record(request, pk):
    if request.user.is_superuser:
        record = Workday.objects.filter(id=pk).first()  # Superuser can access any record
    else:
        record = Workday.objects.filter(user=request.user, id=pk).first()  # Regular user restriction

    if not record:
        messages.error(request, "You don't have permission to view this record.")
        return redirect('dashboard')

    context = {'record': record, 'page_title': 'View Record'}
    return render(request, 'webapp/view-record.html', context=context)


# - Delete a record

@login_required(login_url='login')
def delete_record(request, pk):
    if request.user.is_superuser:
        record = Workday.objects.filter(id=pk).first()  # Superuser can delete any record
    else:
        record = Workday.objects.filter(user=request.user, id=pk).first()  # Regular user restriction

    if not record:
        messages.error(request, "You don't have permission to delete this record.")
        return redirect('dashboard')

    record.delete()
    messages.success(request, "Your record has been deleted!")
    return redirect("dashboard")


# - User logout

def logout(request):

    auth.logout(request)

    messages.success(request, "Logout success!")

    return redirect("login")


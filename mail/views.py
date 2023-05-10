import smtplib
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from .forms import UserForm
from .models import Member
from .models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.sessions.backends.db import SessionStore

# Create your views here.
def home(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())



def mail(request):
    user_id = request.session.get('user_id')

    # If user is not logged in, redirect to login page
    if not user_id:
        return redirect('login')
    mymembers = Member.objects.all().values()
    template = loader.get_template('check.html')
    context = {
        'mymembers': mymembers,
    }
    return HttpResponse(template.render(context, request))

def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('name')
        email = request.POST.get('email')
        member = Member(firstname=firstname, email=email)
        member.save()
        template = loader.get_template('success.html')
        return HttpResponse(template.render())
        
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})

def admin_register(request):
    if request.method == 'POST':
        firstname = request.POST.get('name')
        email = request.POST.get('email')
        member = Member(firstname=firstname, email=email)
        member.save()
        return redirect("/mail")
        
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})

def admin_delete(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        members = Member.objects.filter(email=email)
        if members:
            members.delete()
        return redirect('/mail')

    return render(request, 'delete.html')

def send(request):
    user_id = request.session.get('user_id')

    # If user is not logged in, redirect to login page
    if not user_id:
        return redirect('login')
    if request.method == 'POST':
        # Get the subject and message from the form
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Set up SMTP settings for Outlook
        smtp_server = "smtp.office365.com"
        port = 587
        username = "your outlook email"
        password = "your email password"
        members = Member.objects.all()
        recipient_list = [member.email for member in members]

        # Create an EmailMessage object with the necessary information
        email = EmailMessage(
            subject,
            message,
            'your outlook email', 
            recipient_list,
            
        )

        # Set the SMTP server and port
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()

        try:
            # Log in to your Outlook account using your email address and password
            server.login(username, password)

            # Send the email using the sendmail() method
            server.sendmail(email.from_email, email.to, email.message().as_string())
            message = "Email sent successfully!"

        except Exception as e:
            message = "An error occurred: " + str(e)
            print(message)
            return redirect('/error')

        finally:
            # Close the connection to the SMTP server
            server.quit()

        return redirect('mail')

    else:
        form = UserForm()
    return render(request, 'send.html', {'form': form})
    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('register')

        if (password == user.password):
            
            # user is authenticated, redirect to /mail
            request.session['user_id'] = user.id
            return redirect('mail')
        else:
            print(password)
            print(user.password)
            messages.error(request, 'Invalid username or password')
            return redirect('/')

    return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        # delete session
        SessionStore(session_key=request.session.session_key).delete()
        return redirect('login')

    return render(request, 'index.html')

def error(request):
    template = loader.get_template('error.html')
    return HttpResponse(template.render())
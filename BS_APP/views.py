from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.shortcuts import redirect

# Create your views here.

def home(request):
    return render(request,'home.html')

def user(request):

    users = User.objects.all()
    return render(request, 'users.html',{"users": users})

def transfer(request, pk):
    user = User.objects.get(pk=pk)
    receiver = User.objects.all()
    return render(request, 'transfer.html',{"user":user,"receiver":receiver})
    
def history(request):

    transactions = Transaction.objects.order_by('-created_at')
    return render(request, 'history.html', {"transactions":transactions})

def add_transfer(request, pk):

     if request.method == 'POST':

         sender = request.POST.get('sender',None)
         receiver = request.POST.get('receiver',None)
         amount = request.POST.get('amount',None)

         if int(amount) <= 0:
             user = User.objects.get(pk=pk)
             receiver = User.objects.all()
             return render(request,'transfer.html',{"warning": "Oops! Entered amount is not valid", "receiver":receiver, "user": user})

         sender_instance = User.objects.get(full_name=sender)
         curr_balance = sender_instance.current_balance
         receiver_instance = User.objects.get(full_name=receiver)
        
         if curr_balance > int(amount):
             status = 'Successful'

             receiver_instance.current_balance += int(amount)

             receiver_instance.save()

             sender_instance.current_balance -= int(amount)

             sender_instance.save()

             Transaction.objects.create(sender=sender_instance,recipient=receiver_instance,amount=amount,status=status)
             return redirect(history)
         else:
              status = 'Failed'
              Transaction.objects.create(sender=sender_instance,recipient=receiver_instance,amount=amount,status=status)
              user = User.objects.get(pk=pk)
              receiver = User.objects.all()
              return render(request,'transfer.html',{"warning": "Transaction failed because of insufficient balance :(", "receiver":receiver, "user": user})

def add_amount(request, pk):

    if request.method == 'POST':

        receiver_depot = request.POST.get('receiver_depot',None)
        amount_depot = request.POST.get('amount_depot',None)

        if int(amount_depot) <= 0:
            user = User.objects.get(pk=pk)
            receiver = User.objects.all()
            return render(request,'transfer.html',{"warning": "Oops! Entered amount is not valid", "receiver":receiver_depot, "user": user})



        receiver_instance = User.objects.get(full_name=receiver_depot)
        
        status = 'Successful'

        receiver_instance.current_balance += int(amount_depot)

        receiver_instance.save()


        Transaction.objects.create(sender=receiver_instance,recipient=receiver_instance,amount=amount_depot,status=status)
        return redirect(history)

def del_amount(request, pk):

    if request.method == 'POST':

        receiver_retrait = request.POST.get('receiver_retrait',None)
        amount_retrait = request.POST.get('amount_retrait',None)

        if int(amount_retrait) <= 0:
            user = User.objects.get(pk=pk)
            receiver = User.objects.all()
            return render(request,'transfer.html',{"warning": "Oops! Entered amount is not valid", "receiver":receiver_retrait, "user": user})

        

        receiver_instance = User.objects.get(full_name=receiver_retrait)

        curr_balance = receiver_instance.current_balance

        if curr_balance > int(amount_retrait):
        
            status = 'Successful'

            receiver_instance.current_balance -= int(amount_retrait)

            receiver_instance.save()

            Transaction.objects.create(sender=receiver_instance,recipient=receiver_instance,amount=receiver_instance,status=status)
            return redirect(history)
        else:
            status = 'Failed'
            Transaction.objects.create(sender=receiver_instance,recipient=receiver_instance,amount=receiver_instance,status=status)
            user = User.objects.get(pk=pk)
            receiver = User.objects.all()
            return render(request,'transfer.html',{"warning": "Transaction failed because of insufficient balance :(", "receiver":receiver_retrait, "user": user})



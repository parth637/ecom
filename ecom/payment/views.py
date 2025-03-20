from django.shortcuts import render ,redirect
from cart.cart import Cart
from payment.forms import ShippingForm , PaymentForm
from payment.models import ShippingAddress , Order ,OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product , Profile
import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404





def orders(request, pk):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "Access Denied")
        return redirect('home')

    order = get_object_or_404(Order, id=pk)
    items = OrderItem.objects.filter(order=pk)

    if request.method == "POST":
        status = request.POST.get("shipping_status")

        if status == "true":
            order.shipped = True
            order.date_shipped = timezone.now()
        else:
            order.shipped = False
            order.date_shipped = None  # Reset date if unshipped

        order.save()  # Save the order
        messages.success(request, "Shipping Status Updated")
        return redirect('home')

    return render(request, 'payment/orders.html', {"order": order, "items": items})

def not_shipped_dash(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "Access Denied")
        return redirect('home')

    orders = Order.objects.filter(shipped=False)

    if request.method == "POST":
        num = request.POST.get("num")
        order = get_object_or_404(Order, id=num)

        order.shipped = True
        order.date_shipped = timezone.now()
        order.save()

        messages.success(request, f"Order {order.id} marked as shipped.")
        return redirect('not_shipped_dash')

    return render(request, "payment/not_shipped_dash.html", {"orders": orders})

def shipped_dash(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "Access Denied")
        return redirect('home')

    orders = Order.objects.filter(shipped=True)

    if request.method == "POST":
        num = request.POST.get("num")
        order = get_object_or_404(Order, id=num)

        order.shipped = False
        order.date_shipped = None  # Reset date if unshipped
        order.save()

        messages.success(request, f"Order {order.id} marked as not shipped.")
        return redirect('shipped_dash')

    return render(request, "payment/shipped_dash.html", {"orders": orders})


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')

        full_name = my_shipping ['shipping_full_name']
        email = my_shipping ['shipping_email']


        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals



        if request.user.is_authenticated:

            user=request.user
            create_order =Order(user=user, full_name=full_name,email=email,shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            order_id = create_order.pk

            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key,value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id,product_id=product_id,user=user,quantity=value,price=price)
                        create_order_item.save()

            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]

            current_user = Profile.objects.filter(user__id=request.user.id)


            current_user.update(old_cart="")




            messages.success(request, "Order Placed")  # <-- Moved inside the POST condition
            return redirect('home')
        
        else:
            create_order =Order(full_name=full_name,email=email,shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()


            order_id = create_order.pk

            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key,value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id,product_id=product_id,quantity=value,price=price)
                        create_order_item.save()
            

            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]


            messages.success(request, "Order Placed")  # <-- Moved inside the POST condition
            return redirect('home')
    
    else:
        messages.error(request, "Invalid Request")  # <-- Show an error if accessed incorrectly
        return redirect('home')



def billing_info(request):
    if request.POST:
       
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        my_shipping =request.POST
        request.session['my_shipping'] = my_shipping

        billing_form = PaymentForm()

        if request.user.is_authenticated:
            return render(request, "payment/billing_info.html", {
                "cart_products": cart_products, 
                "quantities": quantities, 
                "totals": totals, 
                "shipping_info": request.POST,  # Fixed comma
                "billing_form": billing_form
            })

        else:
            return render(request, "payment/billing_info.html", {
                "cart_products": cart_products, 
                "quantities": quantities, 
                "totals": totals, 
                "shipping_info": request.POST,  # Fixed comma
                "billing_form": billing_form
            })

    else:
        messages.success(request, "Access Denied")
        return redirect('home')



def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    if request.user.is_authenticated:
		# Checkout as logged in user
		# Shipping User
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		# Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form })
    else:
		# Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form } )
    

def payment_success(request):
    return render(request,"payment/payment_success.html",{})

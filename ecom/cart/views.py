from django.shortcuts import render ,get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from store.models import Product
import json
from django.contrib import messages  # ✅ Ensure this is imported







def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities , "totals":totals})



    
    
def cart_add(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)

        # ✅ Correct way to get cart length
        cart_quantity = len(cart)

        # ✅ Messages should be before return
        messages.success(request, ("Product added to cart"))

        return JsonResponse({'qty': cart_quantity})

    return JsonResponse({'error': 'Invalid request'}, status=400)
         









    

def cart_delete(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		# Call delete Function in Cart
		cart.delete(product=product_id)

		response = JsonResponse({'product':product_id})
		# return redirect('cart_summary')
		messages.success(request, ("Item Deleted From Shopping Cart..."))
		return response



def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        # Log POST data for debugging
        print("POST Data:", json.dumps(request.POST.dict(), indent=4))

        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        # Validate inputs
        if not product_id or not product_qty or not product_qty.strip().isdigit() or not product_id.strip().isdigit():
            return JsonResponse({'error': 'Invalid product ID or quantity'}, status=400)

        # Convert to integers after validation
        product_id = int(product_id)
        product_qty = int(product_qty)

        # Update cart
        cart.update(product=product_id, quantity=product_qty)
        messages.success(request,( "Your Cart has Been Updated..."))


        return JsonResponse({'qty': product_qty})

    return JsonResponse({'error': 'Invalid request'}, status=400)
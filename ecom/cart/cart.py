from store.models import Product, Profile

class Cart:
    
    def __init__(self, request):
        self.session = request.session
        self.request = request  # Store request object

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key!  Create one!
        if not cart:
            cart = self.session['session_key'] = {}

        self.cart = cart  # ✅ Ensure self.cart is always assigned

    def __len__(self):  # ✅ Yeh method add karna hai
        return len(self.cart)
    
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
		# Logic
        if product_id in self.cart:
            pass
        else:
			#self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
            self.session.modified = True

		# Deal with logged in user
        if self.request.user.is_authenticated:
			# Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
    
    

    



    def add(self, product , quantity ):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass  # Product is already in cart, do nothing
        else:
            # self.cart[product_id] = {'price': str(product.price)}
             self.cart[product_id] = int(product_qty)

        self.session.modified = True  # ✅ Ensure session is updated
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart=str(carty))


    def cart_total(self):
      product_ids = self.cart.keys()
      products = Product.objects.filter(id__in=product_ids)
      quantities = self.cart
      total = 0

      for key, value in quantities.items():
         key = int(key)
         for product in products:
           if product.id == key:
             print(f"Product: {product.name}, Sale: {product.is_sale}, Price: {product.price}, Sale Price: {product.sale_price}")  # Debug
             if product.is_sale:
                total += product.sale_price * value
             else:
                   total += product.price * value
      print(f"Total Cart Price: {total}")  # Debug
      return total  # Yeh return loop ke bahar hona chahiye


    def get_prods(self):
          product_ids = self.cart.keys()
          products = Product.objects.filter(id__in=product_ids)
          return products
    

    def get_quants(self):
        quantities = self.cart
        return quantities
    

    def update(self, product, quantity):
         product_id = str(product)
         product_qty = int(quantity)

         {'4':3 , '2':5}

    # Get cart
         ourcart = self.cart
    # Update Dictionary/cart
         ourcart[product_id] = product_qty

         self.session.modified = True

         if self.request.user.is_authenticated:
			# Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
    
    
         thing = self.cart
         return thing
    
    def delete(self, product):
        product_id = str(product)
        # delete from dictniory

        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

        if self.request.user.is_authenticated:
			# Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
    
    
            




		# Deal with logged in user
		# if self.request.user.is_authenticated:
			# Get the current user profile
			# current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
			# carty = str(self.cart)
			# carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
			# current_user.update(old_cart=str(carty))


		 





		
		

	

'''def cart_total(self):
		# Get product IDS
		product_ids = self.cart.keys()
		# lookup those keys in our products database model
		products = Product.objects.filter(id__in=product_ids)
		# Get quantities
		quantities = self.cart
		# Start counting at 0
		total = 0
		
		for key, value in quantities.items():
			# Convert key string into into so we can do math
			key = int(key)
			for product in products:
				if product.id == key:
					if product.is_sale:
						total = total + (product.sale_price * value)
					else:
						total = total + (product.price * value)



		return total '''




 
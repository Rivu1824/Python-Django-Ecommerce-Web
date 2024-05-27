from django.shortcuts import *
from django.views.generic import *
from .models import *
from django.contrib.auth import *
from .forms import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls import reverse
from .mixins import LogoutRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views import generic


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        categories = Categorie.objects.all()
        products = Product.objects.filter(status='PUBLISH')
        logo = Logo.objects.first()
        banners = Banner.objects.all()
        subcategories = SubCategorie.objects.all()
        third_categories = ThirdCategorie.objects.all()

        context = {
            'categories': categories,
            'products': products,
            'logo': logo,
            'banners': banners,
            'subcategories': subcategories,
            'third_categories': third_categories,
        }

        return render(request, self.template_name, context)


@method_decorator(never_cache, name='dispatch')
class Login(LogoutRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        form = LoginForm()
        categories = Categorie.objects.all()
        products = Product.objects.filter(status='PUBLISH')
        logo = Logo.objects.first()
        banners = Banner.objects.all()
        subcategories = SubCategorie.objects.all()
        third_categories = ThirdCategorie.objects.all()

        context = {
            "form": form,
            "categories": categories,
            "products": products,
            "logo": logo,
            "banners": banners,
            "subcategories": subcategories,
            "third_categories": third_categories,
        }
        return render(self.request, 'account/login.html', context)

    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)

        if form.is_valid():
            user = authenticate(
                self.request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                # Set is_active to True when the user logs in
                user.is_active = True
                user.save(update_fields=['is_active'])

                login(self.request, user)
                return redirect('home')
            else:
                messages.warning(self.request, "Wrong credentials")
                return redirect('login')

        return render(self.request, 'account/login.html', {"form": form})


class RegisterView(View):
    template_name = 'account/Register.html'

    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        categories = Categorie.objects.all()
        products = Product.objects.filter(status='PUBLISH')
        logo = Logo.objects.first()
        banners = Banner.objects.all()
        subcategories = SubCategorie.objects.all()
        third_categories = ThirdCategorie.objects.all()

        return render(request, self.template_name, {
            'form': form,
            'categories': categories,
            'products': products,
            'logo': logo,
            'banners': banners,
            'subcategories': subcategories,
            'third_categories': third_categories,
        })

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            # Create user
            user = form.save()

            # Log in the user
            authenticated_user = authenticate(request, username=user.username, password=form.cleaned_data['password1'])
            login(request, authenticated_user)

            # Send welcome email

            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please check the form.')
            return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Logout successful.')
        return redirect('home')
    

class UserDetailView(DetailView):
    model = User
    template_name = 'account/user_profile.html'
    context_object_name = 'user'

    def get_queryset(self):
        return User.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add additional model data to the context
        context['categories'] = Categorie.objects.all()
        context['subcategories'] = SubCategorie.objects.all()
        context['products'] = Product.objects.all()
        context['product_specifications'] = Product_Specification.objects.all()
        context['product_points'] = Product_point.objects.all()
        context['logo'] = Logo.objects.first()
        context['third_categories'] = ThirdCategorie.objects.all()

        return context

class CategorieListView(View):
    template_name = 'function/Categorie.html'

    def get(self, request, *args, **kwargs):
        categories = Categorie.objects.all()

        context = {
            'categories': categories,
            'subcategories': SubCategorie.objects.all(),
            'products': Product.objects.all(),
            'product_specifications': Product_Specification.objects.all(),
            'product_points': Product_point.objects.all(),
            'logo': Logo.objects.first(),
            'third_categories': ThirdCategorie.objects.all(),  # Add ThirdCategorie if needed
        }

        return render(request, self.template_name, context)
    
class CategorieDetailView(View):
    template_name = 'function/Categorie-details.html'

    def get(self, request, slug):
        categories = Categorie.objects.all()
        category = get_object_or_404(Categorie, slug=slug)
        logo = Logo.objects.first()
        subcategories = SubCategorie.objects.filter(parent_categorie=category)
        products = Product.objects.filter(categories__parent_subcategorie__parent_categorie=category)
        third_categories = ThirdCategorie.objects.filter(parent_subcategorie__parent_categorie=category)

        context = {
            'categories':categories,
            'category': category,
            'logo': logo,
            'subcategories': subcategories,
            'products': products,
            'third_categories': third_categories,
        }

        return render(request, self.template_name, context)



class SubCategorieListView(View):
    template_name = 'function/sub-Categorie.html'

    def get(self, request, *args, **kwargs):
        subcategories = SubCategorie.objects.all()

        context = {
            'subcategories': subcategories,
            'categories': Categorie.objects.all(),
            'products': Product.objects.all(),
            'product_specifications': Product_Specification.objects.all(),
            'product_points': Product_point.objects.all(),
            'logo': Logo.objects.first(),
            'third_categories': ThirdCategorie.objects.all(),
        }

        return render(request, self.template_name, context)


class SubCategorieDetailView(View):
    template_name = 'function/sub-Categorie-details.html'

    def get(self, request, slug):
        subcategories = SubCategorie.objects.all()
        subcategorie = get_object_or_404(SubCategorie, slug=slug)
        products = Product.objects.filter(categories__parent_subcategorie=subcategorie)
        third_categories = ThirdCategorie.objects.filter(parent_subcategorie=subcategorie)
        categories = Categorie.objects.all()
        logo = Logo.objects.first()

        context = {
            'subcategories': subcategories,
            'subcategorie': subcategorie,
            'products': products,
            'third_categories': third_categories,
            'categories': categories,
            'logo': logo,
        }

        return render(request, self.template_name, context)





class ThirdCategorieListView(View):
    template_name = 'function/Third-Categorie.html'

    def get(self, request, *args, **kwargs):
        subcategories = SubCategorie.objects.all()

        context = {
            'subcategories': subcategories,
            'categories': Categorie.objects.all(),
            'products': Product.objects.all(),
            'product_specifications': Product_Specification.objects.all(),
            'product_points': Product_point.objects.all(),
            'logo': Logo.objects.first(),
            'third_categories': ThirdCategorie.objects.all(),  # Add ThirdCategorie if needed
        }

        return render(request, self.template_name, context)


class ThirdCategorieDetailView(View):
    template_name = 'function/Third-Categorie-details.html'

    def get(self, request, slug):
        third_categorie = get_object_or_404(ThirdCategorie, slug=slug)

        # Assuming SubCategorie has a parent_categorie field
        subcategories = SubCategorie.objects.filter(parent_categorie=third_categorie.parent_subcategorie.parent_categorie)

        # Assuming Product has a categories__parent_subcategorie__parent_categorie field
        products = Product.objects.filter(categories__parent_subcategorie__parent_categorie=third_categorie.parent_subcategorie.parent_categorie)

        context = {
            'third_categorie': third_categorie,
            'subcategories': subcategories,
            'products': products,
            'categories': Categorie.objects.all(),
            'logo': Logo.objects.first(),
        }

        return render(request, self.template_name, context)



class ProductlistPageView(ListView):
    template_name = 'function/shop.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Categorie.objects.all()
        logo = Logo.objects.first()
        subcategories = SubCategorie.objects.all()
        third_categories = ThirdCategorie.objects.all()
        products = Product.objects.filter(status='PUBLISH')

        context.update({
            'categories': categories,
            'logo': logo,
            'subcategories': subcategories,
            'third_categories': third_categories,
            'products': products,
        })

        return context



class ProductDetailsPageView(View):
    template_name = 'function/single-product-sidebar.html'

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        logo = Logo.objects.first()
        categories = Categorie.objects.all()
        subcategories = SubCategorie.objects.all()
        third_categories = ThirdCategorie.objects.all()
        product_specification = Product_Specification.objects.filter(Product=product).first()
        product_points = Product_point.objects.filter(Product=product)

        context = {
            'product': product,
            'logo': logo,
            'categories': categories,
            'subcategories': subcategories,
            'third_categories': third_categories,
            'product_specification': product_specification,
            'product_points': product_points,
            'cart_form': CartForm(),
        }

        return render(request, self.template_name, context)

class CartPageView(LoginRequiredMixin, View):
    template_name = 'account/cart.html'

    def get(self, request, *args, **kwargs):
        categories = Categorie.objects.all()
        subcategories = SubCategorie.objects.all()
        third_categories = ThirdCategorie.objects.all()
        products = Product.objects.all()
        logo = Logo.objects.first() 
        user_cart_items = OrderItem.objects.filter(user=request.user, ordered=False)

        # Calculate the initial total price
        total_price = sum(item.get_final_price() for item in user_cart_items)

        context = {
            'cart_items': user_cart_items,
            'categories': categories,
            'subcategories': subcategories,
            'third_categories': third_categories,
            'products': products,
            'logo': logo,
            'total_price': total_price,
        }

        if products.exists():
            context['product_id'] = products.first().id

        return render(request, self.template_name, context)

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(pk=product_id)
            color = request.POST.get('color')
            size = request.POST.get('size')
            quantity = request.POST.get('quantity')

            if not quantity.isdigit():
                raise ValueError("Invalid quantity provided.")

            order_item, created = OrderItem.objects.get_or_create(
                user=request.user,
                item=product,
                ordered=False,
                color=color,
                size=size,
                quantity=int(quantity),
            )

            if created:
                messages.success(request, f"{product.title} added to your cart.")
            else:
                order_item.quantity += 1
                messages.success(request, f"{product.title} quantity updated in your cart.")

            order_item.save()
        except Product.DoesNotExist:
            messages.error(request, f"Product with ID {pk} not found.")
            return redirect('home')
        except ValueError:
            messages.error(request, "Invalid quantity provided.")
        except Exception as e:
            messages.error(request, f"Error adding product to cart: {e}")

        return redirect('cart')



class AddSingleItemFromCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            order_item = get_object_or_404(OrderItem, id=pk, user=request.user, ordered=False)

            order_item.quantity += 1
            order_item.save()
            
            messages.success(request, f"{order_item.item.title} quantity updated in your cart.")

            return redirect('cart')
        except OrderItem.DoesNotExist:
            messages.error(request, f"Order item with ID {pk} not found.")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Error updating product quantity in cart: {e}")
            return redirect('cart')



class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order_item = get_object_or_404(OrderItem, id=pk, user=request.user, ordered=False)

        try:
            order_item.delete()
            messages.success(request, f"{order_item.item.title} removed from your cart.")
        except Exception as e:
            messages.error(request, f"Error removing product from cart: {e}")

        return redirect('cart')


class RemoveSingleItemFromCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order_item = get_object_or_404(OrderItem, id=pk, user=request.user, ordered=False)

        try:
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.success(request, f"{order_item.item.title} quantity updated in your cart.")
            else:
                order_item.delete()
                messages.success(request, f"{order_item.item.title} removed from your cart.")
        except Exception as e:
            messages.error(request, f"Error removing product from cart: {e}")

        return redirect('cart')



class GetCouponView(View):
    def post(self, request):
        form = CouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code=code)
                user_cart_items = OrderItem.objects.filter(user=request.user, ordered=False)

                for item in user_cart_items:
                    item.coupon = coupon
                    item.save()

                total_price = sum(item.get_final_price() for item in user_cart_items)

                messages.success(request, "Coupon applied successfully")

                return redirect("cart")
            except ObjectDoesNotExist:
                messages.error(request, "This coupon does not exist")

        return redirect("cart")



class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['logo'] = Logo.objects.first()
        context['categories'] = Categorie.objects.all()
        context['subcategories'] = SubCategorie.objects.all()
        context['products'] = Product.objects.all()


        return context
    


class SendMessageView(View):
    template_name = 'contact.html'
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        logo = Logo.objects.first()
        categories = Categorie.objects.all()
        subcategories = SubCategorie.objects.all()
        return render(request, self.template_name, {'form': form, 'logo': logo, 'categories': categories,'subcategories':subcategories})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, 'Your message was sent successfully.')
            return redirect(self.get_success_url())
        else:
            messages.error(request, 'There was an error in your submission. Please correct the errors below.')
            logo = Logo.objects.first()
            return render(request, self.template_name, {'form': form, 'logo': logo})

    def get_success_url(self):
        return reverse_lazy('login')
    


class CheckoutView(View):
    template_name = 'account/checkout.html'

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            categories = Categorie.objects.all()
            subcategories = SubCategorie.objects.all()
            third_categories = ThirdCategorie.objects.all()
            logo = Logo.objects.first() 
            user_cart_items = OrderItem.objects.filter(user=request.user, ordered=False)
            total_price = sum(item.get_final_price() for item in user_cart_items)

            context = {
                'product': product,
                'cart_items': user_cart_items,
                'total_price': total_price,
                'subcategories': subcategories,
                'third_categories': third_categories,
                'categories': categories,
                'logo': logo,
            }

            return render(request, self.template_name, context)

        except ObjectDoesNotExist:
            messages.error(request, "Product not found")
            return redirect("cart")

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            user_cart_items = OrderItem.objects.filter(user=request.user, ordered=False)

            transaction = Order.objects.create(
                user=request.user,
                transaction_id=generate_unique_transaction_id(),
                amount=sum(item.get_final_price() for item in user_cart_items),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                mobile=request.POST.get('mobile'),
                address=request.POST.get('address'),
                city=request.POST.get('city'),
                payment_status='Pending',
            )

            transaction.product.add(*user_cart_items)
            user_cart_items.update(ordered=True)

            messages.success(request, "Order placed successfully")

            # Redirect to transaction_detail with the transaction ID
            return redirect(reverse('transaction_detail', args=[transaction.transaction_id]))

        except ObjectDoesNotExist:
            messages.error(request, "Product not found")
            return redirect("cart")





class TransactionDetailView(View):
    template_name = 'account/transaction_detail.html'

    def get(self, request, transaction_id):
        try:
            # Retrieve the order using the transaction ID
            order = get_object_or_404(Order, transaction_id=transaction_id, user=request.user)

            # Retrieve additional data
            logo = Logo.objects.first()
            categories = Categorie.objects.all()
            subcategories = SubCategorie.objects.all()
            third_categories = ThirdCategorie.objects.all()

            context = {
                'order': order,
                'logo': logo,
                'categories': categories,
                'subcategories': subcategories,
                'third_categories': third_categories,
            }

            return render(request, self.template_name, context)

        except Order.DoesNotExist:
            messages.error(request, "Order not found")
            return redirect("home")

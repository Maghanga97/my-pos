from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db.models import Sum, Max
import datetime

# Create your views here.

def admin_dashboard(request):
	bills = Bill.objects.all()
	bill_transactions = BillTransaction.objects.all()
	total_amount_received = sum([item.amount_paid for item in bill_transactions])
	total_sales_value = sum([bill.get_bill_total for bill in bills])
	amount_due = total_sales_value - total_amount_received
	bill_items = BillItem.objects.values("bill__id", "bill__customer__first_name", "bill__payment_method__name").annotate(bill_total=Sum("sum_total")).order_by("-bill_total")[:5]
	billed_products = BillItem.objects.values("product__id", "product__name").annotate(quantity_sold=Sum("quantity"), sale_value=Sum("sum_total")).order_by("-quantity_sold")[:5]

	context_data = {"bills": bills,
					"bill_items": bill_items,
					"top_products": billed_products,
					"sales_total": total_sales_value,
					"amount_due": amount_due,
					"total_amount_paid": total_amount_received, 
					"transactions": bill_transactions,
					}
	return render(request, "store/index.html", context_data)

def cashier_dashboard(request):
	bills = Bill.objects.all()
	context_data = {"bills": bills}

	return render(request, "store/cashier.html", context_data)

def billing(request, product_id=None):
	context_data = {"products": None, "product": None, "active_bill": None}
	try:
		active_bill_id = request.session["bill_id"]
		active_bill = Bill.objects.get(id=active_bill_id)

	except:
		active_bill = None

	# search for product
	try:
		product_name = request.GET.get("product-name")
		products = Inventory.objects.filter(name__icontains=product_name)
		context_data["products"] = products
	except:
		pass

	if product_id is not None:
		product = Inventory.objects.get(id=product_id)
		context_data["product"] = product

	if request.method == "POST":	
		# create new product
		product_name = request.POST.get("product-name").capitalize()
		product_quantity = request.POST.get("quantity-bought")
		product_price = request.POST.get("product-price")
		bill_product, created = Inventory.objects.get_or_create(name=product_name, price=product_price)
		new_bill_total = float(bill_product.price)*int(product_quantity)
		if active_bill is not None:
			if active_bill.bill_items.all().filter(product=bill_product).exists():
				get_bill_item = BillItem.objects.get(product=bill_product, bill=active_bill)
				get_bill_item.quantity += int(product_quantity)
				get_bill_item.sum_total += new_bill_total
				get_bill_item.save()
			else:
				new_bill_item = BillItem.objects.create(product=bill_product, 
														bill=active_bill, 
														quantity=product_quantity,
														sum_total=new_bill_total,
														)
		else:
			active_bill = Bill.objects.create(customer=None)
			new_bill_item = BillItem.objects.create(product=bill_product, 
													bill=active_bill, 
													quantity=product_quantity,
													sum_total=new_bill_total,
													)
			request.session["bill_id"] = active_bill.id
		return redirect("/billing/")
	context_data["active_bill"] = active_bill

	return render(request, "store/create-sale.html", context_data)


def checkout(request, bill_id=None):
	context_data = {}
	customer_form = CustomerForm(request.POST or None)
	try:
		active_bill_id = request.session["bill_id"]
		active_bill = Bill.objects.get(id=active_bill_id)
	except:
		active_bill = None
	context_data["active_bill"] = active_bill
	if request.method == "POST":
		get_payment_method = request.POST.get("payment_method")
		get_invoice = request.POST.get("invoice_no")
		get_amount_paid = request.POST.get("amount_paid")
		new_payment_method, created = PaymentMethod.objects.get_or_create(name=get_payment_method)
		if customer_form.is_valid():
			first_name = customer_form.cleaned_data["first_name"]
			last_name = customer_form.cleaned_data["last_name"]
			customer_phone = customer_form.cleaned_data["phone"]
			if Customer.objects.filter(first_name=first_name, last_name=last_name, phone=customer_phone).exists():
				bill_customer = Customer.objects.filter(first_name=first_name, last_name=last_name, phone=customer_phone).first()
			else:
				bill_customer = customer_form.save()
		active_bill.invoice_no = get_invoice
		active_bill.payment_method = new_payment_method
		active_bill.customer = bill_customer
		active_bill.save()

		try:
			if int(get_amount_paid) > 0:
				new_transaction = BillTransaction.objects.create(bill=active_bill, amount_paid=get_amount_paid)
		except:
			pass
			
		return redirect("/checkout/")
	return render(request, "store/checkout.html", context_data)

def sales_invoice(request, bill_id):
	context_data = {}
	try:
		del request.session["bill_id"]
	except:
		pass
	active_bill = Bill.objects.get(id=bill_id)
	active_bill.processed = True
	active_bill.save()
	context_data["active_bill"] = active_bill
	context_data["date_now"] = datetime.datetime.now()
	context_data["amount_due"] = active_bill.get_bill_total - active_bill.get_total_amount_paid
	return render(request, "store/invoice.html", context_data)
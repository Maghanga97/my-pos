from django.db import models
import uuid

# Create your models here.
class Store(models.Model):
	name = models.CharField(max_length=25, unique=True)
	description = models.CharField(max_length=255, blank=True)
	logo = models.FileField(upload_to="images/", null=True, blank=True)
	date_updated = models.DateTimeField(auto_now=True)
	date_created = models.DateTimeField(auto_now_add=True)

class PaymentMethod(models.Model):
	name = models.CharField(max_length=25, unique=True)
	description = models.CharField(max_length=255, blank=True)
	date_updated = models.DateTimeField(auto_now=True)
	date_created = models.DateTimeField(auto_now_add=True)

class TransactionType(models.Model):
	name = models.CharField(max_length=25, unique=True)
	description = models.CharField(max_length=255, blank=True)
	date_updated = models.DateTimeField(auto_now=True)
	date_created = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
	name = models.CharField(max_length=25, unique=True)
	description = models.CharField(max_length=255, blank=True)
	logo = models.FileField(upload_to="images/", null=True, blank=True)
	date_updated = models.DateTimeField(auto_now=True)
	date_created = models.DateTimeField(auto_now_add=True)

class Inventory(models.Model):
	store = models.ForeignKey(Store, related_name="products", on_delete=models.CASCADE, null=True, blank=True)
	category = models.ForeignKey(Category, related_name="products", on_delete=models.SET_NULL, null=True, blank=True)
	name = models.CharField(max_length=25, unique=True)
	description = models.CharField(max_length=255, blank=True)
	price = models.FloatField(blank=True, null=True)
	stock = models.IntegerField(blank=True, null=True)
	date_updated = models.DateTimeField(auto_now=True)
	date_created = models.DateTimeField(auto_now_add=True)

	def is_in_stock(self):
		if self.stock > 0:
			return True
		return False

class Customer(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone = models.CharField(max_length=15, null=True, blank=True)
	email = models.EmailField(max_length=255, null=True, blank=True)
	date_updated = models.DateTimeField(auto_now=True)
	date_created = models.DateTimeField(auto_now_add=True)

class Bill(models.Model):
	customer = models.ForeignKey(Customer, related_name="bills", on_delete=models.CASCADE, null=True, blank=True)
	payment_method = models.ForeignKey(PaymentMethod, related_name="bills", on_delete=models.CASCADE, null=True, blank=True)
	paid = models.BooleanField(default=False)
	invoice_no = models.CharField(max_length=25, blank=True, null=True)
	processed = models.BooleanField(default=False)
	date_updated = models.DateTimeField(auto_now=True)
	date_created = models.DateTimeField(auto_now_add=True)

	@property
	def get_bill_total(self):
		total = sum([item.sum_total for item in self.bill_items.all()])
		return total

	@property
	def get_total_amount_paid(self):
		total = sum([item.amount_paid for item in self.bill_transactions.all()])
		return total

class BillItem(models.Model):
	product = models.ForeignKey(Inventory, related_name="bill_items", on_delete=models.CASCADE, null=True)
	bill = models.ForeignKey(Bill, related_name="bill_items", on_delete=models.CASCADE)
	quantity = models.IntegerField(default=0)
	sum_total = models.FloatField(default=0)
	date_added = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

class ReturnedItem(models.Model):
	product = models.ForeignKey(Inventory, related_name="returned_items", on_delete=models.CASCADE, null=True)
	bill = models.ForeignKey(Bill, related_name="returned_items", on_delete=models.CASCADE)
	quantity = models.IntegerField(default=0)
	date_returned = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

class BillTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill = models.ForeignKey(Bill, related_name="bill_transactions", on_delete=models.CASCADE)
    amount_paid = models.FloatField()
    transaction_type = models.ForeignKey(TransactionType, related_name="bill_transactions", on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
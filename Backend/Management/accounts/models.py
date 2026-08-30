from django.db import models

class Admin(models.Model):
    keycloak_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=100,default="")
    last_name = models.CharField(max_length=100,default="")
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100, blank=True)

    roles = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_authenticated(self):
        return True

class Request(models.Model):
    request_id = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    employee_id = models.CharField(max_length=100)
    employee_name = models.CharField(max_length=150,blank=True)
    employee_email = models.EmailField(blank=True)
    department = models.CharField(max_length=100)
    reason = models.TextField(blank=True)
    remarks = models.TextField(blank=True)
    date_issued = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=150)
    based_on_stock = models.BooleanField(default=False)
    overdue_email_sent = models.BooleanField(default=False)
    



class RequestItem(models.Model):
    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        related_name="items"
    )
    status = models.CharField(max_length=50, default="Pending")
    accessory_req = models.CharField(max_length=150)
    brand_model = models.CharField(max_length=150, blank=True)
    serial_Number = models.CharField(max_length=150, blank=True)
    quantity = models.IntegerField()

class Equipment(models.Model):
    CATEGORY_CHOICES = [
        ("Laptop", "Laptop"),
        ("Desktop", "Desktop"),
        ("Monitor", "Monitor"),
        ("Keyboard", "Keyboard"),
        ("Mouse", "Mouse"),
        ("Headset", "Headset"),
        ("WebCam", "WebCam"),
        ("Other", "Other"),
    ]
    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Issued", "Issued"),
        ("Maintenance", "Maintenance"),
        ("Lost", "Lost"),]
    category = models.CharField(max_length=100,choices=CATEGORY_CHOICES)
    brand_model = models.CharField(max_length=150,blank=True)
    serial_number = models.CharField(max_length=150,blank=True)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default="Available")
    location = models.CharField(max_length=150,blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.category} - {self.brand_model}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


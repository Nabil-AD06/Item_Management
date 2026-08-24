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



class RequestItem(models.Model) :
    request = models.ForeignKey(
        Request,
        on_delete = models.CASCADE
    )
    status = models.CharField(max_length=50, default="Pending")
    accessory_req = models.CharField(max_length=150)
    brand_model = models.CharField(max_length=150 , blank=True)
    serial_Number = models.CharField(max_length=150 , blank=True)
    quantity = models.PositiveIntegerField()
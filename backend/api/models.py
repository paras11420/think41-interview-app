from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class User(models.Model):                      # ← CSV = users.csv
    id           = models.IntegerField(primary_key=True)       # id
    first_name   = models.CharField(max_length=50)             # first_name
    last_name    = models.CharField(max_length=50)             # last_name
    email        = models.EmailField()                         # email
    age          = models.PositiveSmallIntegerField()          # age
    gender       = models.CharField(max_length=1)              # gender  (M/F)
    state        = models.CharField(max_length=50)             # state
    street       = models.CharField(max_length=120)            # street_address
    postal_code  = models.CharField(max_length=20)             # postal_code
    city         = models.CharField(max_length=50)             # city
    country      = models.CharField(max_length=50)             # country
    latitude     = models.DecimalField(max_digits=10, decimal_places=6)   # latitude
    longitude    = models.DecimalField(max_digits=10, decimal_places=6)   # longitude
    traffic_src  = models.CharField(max_length=30)             # traffic_source
    created_at   = models.DateTimeField()                      # created_at

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Order(models.Model):                    # ← CSV = orders.csv
    order_id     = models.IntegerField(primary_key=True)       # order_id
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    status       = models.CharField(max_length=20)             # status
    gender       = models.CharField(max_length=1)              # gender (redundant – keep for demo)
    created_at   = models.DateTimeField()                      # created_at
    returned_at  = models.DateTimeField(null=True, blank=True) # returned_at
    shipped_at   = models.DateTimeField(null=True, blank=True) # shipped_at
    delivered_at = models.DateTimeField(null=True, blank=True) # delivered_at
    num_of_item  = models.PositiveSmallIntegerField()          # num_of_item

    def __str__(self):
        return f'Order {self.order_id}'

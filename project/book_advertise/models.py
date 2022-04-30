from operator import mod
from tabnanny import verbose
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.template.defaultfilters import slugify



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER = [
        ('M',  'Male') , 
        ('F',  'Female')
    ]
    profile_id = models.BigAutoField(primary_key=True)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    email = models.EmailField()
    phoneNumber = PhoneNumberField(null = False, blank = False).formfield()
    gender = models.CharField(choices=GENDER, default='None', max_length=10)
    
    
    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()
        
    def __str__(self):
        return self.user.username
    
class Categories(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    
class Book(models.Model):
    book_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=False, null=False)
    image = models.ImageField(upload_to='img', blank=True, null=True)
    author = models.CharField(max_length=100, blank=False, null=False)
    publisher = models.CharField(max_length=100)
    copies = models.IntegerField()
    available = models.BooleanField()
    average_rating = models.DecimalField(decimal_places=1, max_digits = 2)
    category_id = models.ForeignKey(Categories, related_name='books', on_delete=models.DO_NOTHING)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
   
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    
    def __str__(self):
       return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.first_name)
        super(Book, self).save(*args, **kwargs)
    
    
 
class BookReturnedRecord(models.Model):
    borrower_id =  models.BigAutoField(primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.DO_NOTHING)   
    stud_id = models.ForeignKey(Profile, related_name='borrows', on_delete=models.DO_NOTHING)
    taken_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned = models.BooleanField()
        
   
class BookRating(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    
      
class Login(models.Model):
    user_id = models.IntegerField()
    action = models.BooleanField()   
    action_date = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   
class CartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)    

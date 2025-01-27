from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    
    # This is for clients creating accounts
    
  def create_user(self, first_name, last_name, username, email, password=None):
      if not email:
          raise ValueError('user must have an email address')
      
      if not username:
          raise ValueError('user must have a username')
      
      user = self.model(
          email = self.normalize_email(email),
          username = username,
          first_name = first_name,
          last_name = last_name,
      )
      user.set_password(password)
      user.save(using=self._db)
      return user
  
  # This is Superuser account model
  
  def create_superuser(self, first_name, last_name, username, email, password=None):
      user = self.create_user(
           email = self.normalize_email(email),
           username = username,
           password = password,
           first_name = first_name,
           last_name = last_name,
      )
      user.is_admin = True
      user.is_active = True
      user.is_staff = True
      user.is_superadmin = True
      user.save(using=self._db)
      return user
      



class User(AbstractBaseUser):
    FARM = 1
    CUSTOMER = 2
    
    ROLE_CHOICE = (
        (FARM, 'Farm'),
        (CUSTOMER, 'Customer'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True) # unique=True ensures the field is filled out 
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=11)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True) #null=True handles any errors
    
    
    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    Modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    
    # define login cridential
    USERNAME_FIELD = 'email'  #user login- email
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = UserManager()  #tells the application which user manager to use
    
    def __str__(self):
        return self.email # Displays these fields in the user admin
    
    # Permissions 
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    # Setting restritions for the customer and Farm, the directs them to the right dashboard
    def get_role(self):
        if self.role == 1:
            user_role = 'Farm'
            return user_role
        elif self.role == 2:
            user_role = 'Customer'
            return user_role
        
    # create user registration form 
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True) # one to one allows only single user profile
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photo', blank=True, null=True)
    address_line_1 = models.CharField(max_length=50, blank=True, null=True)
    address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.user.email
    
    



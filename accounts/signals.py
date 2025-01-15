from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile 




    # POST SAVE SIGNAL
      #Creating a receiver alert
      
# another way of connection is below, check the header for the imported document to make this work      
@receiver(post_save, sender=User) 

def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print('user profile is created')  
    else:
        
        
          # User already exists, update profile if needed (optional)
          # ... (your logic for updating the profile)
              print('User is updated (or no profile creation needed)')
              print('user is updated')
        
        
        
        # THIS WAS FROM THE TUTORIA BUT IT WAS GIVING ME AN ERROR WHEN I CLICK SAVE ON THE PROFILE PANEL
#        try:
 #            profile = UserProfile.objects.create(user=instance)
  #           profile.save()
   #     except:
            # create user profile if it doesnt exist
    #        profile = UserProfile.objects.create(user=instance)
     #       print('profile does not exist but i created one ')
      #  print('user is updated')
        
        
# Pre_save alert
        
@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, 'user profile being created')

#post_save.connect(post_save_create_profile_receiver, sender=User)

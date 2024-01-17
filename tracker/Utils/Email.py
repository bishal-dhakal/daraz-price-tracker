from django.core.mail import send_mail
import os

class Email:
    def __init__(self):
        pass

    #TODO: doesnot send email due to .env problem and i dont know the problem yet
    def email(self,email,title,username,price):
        subject = "Price Tracker Alert Email"
        message = f"""Hey {username},
        
                    Hurry up, the price for {title} have dropped @Rs.{price}
                    
                    Have a Great day,
                    Your Well Wisher."""
        sender = os.environ.get('EMAIL_HOST_USER')
        recipient = [email]
        try:
            send_mail(subject, message, sender,
                        recipient, fail_silently=True)
        except Exception as e:
            return f"Error while sending email:{e}"
        print("Alert email to notify desired price in sent successfully")

        return None

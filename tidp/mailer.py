
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse

def task_leader_mail(instance, usermail):
    subject, from_email, to = 'A new task assigned to you', settings.DEFAULT_FROM_EMAIL, instance.contact_email

    text_content = 'Dear {instance.contact_person},\n\n You are invited by {usermail} to participate in a BIM project titled {instance.project.name} through TIDP/MIDP portal where your Task Information Delivery Plan (TIDP) and Master Information Delivery Plan (MIDP) for the whole project could be created and amalgamated. You will be joining as part of the organisation {instance.company.company_name}.\n\n {usermail} is the lead party that is managing the TIDP/MIDP portal for the project. If you have any queries, please contact them directly.\n\n Next steps \n Sign in using the following detail:\n\n.Email: {instance.contact_email}. \n Password: 1a@p8xazi \n \n Click <a href="{settings.SITE_DOMAIN}{instance.project.get_absolute_url()}">here to view the project now</a>.'


    html_content = f'<h2>Dear {instance.contact_person}</h2>You are invited by {usermail} to participate in a BIM project titled {instance.project.name} through TIDP/MIDP portal where your Task Information Delivery Plan (TIDP) and Master Information Delivery Plan (MIDP) for the whole project could be created and amalgamated. You will be joining as part of the organisation {instance.company.company_name}.<br>{usermail} is the lead party that is managing the TIDP/MIDP portal for the project. If you have any queries, please contact them directly.<br>Next steps<br>Sign in using the following detail:<br>Email: {instance.contact_email} <br> Password: 1a@p8xazi <br><br>Click <a href="{settings.SITE_DOMAIN}{instance.project.get_absolute_url()}">here to view the project now</a>'


    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=True)



def task_member_mail(instance):
        subject, from_email, to = 'A new task assigned to you', settings.DEFAULT_FROM_EMAIL, instance.contact_email

        text_content = 'Hello {instance.contact_person},\n\n A task has been assigned to you.\n\n Kindly Login to your dashboard to manage this project\n\n Email: {instance.contact_email} \n Password: 1a@p8xazi.</div>\n\n. Click <a href="{settings.SITE_DOMAIN}{instance.project.get_absolute_url()}">here</a> to view now. \n\n Thank you'

        html_content = f'<h2> Hello {instance.contact_person}, </h2> <p> A task has been assigned to you.</p><p>Kindly Login to your dashboard to manage this project.</p> <div> Email: {instance.contact_email} <br> Password: 1a@p8xazi.</div> <h2>Click <a href="{settings.SITE_DOMAIN}{instance.project.get_absolute_url()}">here</a> to view now. </h2> Thank you'

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

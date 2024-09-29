## Project details
django_part_android and django_part_admin both have simmilar kind of 
codebase. But the django_part_admin has some new module that doesnot work 
with the django_part_android. But i need django_part_android for my mobile 
application and also the newer module in django_part_admin is needed for 
my admin panel. But there are some exect same feature but both of them 
implimented it differently there's the problem arises because the two uses 
two different login auth token and diffrent api route for login so when 
android need to access module on the django_part_admin the client faces 
the problem of double authentication etc. Review the code and find fixes 
the feature can be access by admin and android efficeiently and without 
conflict. Let me give you a example: now theres a ticket creating and 
ticket buying module in both django_part_admin and django_part_androidthe 
admin panel uses api fronm django_part_admin Lottery module and to view 
the ticket the android uses the Ticket_draw_app module so the android 
cannot get the data from admin created ticket. Ticket_draw_app was creted 
before and added to the android. 

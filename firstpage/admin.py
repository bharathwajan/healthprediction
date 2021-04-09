from django.contrib import admin
from .models import connect

admin.site.register(connect)
#creates a table named "connects" 
#remenber django creates the table with the 's' as suffix say if "connect" then "connects"
#connect is the class in models.py with four fields 
#therfore a table named connects is created with four columns as specified in models.py
# Register your models here.

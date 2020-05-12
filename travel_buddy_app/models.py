from django.db import models
import bcrypt
import datetime

class ValiManager(models.Manager):
    def registervalidator(self, postData, request):
        errors = {}
        if len(postData['r_name']) < 3:
            errors["r_name"] = "First name should be at least 3 characters"
            request.session['name'] = ""
        unamecheck = Users.objects.filter(username = postData['r_uname'])
        if len(postData['r_uname']) < 3:
            errors["r_uname"] = "Username should be at least 3 characters"
            request.session['uname'] = ""
        elif len(unamecheck) > 0:
            errors['unamecheck'] = "Username has existing in the system, Please change."
        if len(postData['r_password']) < 8:
            errors['r_pass'] = "Password should be at least 8 characters"
        elif postData['r_password'] != postData['r_passwordcheck']:
            errors['r_passcheck'] = "Password does not match"         
        return errors
            
    def loginvalidator(self, postData, request):
        errors = {}
        if len(postData['l_uname']) < 1:
            errors["l_uname"] = "Please enter the email"
            request.session['luname'] = ""
        else:
            login_user = postData['l_uname'].lower()
            user = Users.objects.filter(username=login_user)
            if user:
                logged_user = user[0]
                print(logged_user)
                if bcrypt.checkpw(request.POST['l_password'].encode(), logged_user.password.encode()):
                    request.session['userid'] = logged_user.id
                else:
                    errors['lpass'] = "Incorrect password, please try again."
            else:
                request.session['luname'] = ""
                errors['luname'] = "Username doesn't exist. Please regiester first."        
        return errors
    
    def recordvalidator(self, postData, request):
        errors = {}
        if len(postData['dest']) < 3:
            errors['dest'] = "Description should at least 3 character"
            request.session['dest'] = ""
        if len(postData['desc']) < 5:
            errors['desc'] = "Description should at least 5 character"
            request.session['desc'] = ""
        present = datetime.date.today()
        datefrom = datetime.datetime.strptime(postData['datefrom'], "%Y-%m-%d").date()
        if datefrom <= present:
            errors["datefrom"] = "Travel dates should be future-dated"
            request.session['datefrom'] = ""
            request.session['dateto'] = ""
        elif postData['datefrom'] > postData['dateto']:
            errors["datecheck"] = "'Travel Date To' should not be before 'the Travel Data From'"
            request.session['dateto'] = ""
        return errors

class Users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ValiManager()

class Trips(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    datefrom = models.DateField()
    dateto = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Users, related_name="trip", on_delete=models.CASCADE)
    favoriter = models.ManyToManyField(Users, related_name = 'favorite')
    objects = ValiManager()
    
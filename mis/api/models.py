from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import JSONField


class Department(models.Model):
    name = models.CharField(max_length=100)
    abbr = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Year(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.number)

class Class(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    section = models.CharField(max_length=4, blank=True, null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    
    default_room_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Shift(models.Model):
    name=models.CharField(max_length=20, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.SUPERADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    class Role(models.TextChoices):
        TEACHER = 'teacher', 'TEACHER'
        ADMIN = 'admin', 'ADMIN'
        SUPERADMIN = 'superadmin', 'SUPERADMIN'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.TEACHER)
    username = models.CharField(max_length=15, unique=False, default='')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
   
    
class Teacher(models.Model):
    name= models.CharField(max_length=100)
    abbr= models.CharField(max_length=10, blank=True, null=True)
    designation= models.CharField(max_length=100, blank=True, null=True)
    phd= models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True)
    def __str__(self):
        return self.name
    
  

    

    
class TimingField(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    department= models.ForeignKey(Department, on_delete=models.CASCADE)
    availability = JSONField(default=dict)  # Store availability in a JSON field

    def __str__(self):
        return f"{self.teacher.name} - {self.shift.name}"

    def set_availability(self, day, periods):
        self.availability[day] = periods
        self.save()

    def get_availability(self, day):
        return self.availability.get(day, [])
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    code= models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.code
    

    
class Period(models.Model):
    class PeriodType(models.IntegerChoices):
        LECTURE = 1, 'Lecture'
        TUTORIAL = 2, 'Tutorial'
        LAB = 3, 'Lab'
        LTUTORIAL = 4, 'Lecture-Tutorial'

    class YearPart(models.IntegerChoices):
        FIRST = 1, '1'
        SECOND = 2, '2'

    class Day(models.IntegerChoices):
        MONDAY = 2, 'Monday'
        TUESDAY = 3, 'Tuesday'
        WEDNESDAY = 4, 'Wednesday'
        THURSDAY = 5, 'Thursday'
        FRIDAY = 6, 'Friday'
        SUNDAY = 1, 'Sunday'

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(Teacher)  # Changed to ManyToManyField
    classid = models.ForeignKey(Class, on_delete=models.CASCADE)
    note = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=4, blank=True, null=True)
    alternate = models.BooleanField(default=False)
    start_period = models.IntegerField()
    end_period= models.IntegerField(default=1)
    period_type = models.IntegerField(choices=PeriodType.choices)
    room_number = models.CharField(max_length=15, blank=True, null=True)
    shift = models.ForeignKey(Shift, on_delete=models.DO_NOTHING, blank=True, null=True)  
    year_part = models.IntegerField(choices=YearPart.choices,default=1)
    day=models.IntegerField(choices=Day.choices,default=1)
    def __str__(self):
        return f"{self.subject.name} - {self.classid.name}"
    

    

    

     

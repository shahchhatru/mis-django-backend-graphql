from django.db import models
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
    class YearPart(models.IntegerChoices):
        FIRST = 1, '1'
        SECOND = 2, '2'

    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    section = models.CharField(max_length=4, blank=True, null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    year_part = models.IntegerField(choices=YearPart.choices)
    default_room_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Shift(models.Model):
    name=models.CharField(max_length=20, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    name= models.CharField(max_length=100)
    abbr= models.CharField(max_length=10, blank=True, null=True)
    designation= models.CharField(max_length=100, blank=True, null=True)
    phd= models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    

    
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

    def __str__(self):
        return f"{self.subject.name} - {self.classid.name}"
    

    

    

     

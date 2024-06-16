import graphene 
from graphene_django import DjangoObjectType
from .models import Class, Department, Year, Shift, Teacher, TimingField, Period, Subject

# # class BookType(DjangoObjectType):
# #     class Meta:
# #         model = Book
# #         fields = ("id","title","excerpt")


# # class Query(graphene.ObjectType):
# #     all_books = graphene.List(BookType)

# #     def resolve_all_books(root, info):
# #         return Book.objects.all()

# # schema = graphene.Schema(query=Query)


class DepartmentType(DjangoObjectType):
    class Meta:
        model = Department
        fields = "__all__"

class YearType(DjangoObjectType):
    class Meta:
        model = Year
        fields = "__all__"

class ClassType(DjangoObjectType):
    class Meta:
        model = Class
        fields = "__all__" 

class ShiftType(DjangoObjectType):
    class Meta:
        model = Shift
        fields = "__all__"

class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher
        fields = "__all__"

class TimingFieldType(DjangoObjectType):
    class Meta:
        model = TimingField
        fields = "__all__"

class SubjectType(DjangoObjectType):
    class Meta:
        model = Subject
        fields = "__all__"

class PeriodType(DjangoObjectType):
    class Meta:
        model = Period
        fields = "__all__"

class Query(graphene.ObjectType):
    all_departments = graphene.List(DepartmentType)
    all_years = graphene.List(YearType)
    all_classes = graphene.List(ClassType)
    all_shifts = graphene.List(ShiftType)
    all_teachers = graphene.List(TeacherType)
    all_timings = graphene.List(TimingFieldType)
    all_subjects = graphene.List(SubjectType)
    all_periods = graphene.List(PeriodType)

    def resolve_all_departments(root, info):
        return Department.objects.all()

    def resolve_all_years(root, info):
        return Year.objects.all()

    def resolve_all_classes(root, info):
        return Class.objects.all()

    def resolve_all_shifts(root, info):
        return Shift.objects.all()

    def resolve_all_teachers(root, info):
        return Teacher.objects.all()

    def resolve_all_timings(root, info):
        return TimingField.objects.all()
    

schema = graphene.Schema(query=Query)
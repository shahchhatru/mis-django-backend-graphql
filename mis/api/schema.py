import graphene 
from graphene_django import DjangoObjectType
from .models import Class, Department, Year, Shift, Teacher, TimingField, Period, Subject
from .schemas.department.schema import DepartmentType,DepartmentMutation,UpdateDepartmentMutation
from .schemas.year.schema import YearMutation,YearType,UpdateYearMutation
from .schemas.collegeclass.schema import ClassType , ClassMutation,UpdateClassMutation
from .schemas.shift.schema import ShiftType,ShiftMutation,UpdateShiftMutation
from .schemas.timingField.schema import TimingFieldType,CreateTimingField,UpdateTimingField,DeleteTimingField
from .schemas.teacher.schema import TeacherType,TeacherMutation,UpdateTeacherMutation,DeleteTeacherMutation
from .schemas.subject.schema import SubjectType,SubjectMutation,UpdateSubjectMutation,DeleteSubjectMutation
from .schemas.period.schema import PeriodType,CreatePeriod



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
    
    def resolve_period(self, info, id):
        return Period.objects.get(id=id)

    def resolve_all_periods(self, info):
        return Period.objects.all()



class Mutation(graphene.ObjectType):
    create_department = DepartmentMutation.Field()
    update_department = UpdateDepartmentMutation.Field()
    create_year = YearMutation.Field()
    update_year = UpdateYearMutation.Field()
    create_class= ClassMutation.Field()
    update_class= UpdateClassMutation.Field()
    create_shift = ShiftMutation.Field()
    update_shift = UpdateShiftMutation.Field()
    create_timing_field = CreateTimingField.Field()
    update_timing_field = UpdateTimingField.Field()
    delete_timing_field = DeleteTimingField.Field()
    create_teacher= TeacherMutation.Field()
    update_teacher = UpdateTeacherMutation.Field()
    delete_teacher = DeleteTeacherMutation.Field()
    create_subject = SubjectMutation.Field()
    update_subject = UpdateSubjectMutation.Field()
    delete_subject = DeleteSubjectMutation.Field()
    create_period = CreatePeriod.Field()

    
    


schema = graphene.Schema(query=Query,mutation=Mutation)
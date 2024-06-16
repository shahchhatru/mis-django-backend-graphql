import graphene
from graphene_django import DjangoObjectType
from api.models import TimingField, Teacher, Shift, Department

class TimingFieldType(DjangoObjectType):
    class Meta:
        model = TimingField
        fields = "__all__"

class CreateTimingField(graphene.Mutation):
    class Arguments:
        teacher_id = graphene.Int(required=True)
        shift_id = graphene.Int(required=True)
        department_id = graphene.Int(required=True)
        availability = graphene.JSONString(required=True)

    timing_field = graphene.Field(TimingFieldType)

    @classmethod
    def mutate(cls, root, info, teacher_id, shift_id, department_id, availability):
        teacher = Teacher.objects.get(id=teacher_id)
        shift = Shift.objects.get(id=shift_id)
        department = Department.objects.get(id=department_id)
        timing_field = TimingField(
            teacher=teacher,
            shift=shift,
            department=department,
            availability=availability
        )
        timing_field.save()
        return CreateTimingField(timing_field=timing_field)

class UpdateTimingField(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        teacher_id = graphene.Int()
        shift_id = graphene.Int()
        department_id = graphene.Int()
        availability = graphene.JSONString()

    timing_field = graphene.Field(TimingFieldType)

    @classmethod
    def mutate(cls, root, info, id, teacher_id=None, shift_id=None, department_id=None, availability=None):
        timing_field = TimingField.objects.get(id=id)
        if teacher_id is not None:
            timing_field.teacher = Teacher.objects.get(id=teacher_id)
        if shift_id is not None:
            timing_field.shift = Shift.objects.get(id=shift_id)
        if department_id is not None:
            timing_field.department = Department.objects.get(id=department_id)
        if availability is not None:
            timing_field.availability = availability
        timing_field.save()
        return UpdateTimingField(timing_field=timing_field)

class DeleteTimingField(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        timing_field = TimingField.objects.get(id=id)
        timing_field.delete()
        return DeleteTimingField(success=True)


# class Query(graphene.ObjectType):
#     timing_field = graphene.Field(TimingFieldType, id=graphene.Int(required=True))
#     all_timing_fields = graphene.List(TimingFieldType)

#     def resolve_timing_field(self, info, id):
#         return TimingField.objects.get(id=id)

#     def resolve_all_timing_fields(self, info):
#         return TimingField.objects.all()

# schema = graphene.Schema(query=Query, mutation=Mutation)

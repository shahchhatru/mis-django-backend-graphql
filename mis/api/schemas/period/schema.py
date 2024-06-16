import graphene
from graphene_django import DjangoObjectType
from api.models import Subject, Teacher, Period, Shift, Class

class PeriodType(DjangoObjectType):
    class Meta:
        model = Period
        fields = "__all__"

class CreatePeriod(graphene.Mutation):
    class Arguments:
        subject_id = graphene.Int(required=True)
        teacher_ids = graphene.List(graphene.Int, required=True)
        classid_id = graphene.Int(required=True)
        note = graphene.String(required=False)
        section = graphene.String(required=False)
        alternate = graphene.Boolean(required=False)
        start_period = graphene.Int(required=True)
        no_of_period = graphene.Int(required=True)
        period_type = graphene.Int(required=True)
        room_number = graphene.String(required=False)
        shift_id = graphene.Int(required=True)

    period = graphene.Field(PeriodType)

    @classmethod
    def mutate(cls, root, info, subject_id, teacher_ids, classid_id, start_period, no_of_period, period_type, shift_id, note=None, section=None, alternate=False, room_number=None):
        subject = Subject.objects.get(id=subject_id)
        classid = Class.objects.get(id=classid_id)
        shift = Shift.objects.get(id=shift_id)
        teachers = Teacher.objects.filter(id__in=teacher_ids)

        end_period = start_period + no_of_period - 1

        # Check if the teacher is already occupied at the given time
        for teacher in teachers:
            occupied_periods = Period.objects.filter(
                teachers=teacher,
                shift=shift
            ).filter(
                (Q(start_period__lte=start_period) & Q(start_period__gte=end_period)) |
                (Q(start_period__lte=end_period) & Q(start_period__gte=start_period)) |
                (Q(start_period__gte=start_period) & Q(start_period__lte=end_period))
            )
            if occupied_periods.exists():
                raise Exception(f"Teacher {teacher.name} is already occupied during the given time span.")

        # Check if the room_number is occupied at the given time
        if room_number:
            occupied_rooms = Period.objects.filter(
                room_number=room_number,
                shift=shift
            ).filter(
                (Q(start_period__lte=start_period) & Q(start_period__gte=end_period)) |
                (Q(start_period__lte=end_period) & Q(start_period__gte=start_period)) |
                (Q(start_period__gte=start_period) & Q(start_period__lte=end_period))
            )
            if occupied_rooms.exists():
                raise Exception(f"Room {room_number} is already occupied during the given time span.")

        period = Period(
            subject=subject,
            classid=classid,
            note=note,
            section=section,
            alternate=alternate,
            start_period=start_period,
            no_of_period=no_of_period,
            period_type=period_type,
            room_number=room_number,
            shift=shift
        )
        period.save()
        period.teachers.set(teachers)
        return CreatePeriod(period=period)

# class Mutation(graphene.ObjectType):
#     create_period = CreatePeriod.Field()

# # class Query(graphene.ObjectType):
#     period = graphene.Field(PeriodType, id=graphene.Int(required=True))
#     all_periods = graphene.List(PeriodType)

#     def resolve_period(self, info, id):
#         return Period.objects.get(id=id)

#     def resolve_all_periods(self, info):
#         return Period.objects.all()

#schema = graphene.Schema(query=Query, mutation=Mutation)

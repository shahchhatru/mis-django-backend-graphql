import graphene
from django.db.models import Q
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
        class_id = graphene.Int(required=True)
        note = graphene.String(required=False)
        section = graphene.String(required=False)
        alternate = graphene.Boolean(required=False)
        start_period = graphene.Int(required=True)
        end_period = graphene.Int(required=True)
        period_type = graphene.Int(required=True)
        room_number = graphene.String(required=False)
        shift_id = graphene.Int(required=True)
        year_part = graphene.Int(required=True)
        day=graphene.Int(required=True)

    period = graphene.Field(PeriodType)

    @classmethod
    def mutate(cls, root, info, subject_id,day, teacher_ids, year_part,class_id, start_period, end_period, period_type, shift_id, note=None, section=None, alternate=False, room_number=None):
        # Retrieve related objects
        subject = Subject.objects.get(id=subject_id)
        class_obj = Class.objects.get(id=class_id)
        shift = Shift.objects.get(id=shift_id)
        teachers = Teacher.objects.filter(id__in=teacher_ids)

        # Check if any teacher is already occupied during the specified period
        for teacher in teachers:
            overlapping_periods = Period.objects.filter(
                teachers=teacher,
                shift=shift,
                year_part=year_part,
                day=day,
                
            ).filter(
                Q(start_period__lt=end_period) & Q(end_period__gt=start_period)
            )
            if overlapping_periods.exists():
                raise Exception(f"Teacher {teacher.name} is already occupied during the given time span.{overlapping_periods}")

        # Check if the room is already occupied during the specified period
        if room_number:
            overlapping_rooms = Period.objects.filter(
                room_number=room_number,
                shift=shift,
                year_part= year_part,
                day=day
            ).filter(
                Q(start_period__lt=end_period) & Q(end_period__gt=start_period)
            )
            if overlapping_rooms.exists():
                raise Exception(f"Room {room_number} is already occupied during the given time span.,{overlapping_rooms}")

        # Create the new period
        period = Period(
            subject=subject,
            classid=class_obj,
            note=note,
            section=section,
            alternate=alternate,
            start_period=start_period,
            end_period=end_period,
            period_type=period_type,
            room_number=room_number,
            shift=shift
        )
        period.save()
        period.teachers.set(teachers)
        
        return CreatePeriod(period=period)
    
class UpdatePeriod(graphene.Mutation):
    class Arguments:
        period_id = graphene.Int(required=True)
        subject_id = graphene.Int(required=True)
        teacher_ids = graphene.List(graphene.Int, required=True)
        class_id = graphene.Int(required=True)
        note = graphene.String(required=False)
        section = graphene.String(required=False)
        alternate = graphene.Boolean(required=False)
        start_period = graphene.Int(required=True)
        end_period = graphene.Int(required=True)
        period_type = graphene.Int(required=True)
        room_number = graphene.String(required=False)
        shift_id = graphene.Int(required=True)

    period = graphene.Field(PeriodType)

    @classmethod
    def mutate(cls, root, info, period_id, subject_id, teacher_ids, class_id, start_period, end_period, period_type, shift_id, note=None, section=None, alternate=False, room_number=None):
        # Retrieve the period to update
        try:
            period = Period.objects.get(id=period_id)
        except Period.DoesNotExist:
            raise Exception(f"Period with id {period_id} does not exist.")

        # Retrieve related objects
        subject = Subject.objects.get(id=subject_id)
        class_obj = Class.objects.get(id=class_id)
        shift = Shift.objects.get(id=shift_id)
        teachers = Teacher.objects.filter(id__in=teacher_ids)

        # Check if any teacher is already occupied during the specified period
        for teacher in teachers:
            overlapping_periods = Period.objects.filter(
                teachers=teacher,
                shift=shift
            ).exclude(
                id=period.id  # Exclude the current period being updated
            ).filter(
                Q(start_period__lt=end_period) & Q(end_period__gt=start_period)
            )
            if overlapping_periods.exists():
                raise Exception(f"Teacher {teacher.name} is already occupied during the given time span.")

        # Check if the room is already occupied during the specified period
        if room_number:
            overlapping_rooms = Period.objects.filter(
                room_number=room_number,
                shift=shift
            ).exclude(
                id=period.id  # Exclude the current period being updated
            ).filter(
                Q(start_period__lt=end_period) & Q(end_period__gt=start_period)
            )
            if overlapping_rooms.exists():
                raise Exception(f"Room {room_number} is already occupied during the given time span.")

        # Update the period
        period.subject = subject
        period.classid = class_obj
        period.note = note
        period.section = section
        period.alternate = alternate
        period.start_period = start_period
        period.end_period = end_period
        period.period_type = period_type
        period.room_number = room_number
        period.shift = shift
        period.save()
        period.teachers.set(teachers)

        return UpdatePeriod(period=period)
    

class DeletePeriod(graphene.Mutation):
    class Arguments:
        period_id = graphene.Int(required=True)

    period_id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, period_id):
        try:
            period = Period.objects.get(id=period_id)
            period.delete()
            return DeletePeriod(period_id=period_id)
        except Period.DoesNotExist:
            raise Exception(f"Period with id {period_id} does not exist.")




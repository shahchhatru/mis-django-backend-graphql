import graphene 
from graphene_django import DjangoObjectType
from api.models import Shift

class ShiftType(DjangoObjectType):
    class Meta:
        model = Shift
        fields = "__all__"

class ShiftMutation(graphene.Mutation):

    class Arguments:
        name= graphene.String(required=True)
        start_time = graphene.Time(required=True)
        end_time = graphene.Time(required=True)

    shift = graphene.Field(ShiftType)

    @classmethod
    def mutate(cls,root,info,name,start_time,end_time):
        shift = Shift(name=name,start_time=start_time,end_time=end_time)
        shift.save()
        return ShiftMutation(shift=shift)
    
class UpdateShiftMutation(graphene.Mutation):

    class Arguments:
        id=graphene.ID()
        name= graphene.String(required=False)
        start_time = graphene.Time(required=False)
        end_time = graphene.Time(required=False)

    shift = graphene.Field(ShiftType)

    @classmethod
    def mutate(cls,root,info,name,start_time,end_time):
        shift = Shift.objects.get(pk=id)
        if name:
            shift.name=name
        if start_time:
            shift.start_time=start_time
        if end_time:
            shift.end_time=end_time
        shift.save()
        return ShiftMutation(shift=shift)
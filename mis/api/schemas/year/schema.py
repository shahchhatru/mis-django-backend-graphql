import graphene
from graphene_django import DjangoObjectType
from api.models import Year

class YearType(DjangoObjectType):
    class Meta:
        model = Year
        fields= "__all__"

#create year
class YearMutation(graphene.Mutation):

    class Arguments:
        name= graphene.String(required=True)
        number= graphene.Int(required=True)

    year = graphene.Field(YearType)

    @classmethod
    def mutate(cls,root,info,name,number):
        year = Year(name=name,number=number)
        year.save()
        return YearMutation(year=year)
    

class UpdateYearMutation(graphene.Mutation):

    class Arguments:
        id=graphene.ID()
        name= graphene.String(required=False)
        number = graphene.Int(required=False)
    
    year = graphene.Field(YearType)

    @classmethod
    def mutate(cls,root,info,id,name,number):
        year = Year.objects.get(pk=id)
        if name:
            year.name=name
        if number:
            year.number=number

        year.save()
        return UpdateYearMutation(year=year)
        
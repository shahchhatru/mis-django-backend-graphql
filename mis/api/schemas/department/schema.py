import graphene
from graphene_django import DjangoObjectType
from api.models import Department

class DepartmentType(DjangoObjectType):
    class Meta:
        model = Department
        fields = "__all__"


#mutation to create department 
class DepartmentMutation(graphene.Mutation):

    class Arguments:
        name= graphene.String(required=True)
        abbr = graphene.String(required=True)

    department = graphene.Field(DepartmentType)

    @classmethod
    def mutate(cls,root,info,name,abbr):
        department = Department(name=name,abbr=abbr)
        department.save()
        return DepartmentMutation(department=department)
    
#update department

class UpdateDepartmentMutation(graphene.Mutation):

    class Arguments:
        id= graphene.ID()
        name = graphene.String(required=False)
        abbr = graphene.String(required=False)

    department = graphene.Field(DepartmentType)

    @classmethod
    def mutate(cls,root,info,id,name,abbr):
        department = Department.objects.get(pk=id)
        if name:
            department.name= name
        if abbr:
            department.abbr= abbr

        department.save()
        return UpdateDepartmentMutation(department=department)
import graphene
from graphene_django import DjangoObjectType
from api.models import Teacher,Department

class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher
        fields = "__all__"


class TeacherMutation(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)
        abbr = graphene.String(required=True)
        department = graphene.String(required=True)
        phd=graphene.Boolean(required=False)
        designation = graphene.String(required=False)


    teacher = graphene.Field(TeacherType)

    @classmethod
    def mutate(cls,root,info,name,abbr,department,phd,designation):
        department= Department.objects.get(code=department)
        teacher = Teacher(name=name,abbr=abbr,department=department,phd=phd,designation=designation)
        teacher.save()
        return TeacherMutation(teacher=teacher)
    
class UpdateTeacherMutation(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=False)
        abbr = graphene.String(required=False)
        department = graphene.String(required=False)
        phd=graphene.Boolean(required=False)
        designation = graphene.String(required=False)

    teacher = graphene.Field(TeacherType)

    @classmethod
    def mutate(cls,root,info,id,name,abbr,department,phd,designation):
        teacher = Teacher.objects.get(pk=id)
        if name:
            teacher.name = name
        if abbr:
            teacher.abbr = abbr
        if department:
            department = Department.objects.get(code=department)
            teacher.department = department
        if phd:
            teacher.phd = phd
        if designation:
            teacher.designation=designation
        teacher.save()
        return UpdateTeacherMutation(teacher=teacher)
    
class DeleteTeacherMutation(graphene.Mutation):

    class Arguments:
        id = graphene.ID()

    teacher = graphene.Field(TeacherType)

    @classmethod
    def mutate(cls,root,info,id):
        teacher = Teacher.objects.get(pk=id)
        teacher.delete()
        return DeleteTeacherMutation(teacher=teacher)
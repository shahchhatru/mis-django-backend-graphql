import graphene
from graphene_django import DjangoObjectType
from api.models import Subject

class SubjectType(DjangoObjectType):
    class Meta:
        model = Subject
        fields = "__all__"

class SubjectMutation(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)
        code= graphene.String(requried=True)

    subject = graphene.Field(SubjectType)

    @classmethod
    def mutate(cls,root,info,name):
        subject = Subject(name=name)
        subject.save()
        return SubjectMutation(subject=subject)
    
class UpdateSubjectMutation(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=False)
        code= graphene.String(required=False)

    subject = graphene.Field(SubjectType)

    @classmethod
    def mutate(cls,root,info,id,name,code):
        subject = Subject.objects.get(pk=id)
        if name:
            subject.name = name
        if code:
            subject.code=code
            
        subject.save()
        return UpdateSubjectMutation(subject=subject)
    
class DeleteSubjectMutation(graphene.Mutation):

    class Arguments:
        id = graphene.ID()

    subject = graphene.Field(SubjectType)

    @classmethod
    def mutate(cls,root,info,id):
        subject = Subject.objects.get(pk=id)
        subject.delete()
        return DeleteSubjectMutation(subject=subject)
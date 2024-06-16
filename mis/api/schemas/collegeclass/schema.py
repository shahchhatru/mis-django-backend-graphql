import graphene
from graphene_django import DjangoObjectType
from api.models import Class, Department, Year
from api.schemas.department.schema import DepartmentType

class ClassType(DjangoObjectType):
    class Meta:
        model = Class
        fields = "__all__"

class ClassMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        department_id = graphene.Int(required=True)  # Use the ID for foreign key relations
        section = graphene.String(required=True)
        year_num = graphene.Int(required=True)
        year_part = graphene.Int(required=True)
        default_room_number = graphene.String(required=True)

    class_type = graphene.Field(ClassType)

    @classmethod
    def mutate(cls, root, info, name, department_id, section, year_num, year_part, default_room_number):
        # Retrieve the department instance using the provided ID
        department = Department.objects.get(id=department_id)
        year = Year.objects.get(number=year_num)
        class_instance = Class(
            name=name,
            department=department,
            section=section,
            year=year,
            year_part=year_part,
            default_room_number=default_room_number
        )
        class_instance.save()
        return ClassMutation(class_type=class_instance)
    
class UpdateClassMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=False)
        department_id = graphene.Int(required=False)
        section = graphene.String(required=False)
        year_num = graphene.Int(required=False)
        year_part = graphene.Int(required=False)
        default_room_number = graphene.String(required=False)

    class_type = graphene.Field(ClassType)

    @classmethod
    def mutate(cls, root, info, id, name, department_id, section, year_num, year_part, default_room_number):
        class_instance = Class.objects.get(pk=id)
        if name:
            class_instance.name = name
        if department_id:
            department = Department.objects.get(pk=department_id)
            class_instance.department = department
        if section:
            class_instance.section = section
        if year_num:
            year= Year.objects.get(number=year_num)
            class_instance.year = year
        if year_part:
            class_instance.year_part = year_part
        if default_room_number:
            class_instance.default_room_number = default_room_number
        class_instance.save()
        return UpdateClassMutation(class_type=class_instance)



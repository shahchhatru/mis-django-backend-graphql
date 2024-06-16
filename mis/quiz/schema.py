import graphene
from graphene_django import DjangoObjectType
from .models import Quizzes, Question, Category, Answer

class QuizType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = "__all__"

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title", "quiz")

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("answer_text", "question", "is_right")

class Query(graphene.ObjectType):
    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())

    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)

    def resolve_all_questions(root, info, id):
        return Question.objects.get(pk=id)

# class CategoryMutation(graphene.Mutation):
#     class Arguments:
#         name = graphene.String(required=True)

#     category = graphene.Field(CategoryType)

#     @classmethod
#     def mutate(cls, root, info, name):
#         category = Category(name=name)
#         category.save()
#         return CategoryMutation(category=category)
    

class CategoryMutation(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
        name= graphene.String(required=True)
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id, name):
        category = Category.objects.get(pk=id)
        category.name = name
        category.save()
        return CategoryMutation(category=category)

class CreateCategoryMutation(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CategoryMutation(category=category)

class DeleteCategoryMutation(graphene.Mutation):

    class Arguments:
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(pk=id)
        category.delete()
        return
    

class Mutation(graphene.ObjectType):
    update_category = CategoryMutation.Field()
    create_category= CreateCategoryMutation.Field()
    delete_category= DeleteCategoryMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

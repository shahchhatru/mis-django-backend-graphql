import graphene
from graphql_jwt.shortcuts import get_token, create_refresh_token
import graphql_jwt
from graphql_jwt.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import default_token_generator
from graphene_django.types import DjangoObjectType
from api.models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "email", "role")

class Register(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        user = User(email=email, role=User.Role.TEACHER)
        user.set_password(password)  # This hashes the password
        user.save()


        token = get_token(user)
        return Register(user=user, token=token)

class Login(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise Exception('User does not exist')

        if not user.check_password(password):
            print(f"Provided password: {password}")
            print(f"Stored password hash: {user.password}")
            raise Exception('Invalid password')

        token = get_token(user)
        refresh_token = create_refresh_token(user)
        return Login(user=user, token=token, refresh_token=refresh_token)
 

class PasswordReset(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

        send_mail(
            'Password Reset',
            f'Please reset your password using the following link: {url}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return PasswordReset(success=True)

class PasswordResetConfirm(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        uid = graphene.String(required=True)
        token = graphene.String(required=True)
        new_password = graphene.String(required=True)

    def mutate(self, info, uid, token, new_password):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return PasswordResetConfirm(success=True)
            else:
                return PasswordResetConfirm(success=False)
        except Exception as e:
            return PasswordResetConfirm(success=False)

class UpdateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.Int(required=True)
        email = graphene.String()
        password = graphene.String()
        role = graphene.String()

    def mutate(self, info, id, email=None, password=None, role=None):
        user = User.objects.get(pk=id)

        if email:
            user.email = email
        if password:
            user.set_password(password)
        if role:
            user.role = role

        user.save()
        return UpdateUser(user=user)

class DeleteUser(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        user = User.objects.get(pk=id)
        user.delete()
        return DeleteUser(success=True)

class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    all_users = graphene.List(UserType)

    @login_required
    def resolve_me(self, info):
        return info.context.user

    def resolve_user(self, info, id):
        return User.objects.get(pk=id)

    def resolve_all_users(self, info):
        return User.objects.all()

class Mutation(graphene.ObjectType):
    register = Register.Field()
    login = Login.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    password_reset = PasswordReset.Field()
    password_reset_confirm = PasswordResetConfirm.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

user_schema = graphene.Schema(query=Query, mutation=Mutation)

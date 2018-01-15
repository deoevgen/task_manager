#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SelectField
from wtforms import SubmitField
from wtforms.validators import EqualTo
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import ValidationError
from app.models import User
from app.models import Role


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")  # TODO: функционал отсутствуует
    submit = SubmitField("Войти")


class RegistrationForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired(message="Нет имени пользователя")])
    email = StringField("Почта", validators=[DataRequired(), Email(message="Неверный формат почты")])
    password = PasswordField("Пароль", validators=[DataRequired(message="Отсутствует пароль")])
    password2 = PasswordField("Повторите пароль", validators=[DataRequired(message="Повторите пароль"),
                                                               EqualTo('password', message="Нет совпадения паролей")])
    select_role = SelectField("Тип пользователя: ", choices=[(str(role.id),
                                                              role.user_role) for role in Role.query.all()])
    submit = SubmitField("Зарегистрировать")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Пользователь существует")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Эта почта уже зарегистрирована")

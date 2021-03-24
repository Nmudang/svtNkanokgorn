from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField,FileField,DateField,MultipleFileField
from wtforms.validators import Length,EqualTo,DataRequired,Email,ValidationError
from svt.models import Member,User

class MemberRes(FlaskForm):

	stage_name = StringField(label='stage_name:',validators=[Length(min=2,max=30),DataRequired()])
	first_name = StringField(label='first_name:',validators=[Length(min=2,max=30),DataRequired()])
	last_name = StringField(label='last_name:',validators=[Length(min=2,max=30),DataRequired()])
	height = IntegerField(label='Height :',validators=[DataRequired()])
	weight = IntegerField(label='Weight :',validators=[DataRequired()])
	birth = DateField(label='Birth: ',validators=[DataRequired()])
	position = StringField(label='Position: ')
	img = FileField(label='Img: ')
	submit = SubmitField(label='Create Member')

class RegisterForm(FlaskForm):
	def validate_username(self,username_to_check):
		user = User.query.filter_by(username=username_to_check.data).first()
		if user:
			raise ValidationError('Username already exists! Please try differnt  username')

	def validate_email_address(self,email_address_to_check):
		email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
		if email_address:
			raise ValidationError('Email Address already exists! Please try differnt  email')

	username = StringField(label='User Name:',validators=[Length(min=2,max=30),DataRequired()])
	email_address = StringField(label='Email Address:',validators=[Email(),DataRequired()])
	password1 = PasswordField(label='Password:',validators=[Length(min=2),DataRequired()])
	img = FileField(label='Img: ')
	password2 = PasswordField(label='Confirm Password:',validators=[EqualTo('password1'),DataRequired()])
	
	submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
	username = StringField(label='User Name:', validators=[DataRequired()])
	password = PasswordField(label='Password', validators=[DataRequired()])
	submit = SubmitField(label='Sign in')	

class Upload_img(FlaskForm):
	imgs = MultipleFileField(render_kw={'multiple': True})
	cap = StringField(label='Comment :', validators=[DataRequired()])
	submit = SubmitField(label='Upload ')

class DeleteForm(FlaskForm):
	delete = SubmitField(label='Delete it')

class MusicForm(FlaskForm):
	name = StringField(label='Name:', validators=[DataRequired()])
	add = StringField(label='link:', validators=[DataRequired()])
	cate =  StringField(label='type:', validators=[DataRequired()])
	submit = SubmitField(label='Submit it')

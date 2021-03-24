from svt import db,login_manager
from svt import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
	id = db.Column(db.Integer(),primary_key=True)
	username = db.Column(db.String(length=30),nullable=False,unique=True)
	email_address =  db.Column(db.String(length=50),nullable=False,unique=True)
	password_hash =  db.Column(db.String(length=60),nullable=False)
	mainimg = db.Column(db.String())
	img = db.relationship('Img',backref='userpic',lazy=True)
	
	@property
	def password(self):
		return self.password

	@password.setter
	def password(self, plain_text_password):
		self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

	def check_password_correction(self,attempted_password):
		return bcrypt.check_password_hash(self.password_hash,attempted_password)

	def main_img(self,file):
		self.mainimg = file

	

class Member(db.Model):
	id = db.Column(db.Integer(),primary_key=True)
	stage_name = db.Column(db.String(length=30),nullable=False)
	first_name = db.Column(db.String(length=100),nullable=False)
	last_name = db.Column(db.String(length=30),nullable=False)
	height = db.Column(db.Integer(),nullable=False)
	weight = db.Column(db.Integer(),nullable=False)
	birth = db.Column(db.Date(),nullable=False)
	position = db.Column(db.String())
	mainimg = db.Column(db.String())
	img = db.relationship('Img',backref='mem_pic',lazy=True)

	def __repr__(self):
		return f'name {self.name}'

	def main_img(self,name_file):
		self.mainimg = name_file
		db.session.commit()


class Img(db.Model):
	id = db.Column(db.Integer(),primary_key=True)
	name = db.Column(db.String(),nullable=False,unique=True)
	img = db.Column(db.LargeBinary(),nullable=False)

	owner = db.Column(db.Integer(),db.ForeignKey('user.id'))
	mem = db.Column(db.Integer(),db.ForeignKey('member.id'))
	cap = db.Column(db.Integer(),db.ForeignKey('caption.id'))

	def __repr__(self):
		return f'name {self.name}'

	def add_cap(self,capt):
		self.cap = capt.id

class Caption(db.Model):
	id = db.Column(db.Integer(),primary_key=True)
	text = db.Column(db.Text(),nullable=False)
	owner = db.Column(db.Integer(),db.ForeignKey('user.id'))
	img = db.relationship('Img',backref='cap_pic',lazy=True)


class Music(db.Model):
	id = db.Column(db.Integer(),primary_key=True)
	name = db.Column(db.String(),nullable=False)
	add = db.Column(db.Text(),nullable=False)
	cate =  db.Column(db.Text(),nullable=False)

	def __repr__(self):
		return f'name {self.name}'

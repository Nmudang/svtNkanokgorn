from svt import app,db
from flask_login import login_user,logout_user,login_required,current_user
from flask import render_template,redirect,url_for,flash,request,send_from_directory
from svt.models import Member,Img,User,Caption,Music
from svt.forms import MemberRes,RegisterForm,LoginForm,Upload_img,DeleteForm,MusicForm
from werkzeug.utils import secure_filename
import os
from svt.funcs import create_name

@app.route('/')
@app.route('/home')
def home_page():
	return render_template('member.html')

@app.route('/login',methods=['GET','POST'])
def login_page():
	if current_user.is_authenticated == True:
		return  redirect(url_for('member_page'))
	form = LoginForm()
	if form.validate_on_submit():
		attempted_user = User.query.filter_by(username=form.username.data).first()
		if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
			login_user(attempted_user)
			return redirect(url_for('member_page'))
	return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register_page():
	form = RegisterForm()
	if form.validate_on_submit():
		user_to_create = User(username=form.username.data,email_address=form.email_address.data,password=form.password1.data)
		db.session.add(user_to_create)
		db.session.commit()
		file_img = form.img.data
		filename = secure_filename(file_img.filename)
		if filename != '':
			des = "/".join([app.config['IMAGE_UPLOADS'],filename])
			file_img.save(des)
			create_pic = Img(name=filename,img=file_img.read(),mem=user_to_create.id)
			db.session.add(create_pic)
			db.session.commit()
			user_to_create.main_img(filename)
		login_user(user_to_create)
		return redirect(url_for('member_page'))
	return render_template('register.html',form=form)

@app.route('/logout_page')
def logout_page():
	logout_user()
	flash("You have bee logged out!", category='info')
	return redirect(url_for('home_page'))
	

@app.route('/member')
def member_page():
	members = Member.query.all()
	return render_template('member.html',members=members)


@app.route('/pic/<filename>')
def send_image(filename):
    return send_from_directory("static/images", filename)

@app.route('/search',methods=['GET','POST'])
def find_page():
	musics = Music.query.all()
	if request.method == 'POST':
		word = request.form.get('search')
		musics = Music.query.filter(Music.cate.contains(word)).all()
	return render_template("youtube.html", musics=musics)
	
    

@app.route('/regmem',methods=['GET','POST'])
def reg_mem():
	form = MemberRes()
	if form.validate_on_submit():
		create_mem = Member(stage_name= form.stage_name.data,first_name= form.first_name.data,
			last_name= form.last_name.data,height= form.height.data,weight= form.weight.data,
			birth= form.birth.data,position= form.position.data)
		db.session.add(create_mem)
		db.session.commit()
		file_img = form.img.data
		filename = secure_filename(file_img.filename)
		if filename != '':
			filename = create_name(filename)
			des = "/".join([app.config['IMAGE_UPLOADS'],filename])
			file_img.save(des)
			create_pic = Img(name=filename,img=file_img.read(),mem=create_mem.id)
			db.session.add(create_pic)
			db.session.commit()
			create_mem.main_img(filename)
		return redirect(url_for('member_page'))
	return render_template('regmem.html',form=form)


@app.route('/uploadimg',methods=['GET','POST'])
@login_required
def upload_img():
	form = Upload_img()
	if form.validate_on_submit():
		creat_com = Caption(text = form.cap.data,owner=current_user.id)
		db.session.add(creat_com)
		db.session.commit()
		for file_img in form.imgs.data:
			filename = secure_filename(file_img.filename)
			if filename != '':
				filename = create_name(filename)
				des = "/".join([app.config['IMAGE_UPLOADS'],filename])
				file_img.save(des)
				print(file_img.read())
				create_pic = Img(name=filename,img=file_img.read(),owner=current_user.id,cap=creat_com.id)
				db.session.add(create_pic)
				db.session.commit()
				current_user.main_img(filename)
		return  redirect(url_for('show_page_user'))
	return render_template('uploadimg.html',form=form)


@app.route('/myimg',methods=['GET','POST'])
@login_required
def show_page_user():
	form = DeleteForm()
	if request.method == "POST":
		delete_capID = request.form.get('delete')
		cap_item = Caption.query.filter_by(id=delete_capID).first()
		img_item = Img.query.filter_by(cap=delete_capID).all()
		for img in img_item:
			des = "/".join([app.config['IMAGE_UPLOADS'],img.name])
			os.remove(des)
			db.session.delete(img)
			db.session.commit()
		db.session.delete(cap_item)
		db.session.commit()
	imgs = Img.query.filter_by(owner=current_user.id)
	caps = Caption.query.filter_by(owner=current_user.id)
	return render_template('showimg.html',imgs=imgs,caps=caps,form=form)


@app.route('/recmusic',methods=['GET','POST'])
def recmem_user():
	form = MusicForm()
	if form.validate_on_submit():
		create_music = Music(name=form.name.data,add=form.add.data,cate=form.cate.data)
		db.session.add(create_music)
		db.session.commit()
	musics = Music.query.all()
	return render_template('regMu.html',form=form,musics=musics)

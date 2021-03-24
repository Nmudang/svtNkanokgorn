import random
import string
import os
from svt.models import Member,Img,User

def create_name(file_change):
	filename, file_extension = os.path.splitext(file_change)
	result_str = file_change
	check =  Img.query.filter_by(name=result_str).first()
	while(check is not None):
		result_str = ''.join(random.choice(string.ascii_letters) for i in range(5))
		result_str = result_str+file_extension
		check =  Img.query.filter_by(name=result_str).first()
	return result_str

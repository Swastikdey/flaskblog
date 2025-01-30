
from flask import url_for,current_app
from my_app import mail
from PIL import Image
import secrets,os
from flask_mail import Message
 




def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename) #extractss the extension
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(current_app.root_path,'static/profile_pics',picture_fn)
    
    output_size=(200,200)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path) #saves the image to the path that we created, db is not yet touched
    print(picture_path)
    return picture_fn


def send_reset_mail(user):#user is an instance of User class
    
    token=user.get_reset_token()
    msg=Message('Password Reset Request', sender='swastik.dey.2003@gmail.com',
                recipients=[user.email])
    msg.body=f''' To reset your password, visit the following link:
{url_for('users.reset_token',token=token, _external=True)} 

If you did not make the request, ignore this
''' # _external=True is used to get the full path, not relative
    mail.send(msg)

    
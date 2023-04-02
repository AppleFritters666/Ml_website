from flask import Blueprint,render_template,request
from keras.models import load_model
from tensorflow.keras.utils import load_img
from tensorflow.keras.preprocessing.image import img_to_array

from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np

model = load_model(r'C:\Users\Lenovo\Desktop\sl_predictor.h5',compile=False)
def load_image(img, show=False):

    image = Image.open(img)
    image = ImageOps.grayscale(image)
    image = image.resize((28, 28))
    img_tensor = img_to_array(image)                    
    img_tensor = np.expand_dims(img_tensor, axis=0)         
    img_tensor /= 255.                                      

    if show:
        plt.imshow(img_tensor[0])                           
        plt.axis('off')
        plt.show()

    return img_tensor

views = Blueprint('views',__name__)


@views.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        image_path = request.form.get('path')
        print(image_path)
        if image_path != None:
            new_image = load_image(image_path,show=False)
            prediction = model.predict(new_image)
            prediction = list(prediction[0])
            prediction = prediction.index(max(prediction))
            result = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'K',10:'L',11:'M',12:'N',13:'O',14:'P',15:'Q',16:'R'
            ,17:'S',18:'T',19:'U',20:'V',21:'W',22:'X',23:'Y'}
            return render_template("home.html",uploaded=True,image_path=image_path,letter=result[prediction])
    return render_template("home.html",uploaded=False,path="",result="")






from flask import Flask, request
import json
import pytesseract
from PIL import Image
import datefinder
import datetime
import base64

app = Flask(__name__)

@app.route('/image_to_text', methods=['POST'])
def image_to_text():
    if request.method == 'POST':
        # check if the post request has the file part
        if ('base_64_image_content' in request.files):    
            file1 = request.files.get('base_64_image_content') # get the image file 
            im = Image.open(file1)
            image_to_text = pytesseract.image_to_string(im, lang='eng')  # using pytesseract ocr to convert image to string 
            matches = datefinder.find_dates(image_to_text)   
            dates = []
            for i in matches:
                if(i < datetime.datetime.today() and i.month<11 and i.year>2000 and i.year<2019):
                    dates.append(str(i.date()))
            if(len(dates)>=1):
                dic = {'date':dates[0]}
            else:
                dic = {'date':'Null'}
            response = json.dumps(dic)                
            return response                            
# When debug = True, code is reloaded on the fly while saved
#app.run(host='0.0.0.0', port='5008', debug=True)
if __name__ =='__main__':
    app.run()

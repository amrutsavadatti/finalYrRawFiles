#importing modules for image classification
import cv2
import tensorflow as tf

#importing modules for ocr.space
import ocrspace
import requests



#function to preprocess the image before sending it through CNN for classification
def prepare(file):
    IMG_SIZE = 50
    img_array = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)



def execute(image):
    print("==================Begin with image classification================")

    #Image classification CNN are trained in these to categories
    CATEGORIES = ["handwritten", "marksheets"]

    #loading the CNN model
    model = tf.keras.models.load_model("C:/Users/Chelamallu/Desktop/askIt2021/finalYrRawFiles/askIt/Forum/model.h5")

    #Allowed file extensions: .pdf,.jpg,.png,.jpeg,.bmp,.gif,.tif,.tiff,.webp
    #defining the path to the image
    #Make sure to deine right image path with right image extension
    filename= image

    #sending the preprocessed image to the CNN model
    image=prepare(image)
    prediction = model.predict([image])
    prediction = list(prediction[0])

    #printing the predication made by CNN
    print("Image is recognized as ", CATEGORIES[prediction.index(max(prediction))])

    print("==================Done with image classification================")

    #if CNN model predicts image as marksheet it is send for ocr.space
    if (CATEGORIES[prediction.index(max(prediction))]=='marksheets'):

    #Entered the ocr.space api
        api = ocrspace.API('5446eba92c88957')
    #loading the image to ocr.space
        text=api.ocr_file(open(filename, 'rb'))
        text.upper()
        print(text)
        if (text.find("TECHNOLOGY") == -1 and text.find("FRANCIS") == -1 and text.find("INSTITUTE") == -1 ):
            print("Error: Upload a valid marksheet")
            return ('0')
        else:
            print("It is a valid marksheet")
            return ('1')
            
    else:
        print("Error: Upload a valid marksheet")
        return ('-1')

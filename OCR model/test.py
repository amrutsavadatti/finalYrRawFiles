import cv2
import tensorflow as tf
print("Begin")

CATEGORIES = ["handwritten", "marksheets"]
def prepare(file):
    IMG_SIZE = 50
    img_array = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
print("Begin")
model = tf.keras.models.load_model("CNN.model")
image = "C:/Users/VINUTHA/Desktop/Project/OCR model/page10.jpg" #your image path
print("Begin")
image=prepare(image)
prediction = model.predict([image])
prediction = list(prediction[0])

print(CATEGORIES[prediction.index(max(prediction))])
print("Done")

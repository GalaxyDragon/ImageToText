import numpy as np
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
from sklearn.svm import SVC
import pickle

# this is code for "teach" sklearn machine
# image to vector. 1-black, 0-white
def img_to_vec(img):
    vect =[]
    for x in range(img.size[1]):
        for y in range(img.size[0]):
            pix = img.getpixel((y, x))
            vect.append(1-pix)
    return vect
#                 |
# uncomment this \|/ for teach machine again. Now it work just with Russian language with one font
# vectors = []
# results = []
# alphabet = "абвгдеёжзиклмнопрстуфхчшщъьэюя123456789АБВГДЕЖЗИКЛМНОПРСТУФХЧШЩЪЬЭЮЯ"
# for i in range(len(alphabet)):
#     im = Image.open("char's/Teach/"+alphabet[i]+".gif")
#     vectors.append(img_to_vec(im))
#     results.append(alphabet[i])
# a = np.array(vectors)
# b = np.array(results)
# clf = SVC()
# clf.fit(a, b)
# SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
#     decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
#     max_iter=-1, probability=False, random_state=None, shrinking=True,
#     tol=0.001, verbose=False)
# with open('machine.pickle', 'wb') as f:
#     pickle.dump(clf, f)
#
# # print(a)
# # print(b)

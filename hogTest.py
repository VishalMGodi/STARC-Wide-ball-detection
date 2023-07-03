import cv2
import numpy as np
import os 
from sklearn.metrics import confusion_matrix, accuracy_score
dir = os.listdir('./Dataset/newBallDataset/posDataset')
positive = ["./Dataset/newBallDataset/posDataset/" + x for x in dir]
# Dataset\newBallDataset\negDataset\1.jpg
# ballDataset\n1.jpg
dir = os.listdir('./Dataset/newBallDataset/negDataset')
negative = ["./Dataset/newBallDataset/negDataset/" + x for x in dir]

print("Asserting Postive Dataset")
for i,path in enumerate(positive):
    # print("Pos: ",i)
    assert os.path.exists(path)

print("Asserting Negative Dataset")
for i,path in enumerate(negative):
    # print("Neg: ",i)
    assert os.path.exists(path)

# print(len(negative))
# print(positive[0])
# print(negative[0])
# print(type(positive[0]))
# assert os.path.exists(positive[0])
# image = cv2.imread(positive[0])
# cv2.imshow("image",image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# print(negative)

# quit()




# Initialize the HOG descriptor
winSize = (32, 32)  # Define the sliding window size for HOG feature extraction
blockSize = (8, 8)  # Define the size of blocks for normalization
blockStride = (4, 4)  # Define the stride between blocks
cellSize = (4, 4)  # Define the size of cells within blocks
nbins = 9  # Define the number of orientation bins

hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)

# List to store HOG features and labels
hog_features = []
labels = []

# Iterate over positive samples (images with ball)
for i,positive_image in enumerate(positive):
    try:
        # print(i)
        # Read and preprocess the image
        image = cv2.imread(positive_image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Extract HOG features
        features = hog.compute(gray)
        
        # Append the features to the list
        hog_features.append(features)
        labels.append(1)  # Label as positive (ball)
    except Exception as e:
        print(f"____________________ POS {i}")
        print(f"{e} : : {positive[i][:]}")
        quit()
    
# Iterate over negative samples (images without ball)
for i,negative_image in enumerate(negative):
    # print("----",negative[i],"----")
    try:
        # print("N: ",i+1)
        # Read and preprocess the image
        image = cv2.imread(negative_image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Extract HOG features
        features = hog.compute(gray)
        
        # Append the features to the list
        hog_features.append(features)
        labels.append(0)  # Label as negative (non-ball)
    except Exception as e:
        print(f"____________________ NEG {i}")
        print(f"{e} : : {negative[i][:]}")
        quit()

# print(len(hog_features)," : ", hog_features[0])
# print(len(labels) , ":" , labels)


# for i,fet in enumerate(hog_features):
#     print(i+1," : ",len(fet))


# Convert the lists to numpy arrays
feature_matrix = np.array(hog_features, dtype = np.float32)
label_vector = np.array(labels,dtype = np.int32)


# Print the shapes of feature matrix and label vector
print("Feature matrix shape:", feature_matrix.shape)
print("Label vector shape:", label_vector.shape)


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(feature_matrix, label_vector, test_size = 0.2, random_state = 0)

# print("TRAIN - ",X_train)
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# print("TRAIN - ",X_train[0])
# print("------------")
# print("TEST - ",X_test[0])

from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(X_train, y_train)

dir = os.listdir('./Dataset/ballDataset')
oXTest = ["./Dataset/ballDataset/" + str(x) for x in dir]

print("Asserting Test Dataset")
for i,path in enumerate(oXTest):
    # print("oXTest: ",i)
    assert os.path.exists(path)

oYTest = []
for i in range(1,16):
    oYTest.append(1)
for i in range(1,16):
    oYTest.append(0)

print("Done")

xTestHog = []

# Iterate over negative samples (images without ball)
for i,testImg in enumerate(oXTest):
    # print("----",oXTest[i],"----")
    try:
        # print("N: ",i+1)
        # Read and preprocess the image
        image = cv2.imread(testImg)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Extract HOG features
        features = hog.compute(gray)
        
        # Append the features to the list
        xTestHog.append(features)
        # labels.append(0)  # Label as oXTest (non-ball)
    except Exception as e:
        print(f"____________________ XTEST {i}")
        print(f"{e} : : {oXTest[i][:]}")
        quit()

xTestFeatures = np.array(xTestHog, dtype = np.float32)
xTestFeatures = sc.transform(xTestFeatures)
# print(f"X,Y Test: {len(oXTest)} : {len(oYTest)}")
# print(oXTest)
# print(oYTest)



y_pred = classifier.predict(xTestFeatures)
print("Prediction Done")
cm = confusion_matrix(oYTest, y_pred)
print(cm)
print(classifier.score(oYTest,y_pred))
# print(np.concatenate((y_pred.reshape(len(y_pred),1), oYTest.reshape(len(oYTest),1)),1))

# # # Create an SVM object
# svm = cv2.ml.SVM_create()
# svm.setType(cv2.ml.SVM_C_SVC)  # Set SVM type to C-Support Vector Classification
# svm.setKernel(cv2.ml.SVM_LINEAR)  # Set SVM kernel type to Linear


# # Create the training data
# train_data = cv2.ml.TrainData_create(feature_matrix, cv2.ml.ROW_SAMPLE, label_vector)

# # Train the SVM model
# svm.train(train_data)

# # Apply the SVM model to the feature matrix for predictions
# _, predictions = svm.predict(feature_matrix)

# # Calculate accuracy
# accuracy = np.mean(predictions == label_vector) * 100
# print("Accuracy: {:.2f}%".format(accuracy))
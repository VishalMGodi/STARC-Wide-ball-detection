import cv2
import numpy as np
import sklearn as sk

positive = [r"ballDataset/"+str(x)+"Ball.png" for x in range(1,16)]
# ballDataset\n1.png
negative = [r"ballDataset/n"+str(x)+".png" for x in range(1,16)]



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
    print(i)
    # Read and preprocess the image
    image = cv2.imread(positive_image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Extract HOG features
    features = hog.compute(gray)
    
    # Append the features to the list
    hog_features.append(features)
    labels.append(1)  # Label as positive (ball)
    
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
        print(f"{e} : LOLOLOL : {negative[i][-6:]}")

# print(len(hog_features)," : ", hog_features[0])
# print(len(labels) , ":" , labels)


for i,fet in enumerate(hog_features):
    print(i+1," : ",len(fet))


# Convert the lists to numpy arrays
feature_matrix = np.array(hog_features, dtype = np.float32)
label_vector = np.array(labels,dtype = np.int32)


# Print the shapes of feature matrix and label vector
print("Feature matrix shape:", feature_matrix.shape)
print("Label vector shape:", label_vector.shape)


# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(feature_matrix, label_vector, test_size = 0.2, random_state = 0)

# # print("TRAIN - ",X_train)
# from sklearn.preprocessing import StandardScaler

# sc = StandardScaler()
# X_train = sc.fit_transform(X_train)
# X_test = sc.transform(X_test)

# print("TRAIN - ",X_train)
# print("------------")
# print("TEST - ",X_test)

# from sklearn.svm import SVC
# classifier = SVC(kernel = 'linear', random_state = 0)
# classifier.fit(X_train, y_train)


# y_pred = classifier.predict(X_test)
# print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

# Create an SVM object
svm = cv2.ml.SVM_create()
svm.setType(cv2.ml.SVM_C_SVC)  # Set SVM type to C-Support Vector Classification
svm.setKernel(cv2.ml.SVM_LINEAR)  # Set SVM kernel type to Linear


# # Convert labels to integers (-1 for negative class, +1 for positive class)
# label_vector = label_vector.astype(np.int32)
# label_vector = np.where(label_vector == 0, -1, label_vector)


# # Convert the feature matrix and label vector to the appropriate data types
# feature_matrix = np.float32(feature_matrix)
# label_vector = np.int32(label_vector)


# # Create the training data
train_data = cv2.ml.TrainData_create(feature_matrix, cv2.ml.ROW_SAMPLE, label_vector)

# # Train the SVM model
svm.train(train_data)


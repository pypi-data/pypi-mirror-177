# Imports
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
import requests


def download_data():
    URL = "https://github.com/optimization-for-data-driven-science/FERMI/raw/master/Datasets/adult.data"
    response = requests.get(URL)
    open("adult.data", "wb").write(response.content)

    URL = "https://github.com/optimization-for-data-driven-science/FERMI/raw/master/Datasets/adult.test"
    response = requests.get(URL)
    open("adult.test", "wb").write(response.content)

    URL = "https://github.com/optimization-for-data-driven-science/FERMI/raw/master/Datasets/AdultTrain2Sensitive.csv"
    response = requests.get(URL)
    open("AdultTrain2Sensitive.csv", "wb").write(response.content)

    URL = "https://github.com/optimization-for-data-driven-science/FERMI/raw/master/Datasets/AdultTest2Sensitive.csv"
    response = requests.get(URL)
    open("AdultTest2Sensitive.csv", "wb").write(response.content)


# Prepare Data:
def read_demographics_and_labels(data_name, number_of_sensitive_attributes=1):
    data = pd.read_csv(data_name)

    print(data.columns)

    # Shuffle Data
    # data = data.sample(frac=1)

    data['y'] = 1
    if data_name == "adult.data":
        data['y'].values[data['income'].values == '<=50K'] = 0
    else:
        data['y'].values[data['income'].values == '<=50K.'] = 0

    if number_of_sensitive_attributes == 2:
        data['s0'] = 0
        data['s0'].values[(data['gender'].values == 'Male') & (data['race'].values == 'White')] = 1

        data['s1'] = 0
        data['s1'].values[(data['gender'].values != 'Male') & (data['race'].values == 'White')] = 1

        data['s2'] = 0
        data['s2'].values[(data['gender'].values == 'Male') & (data['race'].values != 'White')] = 1

        data['s3'] = 0
        data['s3'].values[(data['gender'].values != 'Male') & (data['race'].values != 'White')] = 1

        S = data[['s0', 's1', 's2', 's3']]

    else:
        data['s0'] = 0
        data['s0'].values[(data['gender'].values == 'Male')] = 1

        data['s1'] = 0
        data['s1'].values[(data['gender'].values != 'Male')] = 1

        S = data[['s0', 's1']]

    S_matrix = S.to_numpy()
    return data[['y']].to_numpy(), S_matrix


def read_data(training_data_name, test_data_name):
    training_data = pd.read_csv(training_data_name)

    test_data = pd.read_csv(test_data_name)

    X_train = training_data.to_numpy()
    X_test = test_data.to_numpy()

    X_train = normalize(X_train, axis=0)
    X_test = normalize(X_test, axis=0)
    # sc = StandardScaler()

    # X_train = np.array(X_train)
    # sc.fit(X_train)
    # X_train = sc.transform(X_train)
    # X_test = sc.transform(X_test)

    intercept = X_train.shape[0] * [1]
    intercept_numpy = np.array(intercept)
    intercept_numpy = intercept_numpy[:, np.newaxis]
    X_train = np.append(X_train, intercept_numpy, axis=1)

    intercept = X_test.shape[0] * [1]
    intercept_numpy = np.array(intercept)
    intercept_numpy = intercept_numpy[:, np.newaxis]
    X_test = np.append(X_test, intercept_numpy, axis=1)

    return X_train, X_test


def read_binary_adult(mode='train'):
    Y_Train, S_Train = read_demographics_and_labels('adult.data', number_of_sensitive_attributes=1)
    Y_Test, S_Test = read_demographics_and_labels('adult.test', number_of_sensitive_attributes=1)
    X_Train, X_Test = read_data('AdultTrain2Sensitive.csv', 'AdultTest2Sensitive.csv')

    if mode == 'train':
        return X_Train, S_Train, Y_Train

    else:
        return X_Test, S_Test, Y_Test

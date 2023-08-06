from FERMI import AdultDataset
from FERMI import FERMIBinary

AdultDataset.download_data()
X_train, S_train, Y_train = AdultDataset.read_binary_adult(mode='train')
X_test, S_test, Y_test = AdultDataset.read_binary_adult(mode='test')


fermi_instance = FERMIBinary.FERMI(X_train, X_test, Y_train, Y_test, S_train, S_test)
FERMIBinary.FERMI_Logistic_Regression(fermi_instance)

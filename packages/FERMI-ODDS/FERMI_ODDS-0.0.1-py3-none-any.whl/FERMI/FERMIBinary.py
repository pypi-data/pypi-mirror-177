# Imports
import numpy as np
import torch
import torch.nn as nn


class FERMI(torch.nn.Module):

    def __init__(self, X_train, X_test, Y_train, Y_test, S_train, S_test, batch_size=64, epochs=2000, lam=10):

        super(FERMI, self).__init__()

        self.X_train = X_train
        self.Y_train = Y_train
        self.X_test = X_test
        self.Y_test = Y_test
        self.S_train = S_train
        self.S_test = S_test

        self.batch_size = batch_size
        self.epochs = epochs

        self.n = X_train.shape[0]
        self.d = X_train.shape[1]
        self.m = Y_train.shape[1]
        if self.m == 1:
            self.m = 2

        self.k = S_train.shape[1]

        self.W = nn.Parameter(torch.zeros(self.k, self.m))  # k: Support of sensitive attributes, m: number of labels
        self.theta = nn.Parameter(torch.zeros(self.d, 1))

        sums = self.S_train.sum(axis=0) / self.n
        print(sums)

        print(sums.shape)

        final_entries = []
        for item in sums:
            final_entries.append(1.0 / np.sqrt(item))

        self.P_s = np.diag(sums)

        self.P_s_sqrt_inv = torch.from_numpy(np.diag(final_entries)).double()
        print(self.P_s_sqrt_inv)
        self.lam = lam

    def forward(self, X):
        outputs = torch.mm(X.double(), self.theta.double())
        logits = torch.sigmoid(outputs)
        return logits

    def fairness_regularizer(self, X, S):

        current_batch_size = X.shape[0]
        summation = 0

        Y_hat = torch.sigmoid(torch.matmul(X, self.theta.double()))

        for i in range(current_batch_size):
            Y_hat_i = torch.zeros(self.m, self.m).double()
            Y_hat_i[0][0] = 1.0 - Y_hat[i]
            Y_hat_i[1][1] = Y_hat[i]

            W_gram = torch.matmul(torch.t(self.W.double()), self.W.double())  # W^T W
            summation -= torch.trace(torch.matmul(Y_hat_i, W_gram))

            P_ys = torch.zeros(self.m, self.k).double()
            P_ys[0][0] = S[i][0] * (1.0 - Y_hat[i])
            P_ys[0][1] = S[i][1] * (1.0 - Y_hat[i])
            P_ys[1][0] = S[i][0] * (Y_hat[i])
            P_ys[1][1] = S[i][1] * (Y_hat[i])
            prob_matrix_mul = torch.matmul(P_ys, self.P_s_sqrt_inv)
            summation += 2 * torch.trace(torch.matmul(prob_matrix_mul, self.W.double())) - 1

        return self.lam * summation


###
def FERMI_Logistic_Regression(fermi, batch_size=64, epochs=1000, initial_epochs=300,
                              initial_learning_rate=1, learning_rate_min=0.01, learning_rate_max=0.01, test_mode='on', test_report_at_every_x_epoch=10):

    X = fermi.X_train
    S_Matrix = fermi.S_train
    Y = fermi.Y_train
    XTest = fermi.X_test
    STest = fermi.S_test
    YTest = fermi.Y_test

    criterion = torch.nn.BCELoss()
    minimizer = torch.optim.SGD([fermi.theta, fermi.W], lr=initial_learning_rate)

    for ep in range(epochs + initial_epochs):
        if test_mode == 'on' and ep % test_report_at_every_x_epoch == test_report_at_every_x_epoch - 1:
            print("Epoch Number: ", ep + 1)
            # Test:
            pre_logits = np.dot(XTest, fermi.theta.detach().numpy())
            output_logits = 1 / (1 + np.exp(-pre_logits))
            final_preds = output_logits > 0.5
            test = YTest == 1
            acc = final_preds == test
            true_preds = acc.sum(axis=0)
            print("Accuracy: ", true_preds[0] / output_logits.shape[0] * 100, "%")

            final_preds = np.array(final_preds)
            intersections = np.dot(final_preds.T, STest)
            numbers = STest.sum(axis=0)

            group1 = intersections[0][0] / numbers[0]
            group2 = intersections[0][1] / numbers[1]
            print("DP Violation: ", np.abs(group1 - group2))

        number_of_iterations = X.shape[0] // batch_size
        for i in range(number_of_iterations):

            start = i * batch_size
            end = (i + 1) * batch_size

            current_batch_X = X[start:end]
            current_batch_Y = Y[start:end]
            current_batch_S = S_Matrix[start:end]

            XTorch = torch.from_numpy(current_batch_X).double()
            logits = fermi(XTorch)
            YTorch = torch.from_numpy(current_batch_Y).double()
            STorch = torch.from_numpy(current_batch_S).double()

            if ep < initial_epochs:
                loss_min = criterion(logits, YTorch)
            else:
                loss_min = criterion(logits, YTorch) + fermi.fairness_regularizer(XTorch, STorch)
            # loss_min = criterion(logits, YTorch)

            minimizer.zero_grad()
            loss_min.backward()

            if ep >= initial_epochs:
                fermi.theta.grad.data.mul_(learning_rate_min / initial_learning_rate)
                fermi.W.grad.data.mul_(-learning_rate_max / initial_learning_rate)

            minimizer.step()
    return fermi.theta, fermi.W

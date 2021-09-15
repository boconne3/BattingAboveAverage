import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, explained_variance_score, f1_score, precision_score, recall_score, confusion_matrix, roc_auc_score
import matplotlib.pyplot as plt
from sklearn import linear_model

def softmax(y):
    for i in range(len(y)):
        if y[i] > .5:
            y[i] = 1
        else:
            y[i] = 0
    return y

def confusion_matrix(y_pred, y):
    tp = tn = fp = fn = 0
    for idx, val in enumerate(y_pred):
        if val == 0 and y[idx] == 0:
            tn += 1
        elif val == 1 and y[idx] == 1:
            tp += 1
        elif val == 0 and y[idx] == 1:
            fn += 1
        elif val == 1 and y[idx] == 0:
            fp += 1
    return tp, tn, fp, fn

def recall_calc(conf_tuple):
    tp = conf_tuple[0]
    fn = conf_tuple[3]
    return tp/(tp+fn)
def precision_calc(conf_tuple):
    tp = conf_tuple[0]
    fp = conf_tuple[2]
    return tp/(tp+fp)
def accuracy_calc(conf_tuple):
    tp = conf_tuple[0]
    tn = conf_tuple[1]
    fp = conf_tuple[2]
    fn = conf_tuple[3]
    return (tp+tn)/(tp+tn+fp+fn)
def f1Score_calc(conf_tuple):
    tp = conf_tuple[0]
    fp = conf_tuple[2]
    fn = conf_tuple[3]
    return tp/(tp+((1/2)*(fp+fn)))

def graph_crossVal(costArray, crossValStatTrain, crossValStatTest, crossValStatName, model_type, k_fold):
    fig = plt.figure()
    plt.rc('font', size=18)
    plt.rcParams['figure.constrained_layout.use'] = True
    plt.plot(costArray,crossValStatTrain,linewidth=3,label='Training',color='b')
    plt.plot(costArray,crossValStatTest,linewidth=3,label='Validation',color='orange')
    plt.xlabel('C')
    plt.ylabel(crossValStatName)
    plt.legend()
    plt.title(model_type + ': ' + crossValStatName +' v Cost')

df_temp5 = pd.read_csv('temp5.csv', comment='#', names=['x','y'])

xFinal = []
# Code for supplying the ML models with ALL player stats 
# See report for details

# times = 0
# for idx, x_in in enumerate(df_temp5.x):
    # if times >= 1:
        #     temp_x = []
        #     str1 = x_in.replace(']','').replace('[','').replace("'",'')
        #     arr1 = str1.replace('"','').split(",")
        #     for a in arr1:
        #         temp_x.append(float(a))
        #     # print(len(temp_x))
        #     if(len(temp_x) == 83):
        #         for i, val in enumerate(temp_x):
        #             if np.isnan(val):
        #                 temp_x[i] = 0
        #         x1.append(temp_x)
        #         y1.append(float(df_temp5.y[idx]))
        #     if(len(temp_x) == 92):
        #         for i, val in enumerate(temp_x):
        #             if np.isnan(val):
        #                 temp_x[i] = 0
        #         x2.append(temp_x)
        #         y2.append(float(df_temp5.y[idx]))
        # times = times + 1
x = []     
for x_in in df_temp5.x:
    temp_x = []
    str1 = x_in.replace(']','').replace('[','').replace("'",'')
    arr1 = str1.replace('"','').split(",")
    for a in arr1:
        temp_x.append(float(a))
    x.append(temp_x)

y = []
for y_in in df_temp5.y:
    y.append(float(y_in))

# Aggregating player offensive stats across American and National Leagues
for i, val in enumerate(x):
    temp_x = []
    divisor = (len(val) - 2) / 9
    total = 0
    statAverage = 0
    for j in range(len(val)):
        if total == divisor:
            temp_x.append(statAverage/divisor)
            total = 0
            statAverage = 0
        if np.isnan(val[j]):
            val[j] = 0
        statAverage += val[j]
        total += 1
    temp_x.append(val[len(val) - 2])
    temp_x.append(val[len(val) - 1])
    xFinal.append(temp_x)

# Snippet can cherry-pick some of the stats for training
# xFinal = np.array(xFinal)
xFinal_temp = []
for i in range(len(xFinal)):
    arr = []
    arr.append(xFinal[i][3])
    arr.append(xFinal[i][7])
    arr.append(xFinal[i][8])
    arr.append(xFinal[i][9])
    arr.append(xFinal[i][10])
    xFinal_temp.append(np.array(arr))
    # xFinal_temp.append(np.array(xFinal[i][1:10]))

xFinal = np.array(xFinal_temp)

y = np.array(y)

costArray = [1, 5, 10, 50, 100, 150]
kArray = [2,5,10]   # 5 provides most reliable results

for model_num in range(1):

    for fold in kArray:
        train_accuracyAvg = []
        train_f1ScoreAvg = []
        train_precisionAvg = []
        train_recallAvg = []
        test_accuracyAvg = []
        test_f1ScoreAvg = []
        test_precisionAvg = []
        test_recallAvg = []
        for cost in costArray:
            kf = KFold(n_splits=fold)
            train_accuracy = []
            train_f1Score = []
            train_precision = []
            train_recall = []
            test_accuracy = []
            test_f1Score = []
            test_precision = []
            test_recall = []
            counter = 0

            model_type = ""
            for train, test in kf.split(xFinal):
                xTrain = xFinal[train]
                xTest = xFinal[test]
                yTrain = y[train]  
                yTest = y[test]

                if model_num == 0:
                    # cost = 50     # Cost for best-fit
                    model = linear_model.Lasso(alpha=(1/(2*cost)))
                    model_type = "Lasso regression"
                elif model_num == 1:
                    # cost = 100    # Cost for best-fit
                    model = linear_model.Ridge(alpha=1/(2*cost))
                    model_type = "Ridge regression"
                elif model_num == 2:
                    # cost = 100    # Cost for best-fit
                    model = LogisticRegression(penalty='l2',C=cost, max_iter=1000)
                    model_type = "Logistic regression"
                else:
                    print("ERR")
                model.fit(xTrain,yTrain)
                counter += 1
                # if counter > fold - 1:
                #     print(f"{model_type}, cost: {cost}: {model.coef_}")

                ypredTrain = softmax(model.predict(xTrain))
                ypredTest = softmax(model.predict(xTest))

                train_recall.append(recall_calc(confusion_matrix(ypredTrain, yTrain)))
                train_precision.append(precision_calc(confusion_matrix(ypredTrain, yTrain)))
                train_accuracy.append(accuracy_calc(confusion_matrix(ypredTrain, yTrain)))
                train_f1Score.append(f1Score_calc(confusion_matrix(ypredTrain, yTrain)))

                test_recall.append(recall_calc(confusion_matrix(ypredTest, yTest)))
                test_precision.append(precision_calc(confusion_matrix(ypredTest, yTest)))
                test_accuracy.append(accuracy_calc(confusion_matrix(ypredTest, yTest)))
                test_f1Score.append(f1Score_calc(confusion_matrix(ypredTest, yTest)))

            train_accuracyAvg.append(np.mean(train_accuracy))
            train_f1ScoreAvg.append(np.mean(train_f1Score))
            train_precisionAvg.append(np.mean(train_precision))
            train_recallAvg.append(np.mean(train_recall))

            test_accuracyAvg.append(np.mean(test_accuracy))
            test_f1ScoreAvg.append(np.mean(test_f1Score))
            test_precisionAvg.append(np.mean(test_precision))
            test_recallAvg.append(np.mean(test_recall))
        
        print(f"Model: {model_type}, cost: {cost}")
        print(f"Train accuracy: {train_accuracyAvg}, test accuracy:{test_accuracyAvg}")
        print(f"Train f1: {train_f1ScoreAvg}, test f1:{test_f1ScoreAvg}")
        print(f"Train precision: {train_precisionAvg}, test precision:{test_precisionAvg}")
        print(f"Train recall: {train_recallAvg}, test recall:{test_recallAvg}\n")
        graph_crossVal(costArray, train_accuracyAvg, test_accuracyAvg, "Accuracy", model_type, fold)
        graph_crossVal(costArray, train_f1ScoreAvg, test_f1ScoreAvg, "F1 Score", model_type, fold)
        graph_crossVal(costArray, train_precisionAvg, test_precisionAvg, "Precision", model_type, fold)
        graph_crossVal(costArray, train_recallAvg, test_recallAvg, "Recall", model_type, fold)


plt.show()

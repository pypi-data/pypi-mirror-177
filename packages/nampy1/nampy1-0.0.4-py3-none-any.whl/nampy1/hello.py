def logistic_scratch():
    return '''
    ## MAKE TRAIN, TEST SPLIT
    def initialize_weights(input_vec):
        weights = np.zeros_like(input_vec)
        bias = 0
        return weights, bias
    
    def sigmoid(z):
        return 1 / (1 + np.exp(-z))
    
    def logloss(y_true, y_pred):
        sum = 0
        for i in range(len(y_true)):
            sum += y_true[i] * np.log(y_pred[i]) + (1 - y_true[i]) * np.log(1 - y_pred[i])
        logloss = (-1) * ( 1 / len(y_true) ) * sum
        return logloss
    
    def gradient_dw(x, y, w, b, n):
        dw = (1/n) * x * ( sigmoid(np.dot(w, x) + b) - y)
        return dw   
    
    def gradient_db(x,y,w,b, n): 
        db = (1/n) * ( sigmoid(np.dot(w, x) + b) - y )
        return db
    
    def getPredictions(Y_actual, Y_predict):
        correct_preds = 0
        for i in range(len(Y_actual)):
            if Y_predict[i] > 0.5:
                Y_predict[i] = 1
            else:
                Y_predict[i] = 0
            if Y_actual[i] == Y_predict[i]:
                correct_preds += 1
        return round((correct_preds/len(Y_actual)) * 100, 2)
    
    def predict(w, b, X):
        n = len(X)
        z = np.dot(w, X) + b
        return sigmoid(z)
    
    def logistic_regression(X_train, y_train, X_test, y_test, epochs, alpha):
        weights, bias = initialize_weights(X_train[0])
        train_loss, test_loss = [], []
        train_accuracies, test_accuracies = [], []
        epoch_list = []
        n = len(X_train)
        prev_train_loss = -1
        for epoch in range(epochs):
            for i in range(n):
                dw = gradient_dw(X_train[i], y_train[i], weights, bias, n)
                db = gradient_db(X_train[i], y_train[i], weights, bias, n)
                weights -= alpha * dw
                bias -= alpha * db
            train_predict, test_predict = [], []
            for i in range(len(X_train)):
                train_predict.append( predict(weights, bias, X_train[i]) )
            for i in range(len(X_test)):
                test_predict.append( predict(weights, bias, X_test[i]) )
            curr_train_loss = logloss(y_train, train_predict)
            if curr_train_loss == prev_train_loss:
                break
            else:
                epoch_list.append(epoch+1)
                prev_train_loss = curr_train_loss
                train_loss.append( curr_train_loss )
                test_loss.append( logloss(y_test, test_predict) )
                train_accuracy = getPredictions(y_train, train_predict)
                train_accuracies.append(train_accuracy)
                test_accuracy = getPredictions(y_test, test_predict)
                test_accuracies.append(test_accuracy)
        results = pd.DataFrame({ "Epochs": epoch_list,
                                "Train Loss": train_loss,
                                "Test Loss": test_loss,
                                "Train Accuracy": train_accuracies,
                                "Test Accuracy": test_accuracies })
        
        return results, weights, bias
        
    epochs = 1000
    learning_rate = 0.001
    main_results, weights, bias = logistic_regression(x_train, y_train, x_test, y_test, epochs, learning_rate)
    display(main_results)
    
    main_results.plot(x='Epochs', y=['Train Loss', 'Test Loss'], kind="line")
    plt.ylabel('Loss')
    plt.title('Epochs vs Loss for Train and Test data')
    plt.show()
    
    def getTestAccuracy(weights, bias, X_test, y_test):
        n = len(X_test)
        y_pred = []
        for i in range(n):
            y_pred.append( predict(weights, bias, X_test[i]) )
        accuracy = getPredictions(y_test, y_pred)
        return accuracy
    
    accuracy = getTestAccuracy(weights, bias, x_test, y_test)
    print(f'For Test Dataset:')
    print(f'Accuracy = {accuracy} %')'''

def knn_scratch():
    return '''
    ##MAKE TRAIN, VAL and TEST SPLIT

    class KNN:
        def __init__(self, X, y, k, classification=True):
            self.X_train = X
            self.y_train = y
            self.k = k
            self.classification = classification
        def euc_dis(self, p1, p2):
            distance = np.linalg.norm(p1-p2)
            return distance
        def get_k_neighbors(self, p1):
            distances = []
            for p2 in self.X_train:
                distances.append(self.euc_dis(p1, p2))
            distances = np.asarray(distances)
            indices = np.argpartition(distances, self.k)
            k_first_indices = indices[:self.k]
            return k_first_indices
        def predict_class(self, p1):
            knn_indices = self.get_k_neighbors(p1)
            knn_labels = []
            for i in knn_indices:
                knn_labels.append(self.y_train[i])
            occurrences = np.bincount(knn_labels)
            mode = np.argmax(occurrences)
            return mode
        def get_accuracy(self, y_true, y_pred):
            correct = y_true == y_pred
            acc = (np.sum(correct) / y_true.shape[0]) * 100.0
            return acc
    
    K = [1,3,5,7,9,11,13,15,17,19,21,23,25]
    accuracies = []
    for k in K:
        classifier = KNN(x_train, y_train, k)
        preds = []
        for i in x_val:
            preds.append(classifier.predict_class(i))
        acc = classifier.get_accuracy(y_val, preds)
        accuracies.append(acc)
        print(f"Accuracy for k = {k} => {acc}")
    
    plt.plot(K, accuracies)
    plt.title('Hyperparameter vs. accuracy')
    plt.xlabel('Value of k')
    plt.ylabel('Accuracy')
    plt.show()
    
    losses = []
    for i in accuracies:
        loss = (1-(i/100)) * 100
        losses.append(loss)
    plt.plot(K, losses)
    plt.title('Hyperparameter vs. Loss')
    plt.xlabel('Value of k')
    plt.ylabel('Loss')
    plt.show()
    
    classifier1 = KNN(x_train, y_train, 21)
    classifier2 = KNN(x_train, y_train, 23)
    preds_21 = []
    preds_23 = []
    for i in x_test:
        preds_21.append(classifier1.predict_class(i))
        preds_23.append(classifier2.predict_class(i))
    acc_21 = classifier1.get_accuracy(y_test, preds)
    acc_23 = classifier2.get_accuracy(y_test, preds)
    acc_21, acc_23'''

def gridcv():
    return '''
    svm = SVC()
    parameters = {'C': [.001, .01, .1, 1, 10, 100], 'gamma': [.001, .01, .1, 1, 10, 100]}
    svm_grid = GridSearchCV(estimator=svm, param_grid=parameters, n_jobs=-1, cv=5, return_train_score=True)
    svm_grid.fit(X_train_scaled, y_train)
    
    params_list = [str((x['C'], x['gamma'])) for x in svm_grid.cv_results_['params']]
    
    fig = plt.figure(figsize = (13,6))
    plt.title("hyperparameters vs accuracy")
    plt.plot(params_list, svm_grid.cv_results_['mean_train_score'], label="train accuracy")
    plt.plot(params_list, svm_grid.cv_results_['mean_test_score'], label="cv accuracy")
    plt.xlabel("(C, gamma) pair")
    plt.ylabel("accuracy")
    plt.xticks(rotation=90)
    plt.show()
    
    print(f"Best score: {svm_grid.best_score_}")
    print(f"Best parmeters: {svm_grid.best_params_}")
    '''
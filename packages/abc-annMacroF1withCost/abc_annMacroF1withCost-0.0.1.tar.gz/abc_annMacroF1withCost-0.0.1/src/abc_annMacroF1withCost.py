class ABC_ANN:
    def __init__(self, inputX, weightMat, target, HLS, k, P, limit, lb, ub, MR, parallelType):
        # This code line determines the parallel type using numpy or cupy
        self.comp = parallelType
        self.X = inputX
        # self.XwithBias = self.comp.append(self.comp.ones((self.X.shape[0], 1)), self.X, axis=1)
        self.FVS = inputX.shape[1]
        self.weightMat = weightMat
        self.y = target
        self.k = k  # the number of output neurons
        # self.k = self.comp.unique(target).shape[0]
        # self.yOneHot = self.oneHotEncoder(target, k)
        self.P = P  # P is population size
        self.limit = limit
        self.HLS = HLS
        # D refers to dimension
        self.D = (self.FVS + 1) * HLS + (HLS + 1) * self.k
        self.lb = lb  # lower bound for parameters
        self.ub = ub  # upper bound for parameters
        self.MR = MR  # modification rate
        self.evaluationNumber = 0
        self.tmpID = [-1] * self.P
        # self.Foods = self.lb + self.comp.random.rand(self.P, self.D) * (self.ub - self.lb)
        self.Foods = self.comp.random.uniform(
            self.lb, self.ub, (self.P, self.D))
        self.solution = self.comp.copy(self.Foods)
        self.f = self.calculateF(self.Foods)
        # self.fitness = 1 / (1 + self.f)
        self.trial = self.comp.zeros(P)
        self.globalMax = self.f[0, 0]
        self.globalParams = self.comp.copy(self.Foods[0:1])  # 1st row
        self.scoutBeeCounts = 0

    def create_new(self, index):
        # new_sol = self.lb + self.comp.random.rand(1, self.D) * (self.ub - self.lb)
        new_sol = self.comp.random.uniform(self.lb, self.ub, size=(1, self.D))
        self.Foods[index, :] = new_sol.flatten()
        self.solution[index, :] = self.comp.copy(new_sol.flatten())
        self.f[index] = self.calculateF(new_sol)[0]
        # self.fitness[index] = 1 / (1 + self.f[index])
        self.trial[index] = 0
        self.scoutBeeCounts += 1

    # def oneHotEncoder(self, y, k):
    #   n = y.shape[0]
    #   res = self.comp.zeros((n,k))
    #   res[self.comp.arange(n), y.reshape(-1,)] = 1
    #   return res

    def memorizeBestSource(self):
        index = self.comp.argmax(self.f)
        if self.f[index, 0] > self.globalMax:
            self.globalMax = self.f[index, 0]
            self.globalParams = self.comp.copy(self.Foods[index: index + 1])

    def calculateProbabilities(self):
        maxfit = self.comp.max(self.f)
        self.prob = (0.9 * (self.f / maxfit)) + 0.1

    def sendEmployedBees(self):
        for i in range(self.P):  # for each clone
            ar = self.comp.random.rand(self.D)
            param2change = self.comp.where(ar < self.MR)[0]
            neighbour = self.comp.random.randint(0, self.P)
            while neighbour == i:
                neighbour = self.comp.random.randint(0, self.P)
            self.solution[i, :] = self.comp.copy(
                self.Foods[i, :])  # ?????????????
            # self.solution[i, :] = self.Foods[i, :] #?????????????
            # random number generation between -1 and 1 values
            r = -1 + (1 + 1) * self.comp.random.rand()
            # self.solution[i, param2change] = self.Foods[i, param2change] + r * (self.Foods[i, param2change] - self.Foods[neighbour, param2change])  # self.comp.copy ?
            # self.solution[i, param2change] = self.comp.where(self.solution[i, param2change] < self.lb, self.lb, self.solution[i, param2change])
            # self.solution[i, param2change] = self.comp.where(self.solution[i, param2change] > self.ub, self.ub, self.solution[i, param2change])
            arr = self.solution[i, param2change]
            # self.comp.copy ?
            arr = arr + r * (arr - self.Foods[neighbour, param2change])
            arr[arr < self.lb] = self.lb
            arr[arr > self.ub] = self.ub
            self.solution[i, param2change] = arr

    def sendOnLookerBees(self):
        i = 0
        t = 0
        while t < self.P:
            if self.comp.random.rand() < self.prob[i, 0]:
                ar = self.comp.random.rand(self.D)
                param2change = self.comp.where(ar < self.MR)[0]

                neighbour = self.comp.random.randint(self.P)
                while neighbour == i:
                    neighbour = self.comp.random.randint(self.P)

                self.solution[t, :] = self.comp.copy(self.Foods[i, :])
                # self.solution[t, :] = self.Foods[i, :]
                # v_{ij} = x_{ij} + phi_{ij}*(x_{kj}-x_{ij})
                # random number generation between -1 and 1 values
                r = -1 + (1 + 1) * self.comp.random.rand()

                # self.solution[t, param2change] = self.Foods[i, param2change] + r * (self.Foods[i, param2change] - self.Foods[neighbour, param2change])  # self.comp.copy ?
                # self.tmpID[t] = i
                # self.solution[t, param2change] = self.comp.where(self.solution[t, param2change] < self.lb, self.lb, self.solution[t, param2change])
                # self.solution[t, param2change] = self.comp.where(self.solution[t, param2change] > self.ub, self.ub, self.solution[t, param2change])

                arr = self.Foods[i, param2change]
                # self.comp.copy ?
                arr = arr + r * (arr - self.Foods[neighbour, param2change])
                self.tmpID[t] = i
                arr[arr < self.lb] = self.lb
                arr[arr > self.ub] = self.ub
                self.solution[t, param2change] = arr

                t += 1
            i += 1
            if i >= self.P:
                i = 0

    def sendScoutBees(self):
        index = self.comp.argmax(self.trial)
        if self.trial[index] >= self.limit:
            self.create_new(index)

    def calculateMacroF1withWeightedError(self, predicted):
        weight_res = self.comp.zeros(predicted.shape[1])
        f1_res = self.comp.zeros((self.k, predicted.shape[1]))
        for i in range(self.k):
            p = predicted == i
            a = self.y == i
            tp = self.comp.sum(p * a, axis=0)
            fp = self.comp.sum(p, axis=0) - tp
            fn = self.comp.sum(a) - tp
            f1 = self.comp.zeros(tp.shape)
            ind = tp != 0
            precision = tp[ind] / (tp[ind] + fp[ind])
            recall = tp[ind] / (tp[ind] + fn[ind])
            f1[ind] = 2*precision*recall / (precision+recall)
            f1_res[i, :] = f1
            for j in range(self.k):
                if i != j:
                    weight_res += self.comp.sum(
                        predicted[a.flatten(), :] == j, axis=0) * self.weightMat[i, j]
        return (self.comp.mean(f1_res, axis=0) + 1) / (weight_res + 1)

    def calculateF(self, foods):
        N, D = self.X.shape
        P = foods.shape[0]
        p_s = self.comp.zeros((self.k, N, P))
        for i in range(self.k):
            p_s[i, :, :] += foods[:, -self.k + i]  # bias addition
        for i in range(self.HLS):
            W1i = foods[:, i*D: (i+1)*D].T
            b1i = foods[:, D*self.HLS + self.HLS*self.k + i]
            z_i = self.sig(self.X.dot(W1i) + b1i)
            for j in range(self.k):
                p_s[j, :, :] += z_i * foods[:, D * self.HLS + 2*j + i]
        p_s = self.comp.exp(p_s)
        total = p_s.sum(axis=0)
        p_s = p_s / total
        p = self.comp.argmax(p_s, axis=0)  # prediction
        f = self.calculateMacroF1withWeightedError(p).reshape(-1, 1)
        self.evaluationNumber += len(f)
        return f

    def sig(self, n):  # Sigmoid function
        return 1 / (1 + self.comp.exp(-n))


class LearnABC:
    def __init__(self, weightMat, inputX, target, hiddenLayerSize, k, P, limit, lb, ub, MR, parallelType, evaluationNumber):
        self.comp = parallelType
        self.abc = ABC_ANN(inputX, weightMat, target,
                           hiddenLayerSize, k, P, limit, lb, ub, MR, parallelType)
        self.total_numberof_evaluation = evaluationNumber

    def learn(self):
        self.f_values = []
        self.abc.memorizeBestSource()
        self.f_values.append(self.abc.globalMax)

        # sayac = 0
        while self.abc.evaluationNumber <= self.total_numberof_evaluation:
            self.abc.sendEmployedBees()
            objValSol = self.abc.calculateF(self.abc.solution)
            # fitnessSol = 1 / (1 + objValSol)
            # a greedy selection is applied between the current solution i and its mutant
            # If the mutant solution is better than the current solution i, replace the solution with the mutant and reset the trial counter of solution i

            ind = self.comp.where(objValSol > self.abc.f)[0]
            ind2 = self.comp.where(objValSol <= self.abc.f)[0]
            self.abc.trial[ind] = 0

            self.abc.Foods[ind, :] = self.abc.solution[ind, :]
            self.abc.f[ind] = objValSol[ind]
            # self.abc.fitness[ind] = fitnessSol[ind]
            # if the solution i can not be improved, increase its trial counter
            self.abc.trial[ind2] += 1

            self.abc.calculateProbabilities()
            self.abc.sendOnLookerBees()

            objValSol = self.abc.calculateF(self.abc.solution)
            # fitnessSol = 1 / (1 + objValSol)

            for i in range(self.abc.P):
                t = self.abc.tmpID[i]
                if objValSol[i] > self.abc.f[t]:
                    self.abc.trial[t] = 0
                    self.abc.Foods[t, :] = self.abc.solution[i, :]
                    self.abc.f[t] = objValSol[i]
                    # self.abc.fitness[t] = fitnessSol[i]
                else:
                    self.abc.trial[t] += 1

            self.abc.sendScoutBees()
            self.abc.memorizeBestSource()

            self.f_values.append(self.abc.globalMax)
            # sayac += 1;
            # if sayac % 5000 == 0: print(f"Sayaç = {sayac}")

        self.net = self.abc.globalParams
        self.globalMax = self.abc.globalMax
        # print(f"Evaluation Number: {self.abc.evaluationNumber}")
        print(f"The number of scout bees: {self.abc.scoutBeeCounts}")


class ABC_LR_Model():
    def __init__(self, hiddenLayerSize=3, k=2, lb=-32, ub=32, evaluationNumber=60000, limit=50, P=40, MR=0.1, weightMat=None, parallelType=None):
        '''
        lb is lower bound for parameters to be learned
        ub is upper bound for parameters to be learned
        limit determines whether a scout bee can be created. 
        If a solution cannot be improved up to the limit number, a scout bee is created instead of the solution.
        '''
        self.lb = lb
        self.ub = ub
        self.evaluationNumber = evaluationNumber
        self.limit = limit
        self.P = P
        self.MR = MR
        self.parallelType = parallelType
        self.HLS = hiddenLayerSize
        self.k = k  # the number of classes
        self.weightMat = weightMat

    def fit(self, trainX, trainY):
        learn = LearnABC(self.weightMat, trainX, trainY, self.HLS, self.k, self.P,
                         self.limit, self.lb, self.ub, self.MR, self.parallelType, self.evaluationNumber)
        learn.learn()
        self.net = learn.net

    def __str__(self) -> str:
        return f"lb={self.lb}, ub={self.ub}, evaNumber={self.evaluationNumber}, limit={self.limit}, P={self.P}, MR={self.MR}, HLS={self.HLS}"

    def sig(self, x):
        return 1 / (1 + self.parallelType.exp(-x))

    def f1_score_multi(self, actual, predicted):
        res = self.parallelType.zeros((self.k, predicted.shape[1]))
        for i in range(self.k):
            p = predicted == i
            a = actual == i
            tp = self.parallelType.sum(p * a, axis=0)
            fp = self.parallelType.sum(p, axis=0) - tp
            fn = self.parallelType.sum(a) - tp
            f1 = self.parallelType.zeros(tp.shape)
            ind = tp != 0
            precision = tp[ind] / (tp[ind] + fp[ind])
            recall = tp[ind] / (tp[ind] + fn[ind])
            f1[ind] = 2*precision*recall / (precision+recall)
            res[i, :] = f1
        return self.parallelType.mean(res, axis=0)

    def calculateWeightedError(self, actual, predicted):
        confMat = self.parallelType.zeros((self.k, self.k))
        for i in range(self.k):
            for j in range(self.k):
                confMat[i, j] = self.parallelType.sum(
                    predicted[(actual == i)] == j)
        meanError = self.parallelType.sum(
            confMat * self.weightMat) / len(actual)
        return [confMat, meanError]

    def score(self, X, y):
        N, D = X.shape
        p_s = self.parallelType.zeros((N, self.k))
        p_s += self.net[:, -self.k:]  # bias addition
        for i in range(self.HLS):
            W1i = self.net[:, i*D: (i+1)*D].T
            b1i = self.net[:, D*self.HLS + self.HLS*self.k + i]
            z_i = self.sig(X.dot(W1i) + b1i)
            for j in range(self.k):
                p_s[:, j] += (z_i.flatten() *
                              self.net[:, D * self.HLS + 2*j + i])

        expA = self.parallelType.exp(p_s)
        p = expA / expA.sum(axis=1, keepdims=True)
        p = self.parallelType.argmax(p, axis=1).reshape(-1, 1)  # prediction

        acc = self.parallelType.average(y == p)
        f1 = self.f1_score_multi(y, p)
        [confMat, meanError] = self.calculateWeightedError(y, p)
        return [acc, f1, p, confMat, meanError]

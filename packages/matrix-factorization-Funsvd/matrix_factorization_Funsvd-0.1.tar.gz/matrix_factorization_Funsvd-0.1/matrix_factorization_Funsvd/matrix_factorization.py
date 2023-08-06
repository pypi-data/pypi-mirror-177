import numpy as np

class FunkSVD():

    """
    This function performs matrix factorization using a basic form of FunkSVD without regularization term, user biases and items  biases
    
    INPUT Parameters :
    ----------------
    latent_factors - (int), default=20
                      The number of latent features (latent factors) used
    
    learning_rate  - (float), default=0.005
                      The learning rate tuning parameter 
    
    n_iters - (int), default=200
                The number of iterations (n_epochs)

    init_mean –(float) Default=0
               The mean of the normal distribution for factor vectors initialization. Default is 0

    init_std_dev-(float) Default=0 
               The standard deviation of the normal distribution for factor vectors initialization  Default is 0       
    
    OUTPUT:
    ------
    users_matrix - (numpy array) 
                 a user(u) by latent feature(k) matrix
                 
    items_matrix - (numpy array) 
                 a latent feature(k) by items(i) matrix
    
    ratings_matrix_pred - (numpy array),
                 a user by items matrix
                  
    Verbose- (Bool) 
                If True, will print computed value. Default is True.
    
    """

    def __init__(self, latent_factors=20, learning_rate=0.005, init_mean=0, init_std_dev=1, n_iters=500):

        self.latent_factors = latent_factors
        self.learning_rate = learning_rate
        self.n_iters = n_iters
        self.init_mean = init_mean
        self.init_std_dev = init_std_dev

    def fit(self, X, verbose=True):
        """
       INPUT Parameters :
       ----------------
        X-(numpy array) 
          user_item matrix (true rating matrix) with shape user x item
        
       OUTPUT  Parameters :
        ------------------
       user_mat - (numpy array) 
                  a user by latent feature matrix
                  
       items_mat - (numpy array) 
                 a latent feature by items matrix (here movie matrix)  
        
        """

        # number of rows in the user_item matrix : n_users
        n_users = X.shape[0]
        # number of columns in the user_item matrix : n_items
        n_items = X.shape[1]
        # total number of ratings in the user_item matrix : n_ratings
        n_ratings = np.count_nonzero(~np.isnan(X))

        # user_item matrix (X) can be decomposed into two thin matrices user_matrix and item_matrix :
        # users_matrix filled with random values of shape users x latent
        # items_matrix filled with random values of shape latent x items
        users_matrix = self.init_std_dev * \
            np.random.randn(n_users, self.latent_factors) + self.init_mean
        items_matrix = self.init_std_dev * \
            np.random.randn(self.latent_factors, n_items) + self.init_mean

        # keep track of iteration and MSE
        if verbose == True:
            print("Optimizaiton Statistics : ")
            print("Epochs | MSE ")

        # initialize sse at 0 for first iteration
        sse_accum = 0

        # for each iteraction
        for iteration in range(1, self.n_iters+1):
            # update our sse
            old_sse = sse_accum
            sse_accum = 0
            # iters.append(iteration)

            # For each user-items pair(u,i)
            for u in range(n_users):
                for i in range(n_items):
                    if X[u, i] > 0:
                        for k in range(self.latent_factors):
                            # predict rating
                            pred = np.dot(
                                users_matrix[u, :], items_matrix[:, i])
                            # sum of square error
                            sse_accum += (X[u, i]-pred)**2
                            # update weights for users_matrix and items_matrix by using SGD
                            users_matrix[u, k] = users_matrix[u, k]+2 * \
                                self.learning_rate * \
                                (X[u, i]-pred)*items_matrix[k, i]
                            items_matrix[k, i] = items_matrix[k, i]+2 * \
                                self.learning_rate * \
                                (X[u, i]-pred)*users_matrix[u, k]

        
            if verbose == True:
                print("%s \t %f" % ("{}".format(iteration), sse_accum / n_ratings))

        return np.around(np.dot(users_matrix, items_matrix)), users_matrix, items_matrix

    def MSE(self, true_rating_matrix, pred_rating_matrix):
        """
        INPUT Parameters :
        ----------------
        true_rating_matrix-(numpy array) true user_item matrix (original matrix) with shape user x item
        
        pred_rating_matrix-(numpy array) prediction user_item matrix with shape user x item
        
       OUTPUT Parameters :
        ------------------
        Mean Squarred Error  of predictions (MSE) - (float) 
        
        """
        n_users = true_rating_matrix.shape[0]       # number of rows in the user_item matrix : n_users
        # number of columns in the user_item matrix : n_items
        n_items = true_rating_matrix.shape[1]
        # total number of ratings in the user_item matrix : n_ratings
        n_ratings = np.count_nonzero(~np.isnan(true_rating_matrix))

        # initialize sum of square error (sse) at 0
        sse_accum = 0
        for i in range(n_users):
            for j in range(n_items):
                if true_rating_matrix[i, j] != np.nan:
                    sse_accum += (true_rating_matrix[i, j] -
                                  pred_rating_matrix[i, j])**2
        MSE = sse_accum/n_ratings

        return print(f"MSE: {MSE:0.4f}")

    def RMSE(self, true_rating_matrix, pred_rating_matrix):
        """
        INPUT Parameters :
        ----------------
        true_rating_matrix-(numpy array) true user_item matrix (original matrix) with shape user x item
        
        pred_rating_matrix-(numpy array) prediction user_item matrix with shape user x item
        
       OUTPUT Parameters :
        ------------------
        Root Mean Squarred Error  of predictions(RMSE) - (float)
        
        """
        n_users = true_rating_matrix.shape[0]       # number of rows in the user_item matrix : n_users
        # number of columns in the user_item matrix : n_items
        n_items = true_rating_matrix.shape[1]
        # total number of ratings in the user_item matrix : n_ratings
        n_ratings = np.count_nonzero(~np.isnan(true_rating_matrix))

        # initialize sum of square error (sse) at 0
        sse_accum = 0

        for i in range(n_users):
            for j in range(n_items):
                if true_rating_matrix[i, j] != np.nan:
                    sse_accum += (true_rating_matrix[i, j] -
                                  pred_rating_matrix[i, j])**2

        RMSE = np.sqrt(sse_accum/n_ratings)

        return print(f"RMSE: {RMSE:0.4f}")

    def MAE(self, true_rating_matrix, pred_rating_matrix, verbose=True):
        """
        INPUT Parameters :
        ----------------
        true_rating_matrix-(numpy array) true user_item matrix (original matrix) with shape user x item
        
        pred_rating_matrix-(numpy array) prediction user_item matrix with shape user x item
        
       OUTPUT Parameters :
        ------------------
         Mean Absolute Error  of predictions(MAE) - (float) 
        
        """
        n_users = true_rating_matrix.shape[0]       # number of rows in the user_item matrix : n_users
        # number of columns in the user_item matrix : n_items
        n_items = true_rating_matrix.shape[1]
        # total number of ratings in the user_item matrix : n_ratings
        n_ratings = np.count_nonzero(~np.isnan(true_rating_matrix))

        # initialize sum of square error (sse) at 0
        sse_accum = 0

        for i in range(n_users):
            for j in range(n_items):
                if true_rating_matrix[i, j] != np.nan:
                    sse_accum += abs(true_rating_matrix[i,j]-pred_rating_matrix[i, j])

        MAE = sse_accum/n_ratings

        return print(f"MAE: {MAE:0.4f}")



import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



customers = pd.read_csv("Ecommerce Customers")

sns.set_palette("GnBu_d")
sns.set_style('whitegrid')

sns_jointplot = sns.jointplot(x='Time on App',y='Yearly Amount Spent',data=customers)
sns_jointplot.savefig("ecs_jointPlot.jpg")

sns_pairplot = sns.pairplot(customers)
sns_pairplot.savefig("ecs_pairPlot.jpg")

sns_lmplot = sns.lmplot(x='Length of Membership',y='Yearly Amount Spent',data=customers)
sns_lmplot.savefig("ecs_lmPlot.jpg")
# Training and Testing Data
# Set a variable X equal to the numerical features of the customers and a variable y equal to the "Yearly Amount Spent" column.

y = customers['Yearly Amount Spent']

X = customers[['Avg. Session Length', 'Time on App','Time on Website', 'Length of Membership']]

# Use model_selection.train_test_split from sklearn to split the data into training and testing sets. Set test_size=0.3 and random_state=101
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split( X
                                                    , y
                                                    , test_size=0.33
                                                    , random_state=101
                                                    )

# Now its time to train our model on our training data!
from sklearn.linear_model import LinearRegression
lm = LinearRegression()

# Train/fit lm on the training data.
lm.fit(X_train, y_train)

# Print out the coefficients of the model
# lm.coef_

# Predicting Test Data
# Now that we have fit our model, let's evaluate its performance by predicting off the test values!
predictions = lm.predict(X_test)

# Create a scatterplot of the real test values versus the predicted values. 
sns.scatterplot(x=predictions, y=y_test)

# Evaluating the Model
# Let's evaluate our model performance by calculating the residual sum of squares and the explained variance score (R^2).
# Calculate the Mean Absolute Error, Mean Squared Error, and the Root Mean Squared Error. Refer to the lecture or to Wikipedia for the formulas
from sklearn import metrics
print('MAE:', metrics.mean_absolute_error(y_test, predictions))
print('MSE:', metrics.mean_squared_error(y_test, predictions))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))

# Conclusion
"""
We still want to figure out the answer to the original question, do we focus our efforst on mobile app or website development? Or maybe that doesn't even really matter, 
and Membership Time is what is really important. 
Let's see if we can interpret the coefficients at all to get an idea.
"""
coeffecients = pd.DataFrame(lm.coef_,X.columns)
coeffecients.columns = ['Coeffecient']

plt.plot(coeffecients)

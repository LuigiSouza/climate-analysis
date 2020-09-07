import pandas            as pd
from sklearn.model_selection          import train_test_split
from sklearn.linear_model             import LinearRegression
from sklearn.tree                     import DecisionTreeRegressor
from collections                      import OrderedDict
from sklearn.metrics                  import max_error
from sklearn.metrics                  import mean_squared_error, r2_score
from sklearn.metrics                  import mean_absolute_error, median_absolute_error

# ==========================================================

# loads the dataset
arquivo = pd.read_csv("../planilhas/planilha-header.csv")

# split the data into training/testing sets
y = arquivo['Energia']
x = arquivo.drop('Energia', axis = 1)
# drops the unecessary columns
x = x.drop('Insolacao', axis = 1)
x = x.drop('Data', axis = 1)
x = x.drop('Estacao', axis = 1)

x['Periodo'] = x['Periodo'].replace('Winter', 1)
x['Periodo'] = x['Periodo'].replace('Autumn', 2)
x['Periodo'] = x['Periodo'].replace('Spring', 3)
x['Periodo'] = x['Periodo'].replace('Summer', 4)

# Split the targets into training/testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)

# Create linear regression object
linear_model = LinearRegression()

# Train the model using the training sets
linear_model.fit(x_train, y_train)
result = linear_model.score(x_test, y_test)

# Make predictions using the testing set
y_pred = linear_model.predict(x_test)

# The coefficients
print('Coefficients: \n', linear_model.coef_)
# The mean squared error
print('Mean squared error: %.2f'
      % mean_squared_error(y_test, y_pred))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_score(y_test, y_pred))
# The mean absolute error
print("The Mean Absolute Error: %.2f " % mean_absolute_error(y_test, y_pred))
# The median absolute error
print("The Median Absolute Error: %.2f " % median_absolute_error(y_test, y_pred))
# The maximum residual error
print("The Maximum Residual Error: %.2f " % max_error(y_test, y_pred))
# show the score result
result = linear_model.score(x_test, y_test)
print("LinearRegression:", result)

# loads the dataset used in real prediction
planilha = open("../planilhas/energia.csv", "w")

# starts the output file
x_hoje = pd.read_csv("../planilhas/prever.csv").drop('Energia', axis = 1)

x_hoje['Periodo'] = x_hoje['Periodo'].replace('Winter', 1)
x_hoje['Periodo'] = x_hoje['Periodo'].replace('Autumn', 2)
x_hoje['Periodo'] = x_hoje['Periodo'].replace('Spring', 3)
x_hoje['Periodo'] = x_hoje['Periodo'].replace('Summer', 4)

# Make predictions using the testing set
previsoes = linear_model.predict(x_hoje)

aux = str(previsoes)
aux = aux.replace("[ ", "")
aux = aux.replace("[", "")
aux = aux.replace("]", "")
aux = aux.replace("  ", "\n")
aux = aux.replace(" ", "\n")
aux = aux.replace("\n\n","\n")
planilha.write(aux)
planilha.close()

soma = 0

for i in range (100):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25)
    modelo = DecisionTreeRegressor(max_depth=4)

    modelo.fit(x_train, y_train)

    result = modelo.score(x_test, y_test)

    soma += result

# same thing but with DecisionTree algorithm
print("\n\DecisionTreeRegressor:", soma/100)

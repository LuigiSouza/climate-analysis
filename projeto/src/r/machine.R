library(caret)
setwd("C:/Users/luigi/OneDrive/Área de Trabalho/ERE/projeto/src/r")

rm(list = ls())

filename <- "planilha-header.csv"
dataset <- read.csv(filename)

View(dataset)

set.seed(7)

linhas <- sample(1:length(dataset$Energia),length(dataset$Energia)*0.75)

treino = dataset[linhas,]
teste = dataset[-linhas,]

library(rpart)
modelo <- rpart(Energia ~ . ,data=treino,control=rpart.control(cp=0))

teste$Previsao <- predict(modelo,teste)

View(teste)


teste$P <- abs(round(teste$Previsao/teste$Energia,4)-1)
R_1 <- summary(teste$P)
R_1

hist(teste$Energia[teste$Energia<quantile(teste$Energia,0.90)], breaks = 8,labels = T)


R_Final_1 <- summary(teste$P[teste$Energia>5 & teste$Energia<20])
R_1
R_Final_1

hoje <- data.frame(Precipitacao = c(0),
                   Umidade = c(69),
                   Nebulosidade = c(8),
                   TempMaxima = c(14),
                   TempMinima = c(6),
                   DiaMes = c(97),
                   Temp1 = c(12),
                   Temp2 = c(12),
                   Temp3 = c(12),
                   Temp4 = c(12),
                   Temp5 = c(14),
                   Temp6 = c(13))
amanha <- data.frame(Precipitacao = c(10),
                     Umidade = c(63),
                     Nebulosidade = c(0),
                     TempMaxima = c(18),
                     TempMinima = c(4),
                     DiaMes = c(107),
                     Temp1 = c(14),
                     Temp2 = c(15),
                     Temp3 = c(16),
                     Temp4 = c(17),
                     Temp5 = c(18),
                     Temp6 = c(15))

teste$PrevisaoHoje <- predict(modelo,hoje)
teste$PrevisaoAmanha <- predict(modelo,amanha)


validation_index <- createDataPartition(dataset$Energia, p=0.75, list=FALSE)

validation <- dataset[-validation_index,]
dataset <- dataset[validation_index,]

# split input and output
x <- dataset[,1:13]
y <- dataset[,14]

# Run algorithms using 10-fold cross validation
control <- trainControl(method="cv", number=10)
metric <- "Accuracy"

# b) linear algorithms
set.seed(7)
fit.lda <- train(Energia~., data=dataset, method="lda", metric=metric, trControl=control)
# b) nonlinear algorithms
# CART
set.seed(7)
fit.cart <- train(Energia~., data=dataset, method="rpart", metric=metric, trControl=control)
# kNN
set.seed(7)
fit.knn <- train(Energia~., data=dataset, method="knn", metric=metric, trControl=control)
# c) advanced algorithms
# SVM
set.seed(7)
fit.svm <- train(Energia~., data=dataset, method="svmRadial", metric=metric, trControl=control)
# Random Forest
set.seed(7)
fit.rf <- train(Energia~., data=dataset, method="rf", metric=metric, trControl=control)

def assign1():
    ans='''
    from sklearn.model_selection import train_test_split\n
    import pandas as pd\n
    import numpy as np\n
    import matplotlib.pyplot as plt\n
    df=pd.read_csv('uber.csv')\n
    df\n
    df.isnull().sum()\n
    df.dropna(inplace=True)\n
    df.isnull().sum()\n
    df.pickup_datetime=pd.to_datetime(df.pickup_datetime,errors='coerce')\n
    df\n
    df=df.assign(hour=df.pickup_datetime.dt.hour,year=df.pickup_datetime.dt.year, month=df.pickup_datetime.dt.month,day=df.pickup_datetime.dt.day)\n
    df\n
    x=df [ [ 'pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude','passenger_count']]\n
    x\n
    y=df[['fare_amount']]\n
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3)\n
    from sklearn.linear_model import LinearRegression\n
    m1=LinearRegression()\n
    m1.fit(x_train,y_train)\n
    y_pred1=m1.predict(x_test)\n
    from sklearn.metrics import r2_score,accuracy_score\n
    r2_score(y_test,y_pred1)\n

    '''
    return ans

def assign2():
    ans='''
    import pandas as pd\n
import numpy as np\n
from sklearn.model_selection import train_test_split\n
from sklearn.preprocessing import scale\n
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report\n
from sklearn.neighbors import KNeighborsClassifier\n
from sklearn.svm import SVC\n
df=pd.read_csv('emails.csv')\n
df\n
df.dropna(inplace=True)\n
df.drop(['Email No.'],axis=1,inplace=True)\n
x=df.drop(['Prediction'],axis=1)\n
y=df['Prediction']\n
x=scale(x)\n
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3)\n
knn=KNeighborsClassifier(n_neighbors=7)\n
knn.fit(x_train,y_train)\n
svm_mod=SVC(C=1)\n
svm_mod.fit(x_train,y_train)\n
y_pred_knn =knn.predict(x_test)\n
y_pred_svm=svm_mod.predict(x_test)\n
accuracy_score(y_test,y_pred_knn)\n
accuracy_score(y_test,y_pred_svm)\n
confusion_matrix(y_test,y_pred_knn)\n
confusion_matrix(y_test,y_pred_svm)\n

    '''
    return ans


def assign3():
    ans='''
    import pandas as pd\n
import numpy as np\n
import matplotlib.pyplot as plt\n
from sklearn.preprocessing import StandardScaler\n
import keras\n
from keras.models import Sequential\n
from sklearn.model_selection import train_test_split\n
df=pd.read_csv('Churn_Modelling.csv')\n
    df\n
    states =pd.get_dummies(df['Geography'])\n
    sex =pd.get_dummies(df['Gender'])\n
    df= pd.concat([df,states,sex],axis=1)\n
    df\n
    X=df[ [ 'CreditScore','Age','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary','Germany','Spain','Female','Male']]\n
X.shape\n
y=df['Exited']\n
 y\n
 x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.3)\n
sc=StandardScaler()\n
x_train=sc.fit_transform(x_train)\n
x_test=sc.transform(x_test)\n
model= Sequential()\n
model.add( Dense( activation='relu',input_dim = 12,units=6,kernel_initializer='uniform'))\n
model.add( Dense( activation='relu',units=6,kernel_initializer='uniform'))\n
model.add( Dense( activation='sigmoid',units=1,kernel_initializer='uniform'))\n
model.compile(optimizer='adam',loss='binary_crossentropy')\n
model.summary()\n
model.fit(x_train,y_train,batch_size=10,epochs=50)\n
y_pred=model.predict(x_test)\n
y_pred=(y_pred>0.5)\n
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report\n
confusion_matrix(y_test,y_pred)\n
print(classification_report(y_test,y_pred))\n
accuracy_score(y_test,y_pred)\n



    '''
    return ans

def assign4():
    ans='''
    current_x=2 \n
rate=0.01\n
prev_step_size=1\n
precision=0.000001\n
iters=0\n
max_iters=1000\n
df= lambda x: 2*(x+3)\n\n\n\n\n
    while( precision <prev_step_size and iters<max_iters):\n
    prev_x=current_x\n
    current_x =current_x - rate*df(prev_x)\n
    prev_step_size= abs(current_x-prev_x)\n
    iters=iters +1\n
    print(iters,"curent value for x is ",current_x,"\n")\n
    
print("local minima val:" ,current_x)\n
    '''
    return ans

def assign5():
    ans='''  
    import pandas as pd \n
import numpy as np\n
import matplotlib.pyplot as plt\n
from sklearn.model_selection import train_test_split\n
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score\n
    df=pd.read_csv('diabetes.csv')\n
df\n
df.columns\n
df.isnull().sum()\n
X=df.drop(['Outcome'],axis=1)\n
X\n
y=df['Outcome']\n
y\n
from sklearn.preprocessing import scale\n
#X=scale(X)\n
x_train,x_test,y_train,y_test =train_test_split(X,y,test_size=0.25)\n
from sklearn.neighbors import KNeighborsClassifier\n
model=KNeighborsClassifier(n_neighbors=7)\n
model.fit(x_train,y_train)\n
y_pred=model.predict(x_test)\n
accuracy_score(y_test,y_pred)\n
cf=confusion_matrix(y_test,y_pred)\n
cf\n
cr=classification_report(y_test,y_pred)\n
print(cr)\n

    '''
    return ans




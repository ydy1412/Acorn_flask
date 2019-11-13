import keras
from keras.models import Sequential
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras import backend as K

from sklearn.metrics import f1_score
from sklearn.preprocessing import OneHotEncoder

from keras import regularizers
from keras.layers import Dense,Dropout
from keras.models import model_from_yaml

import sys
import numpy as np

from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import RandomOverSampler
from imblearn.over_sampling import ADASYN
from imblearn.combine import SMOTETomek
from imblearn.combine import SMOTEENN

from sklearn.model_selection import train_test_split

class NN_model :
    def __init__(self,loss="sparse_categorical_crossentropy",optimizer="adam"):
        self.loss = loss
        self.optimizer = optimizer
        self.model = Sequential()
        self.set_callback()
    def build_model(self,arr,dropout=0.2):
        for i in range(len(arr)):
            if i != 0 and i != len(arr) - 1:
                if i == 1:
                    self.model.add(Dense(arr[i], input_dim=arr[0], kernel_initializer='he_normal', activation='relu'))
                else:
                    self.model.add(Dense(arr[i], activation='relu'))
                self.model.add(Dropout(dropout))
        self.model.add(Dense(arr[-1], kernel_initializer='he_normal', activation='softmax'))
        self.model.compile(loss=self.loss, optimizer=self.optimizer, metrics=[self.f1score])
    def set_callback(self,patient=2,mode = "min",verbose=0):
        self.callbacks = [
            EarlyStopping(monitor='val_loss', patience=patient, mode=mode, verbose=verbose),
            ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=patient / 2, min_lr=0.00001, verbose=verbose,
                              mode=mode)
        ]
    def train_model_test(self,train_x,train_y,validation_x,validation_y,epochs=40, batch_size = 20):
        self.model.fit(np.array(train_x), np.array(train_y), epochs=epochs, batch_size = batch_size,
                       validation_data=(validation_x,validation_y), callbacks=self.callbacks)

    from keras import backend as K
    def recall(self, y_target, y_pred):
        # clip(t, clip_value_min, clip_value_max) : clip_value_min~clip_value_max 이외 가장자리를 깎아 낸다
        # round : 반올림한다
        y_target_yn = K.round(K.clip(y_target, 0, 1))  # 실제값을 0(Negative) 또는 1(Positive)로 설정한다
        y_pred_yn = K.round(K.clip(y_pred, 0, 1))  # 예측값을 0(Negative) 또는 1(Positive)로 설정한다

        # True Positive는 실제 값과 예측 값이 모두 1(Positive)인 경우이다
        count_true_positive = K.sum(y_target_yn * y_pred_yn)

        # (True Positive + False Negative) = 실제 값이 1(Positive) 전체
        count_true_positive_false_negative = K.sum(y_target_yn)

        # Recall =  (True Positive) / (True Positive + False Negative)
        # K.epsilon()는 'divide by zero error' 예방차원에서 작은 수를 더한다
        recall = count_true_positive / (count_true_positive_false_negative + K.epsilon())

        # return a single tensor value
        return recall

    def precision(self, y_target, y_pred):
        # clip(t, clip_value_min, clip_value_max) : clip_value_min~clip_value_max 이외 가장자리를 깎아 낸다
        # round : 반올림한다
        y_pred_yn = K.round(K.clip(y_pred, 0, 1))  # 예측값을 0(Negative) 또는 1(Positive)로 설정한다
        y_target_yn = K.round(K.clip(y_target, 0, 1))  # 실제값을 0(Negative) 또는 1(Positive)로 설정한다

        # True Positive는 실제 값과 예측 값이 모두 1(Positive)인 경우이다
        count_true_positive = K.sum(y_target_yn * y_pred_yn)

        # (True Positive + False Positive) = 예측 값이 1(Positive) 전체
        count_true_positive_false_positive = K.sum(y_pred_yn)

        # Precision = (True Positive) / (True Positive + False Positive)
        # K.epsilon()는 'divide by zero error' 예방차원에서 작은 수를 더한다
        precision = count_true_positive / (count_true_positive_false_positive + K.epsilon())

        # return a single tensor value
        return precision

    def f1score(self, y_target, y_pred):
        _recall = self.recall(y_target, y_pred)
        _precision = self.precision(y_target, y_pred)
        # K.epsilon()는 'divide by zero error' 예방차원에서 작은 수를 더한다
        _f1score = (2 * _recall * _precision) / (_recall + _precision + K.epsilon())

        # return a single tensor value
        return _f1score
    def eval_model(self,test_x,text_y,batch_size=20,verbose = 0):
        _acc, _f1score = self.model.evaluate(test_x,text_y, batch_size=batch_size,
                                                                    verbose=verbose)
        return {"AI_model": self.model,"f1_score" : _f1score}

def save_model(model, yaml_file_name,h5_file_name):
    model_yaml = model.to_yaml()
    with open(yaml_file_name, "w") as yaml_file:
        yaml_file.write(model_yaml)
    # serialize weights to HDF5
    model.save_weights(h5_file_name)

def load_model(yaml_file_name,h5_file_name) :
    yaml_file = open(yaml_file_name, 'r')
    loaded_model_yaml = yaml_file.read()
    yaml_file.close()
    loaded_model = model_from_yaml(loaded_model_yaml)
    # load weights into new AI_model
    loaded_model.load_weights(h5_file_name)
    loaded_model.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=[f1_score])
    return loaded_model

if __name__ == "__main__" :
    if sys.argv[1] == "Oversampling" :
        Input_data = np.load("numpy_array_data/Input5_data.npy")
        Output_data = np.load("numpy_array_data/labels5_data.npy")
        # Output_data = np.expand_dims(Output_data,1)
        # enc = OneHotEncoder()
        # Output_data = enc.fit_transform(Output_data).toarray()
        print(Output_data.shape)
        print(np.unique(Output_data))
        ADASYN_directory = 'numpy_array_data/ADASYN/'
        normal_directory = "numpy_array_data/normal/"
        SMOTE_directory = "numpy_array_data/SMOTE"
        SMOTE_ENN_directory = "numpy_array_data/SMOTE_ENN"
        Oversampling_list = [SMOTE(random_state=0),RandomOverSampler(random_state=0),
                             ADASYN(random_state=0),SMOTETomek(random_state=0),SMOTEENN(random_state=0)]
        sampling_type = ['SMOTE','normal','ADASYN','SMOTE_Tomek','SMOTE_ENN']
        for i,Oversampling_ob in enumerate(Oversampling_list) :
            print(sampling_type[i])
            Sampled_input_data, Sampled_output_data = Oversampling_ob.fit_resample(Input_data, Output_data)
            train_x, test_x, train_y, test_y = train_test_split(Sampled_input_data, Sampled_output_data, test_size = 0.2)
            train_x, val_x, train_y, val_y = train_test_split(train_x, train_y, test_size = 0.2)
            train_x_directory = "numpy_array_data/over_sampled_data/"+sampling_type[i]+"/train_x.npy"
            train_y_directory = "numpy_array_data/over_sampled_data/" + sampling_type[i] + "/train_y.npy"
            val_x_directory = "numpy_array_data/over_sampled_data/" + sampling_type[i] + "/val_x.npy"
            val_y_directory = "numpy_array_data/over_sampled_data/" + sampling_type[i] + "/val_y.npy"
            test_x_directory = "numpy_array_data/over_sampled_data/" + sampling_type[i] + "/test_x.npy"
            test_y_directory = "numpy_array_data/over_sampled_data/" + sampling_type[i] + "/test_y.npy"
            np.save(train_x_directory,train_x)
            np.save(train_y_directory, train_y)
            np.save(val_x_directory, val_x)
            np.save(val_y_directory, val_y)
            np.save(test_x_directory, test_x)
            np.save(test_y_directory, test_y)

    if sys.argv[1] == 'train':
        # AI_model = NN_model()
        engineer_name = sys.argv[2]
        models = {"name" : engineer_name,"models" : []}
        data_directory = "numpy_array_data/over_sampled_data/"+sys.argv[3]+"/"
        best_models = []
        for first_nodes in range(25,100,25) :
            first_best_models = []
            for second_nodes in range(25,100,25) :
                second_best_models =[]
                for third_nodes in range(25,100,25) :
                    third_best_models = []
                    for fourth_nodes in range(25,100,25) :
                        fourth_best_models = []
                        for fifth_nodes in range(25,100,25) :
                            print("layers = [{0},{1},{2},{3},{4}]".format(first_nodes,second_nodes,third_nodes,fourth_nodes,fifth_nodes))
                            model = NN_model()
                            model.build_model([161, first_nodes,second_nodes,third_nodes,fourth_nodes,fifth_nodes,5])
                            model.train_model_test(np.load(data_directory+"train_x.npy"),np.load(data_directory+"train_y.npy"),np.load(data_directory+"val_x.npy"),np.load(data_directory+"val_y.npy"))
                            fourth_best_models.append(model.eval_model(np.load(data_directory+"test_x.npy"),np.load(data_directory+"test_y.npy")))
                        fourth_best_model = fourth_best_models[0]
                        for fourth_model in fourth_best_models[1:]:
                            if fourth_model['f1_score'] > fourth_best_model['f1_score']:
                                fourth_best_model = fourth_model
                        third_best_models.append(fourth_best_model)
                    third_best_model = third_best_models[0]
                    for third_model in third_best_models[1:]:
                        if third_model['f1_score'] > third_best_model['f1_score']:
                            third_best_model = third_model
                    second_best_models.append(third_best_model)
                second_best_model = second_best_models[0]
                for second_model in second_best_models[1:]:
                    if second_model['f1_score'] > second_best_model['f1_score']:
                        second_best_model = second_model
                first_best_models.append(second_best_model)
            first_best_model = first_best_models[0]
            for first_model in first_best_models[1:]:
                if first_model['f1_score'] > first_best_model['f1_score']:
                    first_best_model = first_model
            best_models.append(first_best_model)
        best_model = best_models[0]
        for Model in best_models :
            if Model['f1_score'] > best_model['f1_score']:
                    best_model = Model
        save_model(best_model['AI_model'],"Model_folder/"+engineer_name+".yaml","Model_folder/"+engineer_name+".h5")

    if sys.argv[1] == 'train2':
        engineer_name = sys.argv[2]
        data_directory = "numpy_array_data/over_sampled_data/" + sys.argv[3] + "/"
        data = np.load(data_directory+ "train_x.npy")
        model = NN_model()
        model.build_model([161, 50, 50, 50, 50, 50, 5])
        model.train_model_test(np.load(data_directory + "train_x.npy"), np.load(data_directory + "train_y.npy"),
                               np.load(data_directory + "val_x.npy"), np.load(data_directory + "val_y.npy"))
        save_model(model.model, "Model_folder/" + engineer_name + ".yaml",
                   "Model_folder/" + engineer_name + ".h5")
    # yaml_file_name = "Model_folder/"+ sys.argv[1]
    # h5_file_name = "Model_folder/" + sys.argv[2]
    # AI_model = load_model(yaml_file_name,h5_file_name)
    # data = np.random.randint(0, 1, size=(1, 161))
    # print(AI_model.predict(data))
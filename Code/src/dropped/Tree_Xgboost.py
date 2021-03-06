import pandas as pd
import xgboost as xgb

from sklearn.preprocessing import LabelEncoder
from xgboost.sklearn import XGBClassifier

# Customized functions
from Code.src.dropped.PublicFunctions import *


train_path = r'D:\DataSet\UrbanSoundChallenge\train'
test_path = r'D:\DataSet\UrbanSoundChallenge\test'


train = pd.read_csv(join(train_path, 'train.csv'))
test = pd.read_csv(join(test_path, 'test.csv'))


X_tr = loader_hd(train_path, r'Train\mfccs_train_X_all_256.npy')
y_tr = loader_hd(train_path, r'Train\mfccs_train_y_all_256.npy')

X_ts = loader_hd(test_path, r'Test\mfccs_test_X_all_256.npy')

X_tr = X_tr.reshape((X_tr.shape[0], X_tr.shape[1] * X_tr.shape[2]))
X_ts = X_ts.reshape((X_ts.shape[0], X_ts.shape[1] * X_ts.shape[2]))
# pdb.set_trace()


lb = LabelEncoder()
y_tr = lb.fit_transform(y_tr)

# dtrain = xgb.DMatrix(X_tr, label=y_tr)
dtest = xgb.DMatrix(X_ts)
#
# # xgboost
# param = {
#     'max_depth': 10,  # the maximum depth of each tree
#     'eta': 0.2,  # the training step for each iteration
#     'silent': 1,  # logging mode - quiet
#     'objective': 'multi:softprob',  # error evaluation for multiclass training
#     'num_class': 10}  # the number of classes that exist in this datset
# num_round = 200  # the number of training iterations
#
# bst = xgb.train(param, dtrain, num_round)
# bst.dump_model('dump.raw.txt')
# preds = bst.predict(dtest)
# prediction = np.asarray([np.argmax(line) for line in preds])
# pdb.set_trace()

xgb_model = XGBClassifier(learning_rate=0.01, n_estimators=200, max_depth=9, eta=2, silent=1,
                          min_child_weight=3, gamma=0.2, subsample=0.85, colsample_bytree=0.75,
                          objective='multi:softprob', nthread=4, scale_pos_weight=1, num_class=10,
                          reg_alpha=0.0001)

# pdb.set_trace()

xgb_model.fit(X_tr, y_tr)
prediction = xgb_model.predict(X_ts)

test['Class'] = list(lb.inverse_transform(prediction))
test.to_csv(join(r'D:\DataSet\UrbanSoundChallenge\submission', 'sub_xgb_tuned.csv'), index=False)

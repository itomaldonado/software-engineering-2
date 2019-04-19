Multilayer Neural Network with Back-Propagation:


Requirements:
- Python 3.7+ (https://www.python.org/downloads/)
- pip (https://pip.pypa.io/en/stable/installing/)


Installation:
- Clone repository
- To install dependencies run: pip install -r requirements.txt


Data Format:
- A comma-separated (.csv) file with three or more columns (no headers): x1,x2,..,out
- See example data at: ./training.csv

Usage: Usage: mnn.py [OPTIONS] TRAINING_DATA

  Run MNN with the provided test data and inputs/outputs

Options:
  --debug                    Show debug data
  --hidden INTEGER           Number of hidden layers  [default: 2]
  -e, --error FLOAT          Target error  [default: 0.02]
  -l, --learning_rate FLOAT  Learning rate  [default: 0.5]
  -r, --epochs INTEGER       Max number of epochs for learning  [default: 10000]
  --help                     Show this message and exit.

Example uses:

- Show Help Menu: python ./mnn.py --help

- Run with defaults:
python mnn.py ./training.csv
----------- Start -----------
Initial layer weights
Hidden Layers: 
[[ 0.94413892 -0.93379057]
 [-0.92902977 -0.48875811]]
Output Layers: 
[[0.88059382]
 [0.68203346]]
-----------------------------

--------- Results -----------
First batch error: 0.2785108809462334
Last batch error: 0.24980186168247337
Total number of batches: 100
Final layer weights
Hidden Layers: 
[[ 0.79896263 -0.96068781]
 [-1.06546266 -0.47353581]]
Output Layers: 
[[ 0.06008309]
 [-0.08501365]]
-----------------------------

- Run with pre-defined target error, hidden layers and learning rate:
python mnn.py ./training.csv --error 0.03 --hidden 5 --learning-rate 1.0
----------- Start -----------
Initial layer weights
Hidden Layers: 
[[ 0.30284478 -0.28622992 -0.31726577  0.08129452 -0.29458557]
 [-0.42170599  0.9317324   0.66371194  0.55964972 -0.39666243]]
Output Layers: 
[[ 0.4146758 ]
 [ 0.57391865]
 [ 0.01742985]
 [ 0.96725135]
 [-0.29236065]]
-----------------------------

--------- Results -----------
First batch error: 0.30167326938131533
Last batch error: 0.02984243241464791
Total number of batches: 698
Final layer weights
Hidden Layers: 
[[ 0.57643209 -2.11087173 -1.81194436 -3.58600425 -4.70070385]
 [-1.69339343  0.7624444   4.11733129  1.53185035 -4.79871163]]
Output Layers: 
[[ 2.76491022]
 [ 2.09091154]
 [-3.4391892 ]
 [ 3.84886018]
 [-8.45827802]]
-----------------------------
Run A Bayesian Curve Fitting Example:


Requirements:
- Python 3.7+ (https://www.python.org/downloads/)
- pip (https://pip.pypa.io/en/stable/installing/)


Installation:
- Clone repository
- To install dependencies run: pip install -r requirements.txt


Data Format:
- A comma-separated (.csv) file with two columns (no headers): x,t
- See example data at: ./data.csv and ./data_10.csv 

Usage: python bayesian.py [OPTIONS] DATA PREDICT

Options:
  -a, --alpha FLOAT  Alpha.  [default: 0.005]
  -b, --beta FLOAT   Precision, (1/variance).  [default: 11.1]
  -m, --mth INTEGER  M. The Mth order polynomial.  [default: 9]
  --help             Show this message and exit.


Example uses:

- Show Help Menu: python ./bayesian.py --help

- Run with defaults:
python ./bayesian.py ./data_10.csv 11
Parameters - α:0.005, β:11.1, Data: ./data_10.csv, Mth:9, prediction:11.0
Variance: 1704.3431001614385
Mean: 1077321.3786425989

- Run with pre-defined alpha, beta and M:
python ./bayesian.py -a 0.00 -b 12 -m 15 ./data.csv 249
Parameters - α:0.0, β:12.0, Data: ./data.csv, Mth:15, prediction:249.0
Variance: 0.16594109977207455
Mean: 64570.70930479015
Tested on Python 3.10.10

The script assumes the following folder structure:
.
│
├── preprocess/
│   ├── clinical.py
│   ├── drugs.py
│   ├── demographic.py
│   ├── diagnosis.py
│   └── labs.py
│
├── input/
│
├── logs/
│
├── output/
│
├── requirements/
│   └──  requirements.txt
├── config.json
├── helper.py
├── main.py
└── README.txt

:: steps to create conda environment
conda create -n seha python=3.10 -y
conda activate seha

:: navigate to folder containing `requirements.txt`
pip install -r requirements.txt

:: navigate to folder containing main.py
python main.py
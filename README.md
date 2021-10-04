# RL_Experiments
# Install pip
```
python -m pip install --upgrade pip
```

# Install virtual environment package 

```
python -m pip install virtualenv
```

# Install other required packages 
```
!pip install pandas
pip install pandas

pip install gym

pip install stable_stablebaseline3
```
# Packages needed 

So I use the StableBaselinesLibrary https://stable-baselines.readthedocs.io/en/master/guide/install.html 

However, before you install it you need to install the following libraries with the specified versions and the order is important. 
Anaconda
* Python 3.6.1
* Tensorflow version 1.13.1
* Keras 2.2.4   (NOTE : tensorflow has to be installed first before this)
* Gym 0.15.4

force reinstallation may be needed, which could be done by following command. 


# Creating vitural environment - venv 
```
python -m venv venv
```

# Activate virtual environment 
```
.\venv\scripts\activate
```

# Launch virtual environment 
```
.\venv
```

## If problems with virtual environment execution policy 
```
Set-ExecutionPolicy -ExecutionPolicy Unrestricted
```

## List of packages in current environment 
```
pip freeze -- local 
pip freeze > requirements.txt
pip list > requirements.txt
```
## Installing packages from requirements.txt  
```
pip install r .\requirements.txt
```

# Adding to git 
```
git clone URL 
code .
```

# updating git repo

```
git add . 
git commit -m "Current upade of the branch"
git push 
```

# Remove the current branch from git cache  
```
git reset --soft 
git filter-branch --index-filter 'git rm -r --cached --ignore-unmatch <file/dir>' HEAD
```

# Running the Code 
```
python main.py   <minEpisodes>  <approach>  <areaValsIndex>  <numTargets>  <stepsLimitPerEpisode>  <train/test>

python main.py 100 ManhattanPython 0 2 2 train
python main.py 100 ManhattanPython 0 2 2 test
```

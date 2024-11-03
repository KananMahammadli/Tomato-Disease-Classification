# Tomato Disease Classification
Web app view:
<p align="center">
  <img src = ./assets/web_1.png>
</p>

Prediction Example:
<p align="center">
  <img src = ./assets/web_2.png>
</p>



### Project Web App: [link](https://kananmahammadli-improved-orbit-xpwj9jx4v7gf6rgg-2001.preview.app.github.dev/)

### Project Desktop App: Download `Install Tomato.exe` file and start installation

The aim of this project is to classify tomato diseases based on their leaves that can be very useful in the agriculture. We have 4 branchs for this project, one for training, one for production of our web app which you can go by following [this link](http://46.101.214.183/). Main branch is where we coommit our changes and merge to production to have continuous deployment with the help of our CI/CD pipeline. To be more user-friendly, Desktop app has also been created so that users can interact with the App to upload the images of their tomato leaves and find the diseases. This App can find healthy tomatoes and 9 different diseases.

---

## Table of Contents

- [Requirements for Training](#requirements-for-training)
- [How to Run](#how-to-run)
- [Data and the Code](#data-and-the-code)
- [CNN Architecture](#cnn-architecture)
- [Deployment to Digital Ocean](#deployment-to-digital-ocean)
- [CI CD Pipeline](#ci-cd-pipeline)
- [Desktop App](#desktop-app)

---

## Requirements for Training

This project requires [Python3.8](https://www.python.org/downloads/release/python-380/) and the following Python libraries installed:

- [NumPy](https://numpy.org/)
- [matplotlib](https://matplotlib.org/)
- [tensorflow](https://www.tensorflow.org/)
- [opencv](https://opencv.org/)
- [scikit-learn](https://scikit-learn.org/stable/)

Instead of manually installing the libraries, you can install all of them with `requirements.txt`. Here is how it works:


```bash
pip install -r requirements.txt
```

Since all the code has been written in [Jupyter Notebook](http://jupyter.org/install.html), you also need that to be installed on your computer.
If you do not have Python installed yet, you can install the [Anaconda](https://www.anaconda.com/download/) distribution of Python, which is already coming with NumPy and Matplotlib installed.
If you do not have pip installed, you can run the code below in the terminal or command window

- For Linux / MacOS

```bash
python get-pip.py
```

- For Windows

```bash
C:> py get-pip.py
```

## How to Run

After installing all the libraries properly, go through `modelling.ipynb` and run cells to train the model.

## Data and the Code

[Kaggle Tomato leaves data](https://www.kaggle.com/kaustubhb999/tomatoleaf) has been used for this project. In total we have 10 categories: 9 diseases and healthy tomatoes.For each category, there are 10k images to train and 1k images to test our model. All the images have been resized by 64x64 before uploading to the workspace to reduce the size of zip folder containing the images.



## CNN Architecture

Our CNN architecture consist of 3 feature extraction blocks (each has Conv2D layer with ReLU activation followed by MaxPooling layer) and a heading with Flatten and Dense layer(40 units) followed by softmax activation. Here is the visual intepretation of our architecture:


<p align="center">
  <img src = ./assets/model_architecture.png>
</p>

## Deployment to Digital Ocean

We use Flask to crate api for our model to make prediction on the web with user-friendly interface and dockerize it for deployment by using the Docker. During the whole process we are using SSH keys for authentication, therefore let's go through the authentication first then start actual deployment process.



- Getting access to Github for local PC

 

```bash
ssh-keygen -o -C username@gmail.com
```

You can use -f flag for a specific folder you want to keep you ssh-key and -t to name your key file. It will generate 2 files: a private key and public key that ends with .pub
, usually they are stored at `~/.ssh/` folder. Now we need to put this key on Github so that we can have an access to our repos. From general settings, go to the SSH and GPG keys, add new SSH key, name it whatever you want, like personel-key and copy contents of public key file we created that ends with .pub and paste it, then create the key. Whenever we clone the repo with SSH key, we can have permanent access so that we don't have to login each time.

- Getting access to Github for Digital Ocean

After you create a droplet inside the project on the Digital Ocean, go to the console and do following on the terminal. Run `ssh-keygen`, it will create a ssh-key inside `~.ssh/` with default name `id_rsa.pub`. Now we need to create authorized_keys folder and give it permission to help us to connect to the Github. Run the `cat ~/.ssh/id_rsa.pub` to see the contents of your public key and copy it, then run `nano ~/.ssh/authorized_keys` on the terminal, paste the key, press ctrl + o finish writing, enter to save, then ctrl + x to exit, then run `chmod 700 ~/.ssh/authorized_keys` to give permission. We also need to add this key into Github to have access from Digital Ocean, again go to SSH and GKG keys, new SSH key, name it sth like digital-ocean-auth-key, paste the public key and create. 
After handling the authentication we can start the deployment, but before doing the things on the Digital Ocean you can test the docker locally.

- Docker build local
  

`docker build -t tomato-disease-classifier .`

- Docker run local
  

`docker run -p 80:8080 tomato-disease-classifier`


If you get the link and see website like below when you follow the localhost link, then everything is okay.

<p align="center">
  <img src = ./assets/local_web.png>
</p>

Since docker working fine locally, we can start doing the process on a Digital Ocean. You can either go to the droplet you created and open console or if you can connect to your project locally by running ```sssh root@ipv4```, instead of ipv4 you have to give the link it provides inside the droplet and put your password (you can also add ssh key to the digital ocean to have permenant access which is much safer). Now run the following commands one-by-one



- Clone project into Digital Ocean



```bash
git clone git@github.com:KananMahammadli/Tomato-Disease-Classification.git
```



- Go to the project



```bash
cd Tomato-Disease-Classification
```



- Change branch to production



```bash
git checkout production-web
```



- Start building the docker image



```bash
docker build -t tomato-disease-classifier .
```



- Run the docker image



```bash
docker run -p 80:8080 tomato-disease-classifer
```



Now you can go to the [46.101.214.183](http://46.101.214.183/), to see the same website as we did locally, you can click the upload button to put your tomato leaf image (.png, .jpg, .jpeg, .bmp, .webp formats are allowed), and click the predict button to see the results.


<p align="center">
  <img src = ./assets/web_1.png>
</p>
<p align="center">
  <img src = ./assets/web_2.png>
</p>

## CI CD Pipeline

After deploying our model, it is better to automate the deployment process for the changes in future. We have our yml file to handle this process. We need secrets on Github to access the Digital Ocean. Go to the project settings and select the secrets. We will create 3 secrets. First is ssh key we created on digital ocean, but it should be the private one, not public. Go to Digital Ocean project console and run this `cat ~/.ssh/id_rsa`, and copy the contents. Then go back to the github create new secret, name it as SSH_KEY and paste the key in the value, then create the second key and name it SSH_HOST and put the ipv4 as a value, in our case it is 46.101.214.183, and cretae the last key named SSH_HOST and write root as a value. After compliting you should have these keys below, and then with correct yml, whenever commits are maid to the main branch and merged to production-web it will start the deployment and you can see the process from the actions tab.

<p align="center">
  <img src = ./assets/keys.png>
</p>

## Desktop App

First download `Install Tomato.exe` file and open it, during the installation you can define path where the app should be installed, after the installation completed you will have the App below. Here are some examples:

- Desktop App Interface

<p align="center">
  <img src = ./assets/desk1.png>
</p>

- Correct Input
<p align="center">
  <img src = ./assets/desk2.png>
</p>

- Wrond Image Dimension

<p align="center">
  <img src = ./assets/desk3.png>
</p>

- Quitting the App

<p align="center">
  <img src = ./assets/desk4.png>
</p>

# How to setup the ClassX app on a Linux Server (CentOS Linux release 8 (Core))

## Software Requirements
- MySQL Community Server: Version 8.0.34
- Conda: Version 23.5.2
- Python: Version 3.10
- Nginx: Version 1.20.1

## Install MySQL Server Release el8-8
### Step 1: Remove any previous MySQL packages and clear cache

1. Remove previous installed packages and clear cache
   
   ```
   yum list installed | grep mysql
   ```
   
3. If MySQL package exists, remove it using:
   
   ```
   yum remove mysql80-community-release.noarch
   ```

5. Clear cache

   ```
   yum clean all --verbose
   ```

7. Remove MySQL cache folders

   ```
   sudo rm -R /var/cache/yum/x86_64/7/mysql*
   ```

   ```
   yum update
   ```

### Step 2: Installing MySQL
1. Setup yum repository

```
sudo rpm -Uvh https://repo.mysql.com/mysql80-community-release-el8-8.noarch.rpm 
```

2. Disable all repositories in mysql repo file.

```
sudo sed -i 's/enabled=1/enabled=0/' /etc/yum.repos.d/mysql-community.repo
```

3. Import the new GPG key

```
sudo rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022
```

4. Install MySQL Community Server

```
sudo yum --enablerepo=mysql80-community install mysql-community-server
```

### Step 3: Starting MySQL
1. Start MySQL
   ```
   sudo systemctl start mysqld
   ```

3. Check the status
   ```
   sudo systemctl status mysqld
   ```

5. Retrieve the temporary password
   ```
   sudo grep 'temporary password' /var/log/mysqld.log
   ```

### Step 4: Additional configuration
1. Using the below command to remove anonymous users, disallow remote root login, remove the test database and access to it, and reload the privilege tables.
   ```
   sudo mysql_secure_installation
   ```

3. To access the databased
   ```
   mysql -u root -p
   ```

4. Enter password, when prompted.

### Step 5: Create database
1. In MySQL console, run the below command
   ```
   create database label_db;
   ```

## Install Anaconda for Linux
### Step 1: Download and install the conda package
1. Run the below command
   ```
   wget https://repo.anaconda.com/archive/Anaconda3-2023.07-1-Linux-x86_64.sh
   ```

3. Change the file permission
   ```
   chmod 777 Anaconda3-2023.07-1-Linux-x86_64.sh
   ```

4. Run the installation file
   ```
   ./ Anaconda3-2023.07-1-Linux-x86_64.sh
   ```

   Note: When prompted, press Enter

## Step 2: Clone the ClassX repository
1. Change to the directory where you want the application to be downloaded.
2. Clone the repository using:
   ```
   git clone https://github.com/stccenter/ClassXTool.git
   ```
3. When prompted provide GitHub username and password.
4. Change directory to ClassXTool
5. Create a .env file using the below command
   ```
   vi .env
   ```
6. The content will be shared on request
7. Run the python script
   ```
   python setup.py
   ```
9. Run the command to activate the conda environment
   ```
   conda activate ClassXTool
   ```

## Create ClassX service
### Step 1: Configure Gunicorn
1. Create a new directory under /etc/ named 'gunicorn'
   ```
   mkdir -p /etc/gunicorn'
   ```
2. Create gunicorn configuration file
   ```
   vi /etc/gunicorn/app.py
   ```
3. Copy and paste the following content
   ```
   workers=8
   threads=8
   ```

### Step 2: Create ClassX service
1. Create ClassX service file
   ```
   vi /etc/systemd/system/classx.service
   ```
2. Copy and paste the following content
   ```
   [Unit]
   Description=ClassX web application
   After=network.target
   
   [Service]
   User=root
   WorkingDirectory=/opt/ClassX
   ExecStart=/root/anaconda3/envs/ClassXTool/bin/gunicorn --bind 127.0.0.1:5000 --config /etc/gunicorn/app.py --error-logfile /var/log/classx/error.log --access-logfile /var/log/classx/access.log       --log-level debug  --timeout 600 wsgi:app
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

   Note: Make sure the path to conda environment is properly configured.

### Step 3: Start all the services
1. To start classx service use the below command
   ````
   systemctl start classx
   ```

## Configure Nginx (Optional if port 5000 is not accessible)
###  Step 1: Install Nginx
1. Install Nginx using below command
   ```
   yum install nginx
   ```
###  Step 2: Add Nginx configuration
1. Create the config file using below command
   ```
   vi /etc/nginx/conf.d/classx.conf
   ```
2. Copy and paste the following content
   ```
   server {
    listen 80;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          }
      }
   ```
3. Start Nginx using below command
   ```
   systemctl start nginx
   ```
###  Step 3: Validate application
1. Access application using below url
   ```
   http://10.0.0.0/
   ```
   Note: Please change the IP to your server IP where the application is running
   
### Useful links
  1. https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-centos-7
  2. https://stackoverflow.com/questions/70993613/unable-to-install-mysql-on-centos7
  3. https://www.anaconda.com/download#downloads

===========================================================================
# For developers - Set up ClassX app on a local machine (Windows or Mac)
## To download:

1. MySQL:
  * For MacOS use https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/macos-installation-pkg.html
  * For Windows use https://dev.mysql.com/downloads/installer/ 
2. Anaconda : https://www.anaconda.com/products/distribution#Downloads

## Steps
1. Get access to https://github.com/stccenter/ArcCI-DL-Tool and clone it. 
2. Install all the packages you downloaded, while installing MySQL, make sure you remember your root username and password 
3. Open MySQL client, log in. Then type below comment to create a database:

```create database label_db;```

4. Once you install everything, open anaconda command prompt, cd into your local folder for ArcciDLTool. 
5. Run the command: python setup.py 
6. Run the command: conda activate LabelingTool
7. Create new file named .env and paste in application credentials you recieve from the administrator. Edit DB_PASSWORD to match your MySQL password.
8. Then in your terminal, run the command: python app.py 
9. Contact the administrator for Arctic HSR images or you can download HSR images by following this video https://www.youtube.com/watch?v=-ADhwCBu3vA from this link: https://nsidc.org/icebridge/portal/map. Copy and paste the images inside static/images/default/ReadGUI folder.
10. Open http://127.0.0.1:5000/addDefaultUser in your browser and wait for {"status" : 200} 
11. The final step is to get the JWT token from the ArcCI main portal. To achieve, login to https://arcciserver.stcenter.net/login.php. Go to Labeliing Tool (located in the top right dropdown) and find the token string in the redirect URL. Copy the token and keep it a secure location.
12. Now in your browser type http://127.0.0.1:5000/token=yourtoken


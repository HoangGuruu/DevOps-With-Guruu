```sh

sudo apt-get update -y

cd ~
curl -sL https://deb.nodesource.com/setup_16.x -o /tmp/nodesource_setup.sh


sudo bash /tmp/nodesource_setup.sh

sudo apt install nodejs

node -v
# It should be > version 14


sudo apt install npm -y


sudo apt install nginx -y


sudo mkdir /var/www/html/my-react-app

sudo vi /etc/nginx/conf.d/react.conf
```
### react.conf
```sh
server {
  listen 80;
  listen [::]:80;
  root /var/www/html/my-react-app/build;
  
  #react app
  location / {
    try_files $uri /index.html;  
  }
}
```

```sh
cd /home/ubuntu
mkdir my-app
cd my-app


npx create-react-app .

npm install


npm start

npm build 


sudo cp -R build/ /var/www/html/my-react-app/


sudo vi /etc/nginx/nginx.conf

# Comment this line 
#include /etc/nginx/sites-enabled/*;


sudo nginx -t && sudo systemctl reload nginx
```

### Note : commandto solve problem with ChatGpt
```sh
# If you get the same error . You can try it 
sudo apt remove libnode-dev

sudo dpkg -i --force-overwrite /var/cache/apt/archives/nodejs_16.20.2-deb-1nodesource1_amd64.deb

```
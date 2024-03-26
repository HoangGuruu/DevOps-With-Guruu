```sh
curl -s https://static.us-east-1.prod.workshops.aws/public/8c4076ba-a416-424d-acc7-06e5cc2de102//static/20-infrastructure/InfrastructureApp.tgz | tar -xzv
cd InfrastructureApp
```

```sh
npm install
npm run build


cdk bootstrap


```

```sh
cd ~/environment/InfrastructureApp
cdk deploy
```


```sh
cd ~/environment
git clone <your repository URL>
```

```sh
curl -s https://static.us-east-1.prod.workshops.aws/public/8c4076ba-a416-424d-acc7-06e5cc2de102//static/30-source/DemoApp.tgz | tar -xzv
cd DemoApp
```


```sh
git config --global user.email "you@example.com"
git config --global user.name "Your Name"


git add .
git commit -m "Initial commit"
git push


```
# buildspec.yml
```sh
version: 0.2

phases:
  install:
    runtime-versions:
      java: corretto8
  build:
    commands:
      - mvn install
artifacts:
  files:
    - target/javawebdemo.war
    - appspec.yml
    - scripts/**/*
  discard-paths: no
```

```sh
cd ~/environment/DemoApp
git add .
git commit -m "Add buildspec"
git push
```
# appspec.yml
```sh
version: 0.0
os: linux
files:
  - source: /target/javawebdemo.war
    destination: /tmp/codedeploy-deployment-staging-area/
  - source: /scripts/configure_http_port.xsl
    destination: /tmp/codedeploy-deployment-staging-area/
hooks:
  ApplicationStop:
    - location: scripts/stop_application
      timeout: 300
  BeforeInstall:
    - location: scripts/install_dependencies
      timeout: 300
  ApplicationStart:
    - location: scripts/write_codedeploy_config.sh
    - location: scripts/start_application
      timeout: 300
  ValidateService:
    - location: scripts/basic_health_check.sh

```

```sh
cd ~/environment/DemoApp
git add .
git commit -m "Add appspec"
git push

```
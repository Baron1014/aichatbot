<div align="center">

<img src="./static/scream.jpg" height="250" width="300" >

</div>

## content
- [Edit Environment Variables](#edit-environment-variables)
- [Docker Setup](#docker-setup)
- [Build Your Line Bot](#build-your-line-bot)

## Edit Environment Variables
Modify the information of yourself in the red box.
```shell
vim env_setup.sh
```
![](./static/env_setup.png)

## Docker Setup
Run the startup script to create docker container.
```shell
bash run.sh
```
![](./static/docker.png)

## Build Your Line Bot
In the Line's **Basic setting** has `Channal secret` and **Messaging API**'s bottom has `channel access token`. Pass these keys to `www\secream\config.ini` enables the python script to connect to Linebot.
![](./static/key1.png)
![](./static/key2.png)

- restart your docker container
```shell
#close docker
COMPOSE_PROJECT_NAME=aichatbot docker-compose down
#open docker
COMPOSE_PROJECT_NAME=aichatbot docker-compose up -d
```
![](./static/restart_docker.png)

- ngrok connects the external network to the local machine
    - [ngrok](https://ngrok.com/) registration and installation
    - connect your ngrok account
    ```shell
    ngrok authtoken <your authtoken>
    ```
    ![](./static/ngrok.png)
    - start ngrok service
    ```shell
    ngrok http 8082
    ```
    ![](./static/online.png)
    A URL will be forwarded so that the local server can communicate with the external server.

- Connect line bot and python script
Paste the string of URLs generated by ngrok into the webhook URL under the line message API and add `/callback` at the end.
![](./static/callback.png)

- Click to `verify`, `success` means the connection is successful.
![](./static/success.png)

- If you successfully connect and test on linebot, the following image should be displayed.
![](./static/line.png)

- If you get a 500 error, there is something wrong with your code, you can check the `/tmp/uWSGI.log` in docker container for any error messages. 
![](./static/error.jpg)
# responseAIProject-

First, make sure you have install the JDK8 above, and the nodejs (version above 18), npm(version above 8) command in your machine.

1  git clone this folder to your machine

2  After finish, copy the CVS file to responseAIProject-/serve-end/, and change the names to "training_data.csv" or "inference_data.csv"

3 start the jar with: 

   nohup  java -jar responseAIWeb-0.0.1-SNAPSHOT.jar >log.out &

4 Go to the responseAIProject-\responseAIWeb, exec the commands:

  1)  npm i serve -g
  2)  npm i

  3)  run command "npm run build", 
 Afetr success build, there is "build" folder under responseAIWeb, go into "build" folder,
      
  4) nohup serve -s  -l 3033 & (Remember, this command must be you are in "build" folder)
  5) Then, access the page on any machine  , https://IP:3033


pepper proposes a webserver which is used to display data on tablet.
The tablet is just use a web navigator.
So the html content has to be located on a special special location
you have to give the  name you want  to the directory projectbut next you  need a html subdirectory inside.
So here we create the directories during the scp transfer
scp -r SimpleWeb nao@"adresseIPduPepper":/home/nao/.local/share/PackageManager/apps/

************* CPE EXAMEN **************
IN SIMULATION with naoqi-bin launch directly in a terminal (not the one from choregraphe virtual robot )
cp -r SimpleWebPython ~/.local/share/PackageManager/apps/
************* *************************

You can start the app from a ssh on pepper
:~$ ssh nao@"adresseIPduPepper" 
pepperX [0] ~ $ cd /home/nao/.local/share/PackageManager/apps/SimpleWeb
pepperX [0] ~/.local/share/PackageManager/apps/SimpleWeb $ python app.py

or from a PC where  naoqi (2.5.x) is installed
python app.py --ip ""adresseIPduPepper" 
(but of course the top file and the html have to be previously transfer on the pepper)
																																																																																																																																																																	
You can access directely the website with a webnavigator on desktop.
http://"adresseIPduPepper"/apps/SimpleWeb/


import os,json
import instaloader
import pymongo
import cryptocode 


class database():
    def __init__(self,config):
        self.type = config["database"]["type"]
        self.__connectDatabase(config)            
    @staticmethod
    def createDatabase() -> dict:
        print("Configuracion de la Database.")
        print("1 = Usar un Json como database", "/n","2 = Conectar a un cluster de MongoDb")
        r = int(input().replace(" ",""))
        if r ==1:
            print("Introduzca el string de su cluster")
            string = input("Clúster:")
            print("Ahora una clave. ¡No la olvide! se le pedirá la proxima vez cuando quiera conectarse al clúster.")
            passdowrd=input("passowrd:")              
            return {"type":"mongoDb", "string":string, "password":passdowrd}
    
    def __decodedString(self,string):
        while True:
            password = input("Introduzca Clave de cifrado: ")
            decoded = cryptocode.decrypt(string, password)
            if decoded != False:
                self.password = password
                return decoded
            else:
                continue
    def __connectDatabase(self,config):
        if self.type == "mongoDb":
            self.cluster = self.__decodedString(config["database"]["cluster"])
            myclient = pymongo.MongoClient(self.cluster)
            mydb = myclient["tiktok"]
            self.profiles = mydb["profile"]
            self.posts = mydb["posts"]
        else:
            pass 
    def match(self, context,mode="uniqueId",value=None):
        
        if mode=="id":
            context.find_one({mode:value,"meta.status":{"$ne":"disabled"}},{})

          

      

class trackerTiktok():
    def __init__(self,thumb=True,msd5=True,downloadMode="random",requests=True,directAccess=True):
        #self.database = database()
        config = self.config(thumb,msd5,downloadMode,requests,directAccess)
        self.thumb = config.getboolean("DEFAULT","thumb")
        self.msd5 = config.getboolean("DEFAULT","msd5")
        self.downloadMode = config["DEFAULT"]["downloadMode"]
        self.requests = config.getboolean("DEFAULT","requests")
        self.directAccess = config.getboolean("DEFAULT","directAccess")
        self.database = database(config)

    def config(self,thumb,msd5,downloadMode,requests,directAccess):
        import configparser
        config = configparser.ConfigParser()      
        if not os.path.exists("config.ini"):           
            config['DEFAULT'] = {'thumb':thumb, 'msd5': msd5,'downloadMode': downloadMode,'requests':requests,'directAccess':directAccess}
            configDatabase = database.createDatabase()

            encoded = cryptocode.encrypt(configDatabase["string"],configDatabase["password"])
            #decoded = cryptocode.decrypt(encoded, "mypassword")
            config['database'] = {"type":configDatabase["type"],"cluster":encoded}
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            return config            
        else:
            config.read('config.ini')           
            return config       
    def addToDataBase(self):
        if os.path.exists("queries.json"):
            pass
        else:
            pass
            #passdowrd #creacion del queson



tracker = trackerTiktok(downloadMode="hola",requests=False)


print("hey")
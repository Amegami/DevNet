import requests
import json
import time


choice = input("Хотите ввести новый токен авторизации? (y/n) ")

if choice == "Y" or choice == "y":
	accessToken = input("Введите Ваш новый токен Webex: ")
	accessToken = accessToken
else:
    accessToken = "Bearer NDY0ZTg3ZDItNTgyNy00M2UzLWFhNDUtMzJjMWZhMzA2OGQwM2I4MzdhNWQtMDli_PE93_a8d6e1d4-8a35-402e-bfe5-ba3d72d62eb0"



r = requests.get(   "https://webexapis.com/v1/rooms",
                    headers = {"Authorization": accessToken}
                )

if not r.status_code == 200:
    raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))


print("Список комнат:")
rooms = r.json()["items"]
for room in rooms:
    print ("Тип: " + room["type"] + ", Название: " + room["title"])




while True:
    roomNameToSearch = input("В какой комнате будут произвожиться действия (укажите название)? ")
    roomIdToGetMessages = None
    
    for room in rooms:
        if(room["title"].find(roomNameToSearch) != -1):
            print ("Найдены комнаты под названием " + roomNameToSearch)
            #print(room["title"])
            roomIdToGetMessages = room["id"]
            roomTitleToGetMessages = room["title"]
            print("Обнаруженные команты: " + roomTitleToGetMessages)
            break

    if(roomIdToGetMessages == None):
        print("Извините, я не нашел ни одной комнаты с названием " + roomNameToSearch )
        print("Попробуйте еще раз...")
    else:
        break



while True:
    
    time.sleep(1)

    GetParameters = {
                            "roomId": roomIdToGetMessages,
                            "max": 1
                         }

    r = requests.get("https://webexapis.com/v1/messages", 
                         params = GetParameters, 
                         headers = {"Authorization": accessToken}
                    )
    
    if not r.status_code == 200:
        raise Exception( "Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))
   
    json_data = r.json()
    
    if len(json_data["items"]) == 0:
        raise Exception("В выбранной комнате нет сообщений.")
   
    messages = json_data["items"]
    message = messages[0]["text"]
    print("Полученное сообщение: " + message)
    
    if message.find("/") == 0:
        
        location = message[1:]
        mapsAPIGetParameters = { 
                                "location": location, 
                                "key": '6OKpBJU30eA1H3mqZ5LTIfpkwGfVasYp' # MapQuest API key here
                               }
        r = requests.get("https://www.mapquestapi.com/geocoding/v1/address?", 
                             params = mapsAPIGetParameters
                        )
        json_data = r.json()
        if not json_data["info"]["statuscode"] == 0:
            raise Exception("Incorrect reply from MapQuest API. Status code: {}".format(r.statuscode))

        locationResults = json_data["results"][0]["providedLocation"]["location"]
        print("Обьект: " + locationResults)

        locationLat = json_data["results"][0]["locations"][0]["displayLatLng"]["lat"]
        locationLng = json_data["results"][0]["locations"][0]["displayLatLng"]["lng"]
 
        print("Координаты местоположения МКС: " + str(locationLat) + ", " + str(locationLng))
        test_text = "Координаты местоположения МКС: " + str(locationLat) + ", " + str(locationLng)

        # Заголовок запроса
        HTTPHeaders = { 
          "Authorization": accessToken,
          "Content-Type": "application/json"
        }
        # Параметры запроса
        PostData = {
          "roomId": roomIdToGetMessages,
          "text": test_text
        }
        # Запрос (post)
        r = requests.post("https://webexapis.com/v1/messages",  
                           data = json.dumps(PostData), 
                           headers = HTTPHeaders)
                     


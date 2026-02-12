import requests as rq 

user_name = 'nazfelaksuresi8a4'
repo_ismi = 'Gorsel_yukleme_deposu'
api_base = f'https://api.github.com/repos/{user_name}/{repo_ismi}/contents/'

response = rq.get(api_base)
respond =  None

if response.status_code == 200:
    try:
        print('Response alınıyor..')
        respond = (response.json(),'json')
    
    except:
        try:
            print('Response json değil')
            respond = (response.text,'html')
        except:
            print('Response alınamadı')
            respond = (None,response)
        
else:
    print('Response başarısız')

if isinstance(respond,tuple) == True:
    if len(respond) == 2:
        response_data,response_type = respond
    
        if response_data == 0:
            print(f'hata kodu: {response_data} response objesi: {response_type} Hata: Response alınamadı')
        
        elif response_type == 'json':
            try:
                for respond_dataX in response_data:
                    with open(respond_dataX['name'],'wb') as fx:
                        fx.write(rq.get(respond_dataX['download_url']).content)

            except Exception as e0fx:
                print(f'hata: {e0fx}\n\ngelen response: {response_data}')
        
        elif response_type == 'html':
            print(f'{response_type} türü desteklenmiyor lütfen {api_base} adresini tekrardan kontrol edin')

        else:
            print('bilinmeyen hata')
            exit(0)

else:
    print('Beklenmeyen format')
    exit(0)

    
    

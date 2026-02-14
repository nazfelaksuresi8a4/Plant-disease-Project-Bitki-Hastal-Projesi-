import requests as rq 
import subprocess as sbp


class AGDS:
    def __init__(self,username,reponame,authToken):
        self.user_name = username
        self.repo_ismi = reponame
        self.api_base = f'https://api.github.com/repos/{self.user_name}/{self.repo_ismi}/contents/'
        self.headers = {
            'Authorization':authToken
        }

        print(f'Mevcut api tokeni: {authToken}')
        self.response = rq.get(url=self.api_base,
                               headers=self.headers)
        
        self.respond =  None
    
    def AGDSX(self):
        if self.response.status_code == 200:
            try:
                print('Response alınıyor..')
                respond = (self.response.json(),'json')
            
            except:
                try:
                    respond = (self.response.text,'html')
                except:
                    respond = (None,self.response)
                    return ('Response alınamadı')
                
        else:
            try:
                return (f'Response başarısız\nKulanıcı adı: {self.user_name}\nDepo ismi: {self.repo_ismi}\nDönüş kodu: {self.response.status_code}\nDönen istek çıktısı:{self.response.json()}')
            except:
                return (f'Response başarısız\nKulanıcı adı: {self.user_name}\nDepo ismi: {self.repo_ismi}\nDönüş kodu: {self.response.status_code}\nDönen istek çıktısı:{self.response.text}')

        if isinstance(respond,tuple) == True:
            if len(respond) == 2:
                response_data,response_type = respond
            
                if response_data == 0:
                    return (f'hata kodu: {response_data} response objesi: {response_type} Hata: Response alınamadı')
                
                elif response_type == 'json':
                    try:
                        for respond_dataX in response_data:
                            rxdata = respond_dataX['name']
                            with open(f'DepolamaSistemleri/{rxdata}','wb') as fx:
                                fx.write(rq.get(respond_dataX['download_url']).content)

                    except Exception as e0fx:
                        return (f'hata: {e0fx}\n\ngelen response: {response_data}')
                
                elif response_type == 'html':
                    return (f'{response_type} türü desteklenmiyor lütfen {self.api_base} adresini tekrardan kontrol edin')

                else:
                    return ('bilinmeyen hata')
                    exit(0)

        else:
            return ('Beklenmeyen format')


            
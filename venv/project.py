import requests
from pprint import pprint
from settings  import token


class YandexDisk:

    def __init__(self, token):
        self.token = token
        self.base_url = 'https://cloud-api.yandex.net/v1/disk'
        self.headers = {'Authorization': f"OAuth {token}"}
        
    def create_folder(self, path_disk):
        """Создаёт папку на вашем аккаунте по указанному адресу"""
        url = f'{self.base_url}/resources'
        self.path_disk = path_disk
        
        params = {'path': path_disk}
        response = requests.put(url, headers=self.headers, params=params) 

        
        if response.status_code == 201:
            print(f"{response.status_code}\nпапка {path_disk} успешно создана ")
            return path_disk
        elif response.status_code == 409:
            pass
        elif response.status_code == 404:
            print(f"{response.status_code} \nНекорректный запрос")
            return None
        else:
            print('Error')
            return None

    def delete_folder(self, path_disk):
        """Удаляет папку по указанному адресу"""
        url = f'{self.base_url}/resources'
        self.path = path_disk
        self.headers = {'Authorization': f"OAuth {token}"}
        params = {
            'path': path_disk,
            'permanently': True
        }
        
        response = requests.delete(url, params=params, headers=self.headers)
        if response.status_code == 204:
            print(f'Папка успешно удалена')
            return path_disk
        elif response.status_code in range(400, 499):
            print(f"{response.status_code} \nНекорректный запрос")
            return None
        else:
            print('Error')
            return None

    def add_one_photo(self, photo_url: str, path_disk):
        """ Загружает фото из интернета по ссылке photo_url по указанному адресу. 
            path_disk - Необходимо вводить путь в формате: название папки/название загружаемого фото"""
        self.path_disk = path_disk 
        self.photo_url = photo_url
        params = {
            'url': photo_url,
            "path": path_disk
        }
        url = f'{self.base_url}/resources/upload'
        response = requests.post(url, params=params, headers=self.headers)
        if response.status_code == 202:
            print(f'Фото успешно добавлено в папку {path_disk}')
        elif response.status_code in range(400, 499):
            print(f"{response.status_code} \nНекорректный запрос")
        else:
            print('Error')      
        
    def add_any_photos(self, photo_url: dict):
        """ Загружает несколько фото из интернета по ссылкам photo_url по указанному адресу. 
            Данные необходимо передавать в формате словаря: {папка/название: url}"""
        url = f'{self.base_url}/resources/upload'
        for breed, url in photo_url.items():
            params = {
            'url': url,
            "path": breed
        }
            response = requests.post(url, params=params, headers=self.headers) 
            if response.status_code == 202:
               print(f'Фото успешно добавлено в папку {params['path']}')
            elif response.status_code in range(400, 499):
               print(f"{response.status_code} \nНекорректный запрос")
            else:
               print('Error')  









Y = YandexDisk(token)

class Dogs:
     
     def __init__(self, breed):
        self.breed = breed

     def get_photo(self): 
        
        """возвращает ссылки на фото из интернета"""

        url = 'https://dog.ceo/api/breeds/list/all'
        response = requests.get(url).json()
        
        if response['message'][f'{self.breed}']:
            url_dict = {}
            for sub_breed in response['message'][f'{self.breed}']:
                sub_url = f'https://dog.ceo/api/breed/{self.breed}/{sub_breed}/images/random'
                new_resp = requests.get(sub_url).json()
                url_dict[f'{self.breed}/{sub_breed}'] = new_resp['message']
            return url_dict
        else:
            return f'https://dog.ceo/api/breed/{self.breed}/images/random'
    
        

        

dog = Dogs('australian')
p = dog.get_photo()
Y.add_any_photos(p)


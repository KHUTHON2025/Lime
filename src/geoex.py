import requests

def get_location_by_wifi(api_key):
    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}'

    response = requests.post(url)

    #print(response.text)  # 응답 내용을 확인해보기 위해 추가

    location_data = response.json()

    if response.status_code == 200 and 'location' in location_data:
        latitude = location_data['location']['lat']
        longitude = location_data['location']['lng']
        #print(f"위도: {latitude}, 경도: {longitude}")
    else:
        print("위치 정보를 가져오는 데 실패했습니다.")
    return latitude, longitude
latitude = 0
longitude = 0
kakao_api_key ="64ce3d1a6a44c275c55ba617749bf850"

google_api_key = "AIzaSyBEmcsvK5exQ4KAxVJHLj0ENgLS20s9OO0"
latitude, longitude = get_location_by_wifi(google_api_key)
#print(f"위도: {latitude}, 경도: {longitude}")
def get_address_from_coordinates(lat, lon, kakao_api_key):
    url = f"https://dapi.kakao.com/v2/local/geo/coord2address.json?x={lon}&y={lat}"
    headers = {
        "Authorization": f"KakaoAK {kakao_api_key}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    #print(data)
    if response.status_code == 200 and 'documents' in data:
        address = data['documents'][0]['address']['address_name']
        print(f"주소: {address}")
        return address.split()[-2]
    else:
        print("주소 변환에 실패했습니다.")

def get_address_by_id(id):
    if id == 1:
        latitude,longitude = get_location_by_wifi(google_api_key)
        print(f"위도: {latitude}, 경도: {longitude}")
        addr = get_address_from_coordinates(latitude, longitude, kakao_api_key)
        print(f"주소: {addr}")
        return addr
    elif id == 2:
        latitude = 37.2562588
        longitude = 127.0928905
        return get_address_from_coordinates(latitude, longitude, kakao_api_key)
    elif id == 3:
        latitude = 37.2862588
        longitude = 127.1128905
        return get_address_from_coordinates(latitude, longitude, kakao_api_key)
    else:
        latitude = 37.5665
        longitude = 126.978
        return get_address_from_coordinates(latitude, longitude, kakao_api_key)
    
# latitude, longitude = get_location_by_wifi(google_api_key)
# print(f"위도: {latitude}, 경도: {longitude}")
print(get_address_from_coordinates(latitude, longitude, kakao_api_key))
print(get_address_by_id(1))
print(get_address_by_id(2))
print(get_address_by_id(3))


def get_detect_url(id):
    if id == 1:
        return f"https://calf-exact-anteater.ngrok-free.app/detect"
    else:
        return f"https://calf-exact-anteater.ngrok-free.app/detectt"
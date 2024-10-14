import streamlit as st
import pandas as pd
import json
import joblib

PATH_UNIQUE_VALUES1 = 'model/unique_values1.json'
PATH_MODEL1 = 'model/model2.sav'


@st.cache_data
def load_model(path):

    model = joblib.load(path)
    return model

def station_to_ring(station):
    Sadovoe = ('Новослободская', 'Проспект мира', 'Белорусская','Баррикадная', 'Краснопресненская', 'Киевская', 'Cмоленская', 'Арбатская', 'Александровский сад', 'Кропоткинская', 'Библиотека им. Ленина', 'Полянка',
           'Октябрьская', 'Серпуховская', 'Добрынинская', 'Павелецкая', 'Третьяковская', 'Новокузнецкая', 'Павелецкая', 'Боровицкая', 'Площадь Революции', 'Тетральная', 'Охотный ряд', 'Китай-город', 'Лубянка',
           'Чеховская', 'Пушкинская', 'Тверская', 'Маяковская', 'Цветной бульвар', 'Трубная', 'Сухаревская', 'Сретенский бульвар', 'Тургеневская', 'Кузнецкий Мост', 'Чистые пруды', 'Красные ворота', 'Комсомольска',
           'Курская', 'Таганская', 'Марксистская', 'Парк культуры')

    Second_ring = ('Нижегородская', 'Серп и молот',  'Авиамоторная', 'Лефортово', 'Электрозаводская', 'Бауманская',  'Красносельская', 'Сокольники', 'Пл. трёх вокзалов', 'Рижская', 'Достоевская', 'Марьина Роща',
               'Савёловская', 'Менделеевская',  'Петровский парк', 'Динамо', 'ЦСКА', 'Хорошёвская', 'Беговая', 'Улица 1905 года', 'Тестовская', 'Деловой центр МЦК', 'Международная', 'Выставочная', 'Деловой центр',
               'Кутузовская', 'Студенческая', 'Фрунзенская', 'Спортивная', 'Лужники', 'Шаболовская', 'Ленинский проспект', 'Площадь Гагарина', 'Крымская', 'Тульская', 'Верхние Котлы', 'ЗИЛ', 'Автозаводская', 'Дубровка',
               'Крестьянская Застава', 'Пролетарская', 'Угрешская',  'Римская', 'Площадь Ильича',  'Москва-Товарная', 'Калитники', 'Новохохловская', 'Полежаевская')

    Third_ring = ('Текстильщики', 'Волгоградский проспект', 'Кожуховская', 'Печатники',  'Нагатинский Затон', 'Технопарк', 'Коломенская', 'Кленовый бульвар', 'Каширская', 'Варшавская', 'Севастопольская', 'Каховская',
              'Нахимовский проспект', 'Нагорная, Нагатинская', 'Академическая', 'Профсоюзная', 'Новые Черёмушки', 'Зюзино', 'Воронцовская', 'Калужская', 'Новаторская', 'Проспект Вернадского', 'Университет', 'Воробьёвы горы',
              'Мичуринский проспект', 'Раменки', 'Ломоносовский проспект', 'Минская', 'Поклонская', 'Парк Победы', 'Славянский бульвар', 'Матвеевская', 'Давыдково', 'Аминьевская', 'Кунцевская', 'Пионерская', 'Филёвский парк',
              'Багратионовская', 'Фили', 'Терехово', 'Кутузовская', 'Мнёвники', 'Шелепиха',  'Народное Ополчение', 'Хорошёво', 'Октябрьское поле', 'Зорге', 'Панфиловская', 'Стрешнево', 'Аэропорт', 'Сокол', 'Красный Балтиец',
              'Войковская', 'Гражданская', 'Савёловская', 'Дмитровская', 'Тимирязевская', 'Балтийская', 'Коптево', 'Лихоборы', 'Окружная', 'Владыкино', 'Петровско-Разумовская', 'Фонфизинская', 'Бутырская', 'Останкино', 'ВДНХ',
              'Алексеевская', 'Ботанический сад', 'Ростокино', 'Белокаменная', 'Бульвар Рокоссовского', 'Локомотив', 'Черкизовская', 'Преображенская площадь', 'Партизанская', 'Измайлово', 'Соколиная гора', 'Семёновская', 'Перово',
              'Шоссе Энтузиастов', 'Сортировочная', 'Андроновка')
    if station in Sadovoe:
        return 'Sadovoe'
    elif station in Second_ring:
        return 'Second_ring'
    elif station in Third_ring:
        return 'Third_ring'
    else:
        return 'Beyond_rings'

@st.cache_data
def transform(data):
    data['Apartment type'] = data['Apartment type'].replace(['Новое здание', 'Вторичная недвижимость'], ['New building', 'Secondary'])
    data['Region'] = data['Region'].replace(['Москва', 'Московская область'], ['Moscow', 'Moscow region'])
    data['Number of rooms'] = data['Number of rooms'].replace('Студия', 0).astype(int)
    data['Renovation'] = data['Renovation'].replace(['Косметический', 'Ремонт в европейском стиле', 'Дизайнерский', 'Без ремонта'],
                                                    ['Cosmetic', 'European-style renovation', 'Designer', 'Without renovation'])
    data['Ring'] = data['Metro station'].apply(station_to_ring)
    data['Number of rooms'] = data['Number of rooms'].apply(lambda x: -1 if x == 0 else x)
    data['Area_to_rooms'] = data['Area'] / abs(data['Number of rooms'])
    data['Number of rooms'] = data['Number of rooms'].apply(lambda x: 0 if x == -1 else x)

    return data

st.title('Оценка стоимости жилья в Москве и Московской области')
st.markdown(
    """
    Проект является учебным и содержит 2 страницы. На вкладке "Prediction" Вы можете оценить стоимость недвижимости в зависимости от приведенных 
    характеристик. Для этого введите все необходимые данные и нажмите кнопку "Рассчитать цену". На вкладке "Analysis" представлен анализ зависимости стоимости жилья 
    от указанных признаков, а также важность каждого признака в построенной модели.

"""
)


with open(PATH_UNIQUE_VALUES1) as file:
    dict_unique1 = json.load(file)

dict_unique1['Number of rooms'].remove(0)
dict_unique1['Number of rooms'].sort()
dict_unique1['Number of rooms'].append('Студия')
dict_unique1['Metro station'].sort()

apartment_type = st.selectbox('Тип недвижимости', (['Новое здание', 'Вторичная недвижимость']))
floor = st.slider('Этаж', min_value=min(dict_unique1['Floor']), max_value=30)
floors = st.slider('Количество этажей в доме', min_value=min(dict_unique1['Number of floors']), max_value=40)
rooms = st.selectbox('Количество комнат', (dict_unique1['Number of rooms']))
area = st.slider('Площадь квартиры', min_value=8.0, max_value=150.0)
kitchen_area = st.slider('Площадь кухни', min_value=min(dict_unique1['Kitchen area']), max_value=40.0)
living_area = st.slider('Жилая площадь', min_value=min(dict_unique1['Living area']), max_value=100.0)
renovation = st.selectbox('Тип ремонта', (['Косметический', 'Ремонт в европейском стиле', 'Дизайнерский', 'Без ремонта']))
region = st.selectbox('Регион', (['Москва', 'Московская область']))

Stations = dict_unique1['Metro station']

station = st.text_input("Начните вводить название ближайшей станции метро или МЦД:")

filtered_stations = [st for st in Stations if station.lower() in st.lower()]

metro_station = st.selectbox("Выберите станцию из списка:", filtered_stations)
metro_time = st.slider('Количество минут, необходимое чтобы дойти до станции', min_value=min(dict_unique1['Minutes to metro']), max_value=60.0)

errors = 0
if floor > floors:
    st.error("Ошибка: этаж не может быть больше количества этажей в доме.")
    errors += 1

if area < kitchen_area:
    st.error('Ошибка: площадь кухни не может быть больше общей площади.')
    errors += 1

if area < living_area:
    st.error('Ошибка: жилая площадь не может быть больше общей площади.')
    errors += 1

dict_data = {
    'Apartment type': apartment_type,
    'Metro station': metro_station,
    'Minutes to metro': metro_time,
    'Region': region,
    'Number of rooms': rooms,
    'Area': area,
    'Living area': living_area,
    'Kitchen area': kitchen_area,
    'Floor': floor,
    'Number of floors': floors,
    'Renovation': renovation
}

data_predict = pd.DataFrame([dict_data])
data_predict = transform(data_predict)

model = load_model(PATH_MODEL1)

button = st.button('Рассчитать цену')
if button:
    if errors != 0:
        st.error("Исправьте введенные данные и нажмите кнопку еще раз.")
    else:
        output = model.predict(data_predict)
        output = int(output // 1000 * 1000)
        st.success(f'Цена квартиры будет составлять приблизительно {output} рублей')

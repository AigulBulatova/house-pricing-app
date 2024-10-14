import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from views.prediction import station_to_ring


PATH_DATA = 'model/data_clean.csv'
PATH_MODEL = 'model/model2.sav'

@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    data = data.sample(5000, random_state=42)

    return data

@st.cache_data
def load_model(path):

    model = joblib.load(path)
    return model

def transform(data):
    data['Apartment type'] = data['Apartment type'].replace(['New building', 'Secondary'], ['Новое здание', 'Вторичная недвижимость'])
    data['Region'] = data['Region'].replace(['Moscow', 'Moscow region'], ['Москва', 'Московская область'])
    data['Numbers of rooms'] = data['Number of rooms'].replace(0, 'Студия')
    data['Renovation'] = data['Renovation'].replace(['Cosmetic', 'European-style renovation', 'Designer', 'Without renovation'], 
                                                    ['Косметический', 'Ремонт в европейском стиле', 'Дизайнерский', 'Без ремонта'])
    data['Ring'] = data['Metro station'].apply(station_to_ring)


@st.cache_data
def feature_importances(_model):
    feature_importances = model.get_feature_importance()

    feature_names = ['Тип недвижимости', 'Станция метро', 'Время до метро', 'Регион',
        'Количество комнат', 'Площадь', 'Жилая площадь', 'Площадь кухни', 'Этаж',
        'Количество этажей в доме', 'Ремонт', 'Транспортное кольцо', 'Средняя площадь комнат']
    importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})

    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    
    colors = ['tomato', 'coral', 'orange', 'gold', 'yellow', 'yellowgreen', 'limegreen', 'lightseagreen', 'royalblue', 'slateblue', 'blueviolet', 'purple', 'indigo'] # cmap(norm(importance_df['Importance']))

    figure = plt.figure(figsize=(10, 6))
    plt.barh(importance_df['Feature'], importance_df['Importance'], color=colors)
    plt.xlabel('Важность')
    plt.title('Важность признаков в построенной модели предсказания цены')
    plt.gca().invert_yaxis() 
    plt.grid()
    plt.show()

    return figure


def cat_ranges(df):
    sns.set_palette('rocket')

    fig1, axes = plt.subplots(nrows=2, ncols=2, figsize=(18, 15), dpi=85, tight_layout=True)
    
    sns.barplot(data=df, x='Apartment type', y='Price', hue='Apartment type', legend=False, ax=axes[0][0])
    axes[0][0].set_xlabel("Тип недвижимости")
    axes[0][0].set_ylabel("Цена")
    axes[0][0].grid()

    sns.barplot(data=df, x='Ring', y='Price', hue='Ring', legend=False, ax=axes[0][1])
    axes[0][1].set_xlabel("Транспортное кольцо")
    axes[0][1].set_ylabel("Цена")
    axes[0][1].grid()

    sns.barplot(data=df, x='Region', y='Price', hue='Region', legend=False, ax=axes[1][0])
    axes[1][0].set_xlabel("Регион")
    axes[1][0].set_ylabel("Цена")
    axes[1][0].grid()

    sns.barplot(data=df, x='Renovation', y='Price', hue='Renovation', legend=False, ax=axes[1][1])
    axes[1][1].set_xlabel("Тип ремонта")
    axes[1][1].set_ylabel("Цена")
    axes[1][1].grid()

    plt.suptitle("Зависимости цены на жилье от типа недвижимости, транспортного кольца, региона и типа ремонта.")
    plt.show()

    fig2 = plt.figure(figsize=[5, 5])
    sns.barplot(data=df, x='Number of rooms', y='Price', hue='Number of rooms', legend=False, palette='rocket')
    plt.xlabel('Количество комнат')
    plt.ylabel('Цена')
    plt.grid()

    return fig1, fig2


@st.cache_data
def num_range(df):
    #sns.set_palette("Spectral")
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 12), dpi=100)

    sns.scatterplot(data=df, x='Minutes to metro', y='Price', hue='Number of rooms', ax=axes[0][0])
    axes[0][0].set_xlabel("Время до метро")
    axes[0][0].set_ylabel("Цена")
    axes[0][0].grid()

    sns.scatterplot(data=df, x='Number of floors', y='Price', hue='Number of rooms', ax=axes[0][1])
    axes[0][1].set_xlabel("Количество этажей")
    axes[0][1].set_ylabel("Цена")
    axes[0][1].grid()

    sns.scatterplot(data=df, x='Floor', y='Price', hue='Number of rooms', ax=axes[0][2])
    axes[0][2].set_xlabel("Этаж")
    axes[0][2].set_ylabel("Цена")
    axes[0][2].grid()

    sns.scatterplot(data=df, x='Area', y='Price', hue='Number of rooms', ax=axes[1][0])
    axes[1][0].set_xlabel("Площадь")
    axes[1][0].set_ylabel("Цена")
    axes[1][0].grid()

    sns.scatterplot(data=df, x='Living area', y='Price', hue='Number of rooms', ax=axes[1][1])
    axes[1][1].set_xlabel("жилая площадь")
    axes[1][1].set_ylabel("Цена")
    axes[1][1].grid()

    sns.scatterplot(data=df, x='Kitchen area', y='Price', hue='Number of rooms', ax=axes[1][2])
    axes[1][2].set_xlabel("Площадь кухни")
    axes[1][2].set_ylabel("Цена")
    axes[1][2].grid()

    plt.suptitle("Зависимость цены от числовых признаков")
    plt.show()

    return fig


st.title('')

df = load_data(PATH_DATA)
transform(df)

model = load_model(PATH_MODEL)

fig1, fig = cat_ranges(df)
st.pyplot(fig1)
st.pyplot(fig)

fig2 = num_range(df)
st.pyplot(fig2)

fig3 = feature_importances(model)
st.pyplot(fig3)
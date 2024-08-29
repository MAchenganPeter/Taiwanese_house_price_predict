# https://docs.streamlit.io/library/cheatsheet
# streamlit run app.py
import streamlit as st
import numpy as np
import joblib
import pickle

clf2 = joblib.load('regr_C.joblib')

with open(r'編碼.pickle', 'rb') as f:
    new_data = pickle.load(f)

交易標的 = {new_data['C']['交易標的'][1][i]:new_data['C']['交易標的'][0][i] for i in range(len(new_data['C']['交易標的'][0]))}
都市非都市計畫 = {new_data['C']['都市/非都市計畫'][1][i]:new_data['C']['都市/非都市計畫'][0][i] for i in range(len(new_data['C']['都市/非都市計畫'][0]))}
土地使用分區 = {new_data['C']['土地使用分區'][1][i]:new_data['C']['土地使用分區'][0][i] for i in range(len(new_data['C']['土地使用分區'][0]))}
建物型態 = {new_data['C']['建物型態'][1][i]:new_data['C']['建物型態'][0][i] for i in range(len(new_data['C']['建物型態'][0]))}
隔間 = {new_data['C']['建物現況格局-隔間'][1][i]:new_data['C']['建物現況格局-隔間'][0][i] for i in range(len(new_data['C']['建物現況格局-隔間'][0]))}
是否有附傢俱 = {new_data['C']['有無附傢俱'][1][i]:new_data['C']['有無附傢俱'][0][i] for i in range(len(new_data['C']['有無附傢俱'][0]))}
有無管理組織 = {new_data['C']['有無管理組織'][1][i]:new_data['C']['有無管理組織'][0][i] for i in range(len(new_data['C']['有無管理組織'][0]))}
車位類別 = {new_data['C']['車位類別'][1][i]:new_data['C']['車位類別'][0][i] for i in range(len(new_data['C']['車位類別'][0]))}
租賃層次 = {new_data['C']['租賃層次'][1][i]:new_data['C']['租賃層次'][0][i] for i in range(len(new_data['C']['租賃層次'][0]))}
Combined = {new_data['C']['Combined'][1][i]:new_data['C']['Combined'][0][i] for i in range(len(new_data['C']['Combined'][0]))}


st.markdown('# 不動產租賃價格預測系統')
col1, col2 = st.columns(2)

with col1:
    select_county = list(map(lambda x : x[:3], list(Combined.keys())))
    F1 = st.selectbox('縣市', set(select_county))
    county = list(filter(lambda x : x[:3] == F1, list(Combined.keys())))
    towns = list(map(lambda x : x[4:], county))
    F2 = st.selectbox('鄉鎮市區', towns)
    CT = Combined[F1+'_'+F2].split('_')
    F3 = st.selectbox('交易標的', 交易標的.keys())
    F4 = st.radio('都市/非都市計畫', 都市非都市計畫.keys())
    F5 = st.selectbox('土地使用分區', 土地使用分區.keys())
    F6 = st.selectbox('建物型態', 建物型態.keys())
    F7 = st.number_input("土地(數量)", min_value=0, step=1, placeholder="Type a number...") 
    F8 = st.number_input("建物(數量)", min_value=0, step=1, placeholder="Type a number...") 
    F9 = st.number_input("車位(數量)", min_value=0, step=1, placeholder="Type a number...")       
    F10 = st.number_input("房間(數量)", min_value=0, step=1, placeholder="Type a number...") 
    F11 = st.number_input("客廳/廚房(數量)", min_value=0, step=1, placeholder="Type a number...") 
with col2:
    F12 = st.number_input("衛浴間(數量)", min_value=0, step=1, placeholder="Type a number...")     
    F13 = st.radio('是否有隔間', 隔間.keys())
    F14 = st.number_input("土地面積(坪)", min_value=0.0, step=0.1, placeholder="Type a number...") 
    F15 = st.number_input("建物面積(坪)", min_value=0.0, step=0.1, placeholder="Type a number...") 
    F16 = st.number_input("車位面積(坪)", min_value=0.0, step=0.1, placeholder="Type a number...")      
    F17 = st.number_input("屋齡", min_value=-1, step=1, placeholder="Type a number...")      
    F18 = st.radio('是否有附傢俱', 是否有附傢俱.keys())        
    F19 = st.radio('是否有管理人', 有無管理組織.keys())  
    F20 = st.selectbox('車位類別', 車位類別.keys())    
    F21 = st.selectbox('租賃層次', 租賃層次.keys()) 
    F22 = st.slider('車位總價格', new_data['C']['車位總價元'][0], new_data['C']['車位總價元'][1], 1000)
if st.button('預測總價格'):
    X = np.array([[交易標的[F3], int(CT[0]), int(CT[1]), 都市非都市計畫[F4], 土地使用分區[F5], 建物型態[F6], F10, F11, F12, 隔間[F13], F7, F8,
                  F9, F14, F15, F16, F17, 有無管理組織[F19], 是否有附傢俱[F18], 車位類別[F20], 租賃層次[F21], F22]])

    st.markdown('預測結果：{}元'.format(format(int(clf2.predict(X)[0]),',')))  
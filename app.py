import pickle
import streamlit as st


def get_recommendations(channel_name):
    # 채널을 통해서 전체 데이터 기준 그 채널의 index 값을 얻기
    idx = playlist_channels[playlist_channels == channel_name].index[0]

    # 코사인 유사도 매트릭스 (cosine_sim) 에서 idx 에 해당하는 데이터를 (idx, 유사도) 형태로 얻기
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 코사인 유사도 기준으로 내림차순 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 자기 자신을 제외한 10개의 채널을 슬라이싱
    sim_scores = sim_scores[1:11]

    # 추천 채널 목록 10개의 인덱스 정보 추출
    channel_indices = [i[0] for i in sim_scores]

    # 인덱스 정보를 통해 채널 이름 추출
    channel_names = []
    for i in channel_indices:
        channel_names.append(playlist_channels.iloc[i])

    return channel_names


playlist_channels = pickle.load(open("playlist_channels.pickle", "rb"))
cosine_sim = pickle.load(open("cosine_sim.pickle", "rb"))

st.set_page_config(layout="wide")
st.header("Playlist Recommendation System")

# movie_list = movies["title"].values
playlist_channel_list = list(playlist_channels)
channel = st.selectbox("Choose a playlist channel you like", playlist_channel_list)

if st.button("Recommend"):
    with st.spinner("Please wait..."):
        channel_names = get_recommendations(channel)

        idx = 0
        for i in range(10):
            cols = st.columns(1)
            for col in cols:
                col.write(channel_names[idx])
                idx += 1

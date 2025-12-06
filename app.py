import streamlit as st
import pandas as pd

st.set_page_config(page_title="さだまさし歌詞検索アプリ", layout="wide")

st.title("👓さだまさし歌詞フレーズ検索アプリ")

# 1. データ読み込み
try:
    df = pd.read_csv('songs.csv', encoding='utf-8')
except FileNotFoundError:
    st.error("エラー: 'songs.csv' が見つかりません。")
    st.stop()

# 2. サイドバー（アルバム絞り込み）
st.sidebar.header("検索オプション")
album_list = ['すべてのアルバム'] + list(df['Album'].unique())
selected_album = st.sidebar.selectbox("アルバムを選択", album_list)

if selected_album != 'すべてのアルバム':
    df = df[df['Album'] == selected_album]

# 3. メイン検索バー
query = st.text_input("歌詞のフレーズを入力してください", "")

# 4. 検索結果の表示
if query:
    results = df[df['Lyrics'].str.contains(query, case=False, na=False)]
    
    st.markdown(f"---")
    st.markdown(f"### 検索結果: {len(results)} 件")

    if not results.empty:
        for index, row in results.iterrows():
            # 検索ヒットした曲を1つずつカードのように表示
            with st.expander(f"🎵 {row['Title']}  (アルバム: {row['Album']})", expanded=False):
                # ヒットしたキーワードをハイライト（赤字）にする処理
                highlighted_text = row['Lyrics'].replace(query, f":red[**{query}**]")
                st.markdown(highlighted_text)
    else:
        st.warning("一致する曲が見つかりませんでした。")
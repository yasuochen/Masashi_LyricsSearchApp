import streamlit as st
import pandas as pd

st.set_page_config(page_title="さだまさし歌詩検索アプリ", layout="wide")

# --- 🔐 パスワード認証機能 ---
def check_password():
    """パスワードが正しい場合のみTrueを返す"""
    def password_entered():
        """パスワードが入力された時のチェック処理"""
        if st.session_state["password"] == "sadaken1980":  # ←ここに設定したいパスワード
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # 安全のためパスワードを削除
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # 初回起動時
        st.text_input(
            "パスワードを入力してください", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # パスワード間違い
        st.text_input(
            "パスワードを入力してください", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 パスワードが違います")
        return False
    else:
        # 認証成功
        return True

if check_password():
    # --- 認証成功後に表示されるメインアプリ ---
    
    st.title("👓さだまさし歌詩検索アプリ")

    # データ読み込み
    try:
        df = pd.read_csv('songs.csv', encoding='utf-8')
    except FileNotFoundError:
        st.warning("⚠️ 'songs.csv' が見つかりません。")
        st.stop()

    # サイドバー（アルバム絞り込み）
    st.sidebar.header("検索オプション")
    if 'Album' in df.columns:
        album_list = ['すべてのアルバム'] + list(df['Album'].unique())
        selected_album = st.sidebar.selectbox("アルバムを選択", album_list)

        if selected_album != 'すべてのアルバム':
            df = df[df['Album'] == selected_album]

    # メイン検索バー
    query = st.text_input("歌詩のフレーズを入力してください", "")

    # 検索結果の表示
    if query:
        if 'Lyrics' in df.columns:
            results = df[df['Lyrics'].str.contains(query, case=False, na=False)]
            
            st.markdown(f"---")
            st.markdown(f"### 検索結果: {len(results)} 件")

            if not results.empty:
                for index, row in results.iterrows():
                    title_text = row['Title'] if 'Title' in df.columns else "不明なタイトル"
                    album_text = row['Album'] if 'Album' in df.columns else "不明なアルバム"
                    
                    with st.expander(f"🎵 {title_text}  (アルバム: {album_text})", expanded=False):
                        highlighted_text = row['Lyrics'].replace(query, f":red[**{query}**]")
                        st.markdown(highlighted_text)
            else:
                st.warning("一致する曲が見つかりませんでした。")
        else:
            st.error("CSVファイルに 'Lyrics' 列がありません。")

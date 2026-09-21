# 영화 데이터 그래프 도감 1 - 시간
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    # 1년치(365일) 일별 박스오피스 10위권 기록을 불러옵니다.
    df = pd.read_csv(DATA_URL)
    # 여덟 자리 숫자로 된 날짜 열을 진짜 날짜로 바꿉니다.
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


df = load_data()

# ── 그래프 1. 영화 하나의 흥행 곡선 ──────────────────────────
st.header("1. 한 영화의 흥행 곡선")

# 드롭다운으로 영화를 고릅니다.
movie_list = sorted(df["영화명"].unique())
movie = st.selectbox("영화를 고르세요", movie_list)

one = df[df["영화명"] == movie].sort_values("날짜")
fig = px.line(one, x="날짜", y="일관객", markers=True)
fig.update_traces(hovertemplate="날짜 %{x|%Y-%m-%d}<br>관객 %{y:,}명<extra></extra>")
st.plotly_chart(fig, width="stretch")

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")

# ── 앞으로 그래프 2, 3, 4, 5가 이 아래에 추가됩니다 ──────────

# ==================================================
# 그래프 2
# ==================================================

st.divider()

st.header("📊 그래프 2. 일관객 합계 상위 5편의 날짜별 변화")

# 영화별 전체 기간 일관객 합계
movie_total = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
)

# 합계가 가장 큰 영화 5편
top5_movies = movie_total.head(5).index.tolist()

# TOP 5 영화의 데이터만 가져오기
top5_df = df[df["영화명"].isin(top5_movies)].copy()

# 날짜별 영화별 일관객
top5_daily = (
    top5_df
    .groupby(["날짜", "영화명"], as_index=False)["일관객"]
    .sum()
)

# 날짜순 정렬
top5_daily = top5_daily.sort_values(["날짜", "영화명"])

# 선 그래프
fig2 = px.line(
    top5_daily,
    x="날짜",
    y="일관객",
    color="영화명",
    title="일관객 합계 상위 5편의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)

# 마우스를 올렸을 때 표시되는 내용
fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}"
        "<br>날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화",
    hovermode="x unified"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것**")

st.text_input(
    "내용을 입력하세요.",
    placeholder="예: 기간 동안 일관객 합계가 가장 큰 5편의 날짜별 관객 변화를 비교할 수 있다.",
    key="graph2_description"
)

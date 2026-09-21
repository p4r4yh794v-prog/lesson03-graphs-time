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

# ==================================================
# 그래프 3. 날짜별 10위권 일관객 합계
# ==================================================

st.divider()

st.header("📊 그래프 3. 날짜별 10위권 일관객 합계")

# 날짜별 10위권 일관객 합계 계산
daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 일관객 합계가 가장 큰 날짜 3개
top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values("날짜")
)

# 영역 그래프
fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    }
)

# 마우스를 올렸을 때 표시
fig3.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>10위권 일관객 합계: %{y:,}명"
        "<extra></extra>"
    )
)

# 그래프 위에 상위 3일 표시
for _, row in top3_days.iterrows():
    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=row["날짜"].strftime("%Y-%m-%d"),
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-45
    )

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계(명)"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것**")

st.text_input(
    "내용을 입력하세요.",
    placeholder="예: 날짜에 따라 전체 10위권 영화의 관객 규모가 어떻게 변화했는지 알 수 있다.",
    key="graph3_description"
)

# ==================================================
# 그래프 4. 영화별 일관객 TOP 10
# ==================================================

st.divider()

st.header("📊 그래프 4. 영화별 일관객 TOP 10")

# 영화별 일관객 합계와 10위권에 든 날수 계산
movie_summary = (
    df.groupby("영화명")
    .agg(
        총_일관객=("일관객", "sum"),
        상영일수=("날짜", "nunique")
    )
    .sort_values("총_일관객", ascending=False)
)

# TOP 10만 선택
top10_movies = movie_summary.head(10).reset_index()

# 그래프에서는 관객이 많은 영화가 위에 오도록 역순으로 정렬
top10_movies = top10_movies.sort_values("총_일관객", ascending=True)

fig4 = px.bar(
    top10_movies,
    x="총_일관객",
    y="영화명",
    orientation="h",
    title="기간 내 일관객 합계 TOP 10",
    labels={
        "총_일관객": "기간 내 일관객 합계",
        "영화명": "영화"
    }
)

# 마우스를 올렸을 때 총 관객 수 + 10위권에 든 날수 표시
fig4.update_traces(
    customdata=top10_movies[["상영일수"]].values,
    hovertemplate=(
        "영화: %{y}"
        "<br>기간 내 일관객 합계: %{x:,}명"
        "<br>10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    )
)

fig4.update_layout(
    xaxis_title="기간 내 일관객 합계(명)",
    yaxis_title="영화",
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것**")

st.text_input(
    "내용을 입력하세요.",
    placeholder="예: 전체 기간 동안 10위권에서 누적 관객이 많았던 영화와 그 영화가 10위권에 머문 날수를 비교할 수 있다.",
    key="graph4_description"
)

# ==================================================
# 그래프 5. 월 × 요일별 일관객 합계 히트맵
# ==================================================

st.divider()

st.header("📊 그래프 5. 월 × 요일별 일관객 합계")

# 월과 요일 추출
heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month

weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

heatmap_df["요일"] = heatmap_df["날짜"].dt.dayofweek.map(
    dict(enumerate(weekday_order))
)

# 월 × 요일별 일관객 합계
heatmap_data = (
    heatmap_df
    .groupby(["월", "요일"])["일관객"]
    .sum()
    .unstack(fill_value=0)
)

# 요일을 월요일 → 일요일 순서로 정렬
heatmap_data = heatmap_data.reindex(columns=weekday_order)

# 히트맵
fig5 = px.imshow(
    heatmap_data,
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계"
    },
    x=weekday_order,
    y=heatmap_data.index,
    color_continuous_scale="Blues",
    aspect="auto",
    text_auto=".0f"
)

fig5.update_layout(
    title="월 × 요일별 10위권 일관객 합계",
    xaxis_title="요일",
    yaxis_title="월"
)

fig5.update_traces(
    hovertemplate=(
        "%{y}월 %{x}"
        "<br>일관객 합계: %{z:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것**")

st.text_input(
    "내용을 입력하세요.",
    placeholder="예: 월과 요일에 따라 10위권 영화의 전체 관객 규모가 어떻게 달라지는지 알 수 있다.",
    key="graph5_description"
)

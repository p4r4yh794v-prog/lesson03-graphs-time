# ==================================================
# 그래프 2. 기간 일관객 합계 TOP 5 영화
# ==================================================

st.divider()

st.header("📊 그래프 2. 일관객 합계 상위 5편의 날짜별 변화")

# 영화별 전체 기간 일관객 합계 계산
top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
    .tolist()
)

# 상위 5편만 추출
top5_df = df[df["영화명"].isin(top5_movies)].copy()

# 날짜별 영화별 일관객으로 정리
top5_df = (
    top5_df.groupby(["날짜", "영화명"], as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=False,
    title="일관객 합계 상위 5편의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)

# 마우스를 올렸을 때 날짜와 관객수가 표시되도록 설정
fig2.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra>%{fullData.name}</extra>"
)

fig2.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것**")
st.text_input(
    "내용을 입력하세요.",
    placeholder="예: 기간 동안 일관객 합계가 가장 큰 영화 5편의 관객 변화를 비교할 수 있다.",
    key="graph2_description"
)

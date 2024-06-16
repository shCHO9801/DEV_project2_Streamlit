import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import os

# 로컬 CSV 파일 경로 지정
file_path_daily = os.path.join(os.path.dirname(__file__), '..', 'daily.csv')
file_path_user = os.path.join(os.path.dirname(__file__), '..', 'user_new.csv')


# CSV 파일 로드
day_df = pd.read_csv(file_path_daily)
user_df = pd.read_csv(file_path_user)

# 날짜 변환
day_df['event_date'] = pd.to_datetime(day_df['event_date'])
user_df['last_event_time'] = pd.to_datetime(user_df['last_event_time'], errors='coerce')
user_df['first_visit'] = pd.to_datetime(user_df['first_visit'], errors='coerce')

# fig 1, 2
# Extract relevant columns
dates = np.array(day_df['event_date'])
retention_1d = day_df['1-Day Retention Rate (%)']
retention_3d = day_df['3-Day Retention Rate (%)']
retention_7d = day_df['7-Day Retention Rate (%)']
retention_30d = day_df['30-Day Retention Rate (%)']
purchase_retention_1d = day_df['1-Day Purchase Retention Rate (%)']
purchase_retention_3d = day_df['3-Day Purchase Retention Rate (%)']
purchase_retention_7d = day_df['7-Day Purchase Retention Rate (%)']
purchase_retention_30d = day_df['30-Day Purchase Retention Rate (%)']

# Calculate tick values and labels
tickvals = pd.date_range(start=dates[0], end=dates[-1], freq='1W')
ticktext = [date.strftime('%Y-%m-%d') for date in tickvals]

# Figure 1: Retention Rates with Date Formatting
fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x=dates, y=retention_1d, mode='lines', name='1-Day',
    line=dict(color='rgba(55, 83, 109, 0.6)')
))
fig1.add_trace(go.Scatter(
    x=dates, y=retention_3d, mode='lines', name='3-Day',
    line=dict(color='rgba(26, 118, 255, 0.6)')
))
fig1.add_trace(go.Scatter(
    x=dates, y=retention_7d, mode='lines', name='7-Day',
    line=dict(color='rgba(50, 171, 96, 0.6)')
))
fig1.add_trace(go.Scatter(
    x=dates, y=retention_30d, mode='lines', name='30-Day(%)',
    line=dict(color='rgba(255, 140, 0, 0.6)')
))

fig1.update_layout(
    title='Retention Rates Over Time',
    xaxis_title='Date',
    yaxis_title='Retention Rate (%)',
    xaxis=dict(
        tickvals=tickvals,
        ticktext=ticktext,
        tickangle=45
    ),
    legend=dict(
        title='Retention Rates',
        orientation='h',
        x=0.5,
        y=1.15,
        xanchor='center'
    ),
    template='plotly_white'
)

# Figure 2: Purchase Retention Rates with Date Formatting
fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=dates, y=purchase_retention_1d, mode='lines', name='1-Day',
    line=dict(color='rgba(55, 83, 109, 0.6)')
))
fig2.add_trace(go.Scatter(
    x=dates, y=purchase_retention_3d, mode='lines', name='3-Day',
    line=dict(color='rgba(26, 118, 255, 0.6)')
))
fig2.add_trace(go.Scatter(
    x=dates, y=purchase_retention_7d, mode='lines', name='7-Day',
    line=dict(color='rgba(50, 171, 96, 0.6)')
))
fig2.add_trace(go.Scatter(
    x=dates, y=purchase_retention_30d, mode='lines', name='30-Day(%)',
    line=dict(color='rgba(255, 140, 0, 0.6)')
))

fig2.update_layout(
    title='Purchase Retention Rates Over Time',
    xaxis_title='Date',
    yaxis_title='Purchase Retention Rate (%)',
    xaxis=dict(
        tickvals=tickvals,
        ticktext=ticktext,
        tickangle=45
    ),
    legend=dict(
        title='Purchase Retention Rates',
        orientation='h',
        x=0.5,
        y=1.15,
        xanchor='center'
    ),
    template='plotly_white'
)

# fig 3
# 리텐션 차이 계산
retention_diff_1_3 = retention_3d - retention_1d
retention_diff_3_7 = retention_7d - retention_3d
retention_diff_7_30 = retention_30d - retention_7d

# 결과 데이터프레임 생성
retention_diff_df = pd.DataFrame({
    'event_date': day_df['event_date'],
    '1d_to_3d_diff': retention_diff_1_3,
    '3d_to_7d_diff': retention_diff_3_7,
    '7d_to_30d_diff': retention_diff_7_30
})

# 시각화
fig3 = go.Figure()

fig3.add_trace(go.Bar(
    x=retention_diff_df['event_date'],
    y=retention_diff_df['7d_to_30d_diff'],
    name='7d to 30d Diff',
    marker_color='rgba(255, 204, 0, 0.6)',
    legendgroup='1',
    showlegend=False
))
fig3.add_trace(go.Bar(
    x=retention_diff_df['event_date'],
    y=retention_diff_df['1d_to_3d_diff'],
    name='1d to 3d Diff',
    marker_color='rgba(34, 139, 34, 0.6)',
    legendgroup='2',
    showlegend=False
))
fig3.add_trace(go.Bar(
    x=retention_diff_df['event_date'],
    y=retention_diff_df['3d_to_7d_diff'],
    name='3d to 7d Diff',
    marker_color='rgba(26, 118, 255, 0.6)',
    legendgroup='3',
    showlegend=False
))

# 각 그룹에 대한 레전드 순서 변경
fig3.add_trace(go.Bar(
    x=[None],
    y=[None],
    name='1d to 3d Diff',
    marker_color='rgba(34, 139, 34, 0.6)',
    legendgroup='2'
))
fig3.add_trace(go.Bar(
    x=[None],
    y=[None],
    name='3d to 7d Diff',
    marker_color='rgba(26, 118, 255, 0.6)',
    legendgroup='3'
))
fig3.add_trace(go.Bar(
    x=[None],
    y=[None],
    name='7d to 30d Diff',
    marker_color='rgba(255, 204, 0, 0.6)',
    legendgroup='1'
))

# 1주일 단위의 tick 설정
tickvals = pd.date_range(start=retention_diff_df['event_date'].min(), end=retention_diff_df['event_date'].max(), freq='W')
ticktext = tickvals.strftime('%Y-%m-%d')

# 그래프 레이아웃 설정
fig3.update_layout(
    title='Retention Rate Differences Over Time',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Retention Rate Difference (%)',
        titlefont_size=16,
        tickfont_size=14,
    ),
    xaxis=dict(
        title='Event Date',
        tickvals=tickvals,
        ticktext=ticktext,
        tickangle=45
    ),
    legend=dict(
        orientation='h',  # 가로로 나열
        x=0,
        y=1.1,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='overlay',  # 겹쳐서 표시
    bargap=0.15,  # gap between bars of adjacent location coordinates.
    bargroupgap=0.1  # gap between bars of the same location coordinates.
)

# fig 4
# 리텐션 차이 계산
purchase_retention_diff_1_3 = purchase_retention_3d - purchase_retention_1d
purchase_retention_diff_3_7 = purchase_retention_7d - purchase_retention_3d
purchase_retention_diff_7_30 = purchase_retention_30d - purchase_retention_7d

# 결과 데이터프레임 생성
purchase_retention_diff_df = pd.DataFrame({
    'event_date': day_df['event_date'],
    '1d_to_3d_diff': purchase_retention_diff_1_3,
    '3d_to_7d_diff': purchase_retention_diff_3_7,
    '7d_to_30d_diff': purchase_retention_diff_7_30
})

# 시각화
fig4 = go.Figure()

fig4.add_trace(go.Bar(
    x=purchase_retention_diff_df['event_date'],
    y=purchase_retention_diff_df['7d_to_30d_diff'],
    name='7d to 30d Diff',
    marker_color='rgba(255, 204, 0, 0.6)',
    legendgroup='1',
    showlegend=False
))
fig4.add_trace(go.Bar(
    x=purchase_retention_diff_df['event_date'],
    y=purchase_retention_diff_df['1d_to_3d_diff'],
    name='1d to 3d Diff',
    marker_color='rgba(34, 139, 34, 0.6)',
    legendgroup='2',
    showlegend=False
))
fig4.add_trace(go.Bar(
    x=purchase_retention_diff_df['event_date'],
    y=purchase_retention_diff_df['3d_to_7d_diff'],
    name='3d to 7d Diff',
    marker_color='rgba(26, 118, 255, 0.6)',
    legendgroup='3',
    showlegend=False
))

# 각 그룹에 대한 레전드 순서 변경
fig4.add_trace(go.Bar(
    x=[None],
    y=[None],
    name='1d to 3d Diff',
    marker_color='rgba(34, 139, 34, 0.6)',
    legendgroup='2'
))
fig4.add_trace(go.Bar(
    x=[None],
    y=[None],
    name='3d to 7d Diff',
    marker_color='rgba(26, 118, 255, 0.6)',
    legendgroup='3'
))
fig4.add_trace(go.Bar(
    x=[None],
    y=[None],
    name='7d to 30d Diff',
    marker_color='rgba(255, 204, 0, 0.6)',
    legendgroup='1'
))

# 1주일 단위의 tick 설정
tickvals = pd.date_range(start=purchase_retention_diff_df['event_date'].min(), end=retention_diff_df['event_date'].max(), freq='W')
ticktext = tickvals.strftime('%Y-%m-%d')

# 그래프 레이아웃 설정
fig4.update_layout(
    title='Purchase Retention Rate Differences Over Time',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Purchase Retention Rate Difference (%)',
        titlefont_size=16,
        tickfont_size=14,
    ),
    xaxis=dict(
        title='Event Date',
        tickvals=tickvals,
        ticktext=ticktext,
        tickangle=45
    ),
    legend=dict(
        orientation='h',  # 가로로 나열
        x=0,
        y=1.1,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='overlay',  # 겹쳐서 표시
    bargap=0.15,  # gap between bars of adjacent location coordinates.
    bargroupgap=0.1  # gap between bars of the same location coordinates.
)

# fig 5
# NaN 값 제거
filtered_data = user_df.dropna(subset=['last_event_time', 'first_visit'])

# 최대 이벤트 시간 계산
max_event_time = filtered_data['last_event_time'].max()

# 마지막 접속일로부터 지난 시간 계산
filtered_data['days_since_last_event'] = (max_event_time - filtered_data['last_event_time']).dt.days
filtered_data['days_since_first_visit'] = (max_event_time - filtered_data['first_visit']).dt.days

# NaN 값 및 무한대 값 제거
filtered_data = filtered_data.dropna(subset=['days_since_last_event', 'days_since_first_visit'])
filtered_data = filtered_data[filtered_data['days_since_last_event'] != float('inf')]
filtered_data = filtered_data[filtered_data['days_since_first_visit'] != float('inf')]

# 두 컬럼 중 하나라도 0인 행을 삭제합니다.
filtered_data = filtered_data[(filtered_data['days_since_last_event'] != 0) & (filtered_data['days_since_first_visit'] != 0)]

# 히트맵 시각화
heatmap_data = filtered_data.pivot_table(index='days_since_first_visit', columns='days_since_last_event', aggfunc='size', fill_value=0)
heatmap_data = heatmap_data.reset_index().melt(id_vars='days_since_first_visit')

fig_blues = px.density_heatmap(heatmap_data, x='days_since_first_visit', y='days_since_last_event', z='value', 
                               title='Retention Rate Trend Over Time',
                               labels={'days_since_first_visit': '가입 기간(일)', 'days_since_last_event': '마지막 접속 후 경과 일수(일)', 'value': 'Count'},
                               color_continuous_scale='Blues')

# 페이지 설정
st.title("재방문(Retention) 지표")

# 차트 선택
metrics = [
    "Visit_Retention", "Visit_Purchase_Retention"
]
metric_selection = st.selectbox("시각화할 지표를 선택하세요", metrics)

# 차트 그리기
if metric_selection == "Visit_Retention":
    st.plotly_chart(fig1)
    st.plotly_chart(fig3)
    st.plotly_chart(fig_blues)
elif metric_selection == "Visit_Purchase_Retention":
    st.plotly_chart(fig2)
    st.plotly_chart(fig4)

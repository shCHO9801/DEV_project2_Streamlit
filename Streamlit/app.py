import streamlit as st
import pandas as pd
import os

# 현재 파일의 디렉토리 경로를 기준으로 상대 경로를 지정
file_path = os.path.join(os.path.dirname(__file__), 'user_new.csv')
file_path2 = os.path.join(os.path.dirname(__file__), 'daily.csv')

# CSV 파일 로드
user_df = pd.read_csv(file_path)
daily_df = pd.read_csv(file_path2)

# Streamlit 앱 설정
st.title("AARRR 프레임워크 대시보드")

# 앱 소개
st.write("""
    AARRR 프레임워크 대시보드에 오신 것을 환영합니다. 이 대시보드는 고객 생애 주기의 다양한 단계에서 주요 지표를 분석하는 데 도움을 줍니다.
    왼쪽의 탭을 사용하여 대시보드의 다양한 섹션으로 이동하세요.
    """)

# AARRR 프레임워크 설명 및 네비게이션 안내
st.write("""
    ## 네비게이션
    - **획득(Acquisition)**: 사용자 획득 관련 지표를 확인합니다.
    - **활성화(Activation)**: 사용자 활성화 관련 지표를 확인합니다.
    - **유지(Retention)**: 사용자 유지 관련 지표를 확인합니다.
    - **수익(Revenue)**: 사용자 수익 관련 지표를 확인합니다.
    """)

# 공통 지표 계산 함수
def calculate_aquisition_metrics(df):
    total_users = df['user_id'].nunique()
    new_users = df[df['first_visit'] >= '2023-01-01']['user_id'].nunique()  # 예시: 2023년 이후 신규 사용자
    return {
        "총 사용자 수": total_users,
        "신규 사용자 수 (2023)": new_users
    }

def calculate_activation_metrics(df):
    active_users = df[df['total_visit_cnt'] > 1]['user_id'].nunique()
    return {
        "활성 사용자 수": active_users
    }

def calculate_retention_metrics(df):
    retention_rate = df['30-Day Retention Rate (%)'].mean()
    return {
        "30일 유지율": retention_rate
    }

def calculate_revenue_metrics(df):
    total_revenue = df['total_spending'].sum()
    avg_revenue_per_user = df['total_spending'].mean()
    return {
        "총 수익": total_revenue,
        "사용자당 평균 수익": avg_revenue_per_user
    }

# 데이터 미리보기
st.write("### 데이터 미리보기")
st.write("#### 사용자 데이터")
st.dataframe(user_df.head())
st.write("#### 일별 데이터")
st.dataframe(daily_df.head())

# 공통 데이터 통계
st.write("### 기본 통계")
st.write("#### 사용자 데이터 통계")
st.write(user_df.describe())
st.write("#### 일별 데이터 통계")
st.write(daily_df.describe())

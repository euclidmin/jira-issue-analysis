import jira_analysis as ja


# Jira 분석 객체 생성
guide_robot = ja.JiraAnalysis()

# 정해진 서버 주소에 Login 까지 완료, 환경변수 LG_AD_ID, LG_AD_PW  로그인함
server = 'https://alm.lge.com/issue/'
jira = guide_robot.get_jira(server)

# Jira filter를 정해 주고 issues들 리턴해 줌
filter = 'project = SMARTROBOT AND cf[12914] = 설계평가1차'
issues = guide_robot.get_issues(jira, filter)

# Pandas DataFrame으로 변환
df = guide_robot.make_dataframe(issues)

# 그래프 그릴 준비, ex 폰트 설정
guide_robot.config_plot_font()

# dataFrame으로 저장된 issues들을 원하는 2 Dimentional Graph 그리는 것,
# guide_robot.draw_graph_assignee_count(df)

# guide_robot.draw_2D_x_y(df, x=guide_robot.ASSIGNEE, y=guide_robot.GRADE)
# guide_robot.draw_2D_x_y(df, x=guide_robot.ASSIGNEE)


guide_robot.draw_2D_x_y(df, x=ja.ASSIGNEE, y=ja.STATUS)


import math
import os
import platform
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from jira.client import JIRA
from matplotlib import font_manager, rc


class JiraAnalysis :
    #Constant
    KEY = 'Key'
    ASSIGNEE = 'assignee'
    STATUS = 'status'
    RESOLUTION = 'resolution'
    SUMMARY = 'summary'
    GRADE = 'grade'
    CREATED = 'created'
    UPDATED = 'updated'
    DUE_DATE = 'due date'
    TC_ID = 'TC ID'
    ISSUE_FIELD = [KEY, ASSIGNEE, STATUS, RESOLUTION, SUMMARY, GRADE, CREATED, UPDATED, DUE_DATE, TC_ID]

    def __init__(self):
        self._jira = None
        self.issues = None
        self.key_list = []
        self.summary_list = []
        self.assignee_list = []
        self.status_list = []
        self.resolution_list = []
        self.created_list = []
        self.updated_list = []
        self.issue_grade_list = []
        self.created_date_list = []
        self.tcid_list = []
        self.duedate_list = []
        self.date = datetime.now()

    def get_jira(self, server='https://alm.lge.com/issue/'):
        if self._jira == None :
            options = {'server':server, 'verify':False}
            self._jira = JIRA(options, basic_auth=(os.getenv('LGE_AD_ID'), os.getenv('LGE_AD_PW')))
        return self._jira

    def get_issues(self, jira=None,  filter='project = SMARTROBOT AND cf[12914] = 설계평가1차'):
        if jira != None :
            issues = jira.search_issues(filter, maxResults=1000)
            self.issues = issues
            print("total : {}".format(issues.total))
        else :
            print('you should make jira instance first by get_jira() func')
        return self.issues



    def make_dataframe(self, issues=None):
        def _append_issue(issues):
            df = pd.DataFrame(columns=JiraAnalysis.ISSUE_FIELD)
            for issue in issues :
                df = df.append(
                    {'Key':issue.key,
                     'assignee':str(issue.fields.assignee),
                     'status':issue.fields.status.name,
                     'resolution':str(issue.fields.resolution),
                     'summary':issue.fields.summary,
                     'created':datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z'),
                     'updated':datetime.strptime(issue.fields.updated, '%Y-%m-%dT%H:%M:%S.%f%z'),
                     'due date':issue.fields.duedate,
                     'TC ID':issue.fields.customfield_12922,
                     'grade':str(issue.fields.customfield_12905)
                     },
                    ignore_index=True
                )
            # print(df)
            return df

        def _append_issue_array(issues) :
            issues__ = []
            for issue in issues :
                issue_data_ = [
                    issue.key,
                    str(issue.fields.assignee),
                    issue.fields.status.name,
                    str(issue.fields.resolution),
                    issue.fields.summary,
                    issue.fields.customfield_12905,
                    datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z'),
                    datetime.strptime(issue.fields.updated, '%Y-%m-%dT%H:%M:%S.%f%z'),
                    issue.fields.duedate,
                    str(issue.fields.customfield_12922)
                ]
                issues__.append(issue_data_)

            df = pd.DataFrame(issues__, columns=JiraAnalysis.ISSUE_FIELD)
            return df

        new_df = None
        if issues :
            # DataFrame.append is too slow. it elapsed almost about 2seconds
            # self.print_timestamp()
            # new_df = _append_issue(issues)
            # self.print_timestamp()
            # At first making array and then making DataFrame instance. it takes only 20 milli-seconds.
            new_df = _append_issue_array(issues)
            # self.print_timestamp()

        else :
            print('check that issues object is None ')

        return new_df



    def config_plot_font(self):
        if platform.system() == 'Darwin':
            rc('font', family='AppleGothic')
            plt.rcParams['axes.unicode_minus'] = False
        elif platform.system() == 'Windows':
            path = "c:\Windows\Fonts\malgun.ttf"
            font_name = font_manager.FontProperties(fname=path).get_name()
            rc('font', family=font_name)
        elif platform.system() == 'Linux':
            rc('font', family='NanumBarunGothic')
        else:
            print("Error...")

    def draw_graph_assignee_count(self, df):
        print(df['assignee'])
        print(df['assignee'].value_counts())
        assignee_count = df['assignee'].value_counts()
        print(type(assignee_count))
        assignee_count.plot.bar()
        plt.show()

    def draw_2D_x_y(self, df, x=None, y=None):
        def _draw_sub_plot(pv):
            print('_draw_sub_plot')
            plot_num = pv.shape[1]      #shape tuple(x, y)
            subplot_num = int(math.sqrt(plot_num) // 1)
            for i in range(1, plot_num+1) :
                plt.subplot(subplot_num+1, subplot_num, i)
                # plt.plot(pv.axes[0], pv[pv.columns[i-1]])
                plt.bar(pv.axes[0], pv[pv.columns[i-1]])
                # plt.xlabel(pv.index)
                # plt.ylable(pv.columns[i-1])
            plt.show()

        # ex) x='assignee', y='status'
        if x not in JiraAnalysis.ISSUE_FIELD :
            print('check that x is not in issue_field')
        # if y not in self.ISSUE_FIELD :
        #     print('check that y is not in issue_field')

        # jira_pivot = df.pivot_table(index=x, values=self.KEY , aggfunc = 'count', fill_value = 0)
        jira_pivot = df.pivot_table(index=x, columns=y, values='Key' , aggfunc = 'count', fill_value = 0)
        # print(jira_pivot)

        if y == None :
            jira_pivot.plot.bar()
            plt.show()
        else :
            _draw_sub_plot(jira_pivot)

    def print_timestamp(self):
        print(datetime.now())


def main():
    print('jira_issue_analysis')

    # Jira 분석 객체 생성
    guide_robot_analysis = JiraAnalysis()

    # 정해진 서버 주소에 Login 까지 완료, 환경변수 LG_AD_ID, LG_AD_PW  로그인함
    server = 'https://alm.lge.com/issue/'
    jira = guide_robot_analysis.get_jira(server)

    # Jira filter를 정해 주고 issues들 리턴해 줌
    filter = 'project = SMARTROBOT AND cf[12914] = 설계평가1차'
    issues = guide_robot_analysis.get_issues(jira, filter)

    # Pandas DataFrame으로 변환
    df = guide_robot_analysis.make_dataframe(issues)

    # 그래프 그릴 준비, ex 폰트 설정
    guide_robot_analysis.config_plot_font()

    # dataFrame으로 저장된 issues들을 원하는 2 Dimentional Graph 그리는 것,
    # guide_robot_analysis.draw_graph_assignee_count(df)

    # guide_robot_analysis.draw_2D_x_y(df, x=guide_robot_analysis.ASSIGNEE, y=guide_robot_analysis.GRADE)
    # guide_robot_analysis.draw_2D_x_y(df, x=guide_robot_analysis.ASSIGNEE)
    guide_robot_analysis.draw_2D_x_y(df, x=JiraAnalysis.ASSIGNEE, y=JiraAnalysis.STATUS)




if __name__ == '__main__' :
    main()
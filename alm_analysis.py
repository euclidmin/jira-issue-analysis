import jira.client
from jira.client import JIRA
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
import platform
from matplotlib import font_manager, rc



class JiraAnalysis :

    def __init__(self):
        self._jira = None
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
            print("total : " + issues.total)
        else :
            print('you should make jira instance first by get_jira() func')

    def make_dataframe(self, issues=None):
        def _append_issue(df, issues):
            for issue in issues :
                df = df.append(
                    {'Key':issue.key,
                     'assignee':issue.fields.assignee,
                     'status':issue.fields.status.name,
                     'resolution':issue.fields.resolution,
                     'summary':issue.fields.summary,
                     'created':datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z'),
                     'updated':datetime.strptime(issue.fields.updated, '%Y-%m-%dT%H:%M:%S.%f%z'),
                     'due date':issue.fields.duedate,
                     'TC ID':issue.fields.customfield_12922,
                     'grade':issue.fields.customfield_12905
                     },
                    ignore_index=True
                )

        if issues :
            df = pd.DataFrame(columns=['Key', 'assignee', 'status', 'resolution', 'summary', 'grade', 'created', 'updated', 'due date', 'TC ID'])
            _append_issue(df, issues)
        else :
            print('check that issues object is None ')
        return df

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









def main():
    print('jira_issue_analysis')

    guide_robot_analysis = JiraAnalysis()
    jira = guide_robot_analysis.get_jira()
    issues = guide_robot_analysis.get_issues(jira)
    guide_robot_analysis.make_dataframe(issues)

    guide_robot_analysis.config_plot_font()




if __name__ == '__main__' :
    main()







#    datetime.strptime(str(issue.fields.duedate), "%Y-%m-%d")
    
# for issue in issue_in_test:
#     key_list.append(issue.key)
#     status_list.append(issue.fields.status.name)
#     assignee_list.append(str(issue.fields.assignee))
#     summary_list.append(issue.fields.summary)
#     resolution_list.append(str(issue.fields.resolution))
#     created_list.append(datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z')) # type : 2018-12-11T09:31:12.000+0900
#     updated_list.append(datetime.strptime(issue.fields.updated, '%Y-%m-%dT%H:%M:%S.%f%z')) # type : 2018-12-11T09:31:12.000+0900
#     issue_grade_list.append(str(issue.fields.customfield_12905))
#     tcid_list.append(str(issue.fields.customfield_12922))
#     duedate_list.append(issue.fields.duedate)     # type : 2018-12-20 '%Y-%m-%d'
#
# import pandas as pd
#
# df = pd.DataFrame({'Key':key_list, 'assignee':assignee_list, 'status':status_list , 'resolution':resolution_list , 'summary':summary_list,
#                   'grade':issue_grade_list, 'created':created_list, 'updated':updated_list, 'due date':duedate_list, 'TC ID':tcid_list})

import matplotlib.pyplot as plt
#한글 폰트 설정
import numpy as np
# %matplotlib inline




# 담당자 별 issue 수
print("담당자 별 issue 수")
df['assignee'].value_counts().plot(kind='bar')

plt.show()
# 담당자 별 issue 수
print("담당자 별 issue 수")

df['assignee'].value_counts()

df['status'].value_counts()
#pd.crosstab(df.status, df.grade , margins=True).plot(kind='bar', stacked=True)

pd.crosstab(df.status, df.grade , margins=True)
#pd.crosstab(df.assignee, df.status, margins=True).plot(kind='bar', stacked=True)

pd.crosstab(df.assignee, df.status, margins=True)
open_issue = df.loc[df['status'] == 'Open']

open_issue

open_issue['assignee'].value_counts().plot(kind='bar')

open_issue['assignee'].value_counts()


open_issue.loc[open_issue['assignee'] == '고성훈 seonghoon.ko']
#inprogress_issue

inprogress_issue = df.loc[df['status'] == 'In Progress']

inprogress_issue['assignee'].value_counts()

inprogress_issue['assignee'].value_counts().plot(kind='bar')
#reopen_issue

reopen_issue = df.loc[df['status'] == 'Reopened']
#resolved_issue

resolved_issue = df.loc[df['status'] == 'Resolved']
#fixed_issue

#fixed_issue['assignee'].value_counts()

fixed_issue = df.loc[df['resolution'] == 'Fixed']
#df.loc[df['priority'] == 'P1']


# cell structure
#  - https://jira.readthedocs.io/en/master/jirashell.html
# 
# In [2]: issue.
# issue.delete  issue.fields  issue.id      issue.raw     issue.update
# issue.expand  issue.find    issue.key     issue.self
# 
# In [2]: issue.fields.
# issue.fields.aggregateprogress              issue.fields.customfield_11531
# issue.fields.aggregatetimeestimate          issue.fields.customfield_11631
# issue.fields.aggregatetimeoriginalestimate  issue.fields.customfield_11930
# issue.fields.aggregatetimespent             issue.fields.customfield_12130
# issue.fields.assignee                       issue.fields.customfield_12131
# issue.fields.attachment                     issue.fields.description
# issue.fields.comment                        issue.fields.environment
# issue.fields.components                     issue.fields.fixVersions
# issue.fields.created                        issue.fields.issuelinks
# issue.fields.customfield_10150              issue.fields.issuetype
# issue.fields.customfield_10160              issue.fields.labels
# issue.fields.customfield_10161              issue.fields.mro
# issue.fields.customfield_10180              issue.fields.progress
# issue.fields.customfield_10230              issue.fields.project
# issue.fields.customfield_10575              issue.fields.reporter
# issue.fields.customfield_10610              issue.fields.resolution
# issue.fields.customfield_10650              issue.fields.resolutiondate
# issue.fields.customfield_10651              issue.fields.status
# issue.fields.customfield_10680              issue.fields.subtasks
# issue.fields.customfield_10723              issue.fields.summary
# issue.fields.customfield_11130              issue.fields.timeestimate
# issue.fields.customfield_11230              issue.fields.timeoriginalestimate
# issue.fields.customfield_11431              issue.fields.timespent
# issue.fields.customfield_11433              issue.fields.updated
# issue.fields.customfield_11434              issue.fields.versions
# issue.fields.customfield_11435              issue.fields.votes
# issue.fields.customfield_11436              issue.fields.watches
# issue.fields.customfield_11437              issue.fields.workratio

df['grade'].value_counts()
# | (df['resolution'] == 'Opened')
#fixed_issue = df.loc[df['resolution'] == 'Fixed']
# Closed  In Progress  Open  Reopened  Resolved  All
#on_going_issue

#by_assignee = pd.DataFrame(on_going_issue[(on_going_issue['status'] == 'Open')]['assignee'].value_counts().to_frame(name='Open')) 
#by_assignee = by_assignee.append(on_going_issue[(on_going_issue['status'] == 'In Progress')]['assignee'].value_counts().to_frame(name='In Progress'), sort=True )
#by_assignee = by_assignee.append(on_going_issue[(on_going_issue['status'] == 'Reopened')]['assignee'].value_counts().to_frame(name='Reopened'), sort=True )

on_going_issue = df[(df['status'] == 'Open') | (df['status'] == 'Reopened') | (df['status'] == 'In Progress') ]
by_assignee = pd.DataFrame({'Open':on_going_issue[(on_going_issue['status'] == 'Open')]['assignee'].value_counts(),
                           'In Progress':on_going_issue[(on_going_issue['status'] == 'In Progress')]['assignee'].value_counts(),
                           'Reopened':on_going_issue[(on_going_issue['status'] == 'Reopened')]['assignee'].value_counts()})
by_assignee = by_assignee.groupby(by_assignee.index).sum()
by_assignee['total'] = by_assignee.sum(axis=1)
by_assignee = by_assignee.astype(int)
by_assignee.sort_values(by=['total'], ascending=False)[['In Progress', 'Open', 'Reopened']].plot(kind='bar', stacked=True)

#by_assignee

print(by_assignee)
#datetime.strptime(on_going_issue['due date'], '%Y-%m-%d')

#print (due)
#if due.empty:
#    elapsed = ""
#else:
#    date = datetime.strptime(str(due), '%Y-%m-%d')
#    print(date)
#    elapsed = date - datetime.now()
        
#on_going_issue['due date']
#on_going_issue

#date_str = '2019-01-04'

#date = datetime.strptime(str(date_str), '%Y-%m-%d')
#print(date)
#print(datetime.today())
#elapsed = datetime.now() - date
#print(elapsed.days)

#print((datetime.now() - datetime.strptime(str(date_str), '%Y-%m-%d')).days)

on_going_issue[['Key', 'assignee', 'due date']]

#datetime.strptime(str(on_going_issue['due date'].values), '%Y-%m-%d')

on_going_issue[overdue] = (datetime.now() - datetime.strptime(str(on_going_issue['due date'].values), '%Y-%m-%d')).days

#print (due)
#if due.empty:
#    elapsed = ""
#else:
#    date = datetime.strptime(str(due), '%Y-%m-%d')
#    print(date)

type(on_going_issue['due date'])
#    elapsed = date - datetime.now()


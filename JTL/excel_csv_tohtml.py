import os
import pandas as pd
import argparse
import sys
import datetime
from commands import getoutput as cmd
#from utils import dtb_connection as db
#from utils.common import Commons
class html_context(object):
  def __init__(self):
    self.components = []
  def start(self):
      #p { font-family: helvetica; font-size: 10pt}
      return """<!DOCTYPE html>
          <head>
           <style>
            h4 { font-family: consolas; }
            p { font-family: helvetica; font-size: 10pt}
            table, th, td
            {
              border: 1px solid black;
              border-collapse: collapse;
              font-family: verdana;
              font-size: 8pt;
            }
            th, td
            {
              padding: 5px;
              text-align: center;
            }
           </style>
          </head>
          <body>\n"""
  def end(self):
    return '</body></html>\n'
  def add_component(self, component):
    self.components.append(component)
  def html(self):
    return '{0}{1}{2}'.format(self.start(), ''.join(self.components), self.end())
class mailer(object):
  
  def __init__(self, subject, recipients, sender, message):
    self.body        = MIMEText(message, 'html')
    self.body['Subject']  = subject
    if not isinstance(recipients, list):
      recipients = [recipients]
    self.recipients     = recipients
    self.body['To']     = ",".join(recipients)
    self.sender       = sender
    self.body['From']    = self.sender
#    self.body['Cc']     = 'humam.ahmad@pimco.com'
  def __enter__(self):
    #self.client = smtplib.SMTP('rpc-lb.pimco.imswest.sscims.com')
    self.client = smtplib.SMTP('mail')
    return self
    
  def send(self):
    ##logger.info('Sending mail to => ' + ''.join(['[' + self.recipients[i] + '], ' if i != (len(self.recipients) - 1) else '[' + self.recipients[i] + ']' for i in range(len(self.recipients))]))
    self.client.sendmail(self.sender, self.recipients, self.body.as_string())
  def __exit__(self, *args):
    self.client.quit()
    
    
def argument_parser(args):
  #logger.info(args)
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description = 'process to verify risk measures') 
  parser.add_argument('-jtl-path','--jtl_path',dest='jtl_path',help='jtl path for which calculation has to be done',required=True)
  parser.add_argument('-seperator','--seperator',dest='seperator',help='enter the file seperator',default = ';')
  parser.add_argument('-project','--project',dest = 'project',help='Project name for which the report is to be created.',required=True)  
  parser.add_argument('-columns', '--cols',dest='columns',help='File containing how the data is in jtl_path', required=True)
  options=parser.parse_args()
  #print 'Options', options
  return options
  
def add_data(name,value):
  return """<p style="font-family:consolas; font-size: 12pt">
          <b>{0}</b> : {1}
          <br></br>
        """.format(name,value)
  
def add_notes(message):
#<br>Input meta data was obtained from the file <b>{0}</b>
  return """<p style="font-family:consolas; font-size: 12pt">
          <b>{0}</b>
          <br></br>
        """.format(message)
        
def add_heading(heading):
#<br>Input meta data was obtained from the file <b>{0}</b>
  return """<p style="font-family:consolas; font-size: 12pt">
          <h1><u>{0}</u></h1>
        """.format(heading)
        
def add_table(df,header):
    """"
    This function post process data frame and convert into html string
    :param df : pandas data frame containing data
  
    returns html object
    """
    #html = '<h3> {0} <h3>'.format(header)
    #df.index = df.index + 1
    html = df.to_html(index = False).replace('<th>','<th nowrap bgcolor="#b8b1d2"><font size="2" face="Tahoma">').replace('<table border="1" class="dataframe">','<table cellpadding="5" cellspacing="0" border="1" id="collapsedBorder">')
    #html += '<br>'
    return html
    
    
'''def add_report_link(path):
  path = aux.dos_link(path)
  if '\\thome' in path:
    #logger.info('Replacing path')
    path = path.replace('\\thome','',1)
    path = path.replace('\\thome','',1)
  return """<p><a href="{0}">[To view the report in browser click here]</a></p>""".format(path)
'''    
def time_conversion(series):
  for i in range(len(series)):
    if type(series[i]) == type('string'):
      if '.' in series[i]:
        j = ''.join(series[i].split('.')[:-1])
      elif ' ' in series[i]:
        k = series[i].split(' ')
        if k[-1] == 'PM':
          l = (''.join(k[:-1]).split(':'))
          j = int(l[0])+12
          if j>=24:
             j-=24
          j = str(j)+':'+':'.join(l[1:])
      else:
        j = series[i]
    else:
      j = datetime.datetime.utcfromtimestamp(int(series[i])/1000).strftime('%H:%M:%S')
    series[i] = datetime.datetime.strptime(j, '%H:%M:%S').time()
    j = ''.join(str(series[len(series)-1]).split('.')[:-1])
  return series


def create_df(csv_path,sept,cols):
  with open(cols, 'r') as f:
    row = f.read()
    columns = row.split(',')
    columns[-1] = columns[-1].split('\n')[0]

  if ',' in csv_path:
    path = csv_path.split(',')
    for index in range(len(path)):
      if path[index].split('.')[-1] == 'xlsx':
        read_xl = pd.read_excel(path[index])
        read_xl.columns = columns[:len(read_xl.columns)]
        read_xl.to_csv(''.join(path[index].split('.')[:-1])+'.csv', index=False, header=False)
        path[index] = ''.join(path[index].split('.')[:-1])+'.csv'
    #columns = ['timeStamp','elapsed','label','Response Code','Response Message','threadName','success','failureMessage','bytes','sentBytes','grpThreads','allThreads','Latency','SampleCount','ErrorCount','Hostname','IdleTime','Connect']
    frames = []

    for file in path:
       #logger.info('Reading csv {0}'.format(file))
       frames.append(pd.read_csv(file, sep=sept ,engine ='python', names=columns))
    #logger.info('Creating final dataframe')
    df = pd.concat(frames)
    df.columns = columns

  else:
    if csv_path.split('.')[-1] == 'xlsx':
      read_xl = pd.read_excel(csv_path)
      read_xl.columns = columns[:len(read_xl.columns)]
      read_xl.to_csv('.'.join(csv_path.split('.')[:-1])+'.csv', index=False, header=False)
      csv_path = '.'.join(csv_path.split('.')[:-1])+'.csv'

    #logger.info('Reading csv {0}'.format(csv_path))
    #columns = ['timeStamp','elapsed','label','Response Code','Response Message','threadName','success','failureMessage','bytes','sentBytes','grpThreads','allThreads','Latency','SampleCount','ErrorCount','Hostname','IdleTime','Connect']
    df = pd.read_csv(csv_path, sep=sept, engine='python', names=columns)  
  #logger.info('Data Frame of shape [{0}] created'.format(df.shape))

  if 'timeStamp' in df:
    df['timeStamp'] = time_conversion(df['timeStamp'])

  if 'Response Code' in df:
    df['Response Code'] = df['Response Code'].astype(str)
    return df.sort_values(by=['Response Code'])

  return df

def unique_col_val(df,col_name):
  unique_vals = df[col_name].unique()
  #logger.info('Sorted unique values for column {0} are : \n {1}\n'.format(col_name,sorted(unique_vals)))
  return sorted(unique_vals)

def count_of_colum_values(df,col_name,against_col):
  df2 =df.groupby([col_name],as_index = False)
  count_col = df2.agg({against_col : ['size','min','max']})
  count_col.columns = [col_name,'Count','Start Time','End Time']
  #logger.info('The count for unique value of the column {0} is \n {1}\n'.format(col_name, count_col))
  return count_col.sort_values(by=['Count'],ascending = False)

def diff_times_in_seconds(min_time, max_time):
  # assumes max_time is after min_time
  h1, m1, s1 = min_time.hour, min_time.minute, min_time.second
  h2, m2, s2 = max_time.hour, max_time.minute, max_time.second
  min_time_secs = s1 + 60 * (m1 + 60*h1)
  max_time_secs = s2 + 60 * (m2 + 60*h2)
  return (max_time_secs - min_time_secs)

def calc_time_attrib(df):
  min_time = df['timeStamp'].min() 
  max_time = df['timeStamp'].max()
  #logger.info('Min time found in the column timeStamp is [{0}]'.format(min_time))
  #logger.info('Max time found in the column timeStamp is [{0}]'.format(max_time))
  #diff_times_in_seconds(min_time.time(), max_time.time()) max_time has to be given as a second parameter
  
  elapsed_time = diff_times_in_seconds(min_time, max_time)
  return min_time, max_time, elapsed_time
  
def calc_each_label_time(df, main_col, against_col):
  df_min_max = df.groupby(main_col)
  li = ['API name','Min. Time (secs)','Max. Time (secs)','Avg. Time (secs)','Count']

  if 'Response Code' in df:
    df_ok = df.loc[df['Response Code'] == '200'].groupby(main_col).agg({against_col : ['min','max','mean','size']}).reset_index()
    df_not_ok = df.loc[df['Response Code'] != '200'].groupby(main_col).agg({against_col : ['min','max','mean','size']}).reset_index()
 
  else:
    df_ok = df.groupby(main_col).agg({against_col : ['min', 'max', 'mean', 'size']}).reset_index()
    df_not_ok = df.groupby(main_col).agg({against_col : ['min','max','mean','size']}).reset_index()
 
  df_ok.columns = li
  df_ok['Min. Time (secs)'] = [round(float(i)/1000, 2) for i in df_ok['Min. Time (secs)']]
  df_ok['Max. Time (secs)'] = [round(float(i)/1000, 2) for i in df_ok['Max. Time (secs)']]
  df_ok['Avg. Time (secs)'] = [round(float(i)/1000, 2) for i in df_ok['Avg. Time (secs)']]

  df_not_ok.columns = li
  df_not_ok['Min. Time (secs)'] = [round(float(i)/1000, 2) for i in df_not_ok['Min. Time (secs)']]
  df_not_ok['Max. Time (secs)'] = [round(float(i)/1000, 2) for i in df_not_ok['Max. Time (secs)']]
  df_not_ok['Avg. Time (secs)'] = [round(float(i)/1000, 2) for i in df_not_ok['Avg. Time (secs)']]
  
  df_all = df_min_max.agg({against_col : ['min','max','mean','size']}).reset_index()
  df_all.columns = li
  df_all['Min. Time (secs)'] = [round(float(i)/1000, 2) for i in df_all['Min. Time (secs)']]
  df_all['Max. Time (secs)'] = [round(float(i)/1000, 2) for i in df_all['Max. Time (secs)']]
  df_all['Avg. Time (secs)'] = [round(float(i)/1000, 2) for i in df_all['Avg. Time (secs)']]
  ##logger.info('The values which have response_code as ok are \n{0}\n'.format(df_min_max.filter(lambda x: x['Response Code'] == 200)))
  #logger.info('The api attributes which have response_code as 200 are : \n{0}\n'.format(df_ok))
  #logger.info('The api attributes which do not have response_code as 200 are : \n{0}\n'.format(df_not_ok))
  #logger.info('The total api attributes are as under : \n{0}\n'.format(df_all))
  
  return df_ok.sort_values(by=li[4],ascending = False),df_all.sort_values(by=li[4],ascending = False)
  
  
def exec_start(jtl_path,seperator,pt_obj,columns):
  df = create_df(jtl_path,seperator,columns)

  if 'Response Code' in df.columns:
    pt_obj.responseCode_df = count_of_colum_values(df,'Response Code','timeStamp')

  if 'Response Message' in df.columns:
    pt_obj.responseMessage_df = count_of_colum_values(df,'Response Message','timeStamp') 

  if 'label' in df and 'elapsed' in df:
    pt_obj.attrib_ok_df, pt_obj.attrib_all_df = calc_each_label_time(df,'label','elapsed')

  pt_obj.total_min_time,pt_obj.total_max_time,pt_obj.total_time = calc_time_attrib(df)
  #logger.info('Elapsed time in seconds = [{0}]'.format(pt_obj.total_time))
  pt_obj.total_request_send = len(df.index)
  pt_obj.bandwidth = pt_obj.total_request_send/pt_obj.total_time
  #logger.info('No. of api running per sec = [{0}]'.format(pt_obj.bandwidth))
  return

class performance_test(object):
  def __init__(self):
    self.total_request_send = None
    self.total_min_time   = None
    self.total_max_time   = None
    self.total_time     = None
    self.bandwidth     = None
    self.responseCode_df  = None
    self.responseMessage_df = None
    self.attrib_ok_df    = None
    self.attrib_all_df   = None
  
def data_population(ctx,jtl_path,seperator,columns):
  
  pt_obj = performance_test()
  exec_start(jtl_path,seperator,pt_obj,columns)
  #ctx.add_component(add_notes(input_cfg_path))
  ctx.add_component(add_data('Total Request Sent',pt_obj.total_request_send))
  ctx.add_component(add_data('Suite Start Time(PST)',pt_obj.total_min_time))
  ctx.add_component(add_data('Suite End Time(PST)',pt_obj.total_max_time))
  ctx.add_component(add_data('Total Time Taken In Seconds',pt_obj.total_time))
  ctx.add_component(add_data('Bandwidth[total API/total time(sec)]',pt_obj.bandwidth))

  if type(pt_obj.responseCode_df) != type(None):
    ctx.add_component(add_notes('Response Code attributes'))
    ctx.add_component(add_table(pt_obj.responseCode_df,'Response Code'))

  if type(pt_obj.responseMessage_df) != type(None):
    ctx.add_component(add_notes('Response Message attributes'))
    ctx.add_component(add_table(pt_obj.responseMessage_df,'Response Message'))

  if type(pt_obj.attrib_ok_df) != type(None):
    ctx.add_component(add_notes('Attributes when Response Code is 200 '))
    ctx.add_component(add_table(pt_obj.attrib_ok_df,'Response Code = 200'))

  if type(pt_obj.attrib_all_df) != type(None):
    ctx.add_component(add_notes('Attributes for all API '))
    ctx.add_component(add_table(pt_obj.attrib_all_df,'All api'))
  
  
  
def mail(jtl_path,seperator,project,columns):
  ctx = html_context()
  ctx.add_component(add_heading('Performance Test Report'))
  ctx.add_component(add_notes('Project : {0}'.format(project)))
  data_population(ctx,jtl_path,seperator,columns)
  file_name = jtl_path.split('/')[-1].split('.')[0]
  doc = datetime.datetime.now() #doc ==> date of creation
  append_name = file_name+'_'+str(doc.year)+'_'+str(doc.month)+'_'+str(doc.day)+'_'+str(doc.hour)+'_'+str(doc.minute)+'_'+str(doc.second)
  #ctx.add_component(add_legend())
  #price_date = datetime.date.today()
  #ctx.add_component(add_report_link(report, price_date))
  #recipients = aux.get_mail_ids(mail_id).split(',')
  cycle_date = '22/01/2019'
  #with mailer('[{0}] [{1}] Pars {2} Comparison Report'.format(os.environ['ENV_BASE'], price_date, config.__getattr__('_{0}'.format(risk_measure_group)).report_title), recipients, 'CC{0}Alerts@pimco.com'.format(os.environ['ENV_BASE']), ctx.html()) as mail:
  #mail_path = '/home/ab.srivastava/op_fe-performance_report_{1}_{2}.html'.format(os.environ['ENV_BASE'],cycle_date.replace('/','_'),os.getpid())
  mail_path = '/home/ar.rana/Desktop/Work/Output/op_fe-performance_report_{1}.html'.format('os.environ["ENV_BASE"]',append_name)

  #ctx.add_component(add_report_link(mail_path))
  #with mailer('[{0}] [{1}] {2} Performance Test Report'.format(os.environ['ENV_BASE'],cycle_date,project), recipients, 'CC{0}Alerts@pimco.com'.format(os.environ['ENV_BASE']), ctx.html()) as mail:
  #  mail.send()           
  
  with open(mail_path,'w') as reporting_file:
     reporting_file.write(ctx.html())
  #logger.info("Mail file html saved to location {0}".format(mail_path))
  
def main(args):
  options = argument_parser(args)
  mail(options.jtl_path,options.seperator,options.project,options.columns)
  
    
if __name__== '__main__':
  main(sys.argv[1:])

#BSNAP_LogProcessor.py


import os,sys
import glob
import time,datetime
import string
import socket 
from ftplib import FTP


#Elements define
g_femtoList = ('LOG-BSNAP-300B2015060011',
               'LOG-BSNAP-300B2015060023',
			   'LOG-BSNAP-300B2015060024',
			   'LOG-BSNAP-300B2015060026',
			   'LOG-BSNAP-300B2015060030',
			   'LOG-BSNAP-300B2015060033',
			   'LOG-BSNAP-300B2015060035',
			   'LOG-BSNAP-300B2015060036',
			   'LOG-BSNAP-300B2015060047')

g_femto2Name = {'LOG-BSNAP-300B2015060011':'SongXinling',
                'LOG-BSNAP-300B2015060023':'PeiGuangtao',
				'LOG-BSNAP-300B2015060024':'ShangDan',
				'LOG-BSNAP-300B2015060026':'WangCong',
				'LOG-BSNAP-300B2015060030':'GaoZhongyou',
				'LOG-BSNAP-300B2015060033':'LiLongfang',
				'LOG-BSNAP-300B2015060035':'WangJinling',
				'LOG-BSNAP-300B2015060036':'HeJie',
				'LOG-BSNAP-300B2015060047':'Lining'}
				
g_filePrefix = ('monlog','cfglog','tracelog','cfgcfg')

g_keyWord = ('reboot','fail','failed! ','abnormal','abnormal!','reset','error','timeout')

g_logDiretory = 'D:/boomsense/BSNAP LOG/'
g_WorkDiretory = 'D:/boomsense/log/'


#txtfile = glob.glob(g_logDiretory+r'/*.txt')
#gzfile = glob.glob(g_logDiretory+r'/*.tar.gz')

currentTime = str(time.localtime().tm_year) + str(time.localtime().tm_mon) + str(time.localtime().tm_mday) + str(time.localtime().tm_hour) + str(time.localtime().tm_min) + str(time.localtime().tm_sec) 
currentDate = str(time.localtime().tm_year) + str(time.localtime().tm_mon) + str(time.localtime().tm_mday)
#print currentTime,currentDate

def debug_print(s):  
	print s 

class LOGPARSER:  
    def __init__(self,logsummarydir, sourcelogdir,keyword,day2filter = 1):  
        self.sourcelogdir  = sourcelogdir
        self.logsummarydir = logsummarydir
        self.keyword = keyword
        self.femtoList = g_femtoList
        self.femto2Name = g_femto2Name
        self.day2filter = day2filter
        
    def __del__(self):  
        pass

#Log Parsing
    def txt_parse(self, txtfile,femtoelement):
		datenow  = time.strftime('%Y%m%d%H%M%S', time.localtime())
		parsefromtime = time.time() - (time.time()%86400) - 24*60*60*self.day2filter + time.timezone
		#linetmstamp = 0
		print datenow
		for logfile in txtfile:
			if os.path.exists(logfile):
			
				#if none == file_filter(logfile):
				#	pass
				#else:
					#
				with open(logfile,'r') as log4Parse:
					with open(self.logsummarydir+'logsummary_'+datenow+'.txt','a') as logsummary:
						logsummary.writelines('\n\n'+femtoelement+'  '+self.femto2Name[femtoelement]+'\n')
						logsummary.writelines('Parsed from '+logfile+':\n')
						for line in log4Parse:
							#print line[0:3]
							if '[201' == line[0:4]:
								linetime =time.strptime(line[1:20],'%Y-%m-%d %H:%M:%S')
								linetmstamp = time.mktime(linetime)
								#print linetime
								if linetmstamp < parsefromtime:
									#print time.ctime(linetmstamp),linetmstamp, time.ctime(parsefromtime), 'pass'
									pass
								else:
									#print time.ctime(linetmstamp),linetmstamp, time.ctime(parsefromtime), 'catch'
									for word in self.keyword:
										if word in line.split():
											#print line.strip()					
											logsummary.write(line)			
										else:
											pass
							elif '2015' == line[0:4]:
								linetime =time.strptime(line[0:19],'%Y-%m-%d %H:%M:%S')
								linetmstamp = time.mktime(linetime)
								#print linetime				
								
								if linetmstamp < parsefromtime:
									pass
								else:
									for word in self.keyword:
										if word in line.split():
											#print line.strip()					
											logsummary.write(line)			
										else:
											pass
							else:
								print 'fuck'
								pass
				#except:
					#logstr = u"%s Log file %s parsed fail!\n" %datenow, os.path.basename(logfile)
					#debug_print(logstr)
				#	pass
			else:
				pass

#Log file filter
    def file_filter(self, file2filter):
        file_modification_time=os.stat(file2filter).st_mtime
        now=time.time()		
        midnight = time.time() - (time.time()%86400) - 24*60*60*self.day2filter + time.timezone
        if file_modification_time < midnight:
			return none
        else:
			return file2filter
		
#Tar Log Extraction
    def tarlog_extract(self, tarfile,objectDirectory):
	#TODO
		pass
		
				
if __name__ == '__main__':  
    timenow  = time.localtime()  
    datenow  = time.strftime('%Y-%m-%d %H:%M:%S', timenow)  
    day2filter = 10
    for femtoelement in g_femtoList:
        if os.path.exists(g_logDiretory+femtoelement):
			#print u'file normal'
			txtfile = glob.glob(g_logDiretory+femtoelement+'/*.txt')
			#print txtfile
			try:
				logparse = LOGPARSER(g_WorkDiretory,g_logDiretory,g_keyWord,day2filter)				
				logparse.txt_parse(txtfile,femtoelement)
				
				logstr = u"%s Log files parsed successfully \n" %datenow  
				debug_print(logstr) 
			except:
				logstr = u"%s Log file parsed fail!\n" %datenow
				debug_print(logstr)
    	

# -*- coding: utf-8 -*-
#BSNAP_LogProcessor.py


import os,sys
import re
import time,datetime
import string
import socket 
import logging
from ftplib import FTP


#Elements Dicrtionary
g_femto2Name = {'LOG-BSNAP-300B2015060011':'SongXinling',
                'LOG-BSNAP-300B2015060023':'PeiGuangtao',
				'LOG-BSNAP-300B2015060024':'ShangDan',
				'LOG-BSNAP-300B2015060026':'WangCong',
				'LOG-BSNAP-300B2015060030':'GaoZhongyou',
				'LOG-BSNAP-300B2015060033':'LiLongfang',
				'LOG-BSNAP-300B2015060035':'WangJinling',
				'LOG-BSNAP-300B2015060036':'HeJie',
				'LOG-BSNAP-300B2015060047':'Lining'}

#Log filename list				
g_filePrefix = ('monlog','cfglog','tracelog','cfgcfg')
#Log file extended list
g_fileExtend = ('txt','log')

#keyword to search
g_keyWord = ('reboot','fail','abnormal','reset','error','timeout','warn')

#Directory
g_logDiretory = 'D:/boomsense/BSNAP LOG'
#g_logDiretory = 'D:/30 workspace/log'
g_WorkDiretory = 'D:/30 workspace/code'

#Run log basic parameters
logger=logging.getLogger()
handler=logging.StreamHandler()
logger.addHandler(handler)
formatter = logging.Formatter('[%(asctime)s] %(funcName)10s [%(levelname)8s]: %(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)

class LOGPARSER:  
    def __init__(self,logsummarydir, sourcelogdir,keyword,day2filter = 1):  
        self.sourcelogdir  = sourcelogdir
        self.logsummarydir = logsummarydir
        self.keyword = keyword
        self.femto2Name = g_femto2Name
        self.femtoList = g_femto2Name.keys()        
        self.day2filter = day2filter
        
    def __del__(self):  
        pass

#Log Parsing
    def txt_parse(self, txtfile):		
		datenow  = time.strftime('%Y%m%d%H%M%S', time.localtime())
		parsefromtime = time.time() - (time.time()%86400) - 24*60*60*(self.day2filter-2) + time.timezone		
		linetmstamp = 0		
		with open(self.logsummarydir+'logsummary_'+datenow+'.txt','a') as logsummary:			
			logging.info('callled at %s',datenow)
			for logfile in txtfile:
				logfiledir = os.path.split(logfile)[0]
				femtologdir = logfiledir.split('\\')[-1]				
				if os.path.exists(logfile):	
					with open(logfile,'r') as log4Parse:
							try:
								logsummary.writelines('\n\n'+logfiledir.split('\\')[-1]+'  '+self.femto2Name[femtologdir]+'\n')
							except:					
								logsummary.writelines('\n\n'+logfiledir+'\n')
								
							logsummary.writelines('Parsed from '+logfile+':\n')
							for line in log4Parse:								
								logging.debug(line[0:3])
								if '[201' == line[0:4]:
									linetime =time.strptime(line[1:20],'%Y-%m-%d %H:%M:%S')
									linetmstamp = time.mktime(linetime)									
								elif '2015' == line[0:4]:
									linetime =time.strptime(line[0:19],'%Y-%m-%d %H:%M:%S')
									linetmstamp = time.mktime(linetime)									
								elif '[19' == line[0:3] or '197' == line[0:3]:									
									linetmstamp = parsefromtime
								else:
									pass
								
								
								if linetmstamp < parsefromtime:									
									pass
								else:									
									logging.debug(line.strip())								
									is_line_wroted = False
									for word in self.keyword:											
											to_match = re.search(word,line,re.IGNORECASE)
											logging.debug(type(to_match))
											if (None != to_match) and (False == is_line_wroted):												
												logging.debug(line.strip())
												logsummary.write(to_match.string)
												is_line_wroted  = True	
											else:
												pass											
								
					#except:						
					#	logger.error('Log file %s parsed fail!',os.path.basename(logfile))				
					
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
		
# get 	filelist

    def get_filelist(self,baseDirectory, filetype):
        basepath = ''
        dirlist = []
        allfilelist = []
        typefilelist = []
        for dirpath, dirlist, allfilelist in os.walk(baseDirectory):
			 for filename in allfilelist:
				for ext in filetype:
					if os.path.splitext(filename)[1] == '.'+ext:
					   filepath = os.path.join(dirpath, filename)
					   typefilelist.append(filepath)
        return typefilelist
	
		
if __name__ == '__main__':  
    #timenow  = time.localtime()  
    #datenow  = time.strftime('%Y-%m-%d %H:%M:%S', timenow)  
    day2filter = 4    
    if os.path.exists(g_logDiretory):		
		try:
			logparse = LOGPARSER(g_WorkDiretory,g_logDiretory,g_keyWord,day2filter)	
			logfile = logparse.get_filelist(g_logDiretory,g_fileExtend)
			logparse.txt_parse(logfile)
			
			logging.critical('Log file parsed success!')
		
		except:		
			logging.critical('Log file parsed fail!')
#end of file

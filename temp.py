switch = True if row[0]>1 else False
		for position in range(1,data.shape[0]):
			if switch and row[position]>0:
				before = position
				switch = True
			if switch and row[position]==0:
				switch = False
			if switch==False and before>0 and row[position]==0:
				continue
		position = 0
		switch = True if row[::-1][0]>1 else False
		for position in range(1,data.shape[0]):
			row = row[::-1]
			if switch and row[position]>0:
				after = position
				switch = True
			if switch and row[position]==0:
				switch = False
			if switch==False and after>0 and row[position]==0:
				after = data.shape[0]-after
				continue
				
				
				
				


switch = True if row[0]>1 else False

		for position in range(1,len(row)):
			if switch and row[position]>0:
				before = position
				switch = True
			if switch and row[position]==0:
				switch = False
			if switch==False and before>0 and row[position]==0:
				break
			if switch==False and row[position]>0:
				switch=True
		position = 0
		switch = True if row[::-1][0]>1 else False
		row = row[::-1]
		for position in range(1,len(row)):
			
			if switch and row[position]>0:
				after = position
				switch = True
			if switch and row[position]==0:
				switch = False
			if switch==False and after>0 and row[position]==0:
				after = data.shape[1]-after
				break
			if switch==False and row[position]>0:
				switch=True
				
				
				
				
				
				
				
				
				
				
has_points={}
	flag,flagp,start,stop=False,False,0,0
	flag = True if data[0][0]>2 else False
	flagp = flag
	for i in range(data.shape[0]):
		for position in range(data[i]):
			if flag!=True and flagp!=True and i[position]>2:
				flag = True
			elif flag==True and flagp!=True and 

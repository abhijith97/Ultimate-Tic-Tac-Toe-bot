import sys
import random
import signal
import time
import copy

#ORIGINAL

class Player44:
	def __init__(self):
		self.optimalMove = []
		self.winnable_x = 0
		self.winnable_o = 0
		self.Bval = 16.0
		self.bval = 4.0

	def move(self, board, old_move, flag):
		self.optimalMove = []
		TIME = 14
		signal.signal(signal.SIGALRM, handler)
		moved = False
		maxDepth = 10000
		moveStore = []
		signal.alarm(TIME)
		for maxD in xrange(1,maxDepth+1):
			try:
				self.minimax(board, 0, maxD, old_move, flag, -1000000, 1000000)
				moveStore.append(self.optimalMove)
			except TimedOutExc:
				moved = True
				print len(moveStore)
				if(len(moveStore) == 0):
					cells = board.find_valid_move_cells(old_move)
					return cells[random.randrange(len(cells))]
				print self.optimalMove
				return moveStore[-1]

		if(moved == False):
			print len(moveStore)
			if(len(moveStore) == 0):
				cells = board.find_valid_move_cells(old_move)
				return cells[random.randrange(len(cells))]
			print self.optimalMove
			return moveStore[-1]


	def calcConsecutiveHeur(self, bs, which, flag, old_move, whether):
		
		h=0
		cons3_x = 0
		cons3_o = 0
		cons2_x = 0
		cons2_o = 0
		if(which == 'B'):
			add_2consecutive = 2*self.Bval/3;
			add_3consecutive = 2*self.Bval;
			add_3consAndChance = 5*self.Bval/2;
			add_3consButBlocked = -self.Bval;
			add_2consAndChance = self.Bval;
			add_2condAndBlocked = -self.Bval/2;

		else:
			add_2consecutive = 2*self.bval/3;
			add_3consecutive = 2*self.bval;
			add_3consAndChance = 5*self.bval/2;
			add_3consButBlocked = -self.bval;
			add_2consAndChance = self.bval;
			add_2condAndBlocked = -self.bval/2;


		for i in range(4):
			row = bs[i]					
			col = [x[i] for x in bs]

		majorDiag = [bs[0][0], bs[1][1], bs[2][2], bs[3][3]]
		minorDiag = [bs[0][3], bs[1][2], bs[2][1], bs[3][0]]

		for i in xrange(0, 4):
			xcountr = row[i].count('x') 
			ocountr = row[i].count('o') 
			dcountr = row[i].count('d') 
			xcountc = col[i].count('x') 
			ocountc = col[i].count('o') 
			dcountc = col[i].count('d') 

			if(ocountr + dcountr == 0 or ocountc + dcountc == 0):
				self.winnable_x = 1

			if(xcountr + dcountr == 0 or xcountc + dcountc == 0):
				self.winnable_o = 1


			if(xcountr == 3 and ocountr == 0 and dcountr == 0):
				if(which == 'b'):
					cons3_x = 1 
				if(flag == 'x'):
					if(which == 'B'):
						if(old_move[0]%4 == i):
							h+=add_3consAndChance
						else: 
							h+=add_3consecutive
					else:
						if(whether):
							h+=add_3consAndChance
						else:
							h+=add_3consecutive
				else:
					h+=add_3consecutive

			if(ocountr == 3 and xcountr == 0 and dcountr == 0):
				if(which == 'b'):
					cons3_o = 1 
				if(flag =='o'):
					if(which == 'B'):
						if(old_move[0]%4 == i):
							h-=add_3consAndChance
						else: 
							h-=add_3consecutive
					else:
						if(whether):
							h-=add_3consAndChance
						else:
							h-=add_3consecutive
				else:
					h-=add_3consecutive

			if(xcountr == 3 and ocountr + dcountr == 1):
				h+=add_3consButBlocked
			if(ocountr == 3 and xcountr + dcountr == 1):
				h-=add_3consButBlocked

			if(xcountc == 3 and ocountc == 0 and dcountc == 0):
				if(which == 'b'):
					cons3_x = 1 
				if(flag =='x'):
					if(which == 'B'):
						if(old_move[1]%4 == i):
							h+=add_3consAndChance
						else: 
							h+=add_3consecutive
					else:
						if(whether):
							h+=add_3consAndChance
						else:
							h+=add_3consecutive
				else:
					h+=add_3consecutive
			if(ocountc == 3 and xcountc == 0 and dcountc == 0):
				if(which == 'b'):
					cons3_o = 1 
				if(flag =='o'):
					if(which == 'B'):
						if(old_move[1]%4 == i):
							h-=add_3consAndChance
						else: 
							h-=add_3consecutive
					else:
						if(whether):
							h-=add_3consAndChance
						else:
							h-=add_3consecutive
				else:
					h-=add_3consecutive

			if(xcountc == 3 and ocountc + dcountc == 1):
				h+=add_3consButBlocked
			if(ocountc == 3 and xcountc + dcountc == 1):
				h-=add_3consButBlocked

			if(xcountr == 2 and ocountr == 0 and dcountr == 0):
				if(which == 'b'):
					cons2_x = 1
				if(flag == 'x'):
					if(which == 'B'):
						if(old_move[0]%4 == i):
							h+=add_2consAndChance
						else: 
							h+=add_2consecutive
					else:
						if(whether):
							h+=add_2consAndChance
						else:
							h+=add_2consecutive
				else:
					h+=add_2consecutive
			if(ocountr == 2 and xcountr == 0 and dcountr == 0):
				if(which == 'b'):
					cons2_o = 1
				if(flag == 'o'):
					if(which == 'B'):
						if(old_move[0]%4 == i):
							h-=add_2consAndChance
						else: 
							h-=add_2consecutive
					else:
						if(whether):
							h-=add_2consAndChance
						else:
							h-=add_2consecutive
				else:
					h-=add_2consecutive

			if(xcountc == 2 and ocountc == 0 and dcountc == 0):
				if(which == 'b'):
					cons2_x = 1
				if(flag == 'x'):
					if(which == 'B'):
						if(old_move[1]%4 == i):
							h+=add_2consAndChance
						else: 
							h+=add_2consecutive
					else:
						if(whether):
							h+=add_2consAndChance
						else:
							h+=add_2consecutive
				else:
					h+=add_2consecutive
			if(ocountc == 2 and xcountc == 0 and dcountc == 0):
				if(which == 'b'):
					cons2_o = 1
				if(flag == 'o'):
					if(which == 'B'):
						if(old_move[1]%4 == i):
							h-=add_2consAndChance
						else: 
							h-=add_2consecutive
					else:
						if(whether):
							h-=add_2consAndChance
						else:
							h-=add_2consecutive
				else:
					h-=add_2consecutive

			if(xcountr == 2 and ocountr + dcountr > 0):
				h+=add_2condAndBlocked
			if(ocountr == 2 and xcountr + dcountr > 0):
				h-=add_2condAndBlocked

			if(xcountc == 2 and ocountc + dcountc > 0):
				h+=add_2condAndBlocked
			if(ocountc == 2 and xcountc + dcountc > 0):
				h-=add_2condAndBlocked

		xcountd1 = majorDiag.count('x') 
		ocountd1 = majorDiag.count('o') 
		dcountd1 = majorDiag.count('d')

		xcountd2 = minorDiag.count('x') 
		ocountd2 = minorDiag.count('o') 
		dcountd2 = minorDiag.count('d')

		if(ocountd1 + dcountd1 == 0 or ocountd2 + dcountd2 == 0):
			self.winnable_x = 1

		if(xcountd1 + dcountd1 == 0 or xcountd2 + dcountd2 == 0):
			self.winnable_o = 1

		if(xcountd1 == 3 and ocountd1 == 0 and dcountd1 == 0):
			if(which == 'b'):
				cons3_x = 1 
			if(flag =='x'):
				if(which == 'B'):
					if(old_move[0]%4 == old_move[1]%4):
						h+=add_3consAndChance
					else: 
						h+=add_3consecutive
				else:
					if(whether):
						h+=add_3consAndChance
					else:
						h+=add_3consecutive
			else:
				h+=add_3consecutive
		if(ocountd1 == 3 and xcountd1 == 0 and dcountd1 == 0):
			if(which == 'b'):
				cons3_o = 1 
			if(flag == 'o'):
				if(which == 'B'):
					if(old_move[0]%4 == old_move[1]%4):
						h-=add_3consAndChance
					else: 
						h-=add_3consecutive
				else:
					if(whether):
						h-=add_3consAndChance
					else:
						h-=add_3consecutive
			else:
				h-=add_3consecutive

		if(xcountd1 == 3 and ocountd1 + dcountd1 == 1):
			h+=add_3consButBlocked
		if(ocountd1 == 3 and xcountd1 + dcountd1 == 1):
			h-=add_3consButBlocked

		if(xcountd2 == 3 and ocountd2 == 0 and dcountd2 == 0):
			if(which == 'b'):
				cons3_x = 1 
			if(flag == 'x'):
				if(which == 'B'):
					if(old_move[0]%4 + old_move[1]%4 == 3):
						h+=add_3consAndChance
					else: 
						h+=add_3consecutive
				else:
					if(whether):
						h+=add_3consAndChance
					else:
						h+=add_3consecutive
			else:
				h+=add_3consecutive
		if(ocountd2 == 3 and xcountd2 == 0 and dcountd2 == 0):
			if(which == 'b'):
				cons3_o = 1 
			if(flag == 'o'):
				if(which == 'B'):
					if(old_move[0]%4 + old_move[1]%4 == 3):
						h-=add_3consAndChance
					else: 
						h-=add_3consecutive
				else:
					if(whether):
						h-=add_3consAndChance
					else:
						h-=add_3consecutive
			else:
				h-=add_3consecutive

		if(xcountd2 == 3 and ocountd2 + dcountd2 == 1):
			h+=add_3consButBlocked
		if(ocountd2 == 3 and xcountd2 + dcountd2 == 1):
			h-=add_3consButBlocked

		if(xcountd1 == 2 and ocountd1 == 0 and dcountd1 == 0):
			if(which == 'b'):
				cons2_x = 1
			if(flag == 'x'):
				if(which == 'B'):
					if(old_move[0]%4 == old_move[1]%4):
						h+=add_2consAndChance
					else: 
						h+=add_2consecutive
				else:
					if(whether):
						h+=add_2consAndChance
					else:
						h+=add_2consecutive
			else:
				h+=add_2consecutive
		if(ocountd1 == 2 and xcountd1 == 0 and dcountd1 == 0):
			if(which == 'b'):
				cons2_o = 1
			if(flag == 'o'):
				if(which == 'B'):
					if(old_move[0]%4 == old_move[1]%4):
						h-=add_2consAndChance
					else: 
						h-=add_2consecutive
				else:
					if(whether):
						h-=add_2consAndChance
					else:
						h-=add_2consecutive
			else:
				h-=add_2consecutive
		if(xcountd2 == 2 and ocountd2 == 0 and dcountd2 == 0):
			if(which == 'b'):
				cons2_x = 1
			if(flag == 'x'):
				if(which == 'B'):
					if(old_move[0]%4 + old_move[1]%4 == 3):
						h+=add_2consAndChance
					else: 
						h+=add_2consecutive
				else:
					if(whether):
						h+=add_2consAndChance
					else:
						h+=add_2consecutive
			else:
				h+=add_2consecutive
		if(ocountd2 == 2 and xcountd2 == 0 and dcountd2 == 0):
			if(which == 'b'):
				cons2_o = 1
			if(flag == 'o'):
				if(which == 'B'):
					if(old_move[0]%4 + old_move[1]%4 == 3):
						h-=add_2consAndChance
					else: 
						h-=add_2consecutive
				else:
					if(whether):
						h-=add_2consAndChance
					else:
						h-=add_2consecutive
			else:
				h-=add_2consecutive

		if(xcountd1 == 2 and ocountd1 + dcountd1 > 0):
			h+=add_2condAndBlocked
		if(ocountd1 == 2 and xcountd1 + dcountd1 > 0):
			h-=add_2condAndBlocked

		if(xcountd2 == 2 and ocountd2 + dcountd2 > 0):
			h+=add_2condAndBlocked
		if(ocountd2 == 2 and xcountd2 + dcountd2 > 0):
			h-=add_2condAndBlocked

		return h, cons3_x, cons3_o, cons2_x, cons2_o

	def heuristic(self, board, old_move, flag):
		
		h = 0 
		xwon = 0
		owon = 0
		bs = board.block_status
		checkTerminal = board.find_terminal_state()
		if(checkTerminal[1] == "WON"):
			if(checkTerminal[0] == 'x'):
				return 100000
			if(checkTerminal[0] == 'o'):
				return -100000

		if(checkTerminal[1] == "DRAW"):
			return 0

		for i in xrange(0 , 4):
			for j in xrange(0 , 4):
				if(bs[i][j] == 'x'):
					xwon+=1
				if(bs[i][j] == 'o'):
					owon+=1

		h += (xwon - owon) * self.Bval;

		#CORNER BLOCKS
		if(bs[0][0] == 'x' or bs[0][3] == 'x' or bs[3][0] == 'x' or bs[3][3] == 'x'):
			h+=self.Bval/2

		if(bs[0][0] == 'o' or bs[0][3] == 'o' or bs[3][0] == 'o' or bs[3][3] == 'o'):
			h-=self.Bval/2

		#CENTER BLOCKS
		if(bs[1][1] == 'x' or bs[1][2] == 'x' or bs[2][1] == 'x' or bs[2][2] == 'x'):
			h+=self.Bval/2

		if(bs[1][1] == 'o' or bs[1][2] == 'o' or bs[2][1] == 'o' or bs[2][2] == 'o'):
			h-=self.Bval/2

		#CONSECUTIVE BLOCKS AND WINNABLE
		self.winnable_x = 0
		self.winnable_o = 0
		add_h = 0
		add_h, cons3_x, cons3_o, cons2_x, cons2_o = self.calcConsecutiveHeur(bs, 'B', flag, old_move, 0);
		h+=add_h
		if(self.winnable_x == 0 and self.winnable_o == 0):
			h=0
			#TODO : MAXIMIZE BLOCK WINS 
			return h
		elif(self.winnable_x == 1 and self.winnable_o == 0):
			h+=2*self.Bval
		elif(self.winnable_x == 0 and self.winnable_o == 1):
			h-=2*self.Bval

		#SENT TO A FULL BLOCK
		if(old_move[0] != -1 and old_move[1] != -1):
			if(bs[old_move[0]%4][old_move[1]%4] != '-'):
				if(flag == 'x'):
					h+=2*self.Bval
				else:
					h-=2*self.Bval

		#CONSECUTIVE SQUARES WITHIN BLOCKS
		bs = board.board_status
		bsBlock=[]

		cons3x = []
		cons3o = []

		cons2x = []
		cons2o = []

		for i in xrange(0,4):
			con3x = []
			con3o = []
			con2x = []
			con2o = []
			for j in xrange(0,4):
				if(i == j and bs[i][j] == 'x'):
					h += self.bval/2
				elif(i == j and bs[i][j] == 'o'):
					h -= self.bval/2

				if(i + j == 3 and bs[i][j] == 'x'):
					h += self.bval/2
				elif(i + j == 3 and bs[i][j] == 'o'):
					h -= self.bval/2

				bsBlock = [bs[p][4*j:4*j+4] for p in range(4*i,4*i+4)]
				if(old_move[0]%4 == i and old_move[1]%4 == j):
					whether = 1
				else:
					whether = 0
				add_h = 0
				add_h, cons3_x, cons3_o, cons2_x, cons2_o = self.calcConsecutiveHeur(bsBlock, 'b', flag, old_move, whether);
				h+=add_h
				con3x.append(cons3_x)
				con3o.append(cons3_o)
				con2x.append(cons2_x)
				con2o.append(cons2_o)
			cons3x.append(con3x)
			cons3o.append(con3o)
			cons2x.append(con2x)
			cons2o.append(con2o)

		bs = board.block_status
		add_4cons3Blocks = 4*self.Bval
		add_3cons3Blocks = 2*self.Bval
		add_2cons3Blocks = self.Bval

		add_4cons2Blocks = self.Bval/4
		add_3cons2Blocks = self.Bval/8
		add_2cons2Blocks = self.Bval/16

		for i in range(4):
			row_x = cons3x[i]					
			col_x = [x[i] for x in cons3x]
			row_o = cons3o[i]					
			col_o = [x[i] for x in cons3o]

			row2_x = cons2x[i]					
			col2_x = [x[i] for x in cons2x]
			row2_o = cons2o[i]					
			col2_o = [x[i] for x in cons2o]

			row = bs[i]
			col = [p[i] for p in bs]

			if(row_x.count(1) == 4 and row.count('o') + row.count('d') == 0):
				h+=add_4cons3Blocks
			if(row_o.count(1) == 4 and row.count('x') + row.count('d') == 0):
				h-=add_4cons3Blocks

			if(row_x.count(1) == 3 and row.count('o') + row.count('d') == 0):
				h+=add_3cons3Blocks
			if(row_o.count(1) == 3 and row.count('x') + row.count('d') == 0):
				h-=add_3cons3Blocks

			if(row_x.count(1) == 2 and row.count('o') + row.count('d') == 0):
				h+=add_3cons3Blocks
			if(row_o.count(1) == 2 and row.count('x') + row.count('d') == 0):
				h-=add_2cons3Blocks

			if(col_x.count(1) == 4 and col.count('o') + col.count('d') == 0):
				h+=add_4cons3Blocks
			if(col_o.count(1) == 4 and col.count('x') + col.count('d') == 0):
				h-=add_4cons3Blocks

			if(col_x.count(1) == 3 and col.count('o') + col.count('d') == 0):
				h+=add_3cons3Blocks
			if(col_o.count(1) == 3 and col.count('x') + col.count('d') == 0):
				h-=add_3cons3Blocks

			if(col_x.count(1) == 2 and col.count('o') + col.count('d') == 0):
				h+=add_3cons3Blocks
			if(col_o.count(1) == 2 and col.count('x') + col.count('d') == 0):
				h-=add_2cons3Blocks




			if(row2_x.count(1) == 4 and row.count('o') + row.count('d') == 0):
				h+=add_4cons2Blocks
			if(row2_o.count(1) == 4 and row.count('x') + row.count('d') == 0):
				h-=add_4cons2Blocks

			if(row2_x.count(1) == 3 and row.count('o') + row.count('d') == 0):
				h+=add_3cons2Blocks
			if(row2_o.count(1) == 3 and row.count('x') + row.count('d') == 0):
				h-=add_3cons2Blocks

			if(row2_x.count(1) == 2 and row.count('o') + row.count('d') == 0):
				h+=add_3cons2Blocks
			if(row2_o.count(1) == 2 and row.count('x') + row.count('d') == 0):
				h-=add_2cons2Blocks

			if(col2_x.count(1) == 4 and col.count('o') + col.count('d') == 0):
				h+=add_4cons2Blocks
			if(col2_o.count(1) == 4 and col.count('x') + col.count('d') == 0):
				h-=add_4cons2Blocks

			if(col2_x.count(1) == 3 and col.count('o') + col.count('d') == 0):
				h+=add_3cons2Blocks
			if(col2_o.count(1) == 3 and col.count('x') + col.count('d') == 0):
				h-=add_3cons2Blocks

			if(col2_x.count(1) == 2 and col.count('o') + col.count('d') == 0):
				h+=add_3cons2Blocks
			if(col2_o.count(1) == 2 and col.count('x') + col.count('d') == 0):
				h-=add_2cons2Blocks


		majorDiag = [bs[0][0], bs[1][1], bs[2][2], bs[3][3]]
		minorDiag = [bs[0][3], bs[1][2], bs[2][1], bs[3][0]]

		majorDiag_x = [cons3x[0][0], cons3x[1][1], cons3x[2][2], cons3x[3][3]]
		minorDiag_x = [cons3x[0][3], cons3x[1][2], cons3x[2][1], cons3x[3][0]]

		majorDiag_o = [cons3o[0][0], cons3o[1][1], cons3o[2][2], cons3o[3][3]]
		minorDiag_o = [cons3o[0][3], cons3o[1][2], cons3o[2][1], cons3o[3][0]]

		majorDiag2_x = [cons2x[0][0], cons2x[1][1], cons2x[2][2], cons2x[3][3]]
		minorDiag2_x = [cons2x[0][3], cons2x[1][2], cons2x[2][1], cons2x[3][0]]

		majorDiag2_o = [cons2o[0][0], cons2o[1][1], cons2o[2][2], cons2o[3][3]]
		minorDiag2_o = [cons2o[0][3], cons2o[1][2], cons2o[2][1], cons2o[3][0]]

		if(majorDiag_x.count(1) == 4 and majorDiag.count('o') + majorDiag.count('d') == 0):
			h+=add_4cons3Blocks
		if(majorDiag_o.count(1) == 4 and majorDiag.count('x') + majorDiag.count('d') == 0):
			h-=add_4cons3Blocks

		if(majorDiag_x.count(1) == 3 and majorDiag.count('o') + majorDiag.count('d') == 0):
			h+=add_3cons3Blocks
		if(majorDiag_o.count(1) == 3 and majorDiag.count('x') + majorDiag.count('d') == 0):
			h-=add_3cons3Blocks

		if(majorDiag_x.count(1) == 2 and majorDiag.count('o') + majorDiag.count('d') == 0):
			h+=add_3cons3Blocks
		if(majorDiag_o.count(1) == 2 and majorDiag.count('x') + majorDiag.count('d') == 0):
			h-=add_2cons3Blocks

		if(minorDiag_x.count(1) == 4 and minorDiag.count('o') + minorDiag.count('d') == 0):
			h+=add_4cons3Blocks
		if(minorDiag_o.count(1) == 4 and minorDiag.count('x') + minorDiag.count('d') == 0):
			h-=add_4cons3Blocks

		if(minorDiag_x.count(1) == 3 and minorDiag.count('o') + minorDiag.count('d') == 0):
			h+=add_3cons3Blocks
		if(minorDiag_o.count(1) == 3 and minorDiag.count('x') + minorDiag.count('d') == 0):
			h-=add_3cons3Blocks

		if(minorDiag_x.count(1) == 2 and minorDiag.count('o') + minorDiag.count('d') == 0):
			h+=add_3cons3Blocks
		if(minorDiag_o.count(1) == 2 and minorDiag.count('x') + minorDiag.count('d') == 0):
			h-=add_2cons3Blocks


		if(majorDiag2_x.count(1) == 4 and majorDiag.count('o') + majorDiag.count('d') == 0):
			h+=add_4cons2Blocks
		if(majorDiag2_o.count(1) == 4 and majorDiag.count('x') + majorDiag.count('d') == 0):
			h-=add_4cons2Blocks

		if(majorDiag2_x.count(1) == 3 and majorDiag.count('o') + majorDiag.count('d') == 0):
			h+=add_3cons2Blocks
		if(majorDiag2_o.count(1) == 3 and majorDiag.count('x') + majorDiag.count('d') == 0):
			h-=add_3cons2Blocks

		if(majorDiag2_x.count(1) == 2 and majorDiag.count('o') + majorDiag.count('d') == 0):
			h+=add_3cons2Blocks
		if(majorDiag2_o.count(1) == 2 and majorDiag.count('x') + majorDiag.count('d') == 0):
			h-=add_2cons2Blocks

		if(minorDiag2_x.count(1) == 4 and minorDiag.count('o') + minorDiag.count('d') == 0):
			h+=add_4cons2Blocks
		if(minorDiag2_o.count(1) == 4 and minorDiag.count('x') + minorDiag.count('d') == 0):
			h-=add_4cons2Blocks

		if(minorDiag2_x.count(1) == 3 and minorDiag.count('o') + minorDiag.count('d') == 0):
			h+=add_3cons2Blocks
		if(minorDiag2_o.count(1) == 3 and minorDiag.count('x') + minorDiag.count('d') == 0):
			h-=add_3cons2Blocks

		if(minorDiag2_x.count(1) == 2 and minorDiag.count('o') + minorDiag.count('d') == 0):
			h+=add_3cons2Blocks
		if(minorDiag2_o.count(1) == 2 and minorDiag.count('x') + minorDiag.count('d') == 0):
			h-=add_2cons2Blocks


		return h

	def minimax(self, board, currentDepth, maxDepth, old_move, flag, alpha, beta):
		if(currentDepth == maxDepth):
			return self.heuristic(board, old_move,flag)

		actions = board.find_valid_move_cells(old_move)
		if(flag == 'x'):
			ans = -1000000.0
			for action in actions:
				
				newBoard = Board()
				newBoard = copy.deepcopy(board)
				newBoard.update(old_move, action , 'x');

				curMinimax = self.minimax(newBoard, currentDepth + 1, maxDepth, action, 'o', alpha, beta)
				if(currentDepth == 0 and curMinimax > ans):
					self.optimalMove = action
				ans = max(ans, curMinimax)	
				if(ans >= beta):
					return ans
				alpha = max(alpha, ans)
			return ans

		elif(flag == 'o'):
			ans = 1000000.0
			for action in actions:
				newBoard = Board()
				newBoard = copy.deepcopy(board)
				newBoard.update(old_move, action , 'o');

				curMinimax = self.minimax(newBoard, currentDepth + 1, maxDepth, action, 'x', alpha, beta)
				if(currentDepth == 0 and curMinimax < ans):
					self.optimalMove = action
				ans = min(ans, curMinimax)
				if(ans <= alpha):
					return ans
				beta = min(beta, ans)
			return ans

class Board:

	def __init__(self):
		# board_status is the game board
		# block status shows which blocks have been won/drawn and by which player
		self.board_status = [['-' for i in range(16)] for j in range(16)]
		self.block_status = [['-' for i in range(4)] for j in range(4)]

	def print_board(self):
		# for printing the state of the board
		print '==============Board State=============='
		for i in range(16):
			if i%4 == 0:
				print
			for j in range(16):
				if j%4 == 0:
					print "",
				print self.board_status[i][j],
			print 
		print

		print '==============Block State=============='
		for i in range(4):
			for j in range(4):
				print self.block_status[i][j],
			print 
		print '======================================='
		print
		print


	def find_valid_move_cells(self, old_move):
		#returns the valid cells allowed given the last move and the current board state
		allowed_cells = []
		allowed_block = [old_move[0]%4, old_move[1]%4]
		#checks if the move is a free move or not based on the rules

		if old_move != (-1,-1) and self.block_status[allowed_block[0]][allowed_block[1]] == '-':
			for i in range(4*allowed_block[0], 4*allowed_block[0]+4):
				for j in range(4*allowed_block[1], 4*allowed_block[1]+4):
					if self.board_status[i][j] == '-':
						allowed_cells.append((i,j))
		else:
			for i in range(16):
				for j in range(16):
					if self.board_status[i][j] == '-' and self.block_status[i/4][j/4] == '-':
						allowed_cells.append((i,j))
		return allowed_cells	

	def find_terminal_state(self):
		#checks if the game is over(won or drawn) and returns the player who have won the game or the player who has higher blocks in case of a draw
		bs = self.block_status

		cntx = 0
		cnto = 0
		cntd = 0

		for i in range(4):						#counts the blocks won by x, o and drawn blocks
			for j in range(4):
				if bs[i][j] == 'x':
					cntx += 1
				if bs[i][j] == 'o':
					cnto += 1
				if bs[i][j] == 'd':
					cntd += 1

		for i in range(4):
			row = bs[i]							#i'th row 
			col = [x[i] for x in bs]			#i'th column
			#print row,col
			#checking if i'th row or i'th column has been won or not
			if (row[0] =='x' or row[0] == 'o') and (row.count(row[0]) == 4):	
				return (row[0],'WON')
			if (col[0] =='x' or col[0] == 'o') and (col.count(col[0]) == 4):
				return (col[0],'WON')
		#checking if diagnols have been won or not
		if(bs[0][0] == bs[1][1] == bs[2][2] ==bs[3][3]) and (bs[0][0] == 'x' or bs[0][0] == 'o'):
			return (bs[0][0],'WON')
		if(bs[0][3] == bs[1][2] == bs[2][1] ==bs[3][0]) and (bs[0][3] == 'x' or bs[0][3] == 'o'):
			return (bs[0][3],'WON')

		if cntx+cnto+cntd <16:		#if all blocks have not yet been won, continue
			return ('CONTINUE', '-')
		elif cntx+cnto+cntd == 16:							#if game is drawn
			return ('NONE', 'DRAW')

	def check_valid_move(self, old_move, new_move):
		#checks if a move is valid or not given the last move
		if (len(old_move) != 2) or (len(new_move) != 2):
			return False 
		if (type(old_move[0]) is not int) or (type(old_move[1]) is not int) or (type(new_move[0]) is not int) or (type(new_move[1]) is not int):
			return False
		if (old_move != (-1,-1)) and (old_move[0] < 0 or old_move[0] > 16 or old_move[1] < 0 or old_move[1] > 16):
			return False
		cells = self.find_valid_move_cells(old_move)
		return new_move in cells

	def update(self, old_move, new_move, ply):
		#updating the game board and block status as per the move that has been passed in the arguements
		if(self.check_valid_move(old_move, new_move)) == False:
			return 'UNSUCCESSFUL'
		self.board_status[new_move[0]][new_move[1]] = ply

		x = new_move[0]/4
		y = new_move[1]/4
		fl = 0
		bs = self.board_status
		#checking if a block has been won or drawn or not after the current move
		for i in range(4):
			#checking for horizontal pattern(i'th row)
			if (bs[4*x+i][4*y] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+2] == bs[4*x+i][4*y+3]) and (bs[4*x+i][4*y] == ply):
				self.block_status[x][y] = ply
				return 'SUCCESSFUL'
			#checking for vertical pattern(i'th column)
			if (bs[4*x][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+2][4*y+i] == bs[4*x+3][4*y+i]) and (bs[4*x][4*y+i] == ply):
				self.block_status[x][y] = ply
				return 'SUCCESSFUL'

		#checking for diagnol pattern
		if (bs[4*x][4*y] == bs[4*x+1][4*y+1] == bs[4*x+2][4*y+2] == bs[4*x+3][4*y+3]) and (bs[4*x][4*y] == ply):
			self.block_status[x][y] = ply
			return 'SUCCESSFUL'
		if (bs[4*x+3][4*y] == bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2] == bs[4*x][4*y+3]) and (bs[4*x+3][4*y] == ply):
			self.block_status[x][y] = ply
			return 'SUCCESSFUL'

		#checking if a block has any more cells left or has it been drawn
		for i in range(4):
			for j in range(4):
				if bs[4*x+i][4*y+j] =='-':
					return 'SUCCESSFUL'
		self.block_status[x][y] = 'd'
		return 'SUCCESSFUL'


class TimedOutExc(Exception):
	pass

def handler(signum, frame):
	#print 'Signal handler called with signal', signum
	raise TimedOutExc()



#MONTE CARLO

# parent = {}
# expanded_child = {}
# a = {}
# Q = {}
# N = {}
# untried = {}
# def HASH_IT(board):
# 	s=""
# 	for i in range(0, 16):
# 		for j in range(0,16):
# 			s+=(board.board_status[i][j]);
# 	return s

# def UCTSEARCH(board, old_move, flag):
# 	global a
# 	global Q
# 	global N
# 	global parent
# 	global expanded_child
# 	global untried

# 	TIME = 5
# 	signal.signal(signal.SIGALRM, handler)
# 	v0 = Board()
# 	v0 = copy.deepcopy(board)
# 	untried[HASH_IT(v0)]=v0.find_valid_move_cells(old_move)
# 	i = 0
# 	signal.alarm(TIME)
# 	while(True):
		
# 		try:
# 			# print i
# 			v1, action = TREEPOLICY(v0, old_move, flag)
# 			new_flag = 'o' if (flag == 'x') else 'x'
# 			delta = DEFAULTPOLICY(v1, action, new_flag)
# 			BACKUP(v1, delta)
# 			i+=1
# 		except TimedOutExc:
# 			break;
# 	vtemp, best = BESTCHILD(v0, 0, old_move, flag)
# 	print best
# 	return best

# def TREEPOLICY(v, old_move, flag):
# 	global a
# 	global Q
# 	global N
# 	global parent
# 	global expanded_child
# 	global untried

# 	while v.find_terminal_state()[1] == '-':

# 		hash_v = HASH_IT(v)
		
# 		actions = v.find_valid_move_cells(old_move)
		
# 		if hash_v not in expanded_child:
# 			expanded_child[hash_v] = 0
# 		if expanded_child[hash_v]<len(actions):
# 			return EXPAND(v, old_move, flag)
# 		else:
# 			Cp = 1/math.sqrt(2)
# 			vb, action = BESTCHILD(v, Cp, old_move, flag)
# 			parent[HASH_IT(vb)] = v
# 			old_move = action
# 			flag = 'o' if (flag == 'x') else 'x'
# 			v = copy.deepcopy(vb)

# 	return v, action

# def EXPAND(v, old_move, flag):
# 	global a
# 	global Q
# 	global N
# 	global parent
# 	global expanded_child
# 	global untried

# 	hash_v = HASH_IT(v)

# 	if hash_v not in untried:
# 		untried[hash_v] = v.find_valid_move_cells(old_move)
# 	action = untried[hash_v][random.randrange(len(untried[hash_v]))]
# 	v1 = Board()
# 	v1 = copy.deepcopy(v)
# 	v1.update(old_move, action, flag)
	
# 	hash_v1 = HASH_IT(v1)

# 	a[hash_v1] = action
# 	if hash_v in expanded_child:
# 		expanded_child[hash_v]+=1
# 	else: 
# 		expanded_child[hash_v]=1
# 	untried[hash_v].remove(a[hash_v1])
# 	parent[hash_v1] = v
# 	return v1, action

# def BESTCHILD(v, c, old_move, flag):
# 	global a
# 	global Q
# 	global N
# 	global parent
# 	global expanded_child
# 	global untried

# 	actions = v.find_valid_move_cells(old_move)
# 	highest = -10000.0
# 	highest_action = []

# 	hash_v = HASH_IT(v)

# 	for action in actions:

# 		v1 = Board()
# 		v1 = copy.deepcopy(v)
# 		v1.update(old_move, action, flag)
# 		hash_v1 = HASH_IT(v1)
# 		if hash_v1 not in Q:
# 			Q[hash_v1] = 0.0
# 		if hash_v1 in N and N[hash_v1] > 0:
# 			val = (Q[hash_v1]/N[hash_v1] + 2*c*math.sqrt(2*np.log(N[hash_v]))/ N[hash_v1])
# 			if(val > highest):
# 				vh = Board()
# 				vh = copy.deepcopy(v1)
# 				highest = val
# 				highest_action = action

# 	# print "highest", highest
# 	# print "nodeh", vh
# 	# print "actionh", highest_action
# 	return vh, highest_action

# def DEFAULTPOLICY(v, old_move, flag):
# 	global a
# 	global Q
# 	global N
# 	global parent
# 	global expanded_child
# 	global untried

	
# 	while v.find_terminal_state()[1] == '-' :
# 		actions = []
# 		actions = v.find_valid_move_cells(old_move)
# 		v1 = Board()
# 		v1 = copy.deepcopy(v)
# 		action = actions[random.randrange(len(actions))]
# 		v1.update(old_move, action, flag)
# 		old_move = action
# 		flag = 'o' if (flag == 'x') else 'x'
# 		v = copy.deepcopy(v1)

	
# 	if(v.find_terminal_state()[1] == 'WON'):
# 		if(v.find_terminal_state()[0] == flag):
# 			return 1.0
# 		else:
# 			return -1.0
# 	elif(v.find_terminal_state()[1] == 'DRAW'):
# 		return 0.0

# def BACKUP(v, delta):
# 	global a
# 	global Q
# 	global N
# 	global parent
# 	global expanded_child
# 	global untried

# 	while(True):
# 		hash_v = HASH_IT(v)
# 		if hash_v in N: 
# 			N[hash_v] = N[hash_v] + 1.0
# 		else:
# 			N[hash_v] = 1.0
# 		if hash_v in Q: 
# 			Q[hash_v] = Q[hash_v] + delta
# 		else:
# 			Q[hash_v] = delta

# 		delta=-delta
# 		if hash_v in parent:
# 			v = parent[hash_v]
# 		else:
# 			break

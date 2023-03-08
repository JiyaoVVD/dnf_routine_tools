# coding=utf-8

from dungeonData import DungeonData
from roleData import RoleData, HEALER_WEIGHT_COEFFICIENT

dungeons = {}

roles = []
totalRoleNum = 0
visitedRoleNum = 0

# for routine calculation
modeInstanceStack = []
totalRoutineNum = 0

class Routine:
	def __init__(self) -> None:
		global modeInstanceStack
		self.teamRoleIndices = []
		self.modeNames = []
		self.score = 0.0
		self.strengths = []

		for modeInstance in modeInstanceStack:
			self.teamRoleIndices += [modeInstance.selectedRoles[:]]
			self.modeNames.append(modeInstance.mode.name)
			self.strengths += [modeInstance.strengths]
			# 排班评价
			self.score += sum(modeInstance.strengths)
	
	def show(self):
		global roles
		print('排班综合评分', self.score)
		for i in range(len(self.modeNames)):
			print('\t', self.modeNames[i], '队伍相对强度', self.strengths[i])
			for roleIndex in self.teamRoleIndices[i]:
				role = roles[roleIndex]
				print('\t\t', role.account, role.name)
		print()

CHOSEN_ONE = Routine()

class Role:
	def __init__(self, data) -> None:
		self.account = None
		self.name = data.get('names', ['null'])[0]
		self.isHealer = data.get('isHealer', False)
		self.weight = data.get('weight', 0)
		self.isVisited = False

		# 站街奶量转伤害倍率
		if self.isHealer:
			self.weight *= HEALER_WEIGHT_COEFFICIENT

class DungeonTeam:
	def __init__(self, data) -> None:
		self.requirement = data.get('requirement', 0)
		self.playerCount = data.get('playerCount', 1)

class DungeonMode:
	def __init__(self, dungeon, modeIndex, data) -> None:
		self.name = data.get('name', '无')
		self.globalBuff = data.get('globalBuff')
		self.teams = [DungeonTeam(team) for team in data.get('teams', [])]
		self.maxPlayerCount = sum([team.playerCount for team in self.teams])

		# for dfs
		self.dungeon = dungeon
		self.modeIndex = modeIndex

class DungeonModeInstance:
	def __init__(self, mode: DungeonMode) -> None:
		self.mode = mode
		self.dungeon = mode.dungeon
		self.modeIndex = mode.modeIndex

		self.visited = set() # type: set(str)
		self.selectedRoles = [] # type: list(int)
		self.strengths = []
	
	def pushRoleIndex(self, index):
		self.selectedRoles.append(index)
	
	def popRoleIndex(self):
		# 没有安全检查
		self.selectedRoles.pop()

	def evalAllTeams(self):
		'''
		返回本次排班的相对强度列表
		'''
		self.strengths = []
		mode = self.mode
		beginRoleIndex = 0
		endRoleIndex = len(self.selectedRoles)

		for team in mode.teams:
			weight = 0
			buff = 1 if mode.globalBuff is None else mode.globalBuff
			curNumOfTeam = 0

			for roleIndex in range(beginRoleIndex, endRoleIndex):
				role = roles[self.selectedRoles[roleIndex]]
				curNumOfTeam += 1
				if role.isHealer:
					buff = max(buff, role.weight)
				else:
					weight += role.weight
				if curNumOfTeam == team.playerCount:
					beginRoleIndex = roleIndex + 1
					break
			self.strengths.append(round(weight * buff / team.requirement, 2)) # 队伍强度和副本强度之比

class Dungeon:
	def __init__(self, name, data) -> None:
		self.name = name
		self.modes = [DungeonMode(self, i, mode) for i, mode in enumerate(data.get('modes', []))]
		self.modeSize = len(self.modes)

def preprocess():
	# 把地下城信息和角色信息转成对象
	global roles
	global totalRoleNum
	global dungeons

	# RoleData.pop('旭旭宝宝', None)
	for account, roleList in RoleData.items():
		for roleData in roleList:
			role = Role(roleData)
			role.account = account
			roles.append(role)
	totalRoleNum = len(roles)

	for name, data in DungeonData.items():
		dungeons[name] = Dungeon(name, data)

def dfs_role(modeInstance: DungeonModeInstance, restPlaces: int):
	global roles
	global totalRoleNum
	global visitedRoleNum
	global totalRoutineNum
	global modeInstanceStack
	global CHOSEN_ONE

	if visitedRoleNum == totalRoleNum:
		modeInstance.evalAllTeams()

		routine = Routine()
		totalRoutineNum += 1
		if CHOSEN_ONE.score < routine.score:
			CHOSEN_ONE = routine
			# routine.show()
		return

	if totalRoutineNum >= 114514:
		return

	if restPlaces <= 0:
		# 计算一次评价
		modeInstance.evalAllTeams()

		# TODO
		# 剪枝: 有一队相对强度小于0.9的直接否掉
		# for strength in modeInstance.strengths:
		# 	if strength < 0.9:
		# 		return

		# 枚举完本次副本 接着下一个
		dfs_mode(modeInstance.dungeon)
	else:
		for roleIndex, role in enumerate(roles):
			if role.isVisited:
				continue
			if role.account in modeInstance.visited:
				continue

			# 尝试选择该角色
			role.isVisited = True
			visitedRoleNum += 1
			modeInstance.visited.add(role.account)
			modeInstance.pushRoleIndex(roleIndex)

			dfs_role(modeInstance, restPlaces - 1)

			role.isVisited = False
			visitedRoleNum -= 1
			modeInstance.visited.remove(role.account)
			modeInstance.popRoleIndex()

def dfs_mode(dungeon: Dungeon):
	global modeInstanceStack

	for mode in dungeon.modes:
		modeInstance = DungeonModeInstance(mode)
		modeInstanceStack.append(modeInstance)
		dfs_role(modeInstance, mode.maxPlayerCount)
		modeInstanceStack.pop()

def main():
	global dungeons
	global routines
	global roles
	global CHOSEN_ONE

	preprocess()

	dungeonName = '军团'
	dungeon = dungeons.get(dungeonName)
	if dungeon:
		dfs_mode(dungeon)
		CHOSEN_ONE.show()
	else:
		print('没有该地下城的数据:', dungeonName)

main()

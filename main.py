# coding=utf-8

from dungeonData import DungeonData
from roleData import RoleData, HEALER_WEIGHT_COEFFICIENT

dungeons = {}

accounts = []

roles = []
totalRoleNum = 0
visitedRoleNum = 0

# for routine calculation
modeInstanceStack = []
totalRoutineNum = 0

HIT_CHANCE_REST = 11451419

class Routine:
	def __init__(self) -> None:
		self.teamRoles = []
		self.modeNames = []
		self.score = 114514.0
		self.strengths = []

		for modeInstance in modeInstanceStack:
			self.teamRoles += [modeInstance.selectedRoles[:]]
			self.modeNames.append(modeInstance.mode.name)
			self.strengths += [modeInstance.strengths]

			# 排班评价
			if modeInstance.mode.notConsidered:
				continue
			self.score = min(min(modeInstance.strengths), self.score)

	def show(self):
		global roles
		print('排班综合评分', round(self.score, 2))
		for i in range(len(self.modeNames)):
			print('\t', self.modeNames[i], '队伍相对强度', [round(x, 2) for x in self.strengths[i]])
			for i, role in enumerate(self.teamRoles[i]):
				if i & 3 == 0:
					print('\t  队伍', int(i / 4))
				print('\t\t', accounts[role.accountIndex], role.name)
		print()

CHOSEN_ONE = Routine()
CHOSEN_ONE.score = -999.0

class Role:
	def __init__(self, accountIndex, data) -> None:
		self.accountIndex = accountIndex
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

class DungeonMode:
	def __init__(self, dungeon, modeIndex, data) -> None:
		self.name = data.get('name', '无')
		self.globalBuff = data.get('globalBuff')
		self.needHealer = self.globalBuff is None
		self.notConsidered = data.get('notConsidered', False)

		self.teams = [DungeonTeam(team) for team in data.get('teams', [])]
		self.playersPerTeam = data.get('playersPerTeam', 4)
		self.maxPlayerCount = len(self.teams) * self.playersPerTeam

		# for dfs
		self.dungeon = dungeon
		self.modeIndex = modeIndex

class DungeonModeInstance:
	def __init__(self, mode: DungeonMode, stackIndex) -> None:
		self.mode = mode
		self.dungeon = mode.dungeon
		self.stackIndex = stackIndex
		self.needHealer = mode.needHealer
		self.playersPerTeam = mode.playersPerTeam
		self.maxPlayerCount = mode.maxPlayerCount

		self.visited = set() # type: set(int)
		self.selectedRoles = [] # type: list(int)
		self.strengths = []
	
	def pushRolePure(self, role):
		self.selectedRoles.append(role)

	def pushRole(self, role):
		global visitedRoleNum
		visitedRoleNum += 1

		if not self.mode.notConsidered: # 金团就全塞进去 不考虑人重复出场的情况
			role.isVisited = True
			self.visited.add(role.accountIndex)
		self.selectedRoles.append(role)

	def popRole(self):
		global visitedRoleNum
		visitedRoleNum -= 1

		# 没有安全检查
		role = self.selectedRoles.pop()
		if not self.mode.notConsidered:
			role.isVisited = False
			self.visited.remove(role.accountIndex)

	def evalOneTeam(self):
		if self.mode.notConsidered:
			return 114514

		if not self.strengths:
			self.strengths = [0] * len(self.mode.teams)

		# 计算最后一个队伍的相对强度
		curRoleNum = len(self.selectedRoles)
		teamIndex = int((curRoleNum - 1) / self.playersPerTeam)
		team = self.mode.teams[teamIndex]

		weight = 0
		buff = 1 if self.mode.globalBuff is None else self.mode.globalBuff
		for roleIndex in range(teamIndex * self.playersPerTeam, curRoleNum):
			role = self.selectedRoles[roleIndex]
			if role.isHealer:
				buff = max(buff, role.weight)
			else:
				weight += role.weight
		ret = weight * buff / team.requirement
		self.strengths[teamIndex] = ret
		return ret

class Dungeon:
	def __init__(self, name, data) -> None:
		self.name = name
		self.modes = [DungeonMode(self, i, modeData) for i, modeData in enumerate(data.get('modes', []))]

def preprocess():
	# 把地下城信息和角色信息转成对象
	global roles
	global totalRoleNum
	global dungeons
	global accounts

	# RoleData.pop('旭旭宝宝', None)
	for accountName, roleList in RoleData.items():
		# 初始化账号信息
		curAccountIndex = len(accounts)
		accounts.append(accountName)

		# 初始化账号下所有的角色
		for roleData in roleList:
			role = Role(curAccountIndex, roleData)
			roles.append(role)
	totalRoleNum = len(roles)

	for name, data in DungeonData.items():
		dungeons[name] = Dungeon(name, data)

def RecordOneRoutine():
	global totalRoutineNum
	global CHOSEN_ONE

	routine = Routine()
	totalRoutineNum += 1
	if totalRoutineNum & 8191 == 0:
		print('已迭代方案数:', totalRoutineNum)
	if CHOSEN_ONE.score < routine.score:
		CHOSEN_ONE = routine
		# routine.show()

def dfs_role(curMode: DungeonModeInstance, restPlaces: int, startSearchIndex: int, healerCount: int):
	# 如果执行步骤过多 就需要停止搜索 避免执行过久
	# global HIT_CHANCE_REST
	# HIT_CHANCE_REST -= 1
	# if HIT_CHANCE_REST <= 0:
	# 	return

	# 是否没人可以排了
	if visitedRoleNum == totalRoleNum:
		# 直接计分 枚举下一个
		score = curMode.evalOneTeam()
		if score > CHOSEN_ONE.score:
			RecordOneRoutine()
		return

	# 凑成了一个队伍
	if restPlaces % curMode.playersPerTeam == 0 and restPlaces != curMode.maxPlayerCount:
		# 剪枝: 如果当前队伍没有奶就回溯(系统奶也算奶)
		# 如果一个本没奶也能过说明退环境了 也不用排班工具了 所以不予考虑
		if healerCount <= 0:
			return

		# 剪枝: 如果当前队伍强度不如最好排班中的最差队伍 直接返回
		score = curMode.evalOneTeam()
		if score <= CHOSEN_ONE.score:
			return

		# 如果是副本的最后一个队伍 判断后面是否还有副本
		if restPlaces == 0:
			if curMode.stackIndex + 1 < len(modeInstanceStack):
				# 还有副本需要排
				curMode = modeInstanceStack[curMode.stackIndex + 1]
				restPlaces = curMode.maxPlayerCount
				startSearchIndex = 0
				healerCount = int(not curMode.needHealer)
			else:
				# 所有副本都排了人 返回
				RecordOneRoutine()
				return
		else:
			# 还有队伍 刷新状态准备进入迭代
			healerCount = int(not curMode.needHealer)
			if curMode.playersPerTeam != 1:
				# 凑够了一个多人队才重置枚举位置 否则会导致枚举单人本的时候用全排列
				startSearchIndex = 0

	for roleIndex in range(startSearchIndex, totalRoleNum):
		role = roles[roleIndex]
		if role.isVisited:
			continue
		if role.accountIndex in curMode.visited:
			continue

		curMode.pushRole(role)
		healerCount += int(role.isHealer)

		dfs_role(curMode, restPlaces - 1, roleIndex + 1, healerCount)

		curMode.popRole()
		healerCount -= int(role.isHealer)

def dfs_mode(dungeon: Dungeon, curModeIndex: int, restPlaces: int):
	global modeInstanceStack

	if restPlaces <= 0:
		return

	for modeIndex in range(curModeIndex, len(dungeon.modes)):
		mode = dungeon.modes[modeIndex]

		if mode.notConsidered and len(modeInstanceStack) == 0:
			# 不考虑全部金团的情况
			continue

		'''
		剪枝: 如果此时模式只需要一个人
		则不需要再枚举模式 因为后面的模式也一定是一个人
		'''
		if mode.maxPlayerCount == 1:
			# 快速生成剩余的单人模式
			originTop = len(modeInstanceStack)
			for i in range(restPlaces):
				modeInstance = DungeonModeInstance(mode, originTop + i)
				modeInstanceStack.append(modeInstance)
			dfs_role(
				modeInstanceStack[0],
				modeInstanceStack[0].maxPlayerCount,
				0, int(not modeInstanceStack[0].needHealer)
			)
			# 回退栈
			modeInstanceStack = modeInstanceStack[:originTop]
			# 为了优化起见 单人模式最好放在配置表的末尾
			return

		# 正常递归
		modeInstance = DungeonModeInstance(mode, len(modeInstanceStack))
		modeInstanceStack.append(modeInstance)

		# 如果空位够就不需要再递归了
		if mode.maxPlayerCount >= restPlaces:
			dfs_role(
				modeInstanceStack[0],
				modeInstanceStack[0].maxPlayerCount,
				0, int(not modeInstanceStack[0].needHealer)
			)
		else:
			# 还需要新增排班
			dfs_mode(dungeon, modeIndex, restPlaces - mode.maxPlayerCount)

		modeInstanceStack.pop()

def main():
	preprocess()

	dungeonName = '军团'
	dungeon = dungeons.get(dungeonName)
	if dungeon:
		import time

		print('启动排班:', dungeonName, '待排班人数:', totalRoleNum)
		t = time.time()
		dfs_mode(dungeon, 0, totalRoleNum)
		print('总用时', round(time.time() - t, 2), '秒 迭代方案数:', totalRoutineNum)
		CHOSEN_ONE.show()
	else:
		print('没有该地下城的数据:', dungeonName)

main()

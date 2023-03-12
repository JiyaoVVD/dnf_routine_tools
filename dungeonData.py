# coding = utf-8
'''
副本配置文件
1.参考其他副本配置来编写新地下城的排班规则
2.为了保证所有人都能够被排进去, 务必增加一个大小为1的无门槛金团或单刷模式在最后!!!!!!!!!!!!!
'''

DungeonData = {
	'巴卡尔': {
		'modes': [
			{
				'name': '巴卡尔团本',
				'playersPerTeam': 4,
				'teams': [ # 红黄绿队
					{
						'requirement': 110 * 40 # 总强度门槛
					},
					{
						'requirement': 90 * 35
					},
					{
						'requirement': 70 * 30
					}
				]
			},{
				'name': '巴卡尔金团',
				'globalBuff': 1,
				'playersPerTeam': 9999,
				'notConsidered': True, # 兜底副本 不计入贡献
				'teams': [
					{
						'requirement': 1, # 总强度门槛
					}
				]
			}
		]
	},
	'巴卡妮': {
		'modes': [
			{
				'name': '巴卡妮组队',
				'playersPerTeam': 4,
				'teams': [
					{
						'requirement': 15 * 25
					}
				]
			},
			{
				'name': '巴卡妮单刷',
				'globalBuff': 1,
				'playersPerTeam': 1,
				'teams': [
					{
						'requirement': 5
					}
				]
			}
		]
	},
	'军团': {
		'modes': [ # 模式 纯C、单刷或者组奶
			{
				'name': '军团组队',
				'playersPerTeam': 4,
				'teams': [
					{
						'requirement': 45 * 20
					}
				],
				'globalBuff': 20 # 地下城系统奶系数 有这一项时会考虑无奶的队伍
			},
			{
				'name': '军团单刷',
				'playersPerTeam': 1,
				'teams': [
					{
						'requirement': 8
					}
				],
				'globalBuff': 1
			}
		]
	}
}

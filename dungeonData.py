# coding=utf-8
'''
副本配置文件
1.参考其他副本配置来编写新地下城的排班规则
2.务必增加一个大小为1的无门槛模式(金团或者单刷)，保证所有人都能够被排进去
'''

DungeonData = {
	'巴卡尔': {
		'modes': [
			{
				'name': '巴卡尔团本',
				'teams': [ # 红黄绿队
					{
						'requirement': 110 * 40, # 总强度门槛
						'playerCount': 4
					},
					{
						'requirement': 90 * 35,
						'playerCount': 4
					},
					{
						'requirement': 70 * 30,
						'playerCount': 4
					}
				]
			},{
				'name': '巴卡尔金团',
				'teams': [
					{
						'requirement': 1, # 总强度门槛
						'playerCount': 1
					}
				]
			}
		]
	},
	'军团': {
		'modes': [ # 模式 纯C、单刷或者组奶
			{
				'name': '军团组队',
				'teams': [
					{
						'requirement': 45 * 20,
						'playerCount': 4
					}
				],
				'globalBuff': 20 # 系统奶系数 队伍中有奶时这一项不参与评分
			},
			{
				'name': '军团单刷',
				'teams': [
					{
						'requirement': 10,
						'playerCount': 1
					}
				]
			}
		]
	}
}

# coding=utf-8

# 站街奶量转伤害倍率
HEALER_WEIGHT_COEFFICIENT = 1.0 / 200.0

RoleData = {
	'tr': [
		{
			'names': ['战法', '渣男'],
			'isHealer': False,
			'weight': 70
		},
		# {
		# 	'names': ['精灵', '君狂笑'],
		# 	'isHealer': False,
		# 	'weight': 22
		# },
		{
			'names': ['忍者', '午觉', '睡午觉', '要睡午觉'],
			'isHealer': False,
			'weight': 18
		},
		# {
		# 	'names': ['龙神'],
		# 	'isHealer': False,
		# 	'weight': 11
		# }
	],
	'drt': [
		{
			'names': ['弹药', '弹雨', '牡丹', '女弹药', '大号'],
			'isHealer': False,
			'weight': 58
		},
		{
			'names': ['奥格妮', '奥格尼', '奶妈', '奶'],
			'isHealer': True,
			'weight': 6220 * 1.15 # 站街三攻 * 奶妈系数
		},
		# {
		# 	'names': ['花花', '气功', '女气功', '光兵'],
		# 	'isHealer': False,
		# 	'weight': 25
		# },
		# {
		# 	'names': ['漫游', '漫海游云', '女漫游', '女漫'],
		# 	'isHealer': False,
		# 	'weight': 20
		# }
	],
	'lxj': [
		{
			'names': ['风男', '风法'],
			'isHealer': False,
			'weight': 22
		},
		# {
		# 	'names': ['冰洁', '冰姐'],
		# 	'isHealer': False,
		# 	'weight': 12.1
		# }
	],
	'jiao': [
		# {
		# 	'names': ['魔道', '井盖'],
		# 	'isHealer': False,
		# 	'weight': 46.6
		# },
		# {
		# 	'names': ['刃影'],
		# 	'isHealer': False,
		# 	'weight': 36.8
		# },
		# {
		# 	'names': ['剑宗', '剑魔'],
		# 	'isHealer': False,
		# 	'weight': 15.7
		# },
		{
			'names': ['奶萝', '奶', '奶妈'],
			'isHealer': True,
			'weight': 5824 * 1.25
		}
	],
	'gxy': [
		# {
		# 	'names': ['倏忽', '剑魔', '变身奶'],
		# 	'isHealer': False,
		# 	'weight': 42.5
		# },
		# {
		# 	'names': ['四姨', '七月', '柒月', '魅魔奶'],
		# 	'isHealer': False,
		# 	'weight': 30
		# },
		{
			'names': ['云VS巅峰', '奶爸'],
			'isHealer': True,
			'weight': 5800
		}
	],
	'why': [
		{
			'names': ['召唤'],
			'isHealer': False,
			'weight': 20
		}
	],
	'xlx': [
		# {
		# 	'names': ['花花', '气功', '女气功', '光兵'],
		# 	'isHealer': False,
		# 	'weight': 46
		# },
		# {
		# 	'names': ['元素', '人间不信'],
		# 	'isHealer': False,
		# 	'weight': 16.8
		# },
		{
			'names': ['奶萝'],
			'isHealer': True,
			'weight': 5000 * 1.25
		}
	],
	'wzr': [
		{
			'names': ['风男'],
			'isHealer': False,
			'weight': 20
		},
	],
	'zc': [
		{
			'names': ['奶爸'],
			'isHealer': True,
			'weight': 6500 # ?
		},
	],
	'hc': [
		{
			'names': ['棉筱朵', '元素'],
			'isHealer': False,
			'weight': 25
		},
	],
	'cww': [
		{
			'names': ['剑帝'],
			'isHealer': False,
			'weight': 60
		},
	],
	'默默': [
		{
			'names': ['红眼'],
			'isHealer': False,
			'weight': 60
		},
		{
			'names': ['淑润', '奶妈'],
			'isHealer': True,
			'weight': 5800
		},
		# {
		# 	'names': ['大枪'],
		# 	'isHealer': False,
		# 	'weight': 40
		# },
	]
}

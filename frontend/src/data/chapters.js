// 游戏章节数据
export const chapters = {
  13: {
    id: 13,
    title: '第13章 活力椰汁爽',
    totalPages: 6,
    content: {
      1: [
        {
          type: 'narrative',
          text: '航海日志提供了很多方便的功能。但离开航海日志，这世界简直和现实没区别。'
        },
        {
          type: 'action',
          text: '像砍树，是个力气活，也是技术活，尤其石斧还不怎么锋利，震手。'
        },
        {
          type: 'status',
          text: '砍下这棵最大的椰子树，杨逸精力直接扣了13点，只剩30点。'
        },
        {
          type: 'thought',
          text: '满打满算，满精力，他最多也就砍个五六棵树。再多就不行了，精力低于30，有昏厥的风险。'
        }
      ],
      2: [
        {
          type: 'discovery',
          text: '树倒后，杨逸立刻去捡椰子，刚拿起来，脸上就露出喜色。'
        },
        {
          type: 'item',
          text: '【名称：活力椰子】【类型：食物】【简介：这是一种罕见的特殊椰子，富含维生素和矿物质，里面的椰汁可以提高精力恢复速度。】'
        },
        {
          type: 'action',
          text: '杨逸二话不说，劈开一个椰子痛饮起来，获得了精力恢复加速的buff。'
        },
        {
          type: 'narrative',
          text: '这东西，正是杨逸急缺的，这一趟算是赚大了。'
        }
      ],
      3: [
        {
          type: 'discovery',
          text: '他打开青铜宝箱，里面立刻掉出几个光球，触摸之后变成了三件道具。'
        },
        {
          type: 'item',
          text: '【名称：活力椰汁爽配方】【类型：配方】【品质：良品】【简介：使用后获得活力椰汁爽的配方，需要试剂瓶，盐，活力椰子。】'
        },
        {
          type: 'item',
          text: '【名称：可食用海盐500克】【类型：食物】【简介：调味品，可增加风味，补充盐分。】'
        },
        {
          type: 'item',
          text: '【名称：试剂架】【种类：工具】【品质：良品】【简介：制作各种试剂必不可缺的工具，可用水晶合成。它可以提供试剂瓶，试剂喝完后，试剂瓶将消失。】'
        }
      ],
      4: [
        {
          type: 'action',
          text: '一个宝箱，不仅有配方，还有配方所需的其他两种素材。杨逸大喜，立刻就用掉了配方，然后开始动手调配活力椰汁爽。'
        },
        {
          type: 'crafting',
          text: '所需素材：活力椰子*1，盐10克。必备工具：试剂架'
        },
        {
          type: 'item',
          text: '【名称：活力椰汁爽】【种类：消耗品】【品质：良品】【简介：一款让人活力四射的饮料。可恢复10精力，提高精力恢复速度50%，持续8小时。每次生效间隔24小时。】'
        },
        {
          type: 'narrative',
          text: '杨逸笑了，转头看向海岸线上，那满满当当的椰子，手里的斧头舞出了花。'
        }
      ],
      5: [
        {
          type: 'action',
          text: '反正精力快到30，他就躺在沙滩上休息，等恢复了，就继续去砍树。'
        },
        {
          type: 'narrative',
          text: '到傍晚，他一共砍了四棵树，共获得38个活力椰子，43木料，统统运回了梦魇号。'
        },
        {
          type: 'thought',
          text: '他暂时不准备离开，准备在船上过一夜，第二天接着砍。'
        },
        {
          type: 'discovery',
          text: '但在回去前，他有了新发现。'
        }
      ],
      6: [
        {
          type: 'discovery',
          text: '沙滩上有一条晶莹发光的痕迹，距离杨逸仅百余米。天色变暗，这些痕迹发出微光，这才被杨逸注意到。'
        },
        {
          type: 'investigation',
          text: '这痕迹直通岛内，发光的物质是某种生物体表的粘液，腥臭难闻。'
        },
        {
          type: 'analysis',
          text: '他顺着痕迹往岛内走了两步。从形状上看，这像某种蛇一般的动物，在地上爬过留下的痕迹。杨逸用手掌量了一下，这蛇至少有半米粗，体型不小！'
        },
        {
          type: 'thought',
          text: '"没用枪果然是正确的！"杨逸改了主意，不打算在岸边过夜，准备离远一些，因为岛上...还有某种大型生物。'
        }
      ]
    },
    choices: {
      6: [
        {
          id: 'investigate_trail',
          text: '跟随发光痕迹，深入岛屿调查',
          energyCost: 20,
          risk: 85,
          requirement: '装备武器',
          consequences: {
            success: { chapter: 14, page: 1 },
            failure: { sanity: -15, health: -20 }
          }
        },
        {
          id: 'return_ship_safe',
          text: '立即返回船只，远离危险',
          energyCost: 5,
          risk: 20,
          requirement: null,
          consequences: {
            success: { chapter: 14, page: 3 }
          }
        },
        {
          id: 'set_trap',
          text: '在沙滩设置陷阱，等待生物出现',
          energyCost: 15,
          risk: 60,
          requirement: '制作材料',
          consequences: {
            success: { chapter: 14, page: 2 },
            failure: { chapter: 14, page: 1 }
          }
        }
      ]
    },
    rewards: {
      items: [
        {
          id: 'vitality_coconut',
          name: '活力椰子',
          quantity: 38,
          quality: 'rare'
        },
        {
          id: 'wood',
          name: '木料',
          quantity: 43,
          quality: 'common'
        },
        {
          id: 'vitality_drink_recipe',
          name: '活力椰汁爽配方',
          quantity: 1,
          quality: 'good'
        },
        {
          id: 'sea_salt',
          name: '可食用海盐',
          quantity: 500,
          quality: 'common'
        },
        {
          id: 'reagent_rack',
          name: '试剂架',
          quantity: 1,
          quality: 'good'
        }
      ],
      experience: 150,
      statusEffects: [
        {
          id: 'energy_recovery_boost',
          name: '精力恢复加速',
          duration: 28800, // 8小时
          effect: { energyRecovery: 1.5 }
        }
      ]
    }
  },

  14: {
    id: 14,
    title: '第14章 我手里有枪',
    totalPages: 8,
    content: {
      1: [
        {
          type: 'nightmare',
          text: '杨逸做了一个噩梦。梦里，他见到了三名姿色绝美的女子，围成一圈，默默注视着他。'
        },
        {
          type: 'horror',
          text: '突然，画风突变，一名女子拿出一件物品啃食起来，细细咀嚼，嘴角鲜血淋漓。杨逸起初还有点懵，定睛一看后才发现，那好像是自己的右臂！'
        },
        {
          type: 'realization',
          text: '而且他看清楚了这些女子的样貌，虽然上半身是人，但自腰以下却长出了鱼鳞，再往下更是变成了鱼尾。'
        },
        {
          type: 'pain',
          text: '自己的手臂则已经断裂，一股剧痛直冲天灵。'
        }
      ],
      2: [
        {
          type: 'awakening',
          text: '"艹！"杨逸被剧痛弄醒了，发现自己浑身赤裸，躺在滑腻的地板上。'
        },
        {
          type: 'environment',
          text: '这里光线幽暗，应该是某个洞窟，墙上、地上到处都是那种散发荧光的液体，像是软体动物在上面爬过，残留下来的粘液。'
        },
        {
          type: 'disgust',
          text: '自己身上更是覆盖有厚厚一层，闻一下更是提神醒脑，三日忘食！'
        },
        {
          type: 'relief',
          text: '他立刻看向右边。还好，他右臂完好无损。'
        }
      ],
      3: [
        {
          type: 'encounter',
          text: '疼痛的源头是一位女子，她正用那一口贝齿，狠狠咬在杨逸手臂上，入肉三分，疼的杨逸龇牙咧嘴。'
        },
        {
          type: 'dialogue',
          text: '"松口，你属狗吗，咬我干什么！"杨逸怒骂道。'
        },
        {
          type: 'dialogue',
          text: '女子听见声音，终于松了口，在他肩膀上留下两排深深的牙印。"醒了？我还以为你没醒呢！"女子不满道，鲜红的眼眸妖艳欲滴。'
        },
        {
          type: 'dialogue',
          text: '"我都坐起来了，你说我醒没醒？"杨逸没好气道，不停揉搓自己的右臂，似乎被咬疼了。'
        }
      ],
      4: [
        {
          type: 'observation',
          text: '他打量这名女子。一副典型的亚洲人面孔，挺漂亮的，身材纤细，似乎有些营养不良，皮肤为诱人的小麦色。'
        },
        {
          type: 'observation',
          text: '她被一团不知名的水草捆住，地上还有她爬过来的痕迹，应该费了不少的功夫。'
        },
        {
          type: 'dialogue',
          text: '"你是？"杨逸头疼欲裂，问道。'
        },
        {
          type: 'dialogue',
          text: '"你被海妖魅惑了，是我救了你的命！"女子提醒道。'
        }
      ],
      5: [
        {
          type: 'status_check',
          text: '杨逸闻言，立刻查看活动日志。上面是一连串的魅惑提醒。自己的理智也处在一个微妙的数字上。理智：51/100'
        },
        {
          type: 'dialogue',
          text: '"这伙海妖居然三天都没舍得吃你，还把你养的白白胖胖，真是个奇迹！"女子看着杨逸，继续道。'
        },
        {
          type: 'realization',
          text: '杨逸也明白过来。"我被海妖俘虏了，时间已经过去了三天？""没错！"'
        },
        {
          type: 'information',
          text: '"不止一只海妖？""是的，一共有三只，她们应该是一种群居生物，擅长用歌声魅惑男性，作为媾和的对象....与食物！"'
        }
      ],
      6: [
        {
          type: 'horror_realization',
          text: '杨逸看向自己的身体，发现不着寸缕，忽觉得一阵恶寒！不远处，是散落在地的海盗服，以及锈蚀的燧发枪。'
        },
        {
          type: 'exposition',
          text: '"她们是传说中的奇幻生物，但在这个世界真实存在，习性也和传说类似....."女子继续说着，似乎对海妖这种生物很感兴趣。'
        },
        {
          type: 'action',
          text: '杨逸却只觉得一阵后怕，立刻穿上海盗服，抓起地上的燧发枪。'
        },
        {
          type: 'status',
          text: '【穿上血迹斑斑的海盗服，莫名感到一股寒意，理智下降1】这时他理智正好卡在50，再低一点便会进入癫狂状态。'
        }
      ],
      7: [
        {
          type: 'dialogue',
          text: '"这粘液好恶心啊，海妖怎么还会分泌粘液！"'
        },
        {
          type: 'explanation',
          text: '"在海里，很多软体或者没鳞片的生物都会分泌粘液保护自己，所以海妖有粘液也很正常！而且这粘液在黑暗中会发出荧光，可以照亮吸引猎物，类似鮟鱇鱼的灯笼，方便展现自己诱人的身段，进而辅助完成整个捕猎过程...."'
        },
        {
          type: 'suspicion',
          text: '"你是玩家吧，为何会出现在这里？"杨逸突然问道。这女人来历不明，全身透着古怪，尤其那双鲜艳的红眸，让人不寒而栗，和他噩梦里见过的那双眼睛，一模一样。'
        },
        {
          type: 'warning',
          text: '这让杨逸警惕心爆棚。尽管对方看起来并无恶意，似乎在尝试救自己。'
        }
      ],
      8: [
        {
          type: 'dialogue',
          text: '"我叫苏娜，是路过的玩家，不幸被海妖给抓了，成了应急储备粮。"'
        },
        {
          type: 'dialogue',
          text: '"你不是说海妖的目标都是男性吗，怎么会抓你？"杨逸问道。'
        },
        {
          type: 'deception',
          text: '对此，苏娜早准备好了说辞。她并不打算说实话，而是转头示意一处角落。"我不是一个人，我的同伙已经被海妖吃了。但不知为什么，她们没有吃你。"'
        },
        {
          type: 'horror_evidence',
          text: '杨逸顺着她的视线看去。那里摆着一具未被吃完的男性尸体，已经腐烂，腹腔被打开，内脏被掏空，面孔狰狞，四肢不全，生前恐怕遭受了非人的虐待......而在尸体附近，还散落有不少被吃干抹净的人类骸骨，彰显海妖的凶性。'
        }
      ]
    },
    choices: {
      8: [
        {
          id: 'trust_suna',
          text: '相信苏娜，与她合作逃脱',
          energyCost: 10,
          risk: 40,
          requirement: null,
          consequences: {
            success: { chapter: 15, page: 1 },
            failure: { sanity: -10 }
          }
        },
        {
          id: 'distrust_suna',
          text: '保持警惕，独自寻找出路',
          energyCost: 15,
          risk: 70,
          requirement: '理智 > 40',
          consequences: {
            success: { chapter: 15, page: 2 },
            failure: { health: -15, sanity: -5 }
          }
        },
        {
          id: 'interrogate_suna',
          text: '质疑苏娜的身份，要求她说实话',
          energyCost: 5,
          risk: 30,
          requirement: null,
          consequences: {
            success: { chapter: 15, page: 3 },
            failure: { chapter: 15, page: 1 }
          }
        }
      ]
    },
    statusEffects: [
      {
        id: 'siren_charm_residue',
        name: '海妖魅惑残留',
        duration: 3600, // 1小时
        effect: { sanity: -1, charm_resistance: -20 }
      },
      {
        id: 'slime_coating',
        name: '粘液覆盖',
        duration: 1800, // 30分钟
        effect: { disgust: 5, stealth: -10 }
      }
    ],
    environment: {
      location: '海妖洞穴',
      lighting: 'dim_bioluminescent',
      temperature: 'cold_damp',
      hazards: ['slippery_floor', 'toxic_fumes', 'unstable_ceiling'],
      exits: ['underwater_tunnel', 'hidden_passage', 'main_entrance']
    }
  }
}

// 章节间的连接关系
export const chapterConnections = {
  13: {
    next: 14,
    branches: {
      'investigate_trail': { chapter: 14, page: 1 },
      'return_ship_safe': { chapter: 14, page: 3 },
      'set_trap': { chapter: 14, page: 2 }
    }
  },
  14: {
    previous: 13,
    next: 15,
    branches: {
      'trust_suna': { chapter: 15, page: 1 },
      'distrust_suna': { chapter: 15, page: 2 },
      'interrogate_suna': { chapter: 15, page: 3 }
    }
  }
}

// 获取章节数据的辅助函数
export function getChapter(chapterId) {
  return chapters[chapterId] || null
}

export function getChapterContent(chapterId, page) {
  const chapter = chapters[chapterId]
  if (!chapter) return null
  
  return chapter.content[page] || null
}

export function getChapterChoices(chapterId, page) {
  const chapter = chapters[chapterId]
  if (!chapter) return []
  
  return chapter.choices[page] || []
}

export function getNextChapter(currentChapter, choice = null) {
  const connections = chapterConnections[currentChapter]
  if (!connections) return null
  
  if (choice && connections.branches[choice.id]) {
    return connections.branches[choice.id]
  }
  
  return { chapter: connections.next, page: 1 }
}

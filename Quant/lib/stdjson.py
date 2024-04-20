class StdJson():
    @staticmethod
    def error_msg(msg):
        error_msg ={
        "msg_type": "interactive",
            "card":{
                "config": {
                    "wide_screen_mode": True
                },
                "header": {
                    "template": "red",
                    "title": {
                    "content": "紧急通知",
                    "tag": "plain_text"
                    }
                },
                "i18n_elements": {
                    "zh_cn": [
                    {
                        "fields": [
                        {
                            "is_short": True,
                            "text": {
                            "content": "**时间**\n{}".format(msg['time']),
                            "tag": "lark_md"
                            }
                        },
                        {
                            "is_short": True,
                            "text": {
                            "content": "**标的**\n{}".format(msg['symbol']),
                            "tag": "lark_md"
                            }
                        }
                        ],
                        "tag": "div"
                    },
                    {
                        "tag": "div",
                        "fields": [
                        {
                            "is_short": True,
                            "text": {
                            "tag": "lark_md",
                            "content": "**等级**\n{}".format(msg['level'])
                            }
                        },
                        {
                            "is_short": True,
                            "text": {
                            "tag": "lark_md",
                            "content": "**错误类型：**\n{}".format(msg['type'])
                            }
                        }
                        ]
                    },
                    {
                        "tag": "div",
                        "text": {
                        "content": "<at id=all></at>\n{}".format(msg['content']),
                        "tag": "lark_md"
                        }
                    },
                    {
                        "actions": [
                        {
                            "tag": "button",
                            "text": {
                            "content": "我已知悉",
                            "tag": "plain_text"
                            },
                            "type": "primary",
                            "value": {
                            "key": "value"
                            }
                        }
                        ],
                        "tag": "action"
                    },
                    {
                        "tag": "hr"
                    },
                    {
                        "elements": [
                        {
                            "content": "[来自应急通知]",
                            "tag": "lark_md"
                        }
                        ],
                        "tag": "note"
                    }
                    ]
                }
            }
        }
        return error_msg

    @staticmethod
    def trade_msg(msg):
        trade_msg = {
        "msg_type": "interactive",
        "card":{
                "config": {
                    "wide_screen_mode": True
                },
                "header": {
                    "template": "green"  if msg['type'] == "long" else "red",
                    "title": {
                    "content": "【{}】开仓".format("做多" if msg['type']=='long' else "做空"),
                    "tag": "plain_text"
                    }
                },
                "i18n_elements": {
                    "zh_cn": [
                        {
                            "fields": [
                            {
                                "is_short": True,
                                "text": {
                                "content": "**时间**\n{}".format(msg['time']),
                                "tag": "lark_md"
                                }
                            },
                            {
                                "is_short": True,
                                "text": {
                                "content": "**标的**\n{}".format(msg['symbol']),
                                "tag": "lark_md"
                                }
                            }
                            ],
                            "tag": "div"
                        },
                        {
                        "tag": "div",
                        "fields": 
                        [
                            {
                                "is_short": True,
                                "text": {
                                "tag": "lark_md",
                                "content": "**持仓**\n{:.2f}".format(float(msg['oi']))
                                }
                            },
                            { 
                                "is_short": True,
                                "text": {
                                "tag": "lark_md",
                                "content": "**多空比**\n{:.2f}".format(float(msg['lr']))
                                }
                            }
                        ]
                        },
                        {
                        "tag": "div",
                        "fields": [
                        {
                            "is_short": True,
                            "text": {
                            "tag": "lark_md",
                            "content": "**价格(USD)**\n{:.2f}".format(msg['price'])
                            }
                        },
                        {
                            "is_short": True,
                            "text": {
                            "tag": "lark_md",
                            "content": "**数量**\n{:.2f}".format(msg['vol'])
                            }
                        }
                    ]
                    },]
                }
            }
        }
        return trade_msg

    @staticmethod
    def cover_msg(msg):
        cover_msg =  {
        "msg_type": "interactive",
        "card":{ 
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "yellow",
                "title": {
                "content": "【{}】平仓".format("平多" if msg['type']=="long" else "平空"),
                "tag": "plain_text"
                }
            },
            "i18n_elements": {
                "zh_cn": [
                {
                    "fields": [
                    {
                        "is_short": True,
                        "text": {
                        "content": "**时间**\n{}".format(msg['time']),
                        "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                        "content": "**标的**\n{}".format(msg['symbol']),
                        "tag": "lark_md"
                        }
                    }
                    ],
                    "tag": "div"
                },
                {
                    "tag": "div",
                    "fields": 
                    [
                        {
                            "is_short": True,
                            "text": {
                            "tag": "lark_md",
                            "content": "**持仓**\n{:.2f}".format(float(msg['oi']))
                            }
                        },
                        { 
                            "is_short": True,
                            "text": {
                            "tag": "lark_md",
                            "content": "**多空比**\n{:.2f}".format(float(msg['lr']))
                            }
                        }
                    ]
                },
                {
                    "tag": "div",
                    "fields": [
                        {
                            "is_short": True,
                            "text": {
                            "tag": "lark_md",
                            "content": "**价格(USD)**\n{:.2f}".format(msg['price'])
                            }
                        },
                        {
                            "is_short": True,
                            "text": {
                            "tag": "lark_md",
                            "content": "**收益率**\n{:.3f}%".format(msg['return']*100)
                            }
                        }
                    ]
                },
        ]}
        }
        }
        return cover_msg




        



























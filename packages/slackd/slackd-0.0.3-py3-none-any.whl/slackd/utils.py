
def create_message(**kwargs):
    messageBody = {
    "text": "Hey <@U01TNM2CZLG>, new failed DBT tests", 
    "attachments": [ 
        {
        "color": "#f44336",
        "fields": [
            {
            "title": "Invocation ID",
            "value": kwargs["invocation_id"],
            "short": True
            },
            {
            "title": "Failed Table",
            "value": kwargs["table_name"],
            "short": True
            },
            {
            "title": "Environment",
            "value": "Development",
            "short": True
            },
            {
            "title": "Failed Timestamp",
            "value": kwargs["timestamp"],
            "short": True
            },
            {
            "title": "Please take actions to deal with that failed tests",
            "value": "Please take the following actions to deal with this failed tests",
            "short": False 
            }
        ],
        "actions": [ 
            {
            "type": "button",
            "text": "Take a look",
            "url": "http://example.com" 
            },
            {
            "type": "button",
            "text": "Fixed",
            "style": "primary", 
            "url": "http://example.com"
            },
            {
            "type": "button",
            "text": "Ignore and walk away",
            "style": "danger",
            "url": "http://example.com/order/1/cancel",
            "confirm": {
                "title": "Sorry there is no way to ignore and walk away",
                "text": "Choose again, now only 2 option",
                "ok_text": "Take a look",
                "dismiss_text": "Fixed"
            }
            }
        ]
        }
    ]
    }

    return messageBody
curl -v -X POST https://api.line.me/v2/bot/richmenu \
-H 'Authorization: Bearer H/u5OdbU0fquaqOAuI3z1Hq8R0hAWS5RQqjzWBgjZdajxWysB8KCxgkitqDplssZDcgIINfAfD0+RnhS1It8gcfo+/HM5Ovo/PudGRVswVzMLNqe4nafuaaBofVWvIugdVERFvG8i1pMwKcj3tqR1AdB04t89/1O/w1cDnyilFU=' \
-H 'Content-Type: application/json' \
-d \
'{
    "size": {
      "width": 2500,
      "height": 1686
    },
    "selected": true,
    "name": "menu",
    "chatBarText": "選單",
    "areas": [
      {
        "bounds": {
          "x": 0,
          "y": 0,
          "width": 833,
          "height": 843
        },
        "action": {
          "type": "postback",
          "data": "個人資料",
          "displayText": "個人資料"
        }
      },
      {
        "bounds": {
          "x": 833,
          "y": 0,
          "width": 833,
          "height": 843
        },
        "action": {
          "type": "postback",
          "data": "活動資訊",
          "displayText": "活動資訊"
        }
      },
      {
        "bounds": {
          "x": 1666,
          "y": 0,
          "width": 834,
          "height": 843
        },
        "action": {
          "type": "uri",
          "label": "Find",
          "uri": "line://app/1653599527-KjlZpO3N?page=find"
        }
      },
      {
        "bounds": {
          "x": 0,
          "y": 843,
          "width": 833,
          "height": 843
        },
        "action": {
          "type": "uri",
          "label": "QA",
          "uri": "https://haoqi.one/tgif_slido"
        }
      },
      {
        "bounds": {
          "x": 833,
          "y": 843,
          "width": 833,
          "height": 843
        },
        "action": {
          "type": "uri",
          "label": "collect",
          "uri": "https://line.me/R/ch/1432061434/234mvgki?us=LINE&um=ClientOA&uca=Richmenu"
        }
      },
      {
        "bounds": {
          "x": 1666,
          "y": 843,
          "width": 834,
          "height": 843
        },
        "action": {
          "type": "postback",
          "data": "抽卡",
          "displayText": "抽卡"
        }
      }
   ]
}'

return {"richMenuId":"richmenu-ec3305da20d7fd5a4d94e89fa8cd392f"}

curl -v -X POST https://api.line.me/v2/bot/richmenu/richmenu-ec3305da20d7fd5a4d94e89fa8cd392f/content \
-H "Authorization: Bearer H/u5OdbU0fquaqOAuI3z1Hq8R0hAWS5RQqjzWBgjZdajxWysB8KCxgkitqDplssZDcgIINfAfD0+RnhS1It8gcfo+/HM5Ovo/PudGRVswVzMLNqe4nafuaaBofVWvIugdVERFvG8i1pMwKcj3tqR1AdB04t89/1O/w1cDnyilFU=' \
-H 'Content-Type: application/json" \
-H "Content-Type: image/png" \
-T /Users/toooair/Downloads/menu.png

return {}

-----------------------------------login

curl -v -X POST https://api.line.me/v2/bot/richmenu \
-H 'Authorization: Bearer H/u5OdbU0fquaqOAuI3z1Hq8R0hAWS5RQqjzWBgjZdajxWysB8KCxgkitqDplssZDcgIINfAfD0+RnhS1It8gcfo+/HM5Ovo/PudGRVswVzMLNqe4nafuaaBofVWvIugdVERFvG8i1pMwKcj3tqR1AdB04t89/1O/w1cDnyilFU=' \
-H 'Content-Type: application/json' \
-d \
'{
    "size": {
      "width": 2500,
      "height": 843
    },
    "selected": true,
    "name": "login",
    "chatBarText": "選單",
    "areas": [
      {
        "bounds": {
          "x": 0,
          "y": 0,
          "width": 2500,
          "height": 843
        },
        "action": {
          "type": "uri",
          "label": "login",
          "uri": "line://app/1653599527-KjlZpO3N?page=login"
        }
      }
   ]
}'

{"richMenuId":"richmenu-5b8c6af15e3bf3880f05c71ebea67427"}

curl -v -X POST https://api.line.me/v2/bot/richmenu/richmenu-5b8c6af15e3bf3880f05c71ebea67427/content \
-H "Authorization: Bearer H/u5OdbU0fquaqOAuI3z1Hq8R0hAWS5RQqjzWBgjZdajxWysB8KCxgkitqDplssZDcgIINfAfD0+RnhS1It8gcfo+/HM5Ovo/PudGRVswVzMLNqe4nafuaaBofVWvIugdVERFvG8i1pMwKcj3tqR1AdB04t89/1O/w1cDnyilFU=' \
-H 'Content-Type: application/json" \
-H "Content-Type: image/png" \
-T /Users/toooair/Downloads/login.png

postman
curl -v -X POST https://api.line.me/v2/bot/user/all/richmenu/richmenu-5b8c6af15e3bf3880f05c71ebea67427 \
-H "Authorization: Bearer H/u5OdbU0fquaqOAuI3z1Hq8R0hAWS5RQqjzWBgjZdajxWysB8KCxgkitqDplssZDcgIINfAfD0+RnhS1It8gcfo+/HM5Ovo/PudGRVswVzMLNqe4nafuaaBofVWvIugdVERFvG8i1pMwKcj3tqR1AdB04t89/1O/w1cDnyilFU="

return {}
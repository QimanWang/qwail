# qwail (gmail)

Django app that ingest your gmail metadata. Then you can see stats about your email and batch delete unwanted emails.

## setup

run app
```shell
pip install requirements.txt

python manage.py migrate
python manage.py makemigrations gmail

python manage.py runserver

```

## Architecture

```
get user profile:
{'emailAddress': 'wangqiman0111@gmail.com', 'messagesTotal': 81955, 'threadsTotal': 76605, 'historyId': '15612103'}
Profile('emailAddress'='wangqiman0111@gmail.com', 'messagesTotal'= 81955, 'threadsTotal'= 76605, 'historyId'= '15612103')

get labels:
[{'id': 'INBOX', 'name': 'INBOX', 'messageListVisibility': 'hide', 'labelListVisibility': 'labelShow', 'type': 'system'},
    ...]
Label(id = 'INBOX', name = 'INBOX','messageListVisibility'= 'hide', 'labelListVisibility'=  'labelShow', type'= 'system'  )

get message ids
[{'id': '17a4a8c83e4dbd9f', 'threadId': '17a4a8c83e4dbd9f'},...]
Message(id = '17a4a8c83e4dbd9f', 'threadId'= '17a4a8c83e4dbd9f')

get message 
Message(id = '17a4a8c83e4dbd9f', 'threadId'= '17a4a8c83e4dbd9f'). update(
{
  "id": string,
  "threadId": string,
  "labelIds": [
    string
  ],
  "snippet": string,
  "historyId": string,
  "internalDate": string,
  "payload": {
    object (MessagePart)
  },
  "sizeEstimate": integer,
  "raw": string
}
)


```
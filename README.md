# API Endpoint

```markdown
할거 ㅇㅁㅇ
request : 
 - method:
 - request url: 
 - parameter: param name, param type, madatory(y,n), description 
response: 
	- response example with field and value
```

# *HTTP API*

## CCTV API

### `POST` /api/v1/cctv

- 새로운 CCTV 정보를 등록합니다

### `GET` /api/v1/cctv

- CCTV 의 목록을 모두 가져옵니다

### `GET` /api/v1/cctv/{id}

- id 에 해당하는 cctv의 정보를 가져옵니다 가져옵니다

### `GET` /api/v1/cctv/{id}/video  소켓으로 옮기기

### `DELETE` /api/v1/cctv/{id}

- id 에 해당하는 cctv의 정보를 삭제합니다

### `PUT` /api/v1/cctv/{id}

- id 에 해당하는 cctv 의 정보를 수정합니다

## BOT API

### `POST` /api/v1/bot

- 새로운 로봇의 정보를 등록합니다

### `GET` /api/v1/bot

- 로봇의 정보를 모두 가져옵니다

### `GET` /api/v1/bot/{id}

- id 에 해당하는 로봇의 정보를 가져옵니다

### `DELETE` /api/v1/bot/{id}

- id 에 해당하는 로봇의 정보를 삭제합니다

### `PUT` /api/v1/bot/{id}

- id 에 해당하는 로봇의 정보를 수정합니다

## *WebSocket API*

## Logging API

## Alert API
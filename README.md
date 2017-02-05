### 配置
生成 `COOKIE_SECRET` 的方法：
```python
>>>import base64
>>>import uuid
>>>base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
```
### 

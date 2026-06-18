# 06_API_SCHEMA.md｜易元命名 API 设计文档

## 1. API 设计原则

1. 输入输出结构化。
2. 所有接口返回 request_id。
3. 所有名字结果可追溯。
4. 错误信息必须清晰。
5. 不在 API 层直接拼装业务逻辑。

## 2. POST /api/names/generate

用途：生成候选名字。

请求：

```json
{
  "surname": "陈",
  "gender": "female",
  "birth_datetime": "2026-06-18 09:30",
  "calendar_type": "solar",
  "birth_place": "广东省汕头市",
  "name_length": 2,
  "style_preferences": ["温润", "诗意"],
  "banned_chars": ["梓", "轩"],
  "liked_chars": ["清"],
  "avoid_hot_names": true,
  "need_teochew_check": true,
  "need_culture_origin": true
}
```

响应：

```json
{
  "request_id": "uuid",
  "profile": {},
  "results": [
    {
      "name": "陈清宁",
      "score": 91,
      "pinyin": "chén qīng níng",
      "summary": "清澈安宁，温润明朗。",
      "meaning": {},
      "culture_origin": {},
      "pronunciation": {},
      "teochew": {},
      "bazi": {},
      "zodiac": {},
      "popularity": {},
      "warnings": [],
      "recommendation_reason": "..."
    }
  ]
}
```

## 3. GET /api/names/{request_id}/{name}

用途：查看名字详情。

响应：NameCandidate 完整结构。

## 4. POST /api/names/regenerate

用途：换一批。

请求：

```json
{
  "request_id": "uuid",
  "locked_chars": ["清"],
  "excluded_chars": ["轩"],
  "excluded_names": ["陈清宁"]
}
```

## 5. POST /api/favorites

用途：收藏名字。

请求：

```json
{
  "request_id": "uuid",
  "name": "陈清宁"
}
```

## 6. GET /api/favorites

用途：获取收藏列表。

响应：

```json
{
  "favorites": []
}
```

## 7. 错误码

| code | 说明 |
|---|---|
| INVALID_INPUT | 输入不合法 |
| KNOWLEDGE_MISSING | 知识库缺失 |
| GENERATION_FAILED | 生成失败 |
| QUALITY_REJECTED | 质量审查不通过 |
| NOT_FOUND | 资源不存在 |
```

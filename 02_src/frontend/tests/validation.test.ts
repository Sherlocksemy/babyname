import assert from "node:assert/strict";
import { test } from "node:test";

import { splitChars, validateProfile, type ProfileForm } from "../lib/validation";

const validProfile: ProfileForm = {
  surname: "林",
  gender: "male",
  calendar_type: "solar",
  birth_year: 2025,
  birth_month: 3,
  birth_day: 1,
  birth_hour: 8,
  birth_minute: 30,
  is_leap_month: false,
  birth_province: "广东省",
  birth_city: "汕头市",
  timezone: "Asia/Shanghai",
  region: "teochew",
  style_preferences: ["书卷清雅"],
  liked_chars: [],
  blocked_chars: [],
  generation_seed: null
};

test("valid profile has no form errors", () => {
  assert.deepEqual(validateProfile(validProfile), {});
});

test("unsupported city is rejected", () => {
  const errors = validateProfile({ ...validProfile, birth_city: "广州市" });
  assert.equal(errors.birth_city, "当前MVP仅支持汕头、潮州、揭阳");
});

test("liked and blocked char conflict is rejected", () => {
  const errors = validateProfile({ ...validProfile, liked_chars: ["知"], blocked_chars: ["知"] });
  assert.equal(errors.blocked_chars, "喜欢字和禁用字冲突：知");
});

test("splitChars supports spaces and punctuation", () => {
  assert.deepEqual(splitChars("知 清，予、安"), ["知", "清", "予", "安"]);
});

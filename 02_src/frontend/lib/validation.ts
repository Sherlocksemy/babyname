export type ProfileForm = {
  surname: string;
  gender: string;
  calendar_type: "solar" | "lunar";
  birth_year: number;
  birth_month: number;
  birth_day: number;
  birth_hour: number;
  birth_minute: number;
  is_leap_month: boolean;
  birth_province: string;
  birth_city: string;
  timezone: string;
  region: string;
  style_preferences: string[];
  liked_chars: string[];
  blocked_chars: string[];
  generation_seed: number | null;
};

export type ValidationErrors = Record<string, string>;

export const SUPPORTED_CITIES = ["汕头市", "潮州市", "揭阳市"];

export function splitChars(value: string): string[] {
  return Array.from(value.replace(/[,\s，、]/g, "")).filter(Boolean);
}

export function validateProfile(profile: ProfileForm): ValidationErrors {
  const errors: ValidationErrors = {};
  if (!profile.surname.trim()) errors.surname = "请填写姓氏";
  if (profile.surname.trim().length > 2) errors.surname = "MVP仅支持单姓或双字复姓";
  if (!SUPPORTED_CITIES.includes(profile.birth_city)) errors.birth_city = "当前MVP仅支持汕头、潮州、揭阳";
  if (profile.birth_year < 1900 || profile.birth_year > 2100) errors.birth_year = "年份需在1900-2100之间";
  if (profile.birth_month < 1 || profile.birth_month > 12) errors.birth_month = "月份需在1-12之间";
  if (profile.birth_day < 1 || profile.birth_day > 31) errors.birth_day = "日期需在1-31之间";
  if (profile.birth_hour < 0 || profile.birth_hour > 23) errors.birth_hour = "小时需在0-23之间";
  if (profile.birth_minute < 0 || profile.birth_minute > 59) errors.birth_minute = "分钟需在0-59之间";
  const conflict = profile.liked_chars.find((char) => profile.blocked_chars.includes(char));
  if (conflict) errors.blocked_chars = `喜欢字和禁用字冲突：${conflict}`;
  return errors;
}

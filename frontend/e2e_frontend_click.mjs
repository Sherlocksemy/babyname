import { chromium } from "playwright";

const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const frontendUrl = process.env.FRONTEND_URL || "http://127.0.0.1:3000";

const browser = await chromium.launch({ headless: true, executablePath: chromePath });
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
const consoleErrors = [];
const apiEvents = [];

page.on("console", (msg) => {
  const text = msg.text();
  if (msg.type() === "error" && !text.includes("404") && !text.includes("favicon")) {
    consoleErrors.push(text);
  }
});
page.on("pageerror", (err) => consoleErrors.push(err.message));
page.on("request", (req) => {
  if (req.url().includes("/api/")) {
    apiEvents.push({ type: "request", method: req.method(), url: req.url() });
  }
});
page.on("response", (res) => {
  if (res.url().includes("/api/")) {
    apiEvents.push({ type: "response", status: res.status(), url: res.url() });
  }
});

await page.goto(frontendUrl, { waitUntil: "networkidle", timeout: 60000 });
await page.getByRole("button", { name: /生成名字/ }).click({ timeout: 10000 });
await page.waitForFunction(() => document.querySelectorAll(".card").length === 20, null, { timeout: 30000 });

const result = {
  cardCount: await page.locator(".card").count(),
  detailText: await page.locator(".detail").innerText(),
  apiEvents,
  consoleErrors,
  bodyText: (await page.locator("body").innerText()).slice(0, 2000),
};
await browser.close();

if (result.consoleErrors.length) {
  console.error(JSON.stringify(result, null, 2));
  process.exit(2);
}
if (!result.apiEvents.some((item) => item.type === "response" && item.status === 200)) {
  console.error(JSON.stringify(result, null, 2));
  process.exit(3);
}
if (result.cardCount !== 20 || !result.detailText.includes("文化出处")) {
  console.error(JSON.stringify(result, null, 2));
  process.exit(4);
}

console.log(JSON.stringify(result, null, 2));

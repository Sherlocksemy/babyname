import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "易元命名 Pro MVP",
  description: "宝宝命名顾问 MVP"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}

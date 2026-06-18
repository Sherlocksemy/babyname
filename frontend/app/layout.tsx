import "./styles.css";

export const metadata = {
  title: "易元命名",
  description: "知识库驱动的新生儿智能取名系统"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}

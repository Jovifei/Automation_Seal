# Medusa R2-R3 Session Cookie Adoption Plan

**状态：** `PLAN_READY_FOR_LOCAL_CODEX`

**目标：** 关闭 R2-R2 独立审核 Low F-1/F-2，不扩大 Commerce 权限。

## 1. 已验证根因链

Medusa v2.19.0 官方源码：

1. `/auth/session` POST 只写 `req.session.auth_context = req.auth_context`；
2. HTTP loader 使用 `express-session`；
3. production/staging 默认 `secure=true`；
4. 当前 Jovi Admin smoke 是 `127.0.0.1` HTTP；
5. secure cookie 不应在纯 HTTP transport 上下发；
6. 因此出现 `POST /auth/session = 200` 但无 `Set-Cookie` 与官方实现完全一致。

这比“dashboard 客户端 bug”更符合现场证据。

## 2. 最小变更原则

禁止：

- 修改 `@medusajs/medusa` 上游 session route；
- patch node_modules；
- 永久把 production cookie `secure=false`；
- Bearer token 绕过浏览器 session 作为最终 UI 验收；
- 在证据 JSON 中写硬编码“cookie issued”。

允许：

- 在 Jovi 自己的 `medusa-config.ts` 增加仅 synthetic loopback 可启用的 cookie override；
- 在 Docker/Compose synthetic namespace 显式声明开关；
- 增加 Playwright 真实 cookie-session E2E；
- 修正 browser evidence 生成逻辑为真实 header/cookie capture。

## 3. 推荐配置模式

伪代码：

```ts
const syntheticLoopbackHttp =
  process.env.JOVI_SYNTHETIC_LOOPBACK_HTTP === "true"

if (syntheticLoopbackHttp && process.env.JOVI_REAL_COMMERCE === "true") {
  throw new Error("SYNTHETIC_LOOPBACK_COOKIE_OVERRIDE_FORBIDDEN_IN_REAL_COMMERCE")
}

export default defineConfig({
  projectConfig: {
    // ... existing config
    cookieOptions: {
      sameSite: "lax",
      httpOnly: true,
      ...(syntheticLoopbackHttp ? { secure: false } : {}),
    },
  },
})
```

必须遵守：

- `JOVI_SYNTHETIC_LOOPBACK_HTTP=true` 只在 isolated/local synthetic Compose 中设置；
- 只允许绑定 `127.0.0.1` / internal Docker network；
- production deployment candidate 必须证明该变量未设置，且默认 `secure=true`；
- 不使用 `sameSite=none` 作为本地修复；v2.19.0 默认/官方安全方向是 `lax`。

## 4. Playwright 真实验收

测试必须通过真实浏览器网络链：

1. 打开 `http://127.0.0.1:<admin-port>/app/login`；
2. 提交 synthetic admin credentials；
3. 捕获 `POST /auth/user/emailpass`：200；
4. 捕获 `POST /auth/session`：200；
5. **从真实 response headers 读取 `set-cookie`，断言包含 `connect.sid`**；
6. browser context cookies 断言存在 `connect.sid`；
7. 页面离开 `/app/login`；
8. `/admin/users/me` 通过 cookie-session 返回 200（测试请求不得注入 Bearer）；
9. UI 导航到 Product；
10. UI 导航到 Order；
11. UI/只读 route 读取 Receipt/Entitlement；
12. refresh；
13. session 仍有效；
14. console fatal error=0；
15. pageerror=0；
16. failed request=0（允许预先定义的匿名 401 只能发生在登录前）；
17. external network request=0。

## 5. F-2 证据修复

旧证据存在硬编码 auth 描述。新 evidence 生成器必须记录结构化事实：

```json
{
  "emailpass_status": 200,
  "session_status": 200,
  "set_cookie_present": true,
  "set_cookie_name": "connect.sid",
  "browser_cookie_present": true,
  "users_me_cookie_session_status": 200,
  "bearer_used_for_ui_acceptance": false
}
```

禁止用人工文本替代捕获值。

## 6. 回归

R2-R3 改动后重新运行：

- TypeScript；
- Jest unit/integration natural exit；
- X2 first/replay；
- 10 concurrent；
- negative cases；
- transaction rollback；
- PID1 recovery；
- Oracle 7/7；
- SBOM/license；
- exact source manifest；
- deterministic build；
- secret scan；
- Admin cookie-session Playwright。

## 7. 退出门

只有以下全部成立，才能把 Low F-1/F-2 关闭：

- `R6_POST_IMPORT_PASS` 已先取得；
- cookie override 仅限 synthetic loopback；
- 浏览器拿到真实 `connect.sid`；
- UI 不再回 `/app/login`；
- refresh session 成功；
- production secure-cookie 默认未降低；
- evidence 不再硬编码；
- 完整 synthetic regression 通过；
- 新独立审核 PASS。

成功状态建议：`R2R3_ADMIN_SESSION_CLOSED_READY_FOR_FULL_SYNTHETIC_COMMERCE_E2E`。

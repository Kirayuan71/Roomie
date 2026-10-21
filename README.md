# Roomie · 室友搭子

React 19 + TypeScript + Tailwind CSS 4 的合租生活管理应用。奶油白、鼠尾草绿与暖橘配色，桌面侧栏与移动底栏布局，无需登录。

## 本地开发

需要 Node.js 20.19+（本环境已验证 Node 24）和 npm。

```bash
npm ci
npm run dev
```

```bash
npm test
npm run build
npm run preview
```

## 已实现

- 首页月历（清洁任务联动、年度生日、卫生检查与其他提醒）、日程增改删和完成状态；互动留言板支持发布、回复、点赞、编辑和删除。保留实时统计、今日待办、小家动态和快捷操作。
- 自动升级旧版 localStorage 数据，保留原账单和值日记录。日历和留言仍是浏览器本地演示，不支持跨设备共享。
- 账本新增/编辑/删除、参与人和自定义比例、月份筛选、分类图表、单笔结算与撤销、跨室友净额结算。
- 周日历、值日新增/编辑/删除、换班、截止时间、逾期标记、自动轮换、周期任务完成后创建下一次、本月贡献。
- 公共物品库存/阈值维护、消耗、采购清单、认领、补货、自动创建 AA 账单。
- 公约模板、增改删、全员同意生效、修改后重新投票、修改记录。设置中切换三位室友身份体验投票。
- 明确标注的本地助手演示：金额和付款人规则解析、固定公约模板、友好提醒模板。所有写入均需确认。
- localStorage 持久化（`roomie-v1`），小家设置中可重置。数据仅属于当前浏览器，不是多人云同步。

## Streamlit 部署

`dist/` 已纳入交付，Streamlit Cloud 无需运行 Node 构建。更改前端后，必须重新 `npm run build` 并将更新的 dist 一起提交。

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py --global.developmentMode false --server.headless true
```

Streamlit 入口为 `streamlit_app.py`，通过官方 custom component 服务构建产物。组件使用 Streamlit 消息协议注册就绪状态和设置高度。Hash 路由不请求服务器子路径，因此页面刷新不会因客户端路由导致 404。静态部署时同样发布 dist 目录即可。

在 Streamlit Community Cloud 连接本仓库，选择 main 分支与 `streamlit_app.py`，创建应用时选择固定子域名。之后始终更新同一 Streamlit 应用，以保留站点地址。本项目未自动创建生产站点，也未绑定域名；此操作需要仓库发布权限与部署账号。不要把 API 密钥写进前端；接入真实 AI 时应通过后端读取 Streamlit secrets。

## 验证

已通过 TypeScript/生产构建、Vitest（比例分摊、净额、结算、规则解析、轮换），以及 Chromium 浏览器的账单刷新持久化、采购联动、公约三人投票、移动端宽度检查；Streamlit 本地健康检查和组件渲染通过。

后续生产化可加入共享数据库、真实身份认证、服务端投票权限及多端同步。当前演示身份切换仅用于体验，不能视作安全权限系统。

### Streamlit 滚动回归检查

Streamlit custom component 的 iframe 默认 `scrolling="no"`。应用使用固定视口高度的 `.app` 内部滚动区；外层 Streamlit 不滚动，不根据内容高度反复调整 iframe。移动端底栏预留安全间距。

启动 Streamlit 后，可用 Playwright + Chromium 运行 `python tests/scroll_check.py`。通过 `CHROMIUM_PATH` 指定浏览器路径，`ROOMIE_TEST_URL` 指定本地测试站点。此检查覆盖桌面、手机、短屏和横屏的真实滚轮到底，以及长留言板不使 iframe 高度增长。

# Dr. DevLove (開發之愛)
### *或者是：我如何學會停止分析癱瘓並愛上瘋狂寫程式*

[![GitHub license](https://img.shields.io/github/license/forestsheep911/Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code)](https://github.com/forestsheep911/Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code/blob/main/LICENSE)

> "先生們，這裡不能打架！這是作戰室！" — *奇愛博士*
>
> "開發者們，這裡不能過度思考！這是 IDE！" — *開發之愛博士*

你是否厭倦了盯著閃爍的游標發呆？你是否患有慢性*分析癱瘓*？你花在計畫程式碼上的時間是否比實際寫程式的時間還長？

**Dr. DevLove** (即 `gh-stats`) 就是你的處方藥。它證明了你*確實*在工作。它透過追蹤你在 GitHub 宇宙中的每日程式碼貢獻來驗證你的存在，而且不需要本地複製倉庫——畢竟誰有那麼多硬碟空間呢？

---

[English](./README.md) | [🇨🇳 简体中文](./README.zh-CN.md) | [🇹🇼 繁體中文](./README.zh-TW.md) | [🇯🇵 日本語](./README.ja.md) | [🇰🇷 한국어](./README.ko.md) | [🇪🇸 Español](./README.es.md) | [🇫🇷 Français](./README.fr.md) | [🇸🇦 العربية](./README.ar.md) | [🇮🇳 हिन्दी](./README.hi.md)

---

## 💊 處方 (特性)

*   **遠端診斷**: 直接透過 API 掃描你的 GitHub 活動。無需本地倉庫。
*   **生命徵象**: 美觀的彩色終端輸出和進度條，旋轉速度比你的冒名頂替症候群發作還快。
*   **可擴展治療**: 無論是個人專案還是龐大的組織專案均可使用。
*   **時光旅行**: 查看 `today` (今天)、`week` (本週)、`month` (本月) 或 `year` (本年) 的統計數據。

## 📥 服用方法 (安裝)

Dr. DevLove 需要 Python 3.9+ 和 GitHub CLI (`gh`)。

```bash
brew install gh
gh auth login
# 組織存取權限（正確診斷所必需）：
gh auth refresh -s read:org
```

複製這個名字超長的倉庫並使用 Poetry 安裝：

```bash
git clone https://github.com/forestsheep911/Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code.git
cd Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code
poetry install
```

## 📋 劑量 (使用)

執行工具查看統計。副作用可能包括突如其來的成就感。

```bash
# 證明你今天工作了
poetry run gh-stats --range today

# 向老闆證明你這個月都在工作
poetry run gh-stats --range month --orgs YOUR_COMPANY_ORG
```

## 📄 授權條款

MIT. 想怎麼用就怎麼用，只要寫程式就行。

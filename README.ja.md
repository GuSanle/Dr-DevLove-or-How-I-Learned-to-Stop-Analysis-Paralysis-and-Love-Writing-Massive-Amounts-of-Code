# Dr. DevLove (開発の愛)
### *あるいは：私が如何にして分析麻痺を止めて大量のコードを書くことを愛するようになったか*

[![GitHub license](https://img.shields.io/github/license/forestsheep911/Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code)](https://github.com/forestsheep911/Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code/blob/main/LICENSE)

> "諸君、ここで喧嘩は駄目だ！ここは作戦室だぞ！" — *ドクター・ストレンジラブ*
>
> "開発者諸君、ここで考えすぎては駄目だ！ここはIDEだぞ！" — *ドクター・デブラブ*

点滅するカーソルを見つめるのに疲れていませんか？慢性的な*分析麻痺*に苦しんでいませんか？コードを書く時間よりも、コードを計画する時間の方が長くなっていませんか？

**Dr. DevLove** (別名 `gh-stats`) が処方箋です。これは、あなたが*働いている*ことを証明するCLIツールです。ローカルクローンを必要とせず（ディスク容量の無駄ですからね）、GitHub宇宙全体での毎日のコード貢献を追跡することで、あなたの存在を証明します。

---

[English](./README.md) | [🇨🇳 简体中文](./README.zh-CN.md) | [🇹🇼 繁體中文](./README.zh-TW.md) | [🇯🇵 日本語](./README.ja.md) | [🇰🇷 한국어](./README.ko.md) | [🇪🇸 Español](./README.es.md) | [🇫🇷 Français](./README.fr.md) | [🇸🇦 العربية](./README.ar.md) | [🇮🇳 हिन्दी](./README.hi.md)

---

## 💊 処方箋 (機能)

*   **遠隔診断**: API経由でGitHubのアクティビティを直接スキャンします。ローカルリポジトリは不要です。
*   **バイタルサイン**: 詐欺師症候群（インポスター・シンドローム）よりも速く回転するプログレスバーを備えた、美しいカラーターミナル出力。
*   **スケーラブルな治療**: 個人プロジェクトから大規模な組織まで対応します。
*   **タイムトラベル**: `today` (今日)、`week` (今週)、`month` (今月)、または `year` (今年) の統計を確認できます。

## 📥 服用 (インストール)

```bash
brew install gh
gh auth login
gh auth refresh -s read:org  # 組織リポジトリに必要
```

この巨大なリポジトリをクローンし、Poetryでインストールしてください：

```bash
git clone https://github.com/forestsheep911/Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code.git
cd Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code
poetry install
```

## 📋 用法・用量 (使用法)

```bash
# 今日何かしたことを確認する
poetry run gh-stats --range today

# 今月働いたことを上司に証明する
poetry run gh-stats --range month --orgs YOUR_COMPANY_ORG
```

## 📄 ライセンス

MIT. 好きに使ってください、ただコードを書きましょう。

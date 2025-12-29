# Dr. DevLove (닥터 데브러브)
### *또는: 나는 어떻게 분석 마비를 멈추고 엄청난 양의 코드 작성을 사랑하게 되었는가*

[![GitHub license](https://img.shields.io/github/license/forestsheep911/Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code)](https://github.com/forestsheep911/Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code/blob/main/LICENSE)

> "신사 여러분, 여기서 싸우면 안 됩니다! 여긴 전쟁 상황실이라구요!" — *닥터 스트레인지러브*
>
> "개발자 여러분, 여기서 너무 많이 생각하면 안 됩니다! 여긴 IDE라구요!" — *닥터 데브러브*

깜빡이는 커서를 쳐다보는 데 지치셨나요? 만성적인 *분석 마비*로 고통받고 계신가요? 코드를 작성하는 시간보다 계획하는 데 더 많은 시간을 쓰고 계신가요?

**Dr. DevLove** (일명 `gh-stats`)가 처방전입니다. 이것은 당신이 *일하고 있음*을 증명하는 CLI 도구입니다. 디스크 공간을 낭비하는 로컬 복제 없이, GitHub 우주 전체에서 당신의 일일 코드 기여를 추적하여 당신의 존재를 증명합니다.

---

[English](./README.md) | [🇨🇳 简体中文](./README.zh-CN.md) | [🇹🇼 繁體中文](./README.zh-TW.md) | [🇯🇵 日本語](./README.ja.md) | [🇰🇷 한국어](./README.ko.md) | [🇪🇸 Español](./README.es.md) | [🇫🇷 Français](./README.fr.md) | [🇸🇦 العربية](./README.ar.md) | [🇮🇳 हिन्दी](./README.hi.md)

---

## 💊 처방 (기능)

*   **원격 진단**: API를 통해 GitHub 활동을 직접 스캔합니다. 로컬 저장소가 필요 없습니다.
*   **활력 징후**: 가면 증후군(Imposter Syndrome)보다 빠르게 회전하는 진행바와 함께 제공되는 아름다운 컬러 터미널 출력.
*   **확장 가능한 치료**: 개인 프로젝트부터 거대한 조직까지 모두 작동합니다.
*   **시간 여행**: `today` (오늘), `week` (이번 주), `month` (이번 달), 또는 `year` (올해)의 통계를 확인하세요.

## 📥 복용 (설치)

```bash
brew install gh
gh auth login
gh auth refresh -s read:org  # 조직 저장소 접근에 필요
```

이 거대한 저장소를 복제하고 Poetry로 설치하세요:

```bash
git clone https://github.com/forestsheep911/Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code.git
cd Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code
poetry install
```

## 📋 용법 (사용법)

```bash
# 오늘 무언가를 했는지 확인
poetry run gh-stats --range today

# 이번 달에 일했음을 상사에게 증명
poetry run gh-stats --range month --orgs YOUR_COMPANY_ORG
```

## 📄 라이선스

MIT. 원하는 대로 하세요, 그냥 코드를 작성하세요.

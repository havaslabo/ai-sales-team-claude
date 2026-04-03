<p align="center">
  <img src="banner.svg" alt="AI Sales Team for Claude Code" width="100%">
</p>

<p align="center">
  <a href="#クイックスタート"><img src="https://img.shields.io/badge/install-ワンライナー-blue?style=for-the-badge" alt="Install"></a>
  <a href="#コマンド一覧"><img src="https://img.shields.io/badge/22_スキル-ready-8b5cf6?style=for-the-badge" alt="22 Skills"></a>
  <a href="#仕組み"><img src="https://img.shields.io/badge/5_並列-エージェント-22c55e?style=for-the-badge" alt="5 Agents"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-gray?style=for-the-badge" alt="MIT License"></a>
</p>

> **日本のBtoB営業に特化した AI 営業チームが、Claude Code の中で動きます。**
> コマンド一行で、企業リサーチ・リード評価・意思決定者の特定・稟議支援・見積書・PDF レポートまで自動生成。

---

## できること

Claude Code でコマンドを打つだけで、すぐに使える営業情報が手に入ります。

```
> /sales prospect https://example-company.co.jp

5つのエージェントを並列起動中...

  ✓ 企業リサーチ        適合スコア: 82/100
  ✓ 意思決定者の特定    4名を発見
  ✓ 機会評価 (BANT)     スコア: 78/100
  ✓ 競合調査            3社をマッピング
  ✓ アプローチ戦略      メールシーケンス完成

  総合スコア: 85/100  グレード: A（有望見込み客）
  推奨アクション: 優先的にアプローチ

分析結果を PROSPECT-ANALYSIS.md に保存しました
```

---

## レポートを受け取ったら

`/sales prospect` を実行すると `PROSPECT-ANALYSIS.md` が生成されます。このファイルをどう使うか、具体的な手順です。

### ステップ1：スコアとグレードを確認する

レポートの冒頭にあるスコアを見てください。

```
Prospect Score: 76/100（グレード: A — 有望見込み客）
```

| グレード | 次のアクション |
|---------|-------------|
| **A+ / A** | 今すぐ動く。スコア計算で紹介された「主要意思決定者」に連絡 |
| **B** | 普通に進める。フォローアップシーケンスを回す |
| **C** | 急がない。定期的なコンテンツ送付で温める |
| **D** | 後回し or スキップ |

### ステップ2：メールをコピペして送る

レポートの末尾に「**すぐに送れる最初のメール**」があります。

- `[社名]`、`[氏名]` など `[ ]` で囲まれた部分だけ自分の情報に書き換える
- 件名は A / B の2案があるので、好きな方を選ぶ
- そのまま送信できます（テンプレートではなく、相手に合わせてパーソナライズ済み）

### ステップ3：商談が決まったら次のコマンドを使う

```bash
# 商談の準備（当日のトーク・質問リストを自動生成）
/sales prep https://相手のURL

# 商談後に議事録と確認メールを作成
/sales minutes "会社名"

# 稟議が必要な場合、相手が社内承認を通しやすいように支援
/sales ringi "会社名"

# 見積書を作成
/sales quote "会社名"
```

---

## クイックスタート

### ワンコマンドインストール

```bash
curl -fsSL https://raw.githubusercontent.com/havaslabo/ai-sales-team-claude/main/install.sh | bash
```

### 手動インストール

```bash
git clone https://github.com/havaslabo/ai-sales-team-claude.git
cd ai-sales-team-claude
./install.sh
```

> Python の依存パッケージ（reportlab・beautifulsoup4・requests）はインストーラーが自動でインストールします。

<details>
<summary><strong>インストーラーの実行内容</strong></summary>

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   AI Sales Team — Claude Code スキル                         ║
║   22スキル · 5エージェント · スクリプト · PDF対応            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

スキルをインストールしています...
  ✓ sales（メインスキル）
  ✓ sales-prospect
  ✓ sales-research
  ✓ sales-qualify
  ✓ sales-contacts
  ✓ sales-outreach
  ✓ sales-followup
  ✓ sales-prep
  ✓ sales-proposal
  ✓ sales-objections
  ✓ sales-icp
  ✓ sales-competitors
  ✓ sales-report
  ✓ sales-report-pdf
  ✓ sales-ringi
  ✓ sales-security-qa
  ✓ sales-event-followup
  ✓ sales-poc
  ✓ sales-minutes
  ✓ sales-channel
  ✓ sales-quote
  ✓ sales-renewal

エージェントをインストールしています...
  ✓ sales-company
  ✓ sales-contacts
  ✓ sales-opportunity
  ✓ sales-competitive
  ✓ sales-strategy

Python パッケージをインストールしています...
  ✓ reportlab
  ✓ beautifulsoup4
  ✓ requests

日本語フォントを確認しています...
  ✓ 日本語フォント（reportlab 内蔵）が利用可能です
```

</details>

---

## コマンド一覧

### 見込み客の調査・評価

| コマンド | 説明 | 出力ファイル |
|:--------|:-----|:-----------|
| `/sales prospect <url>` | 完全分析 — **5つのエージェントが並列で動作** | `PROSPECT-ANALYSIS.md` |
| `/sales quick <url>` | 60秒でのクイック確認 | ターミナル出力 |
| `/sales research <url>` | 企業情報・属性の詳細調査 | `COMPANY-RESEARCH.md` |
| `/sales qualify <url>` | リード評価（BANT + MEDDIC） | `LEAD-QUALIFICATION.md` |
| `/sales contacts <url>` | 意思決定者の特定 | `DECISION-MAKERS.md` |
| `/sales icp <説明>` | 理想顧客プロファイル（ICP）の作成 | `IDEAL-CUSTOMER-PROFILE.md` |
| `/sales competitors <url>` | 競合調査 | `COMPETITIVE-INTEL.md` |

### メール・アプローチ

| コマンド | 説明 | 出力ファイル |
|:--------|:-----|:-----------|
| `/sales outreach <会社名>` | 新規開拓メールの作成 | `OUTREACH-SEQUENCE.md` |
| `/sales followup <会社名>` | フォローアップメールの作成 | `FOLLOWUP-SEQUENCE.md` |
| `/sales event-followup <展示会名> <会社名>` | 展示会・セミナー後のフォロー | `EVENT-FOLLOWUP-[会社名].md` |

### 商談・提案

| コマンド | 説明 | 出力ファイル |
|:--------|:-----|:-----------|
| `/sales prep <url>` | 商談前の準備資料 | `MEETING-PREP.md` |
| `/sales minutes <会社名>` | 商談議事録・確認メールの作成 | `MEETING-MINUTES-[会社名]-[日付].md` |
| `/sales proposal <会社名>` | 提案書の作成 | `CLIENT-PROPOSAL.md` |
| `/sales poc <会社名>` | PoC（試験導入）提案書の作成 | `POC-PROPOSAL-[会社名].md` |
| `/sales quote <会社名>` | 見積書の作成（インボイス対応） | `QUOTE-[会社名]-[日付].md` |
| `/sales objections <テーマ>` | 反論への対応集 | `OBJECTION-PLAYBOOK.md` |

### 日本市場向けスキル

| コマンド | 説明 | 出力ファイル |
|:--------|:-----|:-----------|
| `/sales ringi <会社名>` | 稟議支援パッケージ（稟議書・FAQ・比較表） | `RINGI-SUPPORT.md` |
| `/sales security-qa <会社名>` | セキュリティ質問票への回答支援 | `SECURITY-QA-[会社名].md` |
| `/sales channel <パートナー名>` | 代理店・SIer・パートナー経由の営業支援 | `CHANNEL-STRATEGY-[パートナー名].md` |
| `/sales renewal <会社名>` | 契約更新・アップセルの準備 | `RENEWAL-PROPOSAL-[会社名].md` |

### レポート

| コマンド | 説明 | 出力ファイル |
|:--------|:-----|:-----------|
| `/sales report` | 営業パイプラインレポート（Markdown） | `SALES-REPORT.md` |
| `/sales report-pdf` | 営業パイプラインレポート（PDF） | `SALES-REPORT-*.pdf` |

---

## 仕組み

### 構成

1つのメインスキルが21のサブスキルへコマンドを振り分けます。`/sales prospect` を実行すると、5つの専門エージェントが同時に動いて企業を分析します。

```
/sales prospect <url>
        │
        ├─ フェーズ1: 情報収集
        │   サイト取得 → データ抽出 → 業種判定
        │
        ├─ フェーズ2: 並列分析（5エージェント同時実行）
        │   ├── 企業リサーチ     （適合度 25%）
        │   ├── 担当者の特定     （接触性 20%）
        │   ├── 機会評価         （案件質 20%）
        │   ├── 競合分析         （競合優位 15%）
        │   └── アプローチ戦略   （準備度 20%）
        │
        └─ フェーズ3: 総合評価
            スコア算出（0-100）→ アクション提案
```

### スキル間の連携

各スキルは他のスキルの出力を自動的に読み込んで活用します。

```
/sales prospect  →  PROSPECT-ANALYSIS.md
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
 /sales outreach    /sales prep       /sales ringi
 （担当者・企業     （全分析を         （提案書・PoCを
   情報を活用）      統合活用）          もとに稟議）
```

---

## スコアリング

すべての見込み客に **0〜100 の総合スコア** を付けます。5つの軸の加重平均で算出します。

| 評価軸 | 比重 | 主な判断材料 |
|--------|------|------------|
| 企業適合度 | 25% | 規模・業種・成長性・予算シグナル |
| 担当者へのアクセス | 20% | 意思決定者の特定・紹介経路 |
| 案件の質 | 20% | ペインポイント・予算・タイミング |
| 競合優位性 | 15% | 現行ソリューション・切り替えコスト |
| アプローチ準備度 | 20% | メッセージング・チャネル・切り口 |

### グレードの見方

| スコア | グレード | 対応方針 |
|--------|---------|---------|
| 90〜100 | A+ | 即座に優先対応。成約確率が高い |
| 75〜89 | A | 積極的にアプローチする価値がある |
| 60〜74 | B | 標準的な流れで商談を進める |
| 40〜59 | C | 急がず関係を温める |
| 0〜39 | D | 優先度を下げるか対象外とする |

### 評価フレームワーク

<details>
<summary><strong>BANT（0〜100点）</strong></summary>

公開情報をもとに4軸をそれぞれ25点満点で評価します。

| 軸 | 満点 | 主な判断材料 |
|----|------|------------|
| **Budget（予算）** | 25 | 資本金・従業員数・決算期・IT投資規模 |
| **Authority（権限）** | 25 | 意思決定者の特定・役職・稟議ライン |
| **Need（必要性）** | 25 | 課題・求人票・レビューサイト・競合ギャップ |
| **Timeline（時期）** | 25 | 決算期・人事異動・予算申請サイクル |

</details>

<details>
<summary><strong>MEDDIC（充足度 0〜100%）</strong></summary>

6つの観点で情報の充足度を評価します。

- **M**etrics — ビジネス効果を数値で示せるか
- **E**conomic Buyer — 最終承認者は誰か
- **D**ecision Criteria — 何を基準に選ぶか
- **D**ecision Process — 稟議・購買のプロセスはどうなっているか
- **I**dentify Pain — 課題は明確になっているか
- **C**hampion — 社内に推進してくれる人がいるか

</details>

<details>
<summary><strong>日本市場向けの調整要素</strong></summary>

| 要素 | 内容 | スコアへの影響 |
|------|------|-------------|
| 上場区分 | 東証プライム上場 → 予算規模・稟議プロセスが明確 | +5点 |
| グループ企業 | 親会社の承認が必要 → 決裁まで時間がかかる | -5点（時期軸） |
| 決算期 | 3月決算なら10〜12月が予算申請の好機 | 時期によって加減点 |
| 資本金 | 3億円以上 → 中堅〜大企業として予算に余裕あり | 企業適合度に反映 |
| 社歴 | 設立50年以上 → 保守的な意思決定、変更リスクが高い | -5点（案件質軸） |

</details>

---

## 使い方の例

### 見込み客の完全分析

```
> /sales prospect https://example-tech.co.jp

フェーズ1: 企業情報を収集中...
  ✓ サイト取得完了（SaaS / ITサービス）
  ✓ 6ページを解析（会社概要・製品・採用・ニュース・問い合わせ）
  ✓ 23項目のデータを抽出

フェーズ2: 並列分析中（5エージェント）...
  ✓ 企業リサーチ        適合スコア: 88/100
  ✓ 意思決定者の特定    6名を発見
  ✓ 機会評価            BANT: 82/100
  ✓ 競合調査            4社をマッピング
  ✓ アプローチ戦略      メールシーケンス完成

フェーズ3: 結果を統合中...
  ✓ 総合スコア: 85/100（グレード A）
  ✓ 主要担当者: 情報システム部長（社内推進者の可能性あり）
  ✓ 切り口: 採用拡大 + ERPリプレイスの検討シグナルあり

出力: PROSPECT-ANALYSIS.md
```

### リード評価

```
> /sales qualify https://example-mfg.co.jp

  BANTスコア: 78/100（グレード A）

    予算    22 / 25
    権限    18 / 25
    必要性  20 / 25
    時期    18 / 25

  MEDDIC充足度: 72%

  → 初回アポを設定してください（優先度：高）
  出力: LEAD-QUALIFICATION.md
```

### 稟議支援パッケージの作成

```
> /sales ringi "株式会社サンプル製造"

  ✓ エグゼクティブサマリー（1ページ）
  ✓ よくある質問と回答集
  ✓ 競合3社との比較表
  ✓ 導入スケジュール案（3〜6ヶ月）
  ✓ 稟議書の文面（そのまま使えます）

  出力: RINGI-SUPPORT.md
```

### 商談後の議事録

```
> /sales minutes "株式会社サンプル"

  ✓ 顧客へ送る確認メール（です・ます調）
  ✓ 社内保存用の議事録（TODO・懸念点付き）

  出力: MEETING-MINUTES-株式会社サンプル-2026-04-03.md
```

---

## 推奨ワークフロー

### 新規開拓

```bash
/sales icp "自社サービスの説明"          # 理想顧客の定義（初回のみ）
/sales prospect https://example.co.jp    # 完全分析
/sales event-followup 展示会名 会社名    # 展示会後のフォロー（展示会参加時）
/sales outreach "会社名"                 # 新規アプローチ
/sales prep https://example.co.jp        # 商談準備
/sales minutes "会社名"                  # 商談後の議事録
/sales poc "会社名"                      # PoC提案（必要な場合）
/sales ringi "会社名"                    # 稟議支援資料
/sales security-qa "会社名"              # セキュリティ質問票（必要な場合）
/sales quote "会社名"                    # 見積書
/sales proposal "会社名"                 # 提案書
```

### 既存顧客の更新・拡大

```bash
/sales renewal "会社名"                  # 更新商談の準備
/sales minutes "会社名"                  # 商談後の議事録
/sales quote "会社名"                    # 更新見積書
```

### 代理店経由

```bash
/sales channel "パートナー名"            # パートナー向け提案の作成
/sales ringi "会社名"                    # エンドユーザーの稟議支援
```

---

## ファイル構成

```
ai-sales-team-claude/
│
├── sales/SKILL.md                        ← メインスキル（全コマンドのルーティング）
│
├── skills/                               ← 21のサブスキル
│   ├── sales-prospect/SKILL.md              完全分析（5エージェントを並列起動）
│   ├── sales-research/SKILL.md              企業情報の詳細調査
│   ├── sales-qualify/SKILL.md               リード評価（BANT + MEDDIC）
│   ├── sales-contacts/SKILL.md              意思決定者の特定
│   ├── sales-outreach/SKILL.md              新規開拓メールの作成
│   ├── sales-followup/SKILL.md              フォローアップメールの作成
│   ├── sales-prep/SKILL.md                  商談前の準備資料
│   ├── sales-proposal/SKILL.md              提案書の作成
│   ├── sales-objections/SKILL.md            反論への対応集
│   ├── sales-icp/SKILL.md                   理想顧客プロファイルの作成
│   ├── sales-competitors/SKILL.md           競合調査
│   ├── sales-report/SKILL.md                パイプラインレポート（Markdown）
│   ├── sales-report-pdf/SKILL.md            パイプラインレポート（PDF）
│   ├── sales-ringi/SKILL.md                 稟議支援パッケージの作成
│   ├── sales-security-qa/SKILL.md           セキュリティ質問票への回答支援
│   ├── sales-event-followup/SKILL.md        展示会・セミナー後のフォロー
│   ├── sales-poc/SKILL.md                   PoC提案書の作成
│   ├── sales-minutes/SKILL.md               商談議事録・確認メールの作成
│   ├── sales-channel/SKILL.md               代理店・SIer・パートナー経由の営業支援
│   ├── sales-quote/SKILL.md                 見積書の作成（インボイス対応）
│   └── sales-renewal/SKILL.md               契約更新・アップセルの準備
│
├── agents/                               ← 5つの並列エージェント
│   ├── sales-company.md                     企業適合度の評価（25%）
│   ├── sales-contacts.md                    意思決定者のマッピング（20%）
│   ├── sales-opportunity.md                 案件評価・BANTスコアリング（20%）
│   ├── sales-competitive.md                 競合分析（15%）
│   └── sales-strategy.md                    アプローチ戦略の立案（20%）
│
├── scripts/                              ← Python スクリプト
│   ├── analyze_prospect.py                  サイト解析・データ抽出
│   ├── lead_scorer.py                       BANT/MEDDICスコアリング
│   ├── contact_finder.py                    担当者・役員情報の抽出
│   └── generate_pdf_report.py               PDFレポートの生成（日本語対応）
│
├── templates/                            ← 出力テンプレート
│   ├── outreach-cold.md                     新規開拓メール（5通）
│   ├── outreach-warm.md                     温め直しメール（3通）
│   ├── outreach-referral.md                 紹介経由メール（3通）
│   ├── meeting-prep.md                      商談準備資料
│   ├── proposal-template.md                 提案書（11セクション）
│   ├── objection-playbook.md                反論対応集
│   ├── event-followup.md                    展示会フォローメール（3通）
│   ├── poc-proposal.md                      PoC提案書
│   ├── meeting-minutes.md                   商談議事録
│   └── quote-template.md                    見積書（インボイス対応）
│
├── install.sh                            ← インストーラー（Python依存も自動処理）
├── uninstall.sh                          ← アンインストールスクリプト
└── LICENSE                               ← MIT
```

---

## こんな方に

<table>
<tr>
<td width="33%">

### 営業担当・営業チーム

```bash
# 問い合わせリードを評価
/sales qualify https://lead.co.jp

# 稟議支援資料を一括作成
/sales ringi "株式会社〇〇"

# 商談後の議事録をすぐ作成
/sales minutes "株式会社〇〇"
```

</td>
<td width="33%">

### スタートアップ・創業者

```bash
# 見込み客を完全分析
/sales prospect https://target.co.jp

# 展示会後のフォローを一括作成
/sales event-followup Japan IT Week 株式会社〇〇

# 見積書をすぐ作成
/sales quote "株式会社〇〇"
```

</td>
<td width="33%">

### 代理店・パートナー営業

```bash
# パートナー向け提案を作成
/sales channel "〇〇商社"

# エンドユーザーの稟議を支援
/sales ringi "エンドユーザー名"

# 競合との比較資料を作成
/sales competitors https://client.co.jp
```

</td>
</tr>
</table>

---

## 動作要件

| 要件 | 必須/任意 | 備考 |
|:-----|:--------:|:----|
| **Claude Code** | 必須 | [インストールはこちら](https://docs.anthropic.com/en/docs/claude-code) |
| **Python 3.8+** | 任意 | スクリプト・PDF生成に使用（インストーラーが自動確認） |
| **reportlab** | 任意 | PDFレポート生成（インストーラーが自動インストール） |
| **beautifulsoup4** | 任意 | サイト解析の精度向上（インストーラーが自動インストール） |
| **requests** | 任意 | URL取得のフォールバック（インストーラーが自動インストール） |

---

## アンインストール

```bash
# リポジトリのディレクトリから実行
./uninstall.sh

# または直接実行
curl -fsSL https://raw.githubusercontent.com/havaslabo/ai-sales-team-claude/main/uninstall.sh | bash
```

`~/.claude/` からスキル・エージェント・スクリプト・テンプレートをすべて削除します。Python パッケージは削除されません。

---

<p align="center">
  <strong>MIT License</strong> · Copyright (c) 2026 Havaslabo
  <br><br>
  <a href="https://github.com/havaslabo/ai-sales-team-claude/issues">バグを報告する</a> ·
  <a href="https://github.com/havaslabo/ai-sales-team-claude/issues">機能をリクエストする</a>
</p>

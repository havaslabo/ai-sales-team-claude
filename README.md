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
> コマンド一行で、企業リサーチ・リード評価・意思決定者の特定・稟議支援パッケージ・見積書・PDF レポートまで自動生成。

---

## できること

Claude Code でコマンドを打つだけで、すぐに使える営業情報が手に入ります。

```
> /sales prospect https://example-company.co.jp

5つのエージェントを並列起動中...

  ✓ 企業リサーチ            適合スコア: 82/100
  ✓ 意思決定者の特定        4名を発見
  ✓ 機会評価 (BANT)         スコア: 78/100
  ✓ 競合調査                3社をマッピング
  ✓ アウトリーチ戦略        メールシーケンス完成

  総合スコア: 85/100  グレード: A（有望見込み客）
  推奨アクション: 優先的にアプローチ

分析結果を PROSPECT-ANALYSIS.md に保存しました
```

---

## クイックスタート

### ワンコマンドインストール

```bash
curl -fsSL https://raw.githubusercontent.com/havaslabo/ai-sales-team-claude/main/install.sh | bash
```

### マニュアルインストール

```bash
git clone https://github.com/havaslabo/ai-sales-team-claude.git
cd ai-sales-team-claude
./install.sh
```

> Python 依存パッケージ（reportlab・beautifulsoup4・requests）はインストーラーが自動でインストールします。

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
  ✓ sales（オーケストレーター）
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

Python 依存パッケージをインストールしています...
  ✓ reportlab インストール完了
  ✓ beautifulsoup4 インストール完了
  ✓ requests インストール完了

日本語フォントを確認しています...
  ✓ 日本語フォント（reportlab 内蔵 CID フォント）が利用可能です
```

</details>

---

## コマンド一覧

### 見込み客開拓・分析

| コマンド | 説明 | 出力ファイル |
|:--------|:-----|:-----------|
| `/sales prospect <url>` | 完全見込み客監査 — **5つの並列エージェント** | `PROSPECT-ANALYSIS.md` |
| `/sales quick <url>` | 60秒での見込み客スナップショット | ターミナル出力 |
| `/sales research <url>` | 企業リサーチ＆ファーモグラフィクス | `COMPANY-RESEARCH.md` |
| `/sales qualify <url>` | リード評価（BANT + MEDDIC） | `LEAD-QUALIFICATION.md` |
| `/sales contacts <url>` | 意思決定者の特定 | `DECISION-MAKERS.md` |
| `/sales icp <description>` | 理想顧客プロファイル（ICP）作成 | `IDEAL-CUSTOMER-PROFILE.md` |
| `/sales competitors <url>` | 競合インテリジェンス | `COMPETITIVE-INTEL.md` |

### アウトリーチ・コミュニケーション

| コマンド | 説明 | 出力ファイル |
|:--------|:-----|:-----------|
| `/sales outreach <prospect>` | コールドアウトリーチメールシーケンス | `OUTREACH-SEQUENCE.md` |
| `/sales followup <prospect>` | フォローアップメールシーケンス | `FOLLOWUP-SEQUENCE.md` |
| `/sales event-followup <展示会名> <会社名>` | 展示会・セミナー後フォローアップ | `EVENT-FOLLOWUP-[会社名].md` |

### 商談・提案

| コマンド | 説明 | 出力ファイル |
|:--------|:-----|:-----------|
| `/sales prep <url>` | 商談準備ブリーフ | `MEETING-PREP.md` |
| `/sales minutes <company>` | 商談議事録・確認メール生成 | `MEETING-MINUTES-[会社名]-[日付].md` |
| `/sales proposal <client>` | クライアント提案書生成 | `CLIENT-PROPOSAL.md` |
| `/sales poc <company>` | PoC（試験導入）提案書生成 | `POC-PROPOSAL-[会社名].md` |
| `/sales quote <company>` | 日本形式の見積書生成（インボイス対応） | `QUOTE-[会社名]-[日付].md` |
| `/sales objections <topic>` | 反論対応プレイブック | `OBJECTION-PLAYBOOK.md` |

### 日本市場特化スキル

| コマンド | 説明 | 出力ファイル |
|:--------|:-----|:-----------|
| `/sales ringi <prospect>` | 稟議支援パッケージ生成（稟議書・FAQ・比較表） | `RINGI-SUPPORT.md` |
| `/sales security-qa <company>` | 情報セキュリティ質問票対応支援 | `SECURITY-QA-[会社名].md` |
| `/sales channel <partner>` | 代理店・SIer・パートナー経由営業支援 | `CHANNEL-STRATEGY-[パートナー名].md` |
| `/sales renewal <company>` | 契約更新・アップセル・カスタマーサクセス支援 | `RENEWAL-PROPOSAL-[会社名].md` |

### レポート

| コマンド | 説明 | 出力ファイル |
|:--------|:-----|:-----------|
| `/sales report` | 営業パイプラインレポート（Markdown） | `SALES-REPORT.md` |
| `/sales report-pdf` | 営業パイプラインレポート（PDF） | `SALES-REPORT-*.pdf` |

---

## 仕組み

### アーキテクチャ

3層アーキテクチャで構成されています — 1つのオーケストレータースキルが22のサブスキルにコマンドをルーティングし、フラッグシップコマンド `/sales prospect` は5つの専門エージェントを並列起動します。

```
                         ┌──────────────────────────┐
                         │     /sales prospect       │
                         │    （オーケストレーター）  │
                         └────────────┬─────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                  ▼
          ┌─────────────┐   ┌─────────────────┐   ┌──────────────┐
          │  フェーズ1   │   │    フェーズ2     │   │  フェーズ3   │
          │  情報収集   │   │   並列分析       │   │  総合評価    │
          └──────┬──────┘   └────────┬──────────┘   └──────┬───────┘
                 │                   │                      │
                 ▼                   ▼                      ▼
          ┌─────────────┐   ┌───────────────┐       ┌──────────────┐
          │ サイト取得  │   │ 5エージェント  │       │ 集計スコア   │
          │ データ抽出  │   │ 同時実行       │       │ (0-100)      │
          │ 業種判定    │   │               │       │ アクション   │
          └─────────────┘   └───────┬───────┘       └──────────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                   │
        ┌────────────────┐  ┌──────────────┐  ┌───────────────┐
        │ ┌────────────┐ │  │ ┌──────────┐ │  │ ┌───────────┐ │
        │ │  企業      │ │  │ │ 担当者   │ │  │ │ 機会      │ │
        │ │  リサーチ  │ │  │ │ 特定     │ │  │ │ 評価      │ │
        │ │ 適合度:25% │ │  │ │ 接触:20% │ │  │ │ 質:20%    │ │
        │ └────────────┘ │  │ └──────────┘ │  │ └───────────┘ │
        └────────────────┘  └──────────────┘  └───────────────┘
        ┌────────────────┐  ┌──────────────┐
        │ ┌────────────┐ │  │ ┌──────────┐ │
        │ │  競合      │ │  │ │ 戦略     │ │
        │ │  分析      │ │  │ │ 立案     │ │
        │ │ 位置:15%   │ │  │ │ 準備:20% │ │
        │ └────────────┘ │  │ └──────────┘ │
        └────────────────┘  └──────────────┘
```

### クロススキル連携

スキルは自動的に互いの出力を検出し、連携して動作します。

```
/sales prospect  ──►  PROSPECT-ANALYSIS.md
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                     ▼
/sales outreach      /sales prep           /sales ringi
 (リサーチ・担当者   (全分析データを       (提案書・PoC
  データを活用)       統合活用)             内容を基に稟議)
       │                    │                     │
       ▼                    ▼                     ▼
  OUTREACH-              MEETING-              RINGI-
  SEQUENCE.md            PREP.md               SUPPORT.md
```

---

## 見込み客スコアリング

すべての見込み客は **5つの次元から算出した加重複合スコア（0〜100）** を取得します。

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   PROSPECT SCORE 計算式                                             │
│                                                                     │
│   企業適合度 ............. 25%   ████████████░░░░░░░░  規模、業界、 │
│                                                        成長、予算   │
│                                                                     │
│   コンタクトアクセス ..... 20%   █████████░░░░░░░░░░░  意思決定者、 │
│                                                        紹介経路     │
│                                                                     │
│   機会の質 ............... 20%   █████████░░░░░░░░░░░  BANT、      │
│                                                        ペインポイント│
│                                                                     │
│   競合ポジション ......... 15%   ███████░░░░░░░░░░░░░  現行ソリューション、│
│                                                        スイッチコスト│
│                                                                     │
│   アウトリーチ準備度 ..... 20%   █████████░░░░░░░░░░░  チャネル、   │
│                                                        メッセージング│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### グレード解釈基準

```
  スコア   グレード   アクション
 ───────────────────────────────────────────────────────
  90-100    A+      ホットリード — 即座に優先対応
  75-89     A       有望見込み客 — 多大な投資に値する
  60-74     B       評価済みリード — 標準アプローチで追求
  40-59     C       ウォームリード — ナーチャリング、強引な営業はしない
   0-39     D       適合度低 — 優先度を下げるか不適格とする
```

### 評価フレームワーク

<details>
<summary><strong>BANT スコアリング（0〜100）</strong></summary>

公開情報から各次元を 0〜25 でスコアリングします。

| 次元 | 最大 | 評価シグナル |
|------|------|------------|
| **Budget（予算）** | 25 | 資本金、従業員数、決算期、IT投資規模 |
| **Authority（権限）** | 25 | 意思決定者の特定、C-suite、組織図、稟議ライン |
| **Need（需要）** | 25 | ペインポイント、求人票、クチコミ、競合ギャップ |
| **Timeline（時期）** | 25 | 決算期、人事異動、予算申請サイクル、緊急度 |

</details>

<details>
<summary><strong>MEDDIC 評価（0〜100%）</strong></summary>

各次元の充足度を評価します。

- **M**etrics — ビジネスインパクトを数値化できるか？
- **E**conomic Buyer — 予算を握る意思決定者は誰か？
- **D**ecision Criteria — どのように評価・選定するか？
- **D**ecision Process — 稟議プロセス・購買フローはどうなっているか？
- **I**dentify Pain — ペインポイントは確認されているか？
- **C**hampion — 社内推進者（チャンピオン）はいるか？

</details>

<details>
<summary><strong>日本市場向けスコア調整要素</strong></summary>

| 要素 | 内容 | スコア影響 |
|------|------|-----------|
| 上場区分 | 東証プライム上場 → 予算規模・稟議プロセスが明確 | +5点 |
| グループ企業 | 親会社の承認が必要な場合 → タイムラインが長くなる | -5点（Timeline軸） |
| 決算期 | 3月決算（4月年度始まり）→ 10〜12月が予算申請の好機 | 時期によって加点/減点 |
| 資本金規模 | 3億円以上 → 中堅〜大企業として予算容量あり | 企業適合度に反映 |
| 老舗企業 | 設立50年以上 → 保守的な意思決定・変更リスクが高い | -5点（機会の質） |

</details>

---

## 使用例

### 完全見込み客分析

```
> /sales prospect https://example-tech.co.jp

フェーズ1: 企業情報を収集中...
  ✓ ホームページ取得完了 — SaaS / IT サービス 検出
  ✓ 6ページ抽出（会社概要、製品、採用、ニュース、問い合わせ）
  ✓ 23のデータポイントを抽出

フェーズ2: 並列分析実行中（5エージェント）...
  ✓ 企業リサーチ        — 適合スコア: 88/100
  ✓ 担当者特定          — 6名の意思決定者を発見
  ✓ 機会評価            — BANT: 82/100
  ✓ 競合インテリジェンス — 4社の競合をマッピング
  ✓ アウトリーチ戦略    — 5通のメールシーケンス完成

フェーズ3: 結果を統合中...
  ✓ Prospect Score: 85/100（グレード A）
  ✓ トップコンタクト: [情報システム部長] — 社内推進者シグナルあり
  ✓ アプローチ角度: 直近の採用拡大 + ERPリプレイスの検討シグナル

出力: PROSPECT-ANALYSIS.md
```

### リード評価

```
> /sales qualify https://example-mfg.co.jp

example-mfg.co.jp のリード評価を実施中...

  BANTスコア: 78/100（グレード A）
  ┌────────────────────────────────────┐
  │ 予算:      ██████████████████░░ 22  │
  │ 権限:      ████████████████░░░░ 18  │
  │ 需要:      ██████████████████░░ 20  │
  │ 時期:      ████████████████░░░░ 18  │
  └────────────────────────────────────┘
  MEDDIC 充足度: 72%

アクション: 初回アポを設定 — 高優先度の見込み客。
出力: LEAD-QUALIFICATION.md
```

### 稟議支援パッケージ生成

```
> /sales ringi "株式会社サンプル製造"

稟議支援パッケージを生成中...
  ✓ エグゼクティブサマリー（1ページ）
  ✓ よくある質問（FAQ）と回答集
  ✓ 競合他社との比較表（3社対比）
  ✓ 導入スケジュール案（3ヶ月〜6ヶ月）
  ✓ 稟議書文面（コピペ可）

出力: RINGI-SUPPORT.md
```

### 商談後の議事録生成

```
> /sales minutes "株式会社サンプル"

商談議事録を生成中...
  ✓ 顧客送付用 確認メール（です・ます調）
  ✓ 社内保存用 議事録（詳細・TODO付き）

出力: MEETING-MINUTES-株式会社サンプル-2026-04-03.md
```

---

## 推奨ワークフロー（日本BtoB営業）

### 新規開拓の場合

```bash
/sales icp "自社サービスの説明"          # ICP定義（初回のみ）
/sales prospect https://example.co.jp    # 完全分析
/sales event-followup 展示会名 会社名    # 展示会後（または）
/sales outreach "会社名"                  # アウトリーチ
/sales prep https://example.co.jp        # 商談準備
/sales minutes "会社名"                  # 商談後の議事録
/sales poc "会社名"                      # PoC提案（必要な場合）
/sales ringi "会社名"                    # 稟議支援資料
/sales security-qa "会社名"              # セキュリティ質問票（必要な場合）
/sales quote "会社名"                    # 見積書
/sales proposal "会社名"                 # 提案書
```

### 既存顧客の更新・拡大の場合

```bash
/sales renewal "会社名"                  # 更新商談準備
/sales minutes "会社名"                  # 商談後の議事録
/sales quote "会社名"                    # 更新見積書
```

### 代理店経由の場合

```bash
/sales channel "パートナー名"            # パートナー向け提案
/sales ringi "会社名"                    # エンドユーザーの稟議支援
```

---

## プロジェクト構成

```
ai-sales-team-claude/
│
├── sales/SKILL.md                        ← メインオーケストレーター（全 /sales コマンドのルーティング）
│
├── skills/                               ← 21 サブスキル
│   ├── sales-prospect/SKILL.md              完全見込み客監査（5エージェントを起動）
│   ├── sales-research/SKILL.md              企業リサーチ＆ファーモグラフィクス
│   ├── sales-qualify/SKILL.md               リード評価（BANT + MEDDIC）
│   ├── sales-contacts/SKILL.md              意思決定者の特定
│   ├── sales-outreach/SKILL.md              コールドアウトリーチシーケンス
│   ├── sales-followup/SKILL.md              フォローアップメール生成
│   ├── sales-prep/SKILL.md                  商談準備ブリーフ
│   ├── sales-proposal/SKILL.md              クライアント提案書生成
│   ├── sales-objections/SKILL.md            反論対応プレイブック
│   ├── sales-icp/SKILL.md                   理想顧客プロファイル（ICP）作成
│   ├── sales-competitors/SKILL.md           競合インテリジェンス
│   ├── sales-report/SKILL.md                パイプラインレポート（Markdown）
│   ├── sales-report-pdf/SKILL.md            パイプラインレポート（PDF）
│   ├── sales-ringi/SKILL.md                 稟議支援パッケージ生成
│   ├── sales-security-qa/SKILL.md           情報セキュリティ質問票対応
│   ├── sales-event-followup/SKILL.md        展示会・セミナー後フォローアップ
│   ├── sales-poc/SKILL.md                   PoC（試験導入）提案書生成
│   ├── sales-minutes/SKILL.md               商談議事録・確認メール生成
│   ├── sales-channel/SKILL.md               代理店・SIer・パートナー営業支援
│   ├── sales-quote/SKILL.md                 日本形式見積書（インボイス対応）
│   └── sales-renewal/SKILL.md               契約更新・アップセル支援
│
├── agents/                               ← 5つの並列サブエージェント
│   ├── sales-company.md                     企業適合度＆ファーモグラフィクス（25%）
│   ├── sales-contacts.md                    意思決定者マッピング（20%）
│   ├── sales-opportunity.md                 機会評価＆BANTスコアリング（20%）
│   ├── sales-competitive.md                 競合ポジショニング（15%）
│   └── sales-strategy.md                    アウトリーチ戦略＆メッセージング（20%）
│
├── scripts/                              ← Python ユーティリティ
│   ├── analyze_prospect.py                  ウェブスクレイピング＆データ抽出
│   ├── lead_scorer.py                       BANT/MEDDIC スコアリングエンジン
│   ├── contact_finder.py                    チーム＆リーダーシップ抽出
│   └── generate_pdf_report.py               ReportLab PDF ジェネレーター（日本語対応）
│
├── templates/                            ← 出力テンプレート
│   ├── outreach-cold.md                     5通のコールドシーケンス
│   ├── outreach-warm.md                     3通のウォームイントロシーケンス
│   ├── outreach-referral.md                 3通の紹介シーケンス
│   ├── meeting-prep.md                      商談準備ブリーフ
│   ├── proposal-template.md                 11セクションのクライアント提案書
│   ├── objection-playbook.md                反論対応プレイブック
│   ├── event-followup.md                    展示会フォローアップ3通
│   ├── poc-proposal.md                      PoC提案書テンプレート
│   ├── meeting-minutes.md                   商談議事録テンプレート
│   └── quote-template.md                    日本形式見積書（インボイス対応）
│
├── install.sh                            ← ワンコマンドインストーラー（Python依存も自動インストール）
├── uninstall.sh                          ← クリーンアップスクリプト
└── LICENSE                               ← MIT
```

---

## 活用シーン

<table>
<tr>
<td width="33%">

### 営業担当者・営業チーム

```bash
# インバウンドリードを評価
/sales qualify https://lead.co.jp

# 稟議サポートを一括生成
/sales ringi "株式会社〇〇"

# 商談後の議事録を即生成
/sales minutes "株式会社〇〇"
```

</td>
<td width="33%">

### スタートアップ・ファウンダー

```bash
# 完全な見込み客インテリジェンス
/sales prospect https://target.co.jp

# 展示会後のフォロー一括生成
/sales event-followup Japan IT Week 株式会社〇〇

# 見積書をすぐ生成
/sales quote "株式会社〇〇"
```

</td>
<td width="33%">

### 代理店・パートナーセールス

```bash
# パートナー向け戦略を生成
/sales channel "〇〇商社"

# エンドユーザーの稟議を支援
/sales ringi "エンドユーザー企業名"

# 競合ポジショニング
/sales competitors https://client.co.jp
```

</td>
</tr>
</table>

---

## 動作要件

| 要件 | 状態 | 備考 |
|:-----|:----:|:----|
| **Claude Code** | 必須 | [Claude Code をインストール](https://docs.anthropic.com/en/docs/claude-code) |
| **Python 3.8+** | 任意 | スクリプト・PDF生成に必要（インストーラーが自動確認） |
| **reportlab** | 任意 | PDF レポート生成（インストーラーが自動インストール） |
| **beautifulsoup4** | 任意 | 拡張パース機能（インストーラーが自動インストール） |
| **requests** | 任意 | URL フェッチのフォールバック（インストーラーが自動インストール） |

---

## アンインストール

```bash
# リポジトリディレクトリから
./uninstall.sh

# リモートから
curl -fsSL https://raw.githubusercontent.com/havaslabo/ai-sales-team-claude/main/uninstall.sh | bash
```

`~/.claude/` からすべてのスキル・エージェント・スクリプト・テンプレートを削除します。Python パッケージは削除されません。

---

<p align="center">
  <strong>MIT License</strong> · Copyright (c) 2026 Havaslabo
  <br><br>
  <a href="https://github.com/havaslabo/ai-sales-team-claude/issues">バグを報告する</a> ·
  <a href="https://github.com/havaslabo/ai-sales-team-claude/issues">機能をリクエストする</a>
</p>

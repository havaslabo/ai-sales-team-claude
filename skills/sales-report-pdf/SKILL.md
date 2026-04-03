# プロフェッショナル営業レポート PDF 生成

## メタデータ
- **タイトル:** プロフェッショナル営業レポート PDF 生成
- **呼び出し方:** `/sales report-pdf`
- **入力:** なし（カレントディレクトリの SALES-REPORT.md と見込み客ファイルを読み込みます）
- **出力:** カレントディレクトリに `SALES-REPORT-{YYYY-MM-DD}.pdf` を生成します
- **依存関係:** Python 3、`reportlab` ライブラリ、`scripts/generate_pdf_report.py`

---

## 目的

営業パイプラインレポートのプロフェッショナルで見栄えのする PDF 版を生成します。この PDF は、Markdown ファイルではなくクリーンで持ち運び可能なドキュメントを必要とする営業リーダー・投資家・チームメンバーへの共有を目的としています。グラフ・フォーマット済みテーブル・カラーコードスコア・プロフェッショナルなレイアウトが含まれます。

---

## 指示

ユーザーが `/sales report-pdf` を呼び出したら、以下のプロセスに従ってください。

### ステップ1: 前提条件の確認

カレントディレクトリに `SALES-REPORT.md` が存在するか確認してください。

**SALES-REPORT.md が存在しない場合:**
- ユーザーに通知してください：「SALES-REPORT.md が見つかりませんでした。まず `/sales report` を実行してパイプラインレポートを生成し、その後 `/sales report-pdf` を実行して PDF 版を作成してください。」
- 処理を停止してください。

**SALES-REPORT.md が存在する場合:**
- 内容を読み込んでください。
- 個別の見込み客分析ファイル（`**/PROSPECT-ANALYSIS.md`、`**/COMPANY-RESEARCH.md` 等）もスキャンし、PDF に追加情報を反映させてください。

### ステップ2: reportlab の確認

以下を実行して `reportlab` Python ライブラリが利用可能か確認してください。
```bash
python3 -c "import reportlab; print(reportlab.Version)"
```

**reportlab がインストールされていない場合:**
- ユーザーに通知してください：「PDF 生成には `reportlab` Python ライブラリが必要です。次のコマンドでインストールしてください：`pip install reportlab`」
- インストールコマンドを代わりに実行するか確認してください：`pip install reportlab`
- インストール完了後、PDF 生成を続行してください。

**Python 3 が利用できない場合:**
- ユーザーに通知してください：「PDF 生成には Python 3 が必要です。Python 3 と reportlab ライブラリをインストールしてください。」
- 処理を停止してください。

### ステップ3: レポートデータの解析

`SALES-REPORT.md` および見込み客分析ファイルから以下のデータを抽出してください。

#### パイプライン概要データ
- レポート生成日
- 見込み客総数
- パイプライン平均スコア（0〜100）
- パイプライン全体の健全性評価

#### 見込み客データ配列
各見込み客について以下の構造でデータを抽出してください。
```json
{
  "name": "Company Name",
  "url": "https://company.com",
  "score": 85,
  "grade": "A",
  "stage": "Qualified",
  "next_action": "Send intro email to VP Engineering",
  "est_value": "$24,000 ARR",
  "component_scores": {
    "company_fit": 88,
    "contact_access": 75,
    "opportunity_quality": 90,
    "competitive_position": 82,
    "outreach_readiness": 80
  },
  "key_pain_point": "Manual API monitoring causing outages",
  "key_contact": "Jane Smith, VP Engineering",
  "risk_factors": "Long procurement cycle"
}
```

#### トップ見込み客データ
上位5社について以下の詳細データを抽出してください。
- 構成スコアの詳細内訳
- 役職を含む主要コンタクト
- 深刻度を含む課題
- 推奨アプローチ
- リスク要因

#### アクションアイテム
優先順位付きアクションリストを抽出してください。
```json
[
  {
    "priority": 1,
    "company": "Acme Corp",
    "action": "Send personalized email to VP Engineering",
    "urgency": "immediate",
    "reason": "Recent funding round creates budget window"
  }
]
```

#### パイプライン健全性指標
```json
{
  "total_prospects": 10,
  "average_score": 72,
  "a_grade_count": 3,
  "a_grade_pct": 30,
  "b_grade_count": 4,
  "b_grade_pct": 40,
  "c_grade_count": 2,
  "c_grade_pct": 20,
  "d_grade_count": 1,
  "d_grade_pct": 10,
  "highest_score": 92,
  "lowest_score": 35,
  "health_rating": "Good"
}
```

### ステップ4: JSON 入力ファイルの作成

カレントディレクトリの `_pdf_input.json` に抽出したすべてのデータを含む JSON ファイルを書き込んでください。

```json
{
  "title": "営業パイプラインレポート",
  "date": "2025-01-15",
  "overall_pipeline_score": 72,
  "health_rating": "良好",
  "total_prospects": 10,
  "prospects": [
    {
      "name": "...",
      "url": "...",
      "score": 85,
      "grade": "A",
      "stage": "資格認定済み",
      "next_action": "...",
      "est_value": "...",
      "component_scores": { ... },
      "key_pain_point": "...",
      "key_contact": "...",
      "risk_factors": "..."
    }
  ],
  "top_prospects": [ ... ],
  "action_items": [ ... ],
  "pipeline_health": { ... },
  "score_distribution": {
    "A+": { "count": 1, "pct": 10, "prospects": ["Acme Corp"] },
    "A": { "count": 2, "pct": 20, "prospects": ["Beta Inc", "Gamma Ltd"] },
    "B": { "count": 4, "pct": 40, "prospects": ["..."] },
    "C": { "count": 2, "pct": 20, "prospects": ["..."] },
    "D": { "count": 1, "pct": 10, "prospects": ["..."] }
  },
  "weekly_focus": [
    {
      "rank": 1,
      "company": "Acme Corp",
      "score": 92,
      "reason": "最高スコア、かつアクティブなトリガーイベントあり",
      "actions": ["VPエンジニアリング宛に紹介メールを送信", "LinkedInで接続", "デモをスケジュール"]
    }
  ],
  "methodology": {
    "company_fit_weight": 25,
    "contact_access_weight": 20,
    "opportunity_quality_weight": 20,
    "competitive_position_weight": 15,
    "outreach_readiness_weight": 20
  }
}
```

### ステップ5: PDF 生成スクリプトの確認

プロジェクトルートの `scripts/generate_pdf_report.py` に PDF 生成スクリプトが存在するか確認してください。

**プロジェクトルートの検索順序:** 以下の場所を順番に確認してください。
1. ai-sales-team-claude プロジェクトディレクトリ（agents/ および skills/ フォルダがある場所）
2. カレントディレクトリ
3. カレントディレクトリの一つ上のディレクトリ

**スクリプトが存在しない場合:**
- ユーザーに通知してください：「PDF 生成スクリプトが `scripts/generate_pdf_report.py` に見つかりませんでした。このスクリプトは AI Sales Team プロジェクトのセットアップの一部です。プロジェクトが正しくインストールされているか確認してください。」
- 処理を停止してください。

**スクリプトが存在する場合:**
- 実行に進んでください。

### ステップ6: PDF の生成

PDF 生成スクリプトを実行してください。

```bash
python3 scripts/generate_pdf_report.py _pdf_input.json "SALES-REPORT-$(date +%Y-%m-%d).pdf"
```

スクリプトは以下のセクションを含む PDF を生成します。

#### PDF セクション1: 表紙
- タイトル：「営業パイプラインレポート」
- 生成日
- 大きな円形ゲージで表示される総合パイプラインスコア（0〜100）
- カラーインジケータ付きパイプライン健全性評価
- クイック統計：見込み客総数、平均スコア、トップグレード件数

#### PDF セクション2: スコア内訳
- グレード帯別スコア分布の横棒グラフ
- カラーコード：A+ = 濃い緑、A = 緑、B = 青、C = オレンジ、D = 赤
- 件数とパーセンテージのラベル付き

#### PDF セクション3: 見込み客比較テーブル
- 全見込み客の一覧テーブル（列：順位、企業名、スコア、グレード、ステージ、次のアクション、推定規模）
- 読みやすさのための交互行カラー
- グレード列のカラーコード
- スコア降順でソート

#### PDF セクション4: トップ見込み客詳細
- トップ見込み客ごとに1ページ（または半ページ）
- 構成スコアのレーダーチャートまたは棒グラフ
- 主要コンタクトのリスト
- 課題とアプローチのサマリー
- リスク要因のハイライト

#### PDF セクション5: アクションプラン
- 番号付き優先アクションアイテムリスト
- タイムフレームでグループ化：即時・短期・パイプライン強化
- 企業名・具体的アクション・緊急度を記載

#### PDF セクション6: 評価方法論
- スコアリング方法論の簡潔な説明
- パーセンテージ付きウェイト内訳
- グレード帯の定義
- スコアが公開情報に基づいている旨の免責事項

### ステップ7: クリーンアップと報告

PDF 生成後：

1. PDF ファイルが作成されたことを確認し、ファイルサイズを確認してください。
2. 一時ファイル `_pdf_input.json` を削除してください。
3. ユーザーに以下を報告してください。
   - PDF ファイル名と保存場所
   - ファイルサイズ
   - ページ数
   - 内容のサマリー

---

## エラー処理

### reportlab が未インストールの場合
```
PDF 生成には reportlab Python ライブラリが必要です。
以下のコマンドでインストールしてください：pip install reportlab

インストールを実行しますか？
```

### Python が利用できない場合
```
PDF 生成に必要な Python 3 が見つかりませんでした。
https://python.org から Python 3 をインストールし、次を実行してください：
  pip install reportlab
```

### スクリプトが見つからない場合
```
PDF 生成スクリプトが scripts/generate_pdf_report.py に見つかりませんでした。
このスクリプトは AI Sales Team プロジェクトの一部です。プロジェクトの
ディレクトリ構造が正しいか確認してください。
```

### レポートデータがない場合
```
SALES-REPORT.md がカレントディレクトリに見つかりませんでした。
まず `/sales report` を実行してパイプラインレポートを生成し、その後
`/sales report-pdf` を実行して PDF 版を作成してください。
```

### PDF 生成が失敗した場合
Python スクリプトがエラーで終了した場合：
1. エラー出力を取得してください。
2. よくある問題を確認してください。
   - 不正な JSON 入力（不正なデータ形式）
   - ファイルパーミッションエラー
   - ディスク容量の問題
   - reportlab のバージョン非互換
3. 修正案とともに具体的なエラーをユーザーに報告してください。
4. デバッグ用に `_pdf_input.json` ファイルを保持してください（失敗時は削除しないこと）。

---

## 出力仕様

- **ファイル名:** `SALES-REPORT-{YYYY-MM-DD}.pdf`（当日の日付を使用）
- **ページサイズ:** レター（8.5" x 11"）
- **向き:** 基本は縦向き、幅広テーブルが必要な場合は横向き
- **カラースキーム:** プロフェッショナルな青とグレーを基調にカラーコードスコアインジケータを使用
- **フォント:** 読みやすさのために Helvetica または同様のサンセリフ体
- **余白:** 全辺 0.75 インチ
- **想定ページ数:** 見込み客数によって 4〜8 ページ

---

## 重要なルール

1. PDF 生成を試みる前に、必ず SALES-REPORT.md を確認してください。Markdown レポートなしに PDF を一から生成しないでください。
2. スクリプトを実行する前に、必ず reportlab を確認してください。未インストールの場合は明確なインストール手順を提供してください。
3. 成功時は一時ファイル（_pdf_input.json）を削除してください。失敗時はデバッグ用に保持してください。
4. JSON 入力は有効な JSON であること。スクリプトに渡す前にバリデーションを行ってください。
5. PDF スクリプトが失敗した場合、ユーザーがデバッグできるよう完全なエラー出力を提供してください。
6. PDF 生成中に元の SALES-REPORT.md ファイルを変更しないでください。
7. 生成成功後、最終的な PDF ファイルのパス・サイズ・ページ数をユーザーに報告してください。
8. 見込み客データが不完全な場合でも、利用可能なデータで PDF を生成してください。欠損データは PDF 内で「N/A」と表記してください。

#!/bin/bash
# ============================================================================
# AI Sales Team — Claude Code スキルインストーラー
# 14スキル · 5エージェント · スクリプト · PDF対応
# ============================================================================
set -e

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}║${NC}   ${CYAN}AI Sales Team — Claude Code スキル${NC}                         ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}   ${GREEN}14スキル · 5エージェント · スクリプト · PDF対応${NC}             ${BLUE}║${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ---------------------------------------------------------------------------
# スクリプトのディレクトリを検出（ローカル実行と curl | bash 両対応）
# ---------------------------------------------------------------------------
GITHUB_REPO="havaslabo/ai-sales-team-claude"
TEMP_DIR=""

if [ -n "${BASH_SOURCE[0]}" ] && [ "${BASH_SOURCE[0]}" != "bash" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$SCRIPT_DIR/install.sh" ] && [ -d "$SCRIPT_DIR/skills" ]; then
        SOURCE_DIR="$SCRIPT_DIR"
        echo -e "${GREEN}ローカルディレクトリからインストールします:${NC} $SOURCE_DIR"
    else
        SCRIPT_DIR=""
    fi
fi

if [ -z "${SCRIPT_DIR:-}" ] || [ ! -d "${SOURCE_DIR:-}" ]; then
    echo -e "${YELLOW}GitHub からクローン中...${NC}"
    TEMP_DIR=$(mktemp -d)
    if command -v git &>/dev/null; then
        git clone --depth 1 "https://github.com/$GITHUB_REPO.git" "$TEMP_DIR/repo" 2>/dev/null
        SOURCE_DIR="$TEMP_DIR/repo"
    else
        echo -e "${RED}エラー: git がインストールされていません。${NC}"
        echo "git をインストールするか、リポジトリをクローンしてから install.sh を実行してください。"
        exit 1
    fi
    echo -e "${GREEN}クローン完了。${NC}"
fi

# ---------------------------------------------------------------------------
# インストール先ディレクトリ
# ---------------------------------------------------------------------------
SKILLS_DIR="$HOME/.claude/skills"
AGENTS_DIR="$HOME/.claude/agents"

# ---------------------------------------------------------------------------
# Claude Code の確認
# ---------------------------------------------------------------------------
echo -e "${BLUE}前提条件を確認しています...${NC}"
if command -v claude &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Claude Code が見つかりました"
else
    echo -e "  ${YELLOW}⚠${NC} Claude Code CLI が見つかりません（スキルはインストールされますが、Claude Code が必要です）"
fi

# ---------------------------------------------------------------------------
# ディレクトリの作成
# ---------------------------------------------------------------------------
echo -e "${BLUE}ディレクトリを作成しています...${NC}"
mkdir -p "$SKILLS_DIR/sales/scripts"
mkdir -p "$SKILLS_DIR/sales/templates"
echo -e "  ${GREEN}✓${NC} スキルディレクトリ: $SKILLS_DIR"

mkdir -p "$AGENTS_DIR"
echo -e "  ${GREEN}✓${NC} エージェントディレクトリ: $AGENTS_DIR"

# ---------------------------------------------------------------------------
# メインスキル（オーケストレーター）のインストール
# ---------------------------------------------------------------------------
echo -e "${BLUE}スキルをインストールしています...${NC}"

INSTALL_COUNT=0

if [ -f "$SOURCE_DIR/sales/SKILL.md" ]; then
    cp "$SOURCE_DIR/sales/SKILL.md" "$SKILLS_DIR/sales/SKILL.md"
    echo -e "  ${GREEN}✓${NC} sales（オーケストレーター）"
    INSTALL_COUNT=$((INSTALL_COUNT + 1))
fi

# ---------------------------------------------------------------------------
# 13 サブスキルのインストール
# ---------------------------------------------------------------------------
SKILLS=(
    sales-prospect
    sales-research
    sales-qualify
    sales-contacts
    sales-outreach
    sales-followup
    sales-prep
    sales-proposal
    sales-objections
    sales-icp
    sales-competitors
    sales-report
    sales-report-pdf
)

for skill in "${SKILLS[@]}"; do
    if [ -f "$SOURCE_DIR/skills/$skill/SKILL.md" ]; then
        mkdir -p "$SKILLS_DIR/$skill"
        cp "$SOURCE_DIR/skills/$skill/SKILL.md" "$SKILLS_DIR/$skill/SKILL.md"
        echo -e "  ${GREEN}✓${NC} $skill"
        INSTALL_COUNT=$((INSTALL_COUNT + 1))
    else
        echo -e "  ${YELLOW}⚠${NC} $skill（ソースに見つかりません）"
    fi
done

# ---------------------------------------------------------------------------
# 5 エージェントのインストール
# ---------------------------------------------------------------------------
echo -e "${BLUE}エージェントをインストールしています...${NC}"

AGENT_COUNT=0
AGENTS=(
    sales-company
    sales-contacts
    sales-opportunity
    sales-competitive
    sales-strategy
)

for agent in "${AGENTS[@]}"; do
    if [ -f "$SOURCE_DIR/agents/$agent.md" ]; then
        cp "$SOURCE_DIR/agents/$agent.md" "$AGENTS_DIR/$agent.md"
        echo -e "  ${GREEN}✓${NC} $agent"
        AGENT_COUNT=$((AGENT_COUNT + 1))
    else
        echo -e "  ${YELLOW}⚠${NC} $agent（ソースに見つかりません）"
    fi
done

# ---------------------------------------------------------------------------
# Python スクリプトのインストール
# ---------------------------------------------------------------------------
echo -e "${BLUE}スクリプトをインストールしています...${NC}"

SCRIPT_COUNT=0
for script in "$SOURCE_DIR"/scripts/*.py; do
    if [ -f "$script" ]; then
        cp "$script" "$SKILLS_DIR/sales/scripts/"
        echo -e "  ${GREEN}✓${NC} $(basename "$script")"
        SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
    fi
done

# ---------------------------------------------------------------------------
# テンプレートのインストール
# ---------------------------------------------------------------------------
echo -e "${BLUE}テンプレートをインストールしています...${NC}"

TEMPLATE_COUNT=0
for template in "$SOURCE_DIR"/templates/*.md; do
    if [ -f "$template" ]; then
        cp "$template" "$SKILLS_DIR/sales/templates/"
        echo -e "  ${GREEN}✓${NC} $(basename "$template")"
        TEMPLATE_COUNT=$((TEMPLATE_COUNT + 1))
    fi
done

# ---------------------------------------------------------------------------
# Python 依存パッケージのインストール
# ---------------------------------------------------------------------------
echo -e "${BLUE}Python 依存パッケージをインストールしています...${NC}"

if command -v python3 &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Python 3 が見つかりました: $(python3 --version 2>&1)"

    # pip コマンドを確認
    PIP_CMD=""
    if command -v pip3 &>/dev/null; then
        PIP_CMD="pip3"
    elif command -v pip &>/dev/null; then
        PIP_CMD="pip"
    elif python3 -m pip --version &>/dev/null 2>&1; then
        PIP_CMD="python3 -m pip"
    fi

    if [ -n "$PIP_CMD" ]; then
        echo -e "  ${CYAN}reportlab をインストールしています...${NC}"
        if $PIP_CMD install --quiet reportlab 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} reportlab インストール完了"
        else
            # --user フラグで再試行
            if $PIP_CMD install --quiet --user reportlab 2>/dev/null; then
                echo -e "  ${GREEN}✓${NC} reportlab インストール完了（ユーザー環境）"
            else
                echo -e "  ${YELLOW}⚠${NC} reportlab のインストールに失敗しました"
                echo -e "      手動でインストールしてください: ${CYAN}pip3 install reportlab${NC}"
            fi
        fi

        echo -e "  ${CYAN}beautifulsoup4 をインストールしています...${NC}"
        if $PIP_CMD install --quiet beautifulsoup4 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} beautifulsoup4 インストール完了"
        else
            if $PIP_CMD install --quiet --user beautifulsoup4 2>/dev/null; then
                echo -e "  ${GREEN}✓${NC} beautifulsoup4 インストール完了（ユーザー環境）"
            else
                echo -e "  ${YELLOW}⚠${NC} beautifulsoup4 のインストールに失敗しました"
            fi
        fi

        echo -e "  ${CYAN}requests をインストールしています...${NC}"
        if $PIP_CMD install --quiet requests 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} requests インストール完了"
        else
            if $PIP_CMD install --quiet --user requests 2>/dev/null; then
                echo -e "  ${GREEN}✓${NC} requests インストール完了（ユーザー環境）"
            else
                echo -e "  ${YELLOW}⚠${NC} requests のインストールに失敗しました"
            fi
        fi
    else
        echo -e "  ${YELLOW}⚠${NC} pip が見つかりません。手動でインストールしてください:"
        echo -e "      ${CYAN}pip3 install reportlab beautifulsoup4 requests${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠${NC} Python 3 が見つかりません"
    echo -e "      PDF レポート機能を使用するには Python 3 が必要です"
    echo -e "      インストール: ${CYAN}https://www.python.org/downloads/${NC}"
fi

# ---------------------------------------------------------------------------
# 日本語フォントの確認
# ---------------------------------------------------------------------------
echo -e "${BLUE}日本語フォントを確認しています...${NC}"

FONT_OK=false

# reportlab の CID フォント（内蔵）を確認
if python3 -c "from reportlab.pdfbase.cidfonts import UnicodeCIDFont; from reportlab.pdfbase import pdfmetrics; pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} 日本語フォント（reportlab 内蔵 CID フォント）が利用可能です"
    FONT_OK=true
fi

# システムフォントの確認
if [ "$FONT_OK" = false ]; then
    FONT_PATHS=(
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
        "/Library/Fonts/NotoSansCJKjp-Regular.otf"
        "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf"
        "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
        "C:/Windows/Fonts/meiryo.ttc"
    )
    for font_path in "${FONT_PATHS[@]}"; do
        if [ -f "$font_path" ]; then
            echo -e "  ${GREEN}✓${NC} 日本語フォントが見つかりました: $font_path"
            FONT_OK=true
            break
        fi
    done
fi

if [ "$FONT_OK" = false ]; then
    echo -e "  ${YELLOW}⚠${NC} 日本語フォントが見つかりませんでした"
    echo -e "      PDF レポートで日本語が文字化けする場合は以下でインストールしてください:"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "      macOS:  ${CYAN}brew install font-noto-sans-cjk-japanese${NC}"
    else
        echo -e "      Linux:  ${CYAN}sudo apt install fonts-noto-cjk${NC}  または  ${CYAN}sudo yum install google-noto-sans-cjk-ttc-fonts${NC}"
    fi
fi

# ---------------------------------------------------------------------------
# 一時ディレクトリのクリーンアップ
# ---------------------------------------------------------------------------
if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
    echo -e "  ${GREEN}✓${NC} 一時ファイルをクリーンアップしました"
fi

# ---------------------------------------------------------------------------
# インストール完了サマリー
# ---------------------------------------------------------------------------
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  インストール完了！                                          ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${CYAN}スキル:${NC}         $INSTALL_COUNT 件  →  $SKILLS_DIR"
echo -e "  ${CYAN}エージェント:${NC}   $AGENT_COUNT 件  →  $AGENTS_DIR"
echo -e "  ${CYAN}スクリプト:${NC}     $SCRIPT_COUNT 件  →  $SKILLS_DIR/sales/scripts"
echo -e "  ${CYAN}テンプレート:${NC}   $TEMPLATE_COUNT 件  →  $SKILLS_DIR/sales/templates"
echo ""

# ---------------------------------------------------------------------------
# コマンドリファレンス
# ---------------------------------------------------------------------------
echo -e "${BLUE}コマンドリファレンス:${NC}"
echo ""
echo -e "  ${CYAN}/sales prospect <url>${NC}          完全な見込み客分析（5エージェント並列）"
echo -e "  ${CYAN}/sales quick <url>${NC}             60秒でのクイックスナップショット"
echo -e "  ${CYAN}/sales research <url>${NC}          企業リサーチ＆ファーモグラフィクス"
echo -e "  ${CYAN}/sales qualify <url>${NC}           リード評価（BANT + MEDDIC）"
echo -e "  ${CYAN}/sales contacts <url>${NC}          意思決定者の特定"
echo -e "  ${CYAN}/sales outreach <prospect>${NC}     アウトリーチシーケンスの生成"
echo -e "  ${CYAN}/sales followup <prospect>${NC}     フォローアップシーケンスの作成"
echo -e "  ${CYAN}/sales prep <url>${NC}              商談準備ブリーフ"
echo -e "  ${CYAN}/sales proposal <client>${NC}       クライアント提案書の生成"
echo -e "  ${CYAN}/sales objections <topic>${NC}      反論対応プレイブック"
echo -e "  ${CYAN}/sales icp <description>${NC}       理想顧客プロファイル（ICP）の作成"
echo -e "  ${CYAN}/sales competitors <url>${NC}       競合インテリジェンス"
echo -e "  ${CYAN}/sales report${NC}                  営業パイプラインレポート（Markdown）"
echo -e "  ${CYAN}/sales report-pdf${NC}              営業パイプラインレポート（PDF）"
echo ""
echo -e "  ${YELLOW}ヒント:${NC} まずは ${CYAN}/sales prospect <url>${NC} で完全分析を試してみましょう！"
echo ""

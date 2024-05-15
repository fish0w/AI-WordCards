AI-WordCardsは、OpenAIとStableDiffusionの力を活用して、教育的で魅力的なワードカードを作成する革新的なプロジェクトです。このプロジェクトはフロントエンドにStreamlitを使用し、直感的でインタラクティブ、ユーザーフレンドリーなインターフェースを提供します。AI-WordCardsは、言語学習者、教育者、そして興味を持つすべての人にとって、楽しく、ユニークで視覚的に魅力的な方法で語彙を拡張するのに最適です。現在、中国語、英語、日本語の3言語に対応しています。

#インストール
AI-WordCardsをインストールするには、次の手順に従ってください：

1.GitHubリポジトリをクローンします：
```bash 
git clone https://github.com/fish0w/AI-WordCards.git
```

2.プロジェクトディレクトリに移動します：
```bash 
cd AI-WordCards
```
3.requirements.txtファイルを使用してプロジェクトの依存関係をインストールします：
```bash 
pip install -r requirements.txt
```
4.config_.pyをリネームして、Keyを入力してください：
config_.pyをconfig.pyにリネームし、次の内容の中の「Your OPENAI Key」と「Your Stable Diffusion API Key」を実際のOpenAIおよびStable Diffusion APIキーで置き換えてください：
```bash 
OPENAI_KEY = "Your OPENAI Key" SD_API_KEY = "Your Stable Diffusion API Key"
```
# プロジェクトの実行
AI-WordCardsプロジェクトを起動するには、ターミナルで次のコマンドを実行します：
```bash 
streamlit run wordcard.py
```
このコマンドにより、プロジェクトが起動し、ウェブブラウザを介してアプリケーションにアクセスできます。AI-WordCardsでの探索と学習をお楽しみください！

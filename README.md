# SampleGame1

Unreal Engine 5.8 製のサードパーソンゲーム。鍵・扉・レバー・ダメージギミックを備えたステージクリア型ゲーム。

---

## 環境

- Unreal Engine 5.8
- Blueprint のみ（C++ なし）

---

## AIによるセットアップ手順

Python スクリプトを使って不足アセットを自動生成する。

### 1. Python プラグインを有効化

`Edit` → `Editor Preferences` → `Python` → **Enable Python Plugin** にチェック

### 2. プロジェクトを開く

`MyProject.uproject` を UE5.8 で開く

### 3. セットアップスクリプトを実行

`Window` → `Output Log` を開き、コンソールに以下を入力して Enter:

```
py "C:/Users/nabec/Documents/SampleGame1/setup_game.py"
```

作成されるアセット:
- `BP_Player` — BP_MyCharacter を継承したプレイヤーBP
- `BP_Enemy` — BP_MyCharacter を継承したエネミーBP
- `BP_Goal` — ゴール判定アクター（BoxCollision + StaticMesh）
- BP_DeadObject に NiagaraComponent（炎エフェクト用）を追加
- GameMode のデフォルトポーンを BP_Player に設定

### 4. SampleGame_1 レベルに配置

コンソールで実行:

```
py "C:/Users/nabec/Documents/SampleGame1/setup_level.py"
```

配置されるもの:
- BP_Key × 2、BP_Door × 1、BP_SwitchButton × 1
- BP_Lever × 1、BP_DeadObject × 2、BP_Goal × 1
- PlayerStart × 1

---

## 手動で完成させる箇所

Python では Blueprint のノードグラフを自動生成できないため、以下はエディタで実装する。

### BP_Player のイベントグラフ

1. `BP_Player` を開く → `Event BeginPlay`
   - `CreateWidget` (Class: UW_GameUI) → `Add to Viewport`
2. `BP_TestCharacter` の以下の変数・関数を `BP_Player` に移植:
   - 変数: `Age (int)`, `KeyStatus (ST_KeyStatus[])`, `bHasKey (bool)`
   - 関数: `UpdateKeyStatus`, `GetKeyStatus`, `UpdateMessage`
3. `OnCharacterHpChanged` ディスパッチャーをバインドして HP ゲージを更新

### BP_Goal のイベントグラフ

1. `BP_Goal` を開く → `Event BeginPlay` → BoxCollision の `OnComponentBeginOverlap` をバインド
2. Overlap 時:
   - `Cast to BP_Player` で成功したら
   - `BP_Player.UpdateMessage` で "Goal" を表示
   - `Delay` (3 秒)
   - `BP_MyGameInstance` のイベント状態をクリア
   - `Open Level` で SampleGame_1 を再読み込み

### N_Fire (Niagara炎エフェクト)

1. `Content/Project/Assets/Effects/` フォルダを作成
2. 右クリック → `FX` → `Niagara System` → `Fountain` テンプレートを選択
3. 名前を `N_Fire` に変更
4. Niagara エディタで以下を調整:
   - `Sprite Renderer` のカラーを橙〜赤に変更
   - `Spawn Rate`: 50〜100
   - `Lifetime`: 0.5〜1.0
   - `Scale Sprite Size` を追加してサイズ調整
5. `BP_DeadObject` を開き、FireEffect (NiagaraComponent) の `Niagara System Asset` に `N_Fire` を設定

### STM_Lever / STM_LeverBase メッシュ

1. `Place Actors` → `Geometry` → `Box` を2つ配置してレバー形状を作る
2. 選択して右クリック → `Convert to Static Mesh`
   - レバー本体: `STM_Lever`
   - 土台: `STM_LeverBase`
3. `Content/Project/Assets/Meshes/` に保存
4. `BP_Lever` を開き、メッシュコンポーネントに設定

---

## フォルダ構成

```
Content/
  Project/
    Assets/
      Animations/    アニメーションBP・各モーション
      Character/BP/  BP_MyCharacter, BP_Player, BP_Enemy
      Effects/       N_Fire (Niagara)
      Material/      各マテリアル
      Meshes/        スタティックメッシュ
    BluePrints/      ゲームロジックBP一式
    Input/           入力アクション・マッピング
    Levels/
      SampleGame_1/  メインゲームレベル
      TestLevel/     テスト用レベル
```

---

## 実装済みのBP一覧

| BP名 | 役割 |
|---|---|
| BP_MyCharacter | キャラクター基底クラス（HP, ダメージ処理） |
| BP_Player | プレイヤー（入力・カメラ・UI） |
| BP_Enemy | エネミー |
| BP_TestCharacter | 旧プレイヤーBP（参照用） |
| BP_Door | 鍵または スイッチで開く扉 |
| BP_Key | 取得できる鍵オブジェクト |
| BP_Lever | 左クリックで操作するレバー |
| BP_SwitchButton | 触れると反応するスイッチ |
| BP_DeadObject | 触れるとダメージを受けるオブジェクト |
| BP_Goal | ゴール判定 |
| BP_EventBase | イベント管理基底クラス |
| BP_MyGameMode | ゲームモード |
| BP_MyGameInstance | 進行状態の永続保存 |
| UW_GameUI | HUD（HP・メッセージ表示） |
| EN_KeyStatus | 鍵の状態列挙型 |
| EN_EventStatus | イベント状態列挙型 |
| ST_KeyStatus | 鍵の状態構造体 |
| DT_KeyStatus | 鍵のデータテーブル |

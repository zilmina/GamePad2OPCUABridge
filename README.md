# GamePad2OPCUABridge

## 概要

このプログラムは、接続されたゲームパッドのボタン入力状態をOPC UAサーバを介して配信するためのブリッジ機能を提供します。  
OPC UAクライアントは、本プログラムで公開されるノードへアクセスすることで、ゲームパッド入力を取得できます。

## 主な機能

- ゲームパッドのボタン状態をOPC UAノードとして公開  
- カウント用の変数 (`iCount`) を継続的にインクリメントし、OPC UAノードとして公開（サンプル的なカウンタ機能）  
- モニタリング用のサンプリング間隔を1msに設定することで、ボタン状態変化をより即時性の高い形で取得可能

## Install for Win11

Install Python
- pip install numpy
- pip install opcua
- pip install pygame

## OPC UAアドレススペース仕様

### 接続情報

- OPC UA エンドポイント: `opc.tcp://0.0.0.0:4840/freeopcua/server/`  
- Namespace URI: `http://hilab.com/UiConnector`

### ノード構造
Objects
├─ GamePad (Object)
│   └─ bButtons (Variable: Boolean)
└─ Count (Object)
    └─ iCount (Variable: UInt32)


#### GamePadオブジェクト

- `bButtons (Variable)`  
  - データ型: ブール型配列 (List[Boolean])  
  - OPC UAの `ua.Variant` としてブール配列を格納  
  - 接続されているゲームパッドの「ボタン数」に対応する要素数を持つ  
  - `True` は押下状態、`False` は非押下状態を示す  
  - 配列のインデックスは `0` から始まり、`0`番目の要素がゲームパッド上の最初のボタン状態に対応

#### Countオブジェクト

- `iCount (Variable)`  
  - データ型: UInt32  
  - プログラム起動後、一定周期（本コードでは約10ms間隔）でインクリメントされるカウンタ値  
  - 接続確認やシステム動作テスト用として利用可能

## 内部処理フロー（概要）

1. OPC UAサーバ起動とエンドポイント設定
2. `GamePad` および `Count` オブジェクトを生成し、`bButtons` と `iCount` 変数を作成
3. ゲームパッド接続試行（接続確認までリトライ）
4. メインループで以下を定期更新:
    - `iCount` をインクリメント
    - ゲームパッドボタン状態 (`bButtons`) を取得し更新

## 今後の拡張アイデア

- 入力処理のさらなる遅延削減  
- エラーハンドリング強化  
- アナログスティック入力への対応

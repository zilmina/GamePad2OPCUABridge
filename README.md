# GamePad2OPCUABridge

## 概要
このプログラムは、接続されたゲームパッド（**Joy-Con(R)**）の**ボタン入力**と**アナログスティック入力**を、OPC UAサーバ経由でリアルタイム配信するブリッジです。  
> **本リポジトリはサーバー実装のみ**を含みます。クライアント実装は含みません（下記「関連リポジトリ」を参照）。

---

## 主な機能
- `bButtons`: ボタン状態（Boolean[]）を公開  
- `dAxes`: アナログスティックなど軸値（Double[]）を公開  
- 既定モニタ間隔：1 ms（`default_monitored_item_sampling_interval = 1`）  
- 非同期IO（`asyncio`）による効率的動作  
- 未接続時は **5秒ごと** に自動リトライ

---

## 動作環境
- **OS**: Windows 11 Pro  
- **Python**: 3.12.8  
- **必要ライブラリ**:
  ```bash
  pip install numpy
  pip install asyncua==1.1.5
  pip install pygame==2.6.1


⸻

OPC UA アドレススペース
	•	エンドポイント: opc.tcp://0.0.0.0:4841/freeopcua/server/
	•	Namespace URI: https://github.com/zilmina/GamePad2OPCUABridge

Objects
└─ Joystick (Object)
    ├─ bButtons (Variable: Boolean[])
    └─ dAxes    (Variable: Double[])

	•	bButtons: True=押下 / False=非押下。配列長はJoy-Con検出ボタン数に一致
	•	dAxes: 通常 –1.0〜1.0。配列長は検出軸数に一致

⸻

実行手順（サーバー）

1. Joy-Con(R) を Bluetooth で接続
	1.	設定 → Bluetooth とデバイス を開く
	2.	Joy-Con(R) をペアリングし、接続状態「接続済み」を確認

2. サーバー起動

python AsyncGamePad.py

初回接続時に以下のようなログが出力されます：

Joystick connected: Joy-Con (R)  
Button Count: 12, Axis Count: 4

3. 動作確認（任意の OPC UA クライアント）
	•	例：UaExpert
	•	接続先：opc.tcp://<サーバーIP>:4841/freeopcua/server/
	•	Objects → Joystick → bButtons, dAxes を購読または読み取り

⸻

実機検証条件

ハードウェア

項目	内容
PC	GMKtec G3（with Intel I-V225）
メモリ	8.00 GB（7.75 GB 使用可能）
ゲームパッド	Joy-Con (R)
接続方法	Bluetooth

ソフトウェア

項目	バージョン
OS	Windows 11 Pro
Python	3.12.8
asyncua	1.1.5
pygame	2.6.1
numpy	1.26.4

検証結果例（Joy-Con R）
	•	ボタン数: 12（A/B/X/Y/SL/SR/+/–/HOME/キャプチャ/R/ZR）
	•	軸数: 4（例：右スティック X/Y 軸＋他2軸）
	•	更新周期: 約 10 ms 間隔で bButtons / dAxes が更新される

Joy-Con の入力マッピングは OS/ドライバ依存です。必要に応じて OPC UA クライアント側で実測マッピングしてください。

⸻

Bluetooth 接続安定性について

Joy-Con(R) の Bluetooth が切断された場合は、以下の手順で復帰を確認してください：
	1.	Joy-Con(R) のペアリングを解除
	2.	OPC UA サーバを再起動
	3.	Joy-Con(R) を再ペアリング
	4.	UaExpert 等で接続を再確認

⸻

関連リポジトリ（クライアント）

本リポジトリではクライアント実装を含みません。TwinCAT 向けのクライアントは別リポジトリで管理する予定です。
	•	TwinCAT-OPCUA-GamepadClient（予定）
	•	bButtons / dAxes を TwinCAT TF6100 から購読し、PLC 変数へマッピング
	•	例：ARRAY[0..11] OF BOOL（ボタン）、ARRAY[0..3] OF LREAL（軸）
	•	接続先：opc.tcp://<サーバーIP>:4841/freeopcua/server/（Anonymous 可）

⸻


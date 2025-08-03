import asyncio
from asyncua import ua, Server
import pygame
import os
import time  # 時間計測用

os.environ["SDL_VIDEODRIVER"] = "dummy"

async def main():
    # OPC UAサーバーの初期化
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4841/freeopcua/server/")
    server.default_monitored_item_sampling_interval = 1  # 単位: ミリ秒
    uri = "https://github.com/zilmina/GamePad2OPCUABridge"
    idx = await server.register_namespace(uri)

    # ジョイスティックオブジェクトの定義
    objects = server.nodes.objects
    joystickObj = await objects.add_object(idx, "Joystick")

    pygame.init()
    bActiveGamepad = False
    bButtonsVar = None
    dAxesVar = None  # 修正: fAxesVar → dAxesVar
    buttonCount = 0
    axisCount = 0

    while not bActiveGamepad:
        try:
            # ゲームパッドの初期化
            joys = pygame.joystick.Joystick(0)
            joys.init()
            print(f"Joystick connected: {joys.get_name()}")

            # 初回の接続時にボタン数と軸数を取得
            buttonCount = joys.get_numbuttons()
            axisCount = joys.get_numaxes()

            print(f"Button Count: {buttonCount}, Axis Count: {axisCount}")

            # ボタンと軸の変数を初期化
            bButtonsVar = await joystickObj.add_variable(
                idx, "bButtons", [False] * buttonCount, ua.VariantType.Boolean
            )
            dAxesVar = await joystickObj.add_variable(  # 修正: fAxesVar → dAxesVar
                idx, "dAxes", [0.0] * axisCount, ua.VariantType.Double
            )

            # 配列の次元と固定長を設定
            await bButtonsVar.write_array_dimensions([buttonCount])
            await dAxesVar.write_array_dimensions([axisCount])  # 修正: fAxesVar → dAxesVar

            # ValueRankを設定（1次元配列であることを明示）
            await bButtonsVar.write_value_rank(1)
            await dAxesVar.write_value_rank(1)  # 修正: fAxesVar → dAxesVar

            # 書き込み可能に設定
            await bButtonsVar.set_writable()
            await dAxesVar.set_writable()  # 修正: fAxesVar → dAxesVar

            bActiveGamepad = True
        except pygame.error:
            print("Waiting for joystick connection...")
            await asyncio.sleep(5)

    async with server:
        try:
            while True:
                await asyncio.sleep(0.01)
                pygame.event.pump()

                # 動作時間の計測開始
                start_time = time.monotonic()

                # ボタンと軸の状態を取得（接続時の値に基づく）
                bButtons = [bool(joys.get_button(i)) for i in range(buttonCount)]
                dAxes = [joys.get_axis(i) for i in range(axisCount)]  # 修正: fAxes → dAxes

                # 動作時間の計測終了
                elapsed_time_ms = (time.monotonic() - start_time) * 1000000  # ミリ秒に変換
                # print(f"bButtons, dAxes取得時間: {elapsed_time_ms:.3f} ms")  # 修正: fAxes → dAxes

                # 値を更新
                await bButtonsVar.write_value(bButtons)
                await dAxesVar.write_value(dAxes)  # 修正: fAxesVar → dAxesVar

        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    asyncio.run(main())
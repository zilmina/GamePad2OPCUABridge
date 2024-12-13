# GamePad2OPCUABridge
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# Author: zilmina
# Contact: kawase4mt@gmail.com
# Repository: https://github.com/zilmina/GamePad2OPCUABridge
#
# File: GamePadServer.py
# Description: [A brief description of the file’s purpose, e.g., "This script connects a gamepad to an OPC UA server."]
#

import numpy as np

# import for UPCUA
import sys
sys.path.insert(0, "..")
import time
from opcua import ua, Server

# import for pygame
import pygame
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

if __name__ == "__main__":

    # setup our server
    server = Server()
    # モニタリング用のデフォルトサンプリング間隔を100ms以下に設定
    server.default_monitored_item_sampling_interval = 1  # 単位: ミリ秒

    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "https://github.com/zilmina/GamePad2OPCUABridge"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "GamePad")
    myobj2 = objects.add_object(idx, "Count")
    iCount = myobj2.add_variable(idx, "iCount", 0)

    # pygameの初期化
    pygame.init()
    bActiveGamepad = False
    while not bActiveGamepad:
        try:
            # ジョイスティックインスタンスの生成
            joys = pygame.joystick.Joystick(0)
            # ジョイスティックの初期化
            joys.init()
            print('ジョイスティックの名前:', joys.get_name())
            print('ボタン数 :', joys.get_numbuttons())
            bActiveGamepad = True
        except pygame.error:
            print('ジョイスティックが接続されていません')
            time.sleep(5)

    boolean_array = [False] * joys.get_numbuttons() #dummy data
    bButtons = myobj.add_variable(idx, "bButtons", ua.Variant(boolean_array,ua.VariantType.Boolean))

    # bButtons.set_writable()  # クライアントからの変更を許可

    # starting!
    server.start()
    
    try:
        count = 0
        while True:
            time.sleep(0.01)
            events = pygame.event.get()
            # for event in events:
            #     print(event)
            count += 1
            iCount.set_value(ua.Variant(np.uint32(count),ua.VariantType.UInt32))
            # print("{:.1f}".format(count)) #カウントアップ値を表示
            button_count = joys.get_numbuttons()
            button_states = [joys.get_button(i) for i in range(button_count)]
            bButtons.set_value(ua.Variant(button_states,ua.VariantType.Boolean))
            # print(f"ボタン状態: {button_states}")
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()
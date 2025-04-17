import openvr
import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import mojimoji
import time

class JapaneseKeyboardVR:
    def __init__(self):
        # OpenVRの初期化
        self.vr = openvr.init(openvr.VRApplication_Overlay)
        self.overlay = self._create_overlay()
        
        # キーボードの設定
        self.keyboard_layout = [
            ['あ', 'い', 'う', 'え', 'お'],
            ['か', 'き', 'く', 'け', 'こ'],
            ['さ', 'し', 'す', 'せ', 'そ'],
            ['た', 'ち', 'つ', 'て', 'と'],
            ['な', 'に', 'ぬ', 'ね', 'の'],
            ['は', 'ひ', 'ふ', 'へ', 'ほ'],
            ['ま', 'み', 'む', 'め', 'も'],
            ['や', 'ゆ', 'よ', 'わ', 'を'],
            ['ん', '、', '。', '変換', '削除']
        ]
        
        # 入力テキスト
        self.input_text = ""
        self.conversion_text = ""
        
        # キーボードの位置とサイズ
        self.keyboard_pos = np.array([0, 0, -1])  # 正面1mの位置
        self.key_size = 0.1  # キーのサイズ（メートル）
        
        # コントローラーの状態
        self.left_controller = None
        self.right_controller = None
        
    def _create_overlay(self):
        overlay = openvr.VROverlay()
        overlay_key = "japanese_keyboard"
        overlay_name = "Japanese Keyboard"
        overlay.createOverlay(overlay_key, overlay_name)
        return overlay
    
    def _update_controller_positions(self):
        poses = self.vr.getDeviceToAbsoluteTrackingPose(
            openvr.TrackingUniverseStanding, 0, openvr.k_unMaxTrackedDeviceCount
        )
        
        for i in range(openvr.k_unMaxTrackedDeviceCount):
            if poses[i].bPoseIsValid:
                device_class = self.vr.getTrackedDeviceClass(i)
                if device_class == openvr.TrackedDeviceClass_Controller:
                    if self.vr.getControllerRoleForTrackedDeviceIndex(i) == openvr.TrackedControllerRole_LeftHand:
                        self.left_controller = poses[i]
                    elif self.vr.getControllerRoleForTrackedDeviceIndex(i) == openvr.TrackedControllerRole_RightHand:
                        self.right_controller = poses[i]
    
    def _get_key_at_position(self, position):
        # キーボードの位置からキーを特定
        relative_pos = position - self.keyboard_pos
        row = int((relative_pos[1] + 0.5) / self.key_size)
        col = int((relative_pos[0] + 0.25) / self.key_size)
        
        if 0 <= row < len(self.keyboard_layout) and 0 <= col < len(self.keyboard_layout[0]):
            return self.keyboard_layout[row][col]
        return None
    
    def _handle_input(self):
        if self.right_controller is not None:
            # コントローラーの位置を取得
            controller_pos = np.array([
                self.right_controller.mDeviceToAbsoluteTracking[0][3],
                self.right_controller.mDeviceToAbsoluteTracking[1][3],
                self.right_controller.mDeviceToAbsoluteTracking[2][3]
            ])
            
            # トリガーボタンの状態を取得
            trigger_value = self.vr.getControllerState(self.right_controller.deviceIndex).rAxis[1].x
            
            if trigger_value > 0.5:  # トリガーが押されている
                key = self._get_key_at_position(controller_pos)
                if key:
                    if key == "変換":
                        self._convert_text()
                    elif key == "削除":
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += key
    
    def _convert_text(self):
        # ローマ字から漢字への変換（簡易的な実装）
        if self.input_text:
            # 実際のアプリケーションでは、より高度な変換エンジンを使用
            self.conversion_text = mojimoji.han_to_zen(self.input_text)
    
    def _render_keyboard(self):
        # キーボードの描画
        for row in range(len(self.keyboard_layout)):
            for col in range(len(self.keyboard_layout[0])):
                key = self.keyboard_layout[row][col]
                key_pos = self.keyboard_pos + np.array([
                    col * self.key_size - 0.2,
                    -row * self.key_size + 0.4,
                    0
                ])
                
                # キーの描画（OpenGLを使用）
                glPushMatrix()
                glTranslatef(*key_pos)
                glBegin(GL_QUADS)
                glColor3f(0.8, 0.8, 0.8)
                glVertex3f(-self.key_size/2, -self.key_size/2, 0)
                glVertex3f(self.key_size/2, -self.key_size/2, 0)
                glVertex3f(self.key_size/2, self.key_size/2, 0)
                glVertex3f(-self.key_size/2, self.key_size/2, 0)
                glEnd()
                glPopMatrix()
    
    def run(self):
        try:
            while True:
                self._update_controller_positions()
                self._handle_input()
                self._render_keyboard()
                
                # 入力テキストの表示
                print(f"入力: {self.input_text}")
                if self.conversion_text:
                    print(f"変換: {self.conversion_text}")
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("アプリケーションを終了します")
        finally:
            openvr.shutdown()

if __name__ == "__main__":
    app = JapaneseKeyboardVR()
    app.run() 
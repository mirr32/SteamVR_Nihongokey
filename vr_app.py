import openvr
import time

def main():
    # OpenVRの初期化
    vr = openvr.init(openvr.VRApplication_Scene)
    
    print("SteamVRが初期化されました")
    
    try:
        while True:
            # コントローラーの状態を取得
            poses = vr.getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseStanding, 0, openvr.k_unMaxTrackedDeviceCount)
            
            # ヘッドセットの位置と向きを取得
            hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
            if hmd_pose.bPoseIsValid:
                position = hmd_pose.mDeviceToAbsoluteTracking
                print(f"ヘッドセットの位置: {position}")
            
            time.sleep(0.1)  # 10Hzで更新
            
    except KeyboardInterrupt:
        print("アプリケーションを終了します")
    finally:
        openvr.shutdown()

if __name__ == "__main__":
    main() 
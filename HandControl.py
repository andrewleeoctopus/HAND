#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import rospy
from sr_robot_commander.sr_hand_commander import SrHandCommander
import time

if __name__ == '__main__':
    # ROS节点名可以保持不变，或者如果您想同时运行控制左右手的脚本，可以区分它们
    rospy.init_node("sr_left_hand_joint_control_example", anonymous=True)

    # 1. 实例化 SrHandCommander 为左手
    # 确保 "left_hand" (或类似名称如 "lh_hand") 是在您机器人的 SRDF 文件中定义的正确组名
    # 您可能还需要指定 'prefix' 参数，例如 prefix="lh"
    LEFT_HAND_GROUP_NAME = "left_hand" # 或者 "lh_hand"，请根据您的 SRDF 文件确认
    try:
        # 尝试只使用组名，如果不行，可以尝试添加 prefix="lh"
        hand_commander = SrHandCommander(name=LEFT_HAND_GROUP_NAME)
        # 或者 hand_commander = SrHandCommander(name=LEFT_HAND_GROUP_NAME, prefix="lh")
        rospy.loginfo("SrHandCommander '%s' 初始化成功。", LEFT_HAND_GROUP_NAME)
    except Exception as e:
        rospy.logerr("初始化 SrHandCommander 失败: %s", e)
        rospy.logerr("请确保 '%s' 组在 SRDF 中已定义，并且 MoveIt 服务正在运行。", LEFT_HAND_GROUP_NAME)
        exit()

    # 2. 定义左手的目标关节角度 (以度为单位)
    # 注意：所有关节名称的前缀已从 "rh_" 更改为 "lh_"
    # 具体的关节数量和名称取决于您的左手型号

    target_joint_angles_close_left = {
        'lh_FFJ1': 90.0, 'lh_FFJ2': 90.0, 'lh_FFJ3': 90.0, 'lh_FFJ4': 0.0,
        'lh_MFJ1': 90.0, 'lh_MFJ2': 90.0, 'lh_MFJ3': 90.0, 'lh_MFJ4': 0.0,
        'lh_RFJ1': 90.0, 'lh_RFJ2': 90.0, 'lh_RFJ3': 90.0, 'lh_RFJ4': 0.0,
        'lh_LFJ1': 90.0, 'lh_LFJ2': 90.0, 'lh_LFJ3': 90.0, 'lh_LFJ4': 0.0, # 'lh_LFJ5': 0.0, (如有)
        'lh_THJ1': 60.0, 'lh_THJ2': 40.0, 'lh_THJ3': 10.0, 'lh_THJ4': 70.0, 'lh_THJ5': 20.0,
        # 'lh_WRJ1': 0.0, 'lh_WRJ2': 0.0 # (如有且属于手组)
    }

    target_joint_angles_open_left = {
        'lh_FFJ1': 0.0, 'lh_FFJ2': 0.0, 'lh_FFJ3': 0.0, 'lh_FFJ4': 0.0,
        'lh_MFJ1': 0.0, 'lh_MFJ2': 0.0, 'lh_MFJ3': 0.0, 'lh_MFJ4': 0.0,
        'lh_RFJ1': 0.0, 'lh_RFJ2': 0.0, 'lh_RFJ3': 0.0, 'lh_RFJ4': 0.0,
        'lh_LFJ1': 0.0, 'lh_LFJ2': 0.0, 'lh_LFJ3': 0.0, 'lh_LFJ4': 0.0, # 'lh_LFJ5': 0.0,
        'lh_THJ1': 0.0, 'lh_THJ2': 0.0, 'lh_THJ3': 0.0, 'lh_THJ4': 0.0, 'lh_THJ5': 0.0,
        # 'lh_WRJ1': 0.0, 'lh_WRJ2': 0.0
    }

    hand_commander.set_max_velocity_scaling_factor(1.0) 

    rospy.loginfo("准备将左手移动到 'open' 状态...")
    hand_commander.move_to_joint_value_target(
        target_joint_angles_open_left,
        wait=True,
        angle_degrees=True
    )
    rospy.loginfo("左手已移动到 'open' 状态。")

    time.sleep(2) # 等待2秒

    rospy.loginfo("准备将左手移动到 'close' 状态...")
    hand_commander.move_to_joint_value_target(
        target_joint_angles_close_left,
        wait=True,
        angle_degrees=True
    )
    rospy.loginfo("左手已移动到 'close' 状态。")

    rospy.loginfo("左手控制示例完成。")
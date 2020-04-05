/**
 * Created by Administrator on 2018/4/24.
 */
module G559 {
    let i18n_cn = {
        //进入游戏,连接
        "enter_game_tips": "读取数据中...",
        "connect_failed": "链接服务器失败",
        "refresh_roomInfo_tips": "正在获取房间内数据...",
        "requesting_data": "请求数据中，请稍等...",

        //退出房间
        "exit_game_tips": "正在退出房间，清理数据中。。",

        //重连
        "reconnecting_tips": "网络连接中，请稍候。。",
        "reconnecting_failed_tips": "网络重连失败,请检测您的网络是否连通。点击“确定”继续重连，点击“取消”退出游戏。",

        //房间解散退出相关
        "start_btn_tips": "开始游戏",
        "dissolve_btn_tips": "解散房间",
        "exit_btn_tips": "离开房间",
        "invite_btn_tips": "邀请好友",
        "secede_btn_tips": "退出房间",

        "dissolve_room_tips": "是否要解散房间？",
        "exit_room_tips": "是否要退出房间？",
        "dissolved_room_tips": "房主已解散房间，点击确认退出房间。",
        "dissolve_success_tips": "解散房间成功，点击确认显示结算。",
        "reconnect_room_dissolved_tips": "重连失败，房间已解散或者你尚未加入该房间",


        //解散房间
        "ds_ask": "退出将会向其他玩家发出解散申请，是否继续？",
        "ds_tips": "玩家{0}申请解散房间，请等待其他玩家选择（超过{1}分钟未做选择，则默认同意）",
        "ds_wait": "等待选择",
        "ds_agree": "同意解散",
        "ds_disagree": "不同意解散",
        "ds_failed": "解散房间失败",

        //个人信息
        "pr_sex0": "未知",
        "pr_sex1": "男",
        "pr_sex2": "女",
        "pr_ID": "编号：",

        "no_lastSetUserData": "无上局结算数据。",

        //voice
        "voice_record_cancel": "松开手指取消",
        "voice_recording": "松开手指发送\n向上滑动取消",
        "voice_playing_cant_record": "正在播放其他玩家的语音，无法录制",
        "voice_record_cd": "发言频繁",
        "voice_record_short": "发言过短",

        //gps
        "gps_setting_auth": "请您开启定位功能",
        "gps_no_data1": "正在定位中...",
        "gps_no_data2": "未开定位",
        "gps_pos_desc3": "上家",
        "gps_pos_desc2": "对家",
        "gps_pos_desc1": "下家",
        "gps_pos_desc_pattern": "与{0}距离：{1}",
        "gps_valid_distance1": "30米以内",
        "gps_valid_distance2": "100米以内",
        "gps_valid_distance3": "300米以外",
        "gps_valid_distance4": "500米以外",
        "gps_valid_distance5": "千米之外",

        //流程打牌提示
        "no_discard": "不要",
        "btn_discard": "出牌",
        "btn_tips": "提示",

        "no_discard_tips": "您没有更大的牌可以打出",

        "discard_error_tips1": "请选择要出的牌",
        "discard_error_tips2": "选择的牌不符合规则",
        "discard_error_tips3": "首轮必须先出黑桃3",
        "discard_error_tips3_1": "首轮必须先出方块3",
        "discard_error_tips4": "报单必须出最大的",

        "invite_title": "东胜-跑得快-",
        "invite_waiting_count": "【{0}缺{1}】",

        //     未开定位
        //     正在定位中…
        // 30米以内 （小于30）
        // 100米以内（大于30且小于100）
        // 300米以外（大于100且小于500）
        // 500米以外（大于500且小于2000）
        // 千米之外 （大于2000）
    };
    export let getText = function (key) {
        return ExtendMgr.inst.getText4Language(i18n_cn[key]);
    }
}
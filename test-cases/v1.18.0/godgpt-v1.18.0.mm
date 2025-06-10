<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE map SYSTEM "http://freemind.sourceforge.net/dtd/freemind.dtd">
<map version="1.0.1">
    <node ID="ID_ROOT" MODIFIED="1710400000000" TEXT="全部测试用例" FOLDED="false">
        <!-- 历史记录模块 -->
        <node ID="ID_HISTORY" MODIFIED="1710400000000" POSITION="right" TEXT="历史记录" FOLDED="true">
            <node ID="ID_3" MODIFIED="1710400000000" TEXT="RENAME-001: 点击Rename弹出对话框测试" FOLDED="false">
                <node ID="ID_4" MODIFIED="1710400000000" TEXT="优先级: P0"/>
                <node ID="ID_5" MODIFIED="1710400000000" TEXT="前置条件: 用户已登录且有历史记录"/>
                <node ID="ID_6" MODIFIED="1710400000000" TEXT="测试步骤: 点击侧边栏历史记录的Rename按钮"/>
                <node ID="ID_7" MODIFIED="1710400000000" TEXT="预期结果">
                    <node ID="ID_8" MODIFIED="1710400000000" TEXT="1. 菜单栏收起"/>
                    <node ID="ID_9" MODIFIED="1710400000000" TEXT="2. 键盘弹出"/>
                    <node ID="ID_10" MODIFIED="1710400000000" TEXT="3. 弹出Rename Chat对话框"/>
                    <node ID="ID_11" MODIFIED="1710400000000" TEXT="4. 光标自动定位至标题末尾"/>
                </node>
            </node>
            <node ID="ID_12" MODIFIED="1710400000000" TEXT="RENAME-002: 取消重命名测试" FOLDED="false">
                <node ID="ID_13" MODIFIED="1710400000000" TEXT="优先级: P0"/>
                <node ID="ID_14" MODIFIED="1710400000000" TEXT="前置条件: RENAME-001已执行"/>
                <node ID="ID_15" MODIFIED="1710400000000" TEXT="测试步骤: 点击Cancel按钮"/>
                <node ID="ID_16" MODIFIED="1710400000000" TEXT="预期结果">
                    <node ID="ID_17" MODIFIED="1710400000000" TEXT="1. 键盘收起"/>
                    <node ID="ID_18" MODIFIED="1710400000000" TEXT="2. 弹框关闭"/>
                    <node ID="ID_19" MODIFIED="1710400000000" TEXT="3. 标题保持不变"/>
                </node>
            </node>
            <node ID="ID_20" MODIFIED="1710400000000" TEXT="RENAME-003: 确认重命名测试" FOLDED="false">
                <node ID="ID_21" MODIFIED="1710400000000" TEXT="优先级: P0"/>
                <node ID="ID_22" MODIFIED="1710400000000" TEXT="前置条件: RENAME-001已执行"/>
                <node ID="ID_23" MODIFIED="1710400000000" TEXT="测试数据: 新标题: Test Chat"/>
                <node ID="ID_24" MODIFIED="1710400000000" TEXT="测试步骤">
                    <node ID="ID_25" MODIFIED="1710400000000" TEXT="1. 编辑标题为Test Chat"/>
                    <node ID="ID_26" MODIFIED="1710400000000" TEXT="2. 点击Confirm按钮"/>
                </node>
                <node ID="ID_27" MODIFIED="1710400000000" TEXT="预期结果">
                    <node ID="ID_28" MODIFIED="1710400000000" TEXT="1. 键盘收起"/>
                    <node ID="ID_29" MODIFIED="1710400000000" TEXT="2. 弹框关闭"/>
                    <node ID="ID_30" MODIFIED="1710400000000" TEXT="3. 标题更新为Test Chat"/>
                </node>
            </node>
        </node>

        <!-- 支付功能模块 -->
        <node ID="ID_PAYMENT" MODIFIED="1710400000000" POSITION="right" TEXT="支付功能" FOLDED="true">
            <node ID="ID_32" MODIFIED="1710400000000" TEXT="IAP-001: IAP支付成功测试" FOLDED="false">
                <node ID="ID_33" MODIFIED="1710400000000" TEXT="优先级: P0"/>
                <node ID="ID_34" MODIFIED="1710400000000" TEXT="前置条件: iOS设备已登录且未订阅"/>
                <node ID="ID_35" MODIFIED="1710400000000" TEXT="测试数据: Weekly Premium订阅, $6"/>
                <node ID="ID_36" MODIFIED="1710400000000" TEXT="测试步骤">
                    <node ID="ID_37" MODIFIED="1710400000000" TEXT="1. 选择Weekly Premium订阅"/>
                    <node ID="ID_38" MODIFIED="1710400000000" TEXT="2. 点击订阅按钮"/>
                    <node ID="ID_39" MODIFIED="1710400000000" TEXT="3. 确认IAP支付"/>
                </node>
                <node ID="ID_40" MODIFIED="1710400000000" TEXT="预期结果">
                    <node ID="ID_41" MODIFIED="1710400000000" TEXT="1. 支付成功"/>
                    <node ID="ID_42" MODIFIED="1710400000000" TEXT="2. 跳转首页"/>
                    <node ID="ID_43" MODIFIED="1710400000000" TEXT="3. credits隐藏"/>
                    <node ID="ID_44" MODIFIED="1710400000000" TEXT="4. 显示Payment successful提示"/>
                </node>
            </node>
            <node ID="ID_45" MODIFIED="1710400000000" TEXT="IAP-002: IAP支付失败测试" FOLDED="false">
                <node ID="ID_46" MODIFIED="1710400000000" TEXT="优先级: P0"/>
                <node ID="ID_47" MODIFIED="1710400000000" TEXT="前置条件: iOS设备已登录且未订阅"/>
                <node ID="ID_48" MODIFIED="1710400000000" TEXT="测试数据: Weekly Premium订阅, $6"/>
                <node ID="ID_49" MODIFIED="1710400000000" TEXT="测试步骤">
                    <node ID="ID_50" MODIFIED="1710400000000" TEXT="1. 选择Weekly Premium订阅"/>
                    <node ID="ID_51" MODIFIED="1710400000000" TEXT="2. 点击订阅按钮"/>
                    <node ID="ID_52" MODIFIED="1710400000000" TEXT="3. 模拟支付失败"/>
                </node>
                <node ID="ID_53" MODIFIED="1710400000000" TEXT="预期结果">
                    <node ID="ID_54" MODIFIED="1710400000000" TEXT="1. 显示Payment failed. Please try again."/>
                    <node ID="ID_55" MODIFIED="1710400000000" TEXT="2. 充值弹框关闭"/>
                    <node ID="ID_56" MODIFIED="1710400000000" TEXT="3. 页面保持不变"/>
                </node>
            </node>
            <node ID="ID_57" MODIFIED="1710400000000" TEXT="IAP-003: IAP取消订阅测试" FOLDED="false">
                <node ID="ID_58" MODIFIED="1710400000000" TEXT="优先级: P0"/>
                <node ID="ID_59" MODIFIED="1710400000000" TEXT="前置条件: iOS设备已订阅Premium"/>
                <node ID="ID_60" MODIFIED="1710400000000" TEXT="测试数据: Weekly Premium订阅"/>
                <node ID="ID_61" MODIFIED="1710400000000" TEXT="测试步骤">
                    <node ID="ID_62" MODIFIED="1710400000000" TEXT="1. 进入订阅管理"/>
                    <node ID="ID_63" MODIFIED="1710400000000" TEXT="2. 点击取消订阅"/>
                </node>
                <node ID="ID_64" MODIFIED="1710400000000" TEXT="预期结果">
                    <node ID="ID_65" MODIFIED="1710400000000" TEXT="1. 订阅状态更新为已取消"/>
                    <node ID="ID_66" MODIFIED="1710400000000" TEXT="2. 显示订阅到期时间"/>
                </node>
            </node>
        </node>

        <!-- 订阅管理模块 -->
        <node ID="ID_SUBSCRIPTION" MODIFIED="1710400000000" POSITION="right" TEXT="订阅管理" FOLDED="true">
            <node ID="ID_68" TEXT="SUB-001: 切换到Weekly Premium订阅测试" FOLDED="false">
                <node ID="ID_69" TEXT="优先级: P0"/>
                <node ID="ID_70" TEXT="前置条件: 用户已登录未订阅"/>
                <node ID="ID_71" TEXT="测试数据: Weekly Premium $6"/>
                <node ID="ID_72" TEXT="测试步骤">
                    <node ID="ID_73" TEXT="1. 进入订阅页面"/>
                    <node ID="ID_74" TEXT="2. 选择Weekly Premium"/>
                </node>
                <node ID="ID_75" TEXT="预期结果">
                    <node ID="ID_76" TEXT="1. 显示价格$6"/>
                    <node ID="ID_77" TEXT="2. 显示just $0.85/day"/>
                    <node ID="ID_78" TEXT="3. 显示Start for $6"/>
                    <node ID="ID_79" TEXT="4. 显示Perfect for a 7-day glimpse into your future"/>
                </node>
            </node>
            <node ID="ID_80" TEXT="SUB-002: 切换到Monthly Premium订阅测试" FOLDED="false">
                <node ID="ID_81" TEXT="优先级: P0"/>
                <node ID="ID_82" TEXT="前置条件: 用户已登录未订阅"/>
                <node ID="ID_83" TEXT="测试数据: Monthly Premium $20"/>
                <node ID="ID_84" TEXT="测试步骤">
                    <node ID="ID_85" TEXT="1. 进入订阅页面"/>
                    <node ID="ID_86" TEXT="2. 选择Monthly Premium"/>
                </node>
                <node ID="ID_87" TEXT="预期结果">
                    <node ID="ID_88" TEXT="1. 显示价格$20"/>
                    <node ID="ID_89" TEXT="2. 显示just $0.66/day"/>
                    <node ID="ID_90" TEXT="3. 显示Upgrade for $20"/>
                    <node ID="ID_91" TEXT="4. 显示Stay aligned. Daily insights for your month ahead"/>
                </node>
            </node>
            <node ID="ID_140" TEXT="SUB-007: Premium订阅限流测试" FOLDED="false">
                <node ID="ID_141" TEXT="优先级: P0"/>
                <node ID="ID_142" TEXT="前置条件: 用户已订阅Premium"/>
                <node ID="ID_143" TEXT="测试数据: 消息数: 101"/>
                <node ID="ID_144" TEXT="测试步骤: 在3小时内发送101条消息"/>
                <node ID="ID_145" TEXT="预期结果: 第101条消息提示已达到限制"/>
            </node>
            <node ID="ID_146" TEXT="SUB-008: Ultimate订阅无限流测试" FOLDED="false">
                <node ID="ID_147" TEXT="优先级: P0"/>
                <node ID="ID_148" TEXT="前置条件: 用户已订阅Ultimate"/>
                <node ID="ID_149" TEXT="测试数据: 消息数: 101"/>
                <node ID="ID_150" TEXT="测试步骤: 在3小时内发送101条消息"/>
                <node ID="ID_151" TEXT="预期结果: 第101条消息正常发送无限制"/>
            </node>
        </node>

        <!-- Badge显示模块 -->
        <node ID="ID_BADGE" MODIFIED="1710400000000" POSITION="right" TEXT="Badge显示" FOLDED="true">
            <node ID="ID_153" TEXT="BADGE-001: Weekly Premium Badge显示测试" FOLDED="false">
                <node ID="ID_154" TEXT="优先级: P0"/>
                <node ID="ID_155" TEXT="前置条件: 用户已登录未订阅"/>
                <node ID="ID_156" TEXT="测试数据: Weekly Premium"/>
                <node ID="ID_157" TEXT="测试步骤: 订阅Weekly Premium"/>
                <node ID="ID_158" TEXT="预期结果">
                    <node ID="ID_159" TEXT="1. 显示Weekly Badge"/>
                    <node ID="ID_160" TEXT="2. 显示7天有效期"/>
                </node>
            </node>
            <node ID="ID_161" TEXT="BADGE-002: Annual Premium Badge显示测试" FOLDED="false">
                <node ID="ID_162" TEXT="优先级: P0"/>
                <node ID="ID_163" TEXT="前置条件: BADGE-001执行完成"/>
                <node ID="ID_164" TEXT="测试数据: Annual Premium"/>
                <node ID="ID_165" TEXT="测试步骤: 订阅Annual Premium"/>
                <node ID="ID_166" TEXT="预期结果">
                    <node ID="ID_167" TEXT="1. 显示Annual Badge"/>
                    <node ID="ID_168" TEXT="2. 显示397天有效期(7+390)"/>
                </node>
            </node>
            <node ID="ID_169" TEXT="BADGE-003: Weekly Ultimate Badge显示测试" FOLDED="false">
                <node ID="ID_170" TEXT="优先级: P0"/>
                <node ID="ID_171" TEXT="前置条件: BADGE-002执行完成"/>
                <node ID="ID_172" TEXT="测试数据: Weekly Ultimate"/>
                <node ID="ID_173" TEXT="测试步骤: 订阅Weekly Ultimate"/>
                <node ID="ID_174" TEXT="预期结果">
                    <node ID="ID_175" TEXT="1. 显示Weekly Ultimate Badge"/>
                    <node ID="ID_176" TEXT="2. 显示7天无限期权"/>
                    <node ID="ID_177" TEXT="3. 7天后变为Annual Premium"/>
                </node>
            </node>
            <node ID="ID_178" TEXT="BADGE-004: Annual Ultimate Badge显示测试" FOLDED="false">
                <node ID="ID_179" TEXT="优先级: P0"/>
                <node ID="ID_180" TEXT="前置条件: BADGE-003执行完成"/>
                <node ID="ID_181" TEXT="测试数据: Annual Ultimate"/>
                <node ID="ID_182" TEXT="测试步骤: 订阅Annual Ultimate"/>
                <node ID="ID_183" TEXT="预期结果">
                    <node ID="ID_184" TEXT="1. 显示Annual Ultimate Badge"/>
                    <node ID="ID_185" TEXT="2. 显示397天无限期权"/>
                </node>
            </node>
            <node ID="ID_186" TEXT="BADGE-005: Premium升级限制测试" FOLDED="false">
                <node ID="ID_187" TEXT="优先级: P0"/>
                <node ID="ID_188" TEXT="前置条件: 用户已订阅Weekly Ultimate"/>
                <node ID="ID_189" TEXT="测试步骤: 查看Premium订阅选项"/>
                <node ID="ID_190" TEXT="预期结果">
                    <node ID="ID_191" TEXT="1. Premium所有plan按钮置灰"/>
                    <node ID="ID_192" TEXT="2. 显示Already on Ultimate"/>
                </node>
            </node>
        </node>

        <!-- 到期时间显示模块 -->
        <node ID="ID_EXPIRATION" MODIFIED="1710400000000" POSITION="right" TEXT="到期时间显示" FOLDED="true">
            <node ID="ID_194" TEXT="EXP-001: 未订阅时间显示测试" FOLDED="false">
                <node ID="ID_195" TEXT="优先级: P0"/>
                <node ID="ID_196" TEXT="前置条件: 用户已登录未订阅"/>
                <node ID="ID_197" TEXT="测试步骤: 查看订阅到期时间"/>
                <node ID="ID_198" TEXT="预期结果: 不显示任何到期时间信息"/>
            </node>
            <node ID="ID_199" TEXT="EXP-002: Premium未取消时间显示测试" FOLDED="false">
                <node ID="ID_200" TEXT="优先级: P0"/>
                <node ID="ID_201" TEXT="前置条件: 用户已订阅Premium且未取消"/>
                <node ID="ID_202" TEXT="测试数据: 到期时间: 2024-01-23"/>
                <node ID="ID_203" TEXT="测试步骤: 查看订阅到期时间"/>
                <node ID="ID_204" TEXT="预期结果: 显示Your premium plan renews on January 23,2024"/>
            </node>
            <node ID="ID_205" TEXT="EXP-003: Premium已取消时间显示测试" FOLDED="false">
                <node ID="ID_206" TEXT="优先级: P0"/>
                <node ID="ID_207" TEXT="前置条件: 用户已订阅Premium且已取消"/>
                <node ID="ID_208" TEXT="测试数据: 到期时间: 2024-01-23"/>
                <node ID="ID_209" TEXT="测试步骤: 查看订阅到期时间"/>
                <node ID="ID_210" TEXT="预期结果: 显示Your premium plan expires on January 23,2024"/>
            </node>
            <node ID="ID_211" TEXT="EXP-004: Ultimate未取消带Premium时间显示测试" FOLDED="false">
                <node ID="ID_212" TEXT="优先级: P0"/>
                <node ID="ID_213" TEXT="前置条件: 用户已订阅Ultimate且有Premium且未取消"/>
                <node ID="ID_214" TEXT="测试数据">
                    <node ID="ID_215" TEXT="Ultimate到期: 2024-01-23"/>
                    <node ID="ID_216" TEXT="Premium到期: 2024-02-23"/>
                </node>
                <node ID="ID_217" TEXT="测试步骤: 查看订阅到期时间"/>
                <node ID="ID_218" TEXT="预期结果: 显示Your ultimate plan renews on January 23,2024. After that, your premium plan expires on February 23,2024"/>
            </node>
            <node ID="ID_219" TEXT="EXP-005: Ultimate已取消带Premium时间显示测试" FOLDED="false">
                <node ID="ID_220" TEXT="优先级: P0"/>
                <node ID="ID_221" TEXT="前置条件: 用户已订阅Ultimate且有Premium且已取消"/>
                <node ID="ID_222" TEXT="测试数据">
                    <node ID="ID_223" TEXT="Ultimate到期: 2024-01-23"/>
                    <node ID="ID_224" TEXT="Premium到期: 2024-02-23"/>
                </node>
                <node ID="ID_225" TEXT="测试步骤: 查看订阅到期时间"/>
                <node ID="ID_226" TEXT="预期结果: 显示Your ultimate plan expires on January 23,2024. After that, your premium plan expires on February 23,2024"/>
            </node>
        </node>

        <!-- 消息交互模块 -->
        <node ID="ID_MESSAGE" MODIFIED="1710400000000" POSITION="right" TEXT="消息交互" FOLDED="true">
            <node ID="ID_240" TEXT="COPY-001: 长按选词测试" FOLDED="false">
                <node ID="ID_241" TEXT="优先级: P0"/>
                <node ID="ID_242" TEXT="前置条件: iOS/Android端有对话内容"/>
                <node ID="ID_243" TEXT="测试数据: 回复内容"/>
                <node ID="ID_244" TEXT="测试步骤: 长按回复内容中的文字"/>
                <node ID="ID_245" TEXT="预期结果">
                    <node ID="ID_246" TEXT="1. 自动选中离点击位置最近的2个字或1个单词"/>
                    <node ID="ID_247" TEXT="2. 出现Copy按钮"/>
                </node>
            </node>
            <node ID="ID_248" TEXT="COPY-002: 拖动选择测试" FOLDED="false">
                <node ID="ID_249" TEXT="优先级: P0"/>
                <node ID="ID_250" TEXT="前置条件: COPY-001已执行"/>
                <node ID="ID_251" TEXT="测试数据: 回复内容"/>
                <node ID="ID_252" TEXT="测试步骤">
                    <node ID="ID_253" TEXT="1. 拖动选中范围向上扩展"/>
                    <node ID="ID_254" TEXT="2. 拖动选中范围向下扩展"/>
                </node>
                <node ID="ID_255" TEXT="预期结果">
                    <node ID="ID_256" TEXT="1. 拖动时Copy按钮暂时隐藏"/>
                    <node ID="ID_257" TEXT="2. 拖动结束后Copy按钮重新出现"/>
                    <node ID="ID_258" TEXT="3. 选中范围正确扩展或缩小"/>
                </node>
            </node>
            <node ID="ID_259" TEXT="COPY-003: 取消选中测试" FOLDED="false">
                <node ID="ID_260" TEXT="优先级: P0"/>
                <node ID="ID_261" TEXT="前置条件: COPY-001已执行"/>
                <node ID="ID_262" TEXT="测试数据: 回复内容"/>
                <node ID="ID_263" TEXT="测试步骤">
                    <node ID="ID_264" TEXT="1. 点击已选中的文字"/>
                    <node ID="ID_265" TEXT="2. 再次点击已选中的文字"/>
                    <node ID="ID_266" TEXT="3. 点击非选中区域"/>
                </node>
                <node ID="ID_267" TEXT="预期结果">
                    <node ID="ID_268" TEXT="1. 第一次点击关闭Copy按钮"/>
                    <node ID="ID_269" TEXT="2. 第二次点击打开Copy按钮"/>
                    <node ID="ID_270" TEXT="3. 点击非选中区域取消选中状态"/>
                </node>
            </node>
            <node ID="ID_271" TEXT="COPY-004: 复制内容测试" FOLDED="false">
                <node ID="ID_272" TEXT="优先级: P0"/>
                <node ID="ID_273" TEXT="前置条件: COPY-001已执行"/>
                <node ID="ID_274" TEXT="测试数据: 回复内容"/>
                <node ID="ID_275" TEXT="测试步骤: 点击Copy按钮"/>
                <node ID="ID_276" TEXT="预期结果: 以纯文本模式复制选中内容到剪贴板"/>
            </node>
            <node ID="ID_277" TEXT="COPY-005: Android全选测试" FOLDED="false">
                <node ID="ID_278" TEXT="优先级: P0"/>
                <node ID="ID_279" TEXT="前置条件: Android端有对话内容"/>
                <node ID="ID_280" TEXT="测试数据: 回复内容"/>
                <node ID="ID_281" TEXT="测试步骤">
                    <node ID="ID_282" TEXT="1. 长按文字显示功能框"/>
                    <node ID="ID_283" TEXT="2. 点击Select All"/>
                </node>
                <node ID="ID_284" TEXT="预期结果">
                    <node ID="ID_285" TEXT="1. 选中所有回答内容"/>
                    <node ID="ID_286" TEXT="2. 功能框保持打开状态"/>
                    <node ID="ID_287" TEXT="3. Select All按钮隐藏"/>
                </node>
            </node>
            <node ID="ID_288" TEXT="COPY-006: iOS无全选测试" FOLDED="false">
                <node ID="ID_289" TEXT="优先级: P0"/>
                <node ID="ID_290" TEXT="前置条件: iOS端有对话内容"/>
                <node ID="ID_291" TEXT="测试数据: 回复内容"/>
                <node ID="ID_292" TEXT="测试步骤: 长按文字显示功能框"/>
                <node ID="ID_293" TEXT="预期结果: 功能框中不显示Select All选项"/>
            </node>
        </node>
    </node>
</map> 
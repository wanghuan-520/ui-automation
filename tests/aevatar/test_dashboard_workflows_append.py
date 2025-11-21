        logger.info("=" * 80)
        logger.info("🎉 E2E测试完成: Import Workflow功能验证通过")
        logger.info("=" * 80)

    @pytest.mark.e2e
    @pytest.mark.p2
    @allure.title("E2E-P2: 删除Workflow功能验证")
    @allure.description("端到端测试：验证删除Workflow的完整流程")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_workflow_e2e(self):
        """
        E2E测试: 删除Workflow功能
        验证点：删除操作、确认弹窗、列表更新
        """
        logger.info("=" * 80)
        logger.info("🗑️ 开始E2E测试: 删除Workflow功能 [P2]")
        logger.info("=" * 80)
        
        # 1. 确保有可删除的工作流 (如果没有，先创建一个)
        current_list = self.workflows_page.get_workflow_list()
        if not current_list:
            logger.info("当前列表为空，创建一个临时工作流用于删除")
            self.workflows_page.create_and_configure_workflow()
            self.workflows_page.navigate() # 返回列表页
            current_list = self.workflows_page.get_workflow_list()
            
        initial_count = len(current_list)
        target_workflow = current_list[0]
        target_name = target_workflow["name"]
        logger.info(f"📍 准备删除工作流: {target_name}, 当前总数: {initial_count}")
        self.page_utils.screenshot_step("01-删除前列表")
        
        # 2. 执行删除操作
        success = self.workflows_page.delete_workflow(target_name)
        assert success, f"删除工作流失败: {target_name}"
        self.page_utils.screenshot_step("02-删除操作完成")
        logger.info(f"✅ 工作流删除操作已执行: {target_name}")
        
        # 3. 验证列表更新
        # 刷新页面确保数据同步
        self.workflows_page.refresh_page()
        self.page.wait_for_timeout(2000)
        
        updated_list = self.workflows_page.get_workflow_list()
        updated_count = len(updated_list)
        logger.info(f"📍 删除后工作流总数: {updated_count}")
        
        assert updated_count == initial_count - 1, \
            f"删除后数量不正确: 期望 {initial_count - 1}, 实际 {updated_count}"
            
        # 验证被删除的特定项（如果原列表没有重名，或者我们删除了所有重名中的一个）
        # 由于可能有重名，这里主要验证数量减少
        
        self.page_utils.screenshot_step("03-删除验证成功")
        logger.info("✅ 删除验证成功: 列表数量已减少")
        
        logger.info("=" * 80)
        logger.info("🎉 E2E测试完成: 删除Workflow功能验证通过")
        logger.info("=" * 80)


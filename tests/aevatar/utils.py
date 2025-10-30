#!/usr/bin/env python3
"""
Aevatar 测试工具类
包含测试数据加载、选择器查找等辅助函数
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class TestDataLoader:
    """测试数据加载器"""
    
    @staticmethod
    def load_yaml_data(filename: str = "aevatar_test_data.yaml") -> Dict:
        """
        加载YAML测试数据文件
        
        Args:
            filename: YAML文件名
            
        Returns:
            解析后的YAML数据字典
        """
        # 获取项目根目录
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent
        yaml_path = project_root / "test-data" / filename
        
        logger.info(f"📂 加载测试数据: {yaml_path}")
        
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                logger.info(f"✅ 测试数据加载成功")
                return data
        except FileNotFoundError:
            logger.error(f"❌ 测试数据文件不存在: {yaml_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"❌ YAML解析失败: {e}")
            raise
    
    @staticmethod
    def get_login_scenarios(tag: str = None) -> List[Dict]:
        """
        获取登录测试场景
        
        Args:
            tag: 可选的标签过滤（如 "positive", "negative", "smoke"）
            
        Returns:
            登录场景列表
        """
        data = TestDataLoader.load_yaml_data()
        scenarios = data.get('login_scenarios', [])
        
        if tag:
            scenarios = [s for s in scenarios if tag in s.get('tags', [])]
        
        logger.info(f"📋 获取 {len(scenarios)} 个登录测试场景")
        return scenarios
    
    @staticmethod
    def get_workflow_scenarios(tag: str = None) -> List[Dict]:
        """
        获取workflow测试场景
        
        Args:
            tag: 可选的标签过滤
            
        Returns:
            workflow场景列表
        """
        data = TestDataLoader.load_yaml_data()
        scenarios = data.get('workflow_scenarios', [])
        
        if tag:
            scenarios = [s for s in scenarios if tag in s.get('tags', [])]
        
        logger.info(f"📋 获取 {len(scenarios)} 个workflow测试场景")
        return scenarios
    
    @staticmethod
    def get_environment_config() -> Dict:
        """获取环境配置"""
        data = TestDataLoader.load_yaml_data()
        return data.get('environment', {})
    
    @staticmethod
    def get_browser_config() -> Dict:
        """获取浏览器配置"""
        data = TestDataLoader.load_yaml_data()
        return data.get('browser', {})
    
    @staticmethod
    def get_selectors(section: str) -> Dict:
        """
        获取页面选择器配置
        
        Args:
            section: 选择器分类（如 "login", "workflow"）
            
        Returns:
            选择器字典
        """
        data = TestDataLoader.load_yaml_data()
        selectors = data.get('selectors', {})
        return selectors.get(section, {})


class SelectorHelper:
    """选择器辅助类"""
    
    @staticmethod
    async def find_element_with_selectors(page, selectors: List[str], timeout: int = 3000):
        """
        使用多个选择器尝试查找元素
        
        Args:
            page: Playwright页面对象
            selectors: 选择器列表
            timeout: 超时时间（毫秒）
            
        Returns:
            找到的元素，如果都找不到则返回None
        """
        for selector in selectors:
            try:
                element = await page.wait_for_selector(selector, timeout=timeout)
                if element:
                    logger.info(f"✅ 找到元素: {selector}")
                    return element
            except Exception as e:
                logger.debug(f"选择器未找到元素: {selector}")
                continue
        
        logger.warning(f"⚠️ 所有选择器都未找到元素")
        return None
    
    @staticmethod
    async def check_error_message(page, expected_keywords: List[str] = None, timeout: int = 5000) -> bool:
        """
        检查页面上是否出现错误消息
        
        Args:
            page: Playwright页面对象
            expected_keywords: 期望的错误关键词列表
            timeout: 超时时间（毫秒）
            
        Returns:
            是否找到匹配的错误消息
        """
        # 获取错误消息选择器
        error_selectors = TestDataLoader.get_selectors('login').get('error_message', [])
        
        for selector in error_selectors:
            try:
                error_element = await page.wait_for_selector(selector, timeout=timeout)
                if error_element:
                    error_text = await error_element.inner_text()
                    logger.info(f"🔍 找到错误消息: {error_text}")
                    
                    # 如果指定了期望的关键词，检查是否匹配
                    if expected_keywords:
                        for keyword in expected_keywords:
                            if keyword.lower() in error_text.lower():
                                logger.info(f"✅ 错误消息包含期望关键词: {keyword}")
                                return True
                    else:
                        # 没有指定关键词，只要找到错误消息就返回True
                        return True
            except:
                continue
        
        logger.warning("⚠️ 未找到错误消息")
        return False


def pytest_generate_tests(metafunc):
    """
    Pytest钩子函数，用于动态生成参数化测试
    """
    # 如果测试函数有 scenario 参数，从YAML加载数据
    if "login_scenario" in metafunc.fixturenames:
        scenarios = TestDataLoader.get_login_scenarios()
        metafunc.parametrize(
            "login_scenario", 
            scenarios,
            ids=[s['id'] for s in scenarios]
        )
    
    if "workflow_scenario" in metafunc.fixturenames:
        scenarios = TestDataLoader.get_workflow_scenarios()
        metafunc.parametrize(
            "workflow_scenario",
            scenarios,
            ids=[s['id'] for s in scenarios]
        )


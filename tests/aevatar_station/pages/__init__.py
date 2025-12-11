# Aevatar Station Page Objects
# 页面对象模块初始化文件

from tests.aevatar_station.pages.base_page import BasePage
from tests.aevatar_station.pages.landing_page import LandingPage
from tests.aevatar_station.pages.login_page import LoginPage
from tests.aevatar_station.pages.register_page import RegisterPage
from tests.aevatar_station.pages.dashboard_page import DashboardPage
from tests.aevatar_station.pages.profile_settings_page import ProfileSettingsPage
from tests.aevatar_station.pages.admin_panel_page import AdminPanelPage
from tests.aevatar_station.pages.admin_users_page import AdminUsersPage
from tests.aevatar_station.pages.admin_roles_page import AdminRolesPage
from tests.aevatar_station.pages.admin_settings_page import AdminSettingsPage
from tests.aevatar_station.pages.feature_management_page import FeatureManagementPage
from tests.aevatar_station.pages.settings_emailing_page import SettingsEmailingPage

__all__ = [
    'BasePage',
    'LandingPage',
    'LoginPage',
    'RegisterPage',
    'DashboardPage',
    'ProfileSettingsPage',
    'AdminPanelPage',
    'AdminUsersPage',
    'AdminRolesPage',
    'AdminSettingsPage',
    'FeatureManagementPage',
    'SettingsEmailingPage',
]

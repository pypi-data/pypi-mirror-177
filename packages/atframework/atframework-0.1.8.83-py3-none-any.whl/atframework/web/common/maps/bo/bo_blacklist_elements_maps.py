"""
Created on Aug 13, 2021

@author: Siro

"""


class BoBlacklistElementsMaps(object):

    bo_blacklist_select_type_css = "select[name='includeItem.type'][id='_includeItem_type']"
    bo_blacklist_select_type_css_excluded = "select[name='excludeItem.type'][id='_excludeItem_type']"
    bo_blacklist_select_type_value_country = "country"
    bo_blacklist_select_country_css = "select[name='includeItem.value'][id='_includeItem_value']"
    bo_blacklist_add_button_xpath = "//*[@id='_0']"
    bo_blacklist_add_button_xpath_excluded = "//div[@class='bo-group bo-group--blacklist-excluded-add']//div[@class='bo-buttons-area']//span"
    bo_blacklist_first_row_value_xpath = "//*[@id='blacklistIncluded']/tbody/tr[1]/td[1]"
    bo_blacklist_first_row_value_xpath_excluded = "//*[@id ='blacklistExcluded']/tbody/tr[1]/td[1]"
    bo_blacklist_first_row_remove_button_xpath = "//*[@id='blacklistIncluded']/tbody/tr[1]/td[5]/a"
    bo_blacklist_first_row_remove_button_xpath_excluded = "//*[@id='blacklistExcluded']/tbody/tr[1]/td[5]/a"
    bo_blacklist_select_type_value_ip_address = "Ip Address"
    bo_blacklist_select_include_value_css = "input[type='text'][name='includeItem.value']"
    bo_blacklist_select_include_value_css_user_excluded = "input[type='text'][name='excludeItem.value'][class='bo-field__control form-control bo-field__control--textfield bo-blacklist-excluded-user']"
    bo_blacklist_select_include_value_css_excluded = "input[type='text'][name='excludeItem.value']"
    bo_blacklist_select_type_value_credit_card = "Credit Card"
    bo_blacklist_select_type_value_user = "User"
    bo_blacklist_select_type_value_subdivision = "Subdivision"

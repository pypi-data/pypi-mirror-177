"""
Created on Aug 18, 2021

@author: Siro

"""


class BoGameTransactionElementsMaps(object):
    bo_game_transaction_link_css = "a[class='bo-nav__control'][href='gameTransactions!view']"
    bo_game_transaction_search_header_xpath = "//*[@id='bo-page-games-transactions']/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]"
    bo_game_transaction_header_text = "Search transaction(s)"

    bo_game_transaction_round_id_field_css = "input[type='text'][name='gameRoundId'][id='gameTransactions_gameRoundId']"
    bo_game_transaction_round_id_field_xpath = "//*[@id='gameTransactions_gameRoundId']"
    bo_game_transaction_from_xpath = "//*[@id='gameTransactions_from']"
    bo_game_transaction_to_xpath = "//*[@id='gameTransactions_to']"

    bo_game_transaction_search_button_xpath = "//*[@id='gameTransactions_0']"
    bo_game_transaction_table_first_row_round_id_item_live = '//*[@id="transactionsLive"]/tbody/tr/td[14]/a'

    bo_game_transaction_round_status_field_css = "select[name='gameRoundStatus'][id='gameTransactions_gameRoundStatus']"
    bo_game_transaction_round_status_value = "Win"
    bo_game_transaction_table_first_row_game_status_item_live = '//*[@id="transactionsLive"]/tbody/tr[1]/td[13]/a'
    bo_game_transaction_game_provider_field_xpath = "//*[@id='gameTransactions']/fieldset/div[1]/div/div[2]/div[2]/div/div/div[1]"
    bo_game_transaction_game_provider_type_field_css = "input[placeholder='Search options'][class='fstQueryInput']"
    bo_game_transaction_game_provider_value = "Microgaming"
    bo_game_transaction_game_provider_result_xpath = '//*[@id="gameTransactions"]/fieldset/div[1]/div/div[2]/div[2]/div/div/div[2]/div/span'
    bo_game_transaction_table_first_row_game_provider_item_live = '//*[@id="transactionsLive"]/tbody/tr[1]/td[4]/a'



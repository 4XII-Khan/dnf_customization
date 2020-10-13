#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging
from decimal import Decimal, ROUND_HALF_UP


class DnfTools:

    def __init__(self, deal_gold, proportion, poundage, auction_token_money, point_iscount):
        """

        :param deal_gold: 交易金币
        :param proportion: 售卖比例
        :param poundage: 交易税点
        :param auction_token_money: 拍卖行售卖1亿 需点券
        :param point_iscount: 点券购买折扣
        """
        # 交易金币
        self.deal_gold = deal_gold
        # 比例
        self.proportion = proportion
        # 税点
        self.poundage = poundage
        # 缴纳rmb
        self.rmb = 0
        # 税后金币
        self.after_tax_gold = 0
        # 税后比例
        self.after_tax_proportion = 0
        # 拍卖代币券
        self.auction_token_money = auction_token_money
        # 代币券比例（1亿）
        self.token_money_proportion = 0
        # 代币券税点
        self.token_money_poundage = 0.01
        # 税后金币
        self.after_tax_token_money = 0
        # 点券折扣
        self.point_iscount = point_iscount
        # 直接购买点券
        self.cost_point = 0

    @staticmethod
    def cuntom_round(cer):
        """
        精确四舍五入
        """
        _cer = Decimal(str(cer)).quantize(Decimal("0.00000"), rounding=ROUND_HALF_UP)
        cer = "%.3f" % (_cer)
        return cer

    def payable_rmb(self):
        """
        获取实际缴纳rmb
        :return:
        """
        self.rmb = DnfTools.cuntom_round(self.deal_gold / self.proportion)

    def get_after_tax_gold(self):
        """
        获取实际税后金币
        :return:
        """
        self.after_tax_gold = DnfTools.cuntom_round(self.deal_gold * (1 - self.poundage))

    def get_after_tax_proportion(self):
        """
        获取税后的实际金币比例
        :return:
        """
        self.payable_rmb()
        self.get_after_tax_gold()
        self.after_tax_proportion = DnfTools.cuntom_round(float(self.after_tax_gold) / float(self.rmb))

    def get_token_money_proportion(self):
        """
        计算拍卖行金币售卖 比例
        :return:
        """
        self.token_money_proportion = DnfTools.cuntom_round(10000 / (self.auction_token_money * 0.01))

    def get_token_money(self):
        """
        计算税后获取代币券
        :return:
        """
        self.get_after_tax_gold()
        self.get_token_money_proportion()
        self.after_tax_token_money = DnfTools.cuntom_round(float(self.after_tax_gold) / float(self.token_money_proportion))

    def get_cost_point(self):
        """
        计算获取同等代币券需要的rmb数量
        :return:
        """
        self.cost_point = DnfTools.cuntom_round(float(self.after_tax_token_money) * float(self.point_iscount))

    @staticmethod
    def asr_log(level, log):
        """
        日志模块
        :param level:
        :param log:
        :param log_filename:
        :return:
        """
        if level.upper() == 'ERROR':

            print("{0}[31;2m{1}{2}[0m".format(chr(27), log, chr(27)))
        elif level.upper() == 'INFO':

            print("{0}[32;2m{1}{2}[0m".format(chr(27), log, chr(27)))
        elif level.upper() == 'WARN':

            print("{0}[33;2m{1}{2}[0m".format(chr(27), log, chr(27)))

if __name__ == "__main__":
    dnf = DnfTools(50000, 68.31, 0.03, 20030, 0.95)

    dnf.payable_rmb()
    dnf.get_after_tax_gold()
    dnf.get_after_tax_proportion()
    dnf.get_token_money_proportion()
    dnf.get_token_money()
    dnf.get_cost_point()

    log = "购买金币(万)：{7}, 花费Rmb：{0}, 金币购买比例：{1}\n    " \
          "税后实际到手金币(万)：{2}, 税后金币比例：{3}\n    " \
          "拍卖行比例：{4}, 税后实际到手代币券：{5} \n    " \
          "点券充值折扣：{8} 获取同等代币券需花费rmb：{6} ".format(
           dnf.rmb, dnf.proportion, dnf.after_tax_gold,
           dnf.after_tax_proportion, dnf.token_money_proportion,
           dnf.after_tax_token_money, dnf.cost_point,
           dnf.deal_gold, dnf.point_iscount)

    dnf.asr_log("warn", log)

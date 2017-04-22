import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class Profitcalc:
    """購入した価格からプロフィットカーブを計算する
        引数:
            price: 購入価格と日付のSeries
            unit_cost: 一定購入額
        戻り値: price, tickets, cost, total_cost, profitを入れたdataframe"""

    def __init__(self, periods):
        self.periods = periods  # 期間
        self.initprice = 115  # 価格の初期値
        self.price = self.randomwalk() + self.initprice  # 価格
        self.unit_cost = 10000  # 定期買付額
        self.lowprice = self.lowweek()
        self.tickets = self.dollcost(self.lowprice)  # dollcost関数: 一定額ずつの購入
        self.cost = self.tickets * self.lowprice  # 購入ごとにかかった費用
        self.total_cost = self.cost.cumsum().resample('D').ffill()  # 全費用の合計(ただし手数料やスリッページ、スワップは除く)
        self.value = self.tickets.cumsum().resample('D').ffill(
        ) * self.price.ffill()  # 全ポジションの現在価値: 口数の累積和を週から日ごとに直して価格にかける
        self.profit = self.value - self.total_cost  # 利益: 現在価値と費用の差

    def randomwalk(self, start=pd.datetime.today().date(), name=None):
        """periods日分だけランダムウォークを返す"""
        np.random.seed(1)
        ts = pd.date_range(start=start, periods=self.periods, freq='B')  # 今日の日付からperiod日分の平日
        bullbear = pd.Series(np.random.randint(-1, 2, self.periods),
                             index=ts, name=name)  # -1,0,1のどれかを吐き出すSeries
        return bullbear.cumsum()  # 累積和

    def lowweek(self):
        """毎週の最安値を返す"""
        return self.price.resample('W').min()

    def dollcost(self, lowprice):
        """一定額ずつの購入
        引数:
            price: 購入したときの価格と日付のSeries
            unit_cost: 購入するときの一定金額
        戻り値:
            tickets: 購入口数
        """
        tickets = self.unit_cost / lowprice
        return tickets.astype(int)

    def out(self):
        return pd.DataFrame([self.price, self.lowprice, self.tickets, self.cost,
                             self.total_cost, self.value, self.profit],
                            index=['price', 'lowprice', 'tickets', 'cost',
                                   'total_cost', 'value', 'profit']).T

    def print(self):
        total_cost = self.out().total_cost[-1]
        print('Final Total Cost: %f'% total_cost)
        profit = self.out().profit[-1]
        print('Final Profit: %f'% profit)


# class MyClass2(Profitcalc):
#     def __init__(self):
#         super(MyClass2, self).__init__()
#         self.price = Profitcalc.randomwalk()

# class Doll(object):
#     """docstring for Doll"""
#     def __init__(self, arg):
#         super(Doll, self).__init__()
#         self.arg = arg

#         self.lowprice =

    # df = pd.DataFrame([price, tickets, cost, total_cost, profit],
    #         index=['price', 'tickets', 'cost', 'total_cost', 'profit']).T
    # print('Final total_cost: %d'% df.total_cost[-1])
    # print('Final Profit: %d'% df.profit[-1])
    # return df


if __name__ == "__main__":
    # price = randomwalk(100)
    x = Profitcalc(14)
    print(x.price)
    print(x.lowweek())
    print(x.tickets)
    print(x.out())
    x.print()

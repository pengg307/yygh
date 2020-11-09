from tqsdk import TqApi, TqAuth, TargetPosTask, TqReplay, TqBacktest
from tqsdk.ta import MA
from datetime import date, datetime
import threading
import logging

class WorkerThread(threading.Thread):
    def __init__(self, api, symbol):
        threading.Thread.__init__(self)
        self.api = api
        self.symbol = symbol
        #logging
        logfile = open("log-"+symbol+"-"+datetime.now().strftime("%Y%m%d-%H%M%S"), encoding="utf-8", mode="w")
        LOG_FORMAT = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s"
        logging.basicConfig(stream = logfile,
                    datefmt = '%a %d %b %Y %H:%M:%S',
                    format = LOG_FORMAT)

    def run(self):
        SHORT = 5  # 短周期
        LONG = 30 # 长周期
        data_length = LONG + 60 # k线数据长度
        klines = self.api.get_kline_serial(self.symbol, duration_seconds=60, data_length=data_length)
        target_pos = TargetPosTask(self.api, self.symbol)

        while True:
            self.api.wait_update()
            if self.api.is_changing(klines.iloc[-1], "datetime"):  # 产生新k线:重新计算SMA
                print("[-1:-N]:", klines.iloc[-1].close,",",klines.iloc[-2].close,",",klines.iloc[-3].close,",", \
                               klines.iloc[-4].close,",",klines.iloc[-5].close,",",klines.iloc[-6].close,",", \
                               klines.iloc[-7].close,",",klines.iloc[-8].close,",",klines.iloc[-9].close,",", \
                               klines.iloc[-10].close,",",klines.iloc[-11].close,",",klines.iloc[-12].close,",", \
                               klines.iloc[-13].close,",",klines.iloc[-14].close,",",klines.iloc[-15].close,",", \
                               klines.iloc[-16].close,",",klines.iloc[-17].close,",",klines.iloc[-18].close)

                logging.info("[-1:-N]:", klines.iloc[-1].close,",",klines.iloc[-2].close,",",klines.iloc[-3].close,",", \
                               klines.iloc[-4].close,",",klines.iloc[-5].close,",",klines.iloc[-6].close,",", \
                               klines.iloc[-7].close,",",klines.iloc[-8].close,",",klines.iloc[-9].close,",", \
                               klines.iloc[-10].close,",",klines.iloc[-11].close,",",klines.iloc[-12].close,",", \
                               klines.iloc[-13].close,",",klines.iloc[-14].close,",",klines.iloc[-15].close,",", \
                               klines.iloc[-16].close,",",klines.iloc[-17].close,",",klines.iloc[-18].close)
                short_avg = MA(klines["close"], SHORT)  # 短周期
                long_avg = MA(klines["close"], LONG)  # 长周期
                if long_avg.iloc[-2] < short_avg.iloc[-2] and long_avg.iloc[-1] > short_avg.iloc[-1]:
                    target_pos.set_target_volume(-3)
                    print("均线下穿，做空")
                    logging.info("最新价,acctprofit:")
                if short_avg.iloc[-2] < long_avg.iloc[-2] and short_avg.iloc[-1] > long_avg.iloc[-1]:
                    target_pos.set_target_volume(3)
                    print("均线上穿，做多")
                    logging.info("最新价,acctprofit:")


if __name__ == "__main__":
    #replay block
    replay = TqReplay(date(2020, 11, 5))#int(sys.argv[1])))
    replay.set_replay_speed(2000.0)
    api_master = TqApi(backtest=replay, auth=TqAuth("aimoons", "112411"))

    #prof...api = TqApi(web_gui=":16666", backtest=TqBacktest(start_dt=date(2020, 10, 12), end_dt=date(2020, 10, 16)), auth=TqAuth("aimoons", "112411"))
    #api_master = TqApi(web_gui=":26789", auth=TqAuth("aimoons", "112411"))

    # Create new threads
    thread1 = WorkerThread(api_master.copy(), "SHFE.ag2102")
    thread2 = WorkerThread(api_master.copy(), "SHFE.cu2102")
    #thread3 = WorkerThread(api_master.copy(), "SHFE.rb2102")

    # Start new Threads
    thread1.start()
    thread2.start()

    while True:
        api_master.wait_update()

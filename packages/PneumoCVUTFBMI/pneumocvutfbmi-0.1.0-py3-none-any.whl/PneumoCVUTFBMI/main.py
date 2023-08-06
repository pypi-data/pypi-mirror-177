from DeviceLoader import DeviceLoader

dl=DeviceLoader()
b1 = dl.getBoard3()
b2 = dl.getBoard5()
# fifo = []
while(1):
    print(b2.readA0())
    # fifo.append(ssd.readA0())
    # # time.sleep(0.05)
    # print(sum(fifo)/len(fifo))
    # if(len(fifo)>1000):
    #     fifo.pop(0)

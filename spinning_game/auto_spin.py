# from time import sleep
# from spinning_game.models import SpinningBatch,Bid
# import asyncio

# # async def auto_spin():
# #     i=0
# #     while True:
# #         if i==0:
# #             newBatch=SpinningBatch()
# #             newBatch.save()
# #         if i==30:
# #             newBatch.batchStatus="Game Start"
# #             newBatch.save()
# #         if i==35:
# #             newBatch.batchStatus="Spinning"
# #             newBatch.save()
# #             bids=Bid.objects.filter(batch=newBatch)
# #             bids4x=bids.filter(bidType="4x")
# #             bids2x=bids.filter(bidType="2x")
# #             bids6x=bids.filter(bidType="6x")
# #             amountOf4x=0
# #             amountOf2x=0
# #             amountOf6x=0
# #             for each in bids4x :
# #                 amountOf4x+=each.amount*4
# #             for each in bids2x :
# #                 amountOf2x+=each.amount*2
# #             for each in bids6x :
# #                 amountOf6x+=each.amount*6
# #             if amountOf2x<amountOf4x and amountOf2x<amountOf6x:
# #                 newBatch.winField="2x"
# #             elif amountOf4x<amountOf2x and amountOf4x<amountOf6x:
# #                 newBatch.winField="4x"
# #             elif amountOf6x<amountOf4x and amountOf6x<amountOf2x:
# #                 newBatch.winField="6x"
# #             else:
# #                 newBatch.winField="6x"
# #             newBatch.save()
            
# #         if i==45:
# #             newBatch.batchStatus="Result"
# #             newBatch.save()
# #         if i==55:
# #             newBatch.batchStatus="Next Game"
# #             newBatch.save()
# #         newBatch.second=i
# #         newBatch.save()
# #         # 10 second to be prepare
# #         # 30 second for bid
# #         # 10 second spin
# #         # 5 second for result
# #         # 5 second for next spin
# #         if i==60:
# #             newBatch.onGoingBatch=False
# #             newBatch.batchStatus="End"
# #             newBatch.save()
# #             i=0
# #         print(i)
# #         i+=1
# #         sleep(1)

# # # asyncio.run(auto_spin())
# # loop = asyncio.get_event_loop()
# # loop.run_until_complete(auto_spin())
# # loop.close()

from utils import send_text_message
from transitions.extensions import GraphMachine

#line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_milkshop(self, event): #進到迷客夏裡面
        text = event.message.text
        return text.lower() == "迷客夏"

    def is_going_to_louisa(self, event):  
        text = event.message.text
        return text.lower() == "路易莎"
        
    def is_going_to_dandan(self, event):  
        text = event.message.text
        return text.lower() == "丹丹"
    
    def is_going_to_mcalories(self, event): #進到迷客夏裡面
        text = event.message.text
        return text.lower() == "1"

    def is_going_to_lcalories(self, event): #進到迷客夏裡面
        text = event.message.text
        return text.lower() == "1"
        
    def is_going_to_change(self, event):  
        text = event.message.text
        return text.lower() == "換別家"


    def on_enter_milkshop(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "你可能會喜歡...\n珍珠青茶拿鐵 60元\n青檸香茶 60元\n柳丁綠茶 55元\n出雲抹茶鮮奶 65元\n小山見晴(冷泡無糖) 70元\n想知道熱量請回1，輸入換別家可重新選擇")
        """
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Trigger state1")
        )
        """
        
    def on_enter_mcalories(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "以下熱量以全糖計算，要當個有自尊的台南人\n珍珠青茶拿鐵 455kcal\n青檸香茶 290kcal\n柳丁綠茶 282kcal\n出雲抹茶鮮奶 212kcal\n小山見晴 0kcal\n想來點咖啡或食物嗎?輸入其他店家名稱即可查看")
        self.go_back()

    """def on_exit_milkshop(self):
        print("Leaving state1")"""
    
    def on_enter_louisa(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "私心推薦\n豬肉起司馬芬堡 50元\n烤腿排佛卡夏 75元\n薑汁燒肉磚壓 65元\n卡布奇諾 85元\n水洗耶加雪菲 85元\n想知道熱量請回1，輸入換別家可重新選擇")

    """def on_exit_louisa(self):
        print("Leaving state2")"""
    def on_enter_lcalories(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "豬肉起司馬芬堡 390.6kcal\n烤腿排佛卡夏 275.6kcal\n薑汁燒肉磚壓 350.8kcal\n卡布奇諾 186kcal\n水洗耶加雪菲 0kcal\n沒有你喜歡的嗎?輸入其他店家名稱查看其他菜單吧")
        self.go_back()
        
    def on_enter_dandan(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "私心推薦\n香酥雞肉羹 39元\n豬肉可樂餅 29元\n脆皮雞腿堡 55元\n超長熱狗 25元\n脆皮雞腿 39元\n不喜歡的話可以輸入其他店家名稱查看其他菜單")
        self.go_back()
       
    def on_enter_change(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token,"想知道迷客夏、路易莎還是丹丹的推薦菜單呢?回覆店名我就會告訴你")
        self.go_back()
    
    """def on_exit_dandan(self):
        print("Leaving state2")"""

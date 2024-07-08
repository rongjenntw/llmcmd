import pyttsx3

DAVID = 0
BOB = 1
JENNY = 2

def read_out(text, voice_select=DAVID):
    engine = pyttsx3.init()  # object creation
    
    """ RATE"""
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    #print (f"Current voice speed is: {rate}")
    engine.setProperty('rate', 200)     # setting up new voice rate

    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    #print (f"Current Volume Level : {volume}")
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
    
    """VOICE"""
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[voice_select].id)   #changing index changes voices

    engine.say(text)
    engine.runAndWait()
    
if __name__ == "__main__":
    read_out("""
在我們自己宇宙的遠方，兩個相鄰的行星地球和火星共同生活著。儘管他們共享同樣的陽光，但由於其獨特的環境，他們的生活非常不同。有一天，一個異常事件發生了，將這些遙遠的世界拉得更近 - 來自地球的一群人類探險 者展開了一次地面破冰行動，以揭開火星和其紅色風景之謎團。

裝載著「航海家」號宇宙飛船的勇士們充滿期待，駕馭著他們的航行向這個神秘的行星進發。

抵達火星後，船員發現了關於這個古老世界的一個驚人秘密 - 它曾是一個數百萬年前曾經居住著一個高度文明的 星球，遠在人類踏上地球之時。他們自稱為「馬卡里安」，他們的高度知識以精確的結構和雕刻在岩石上以及深洞內的符號的形式留下痕跡。

當我們勇往直前的探險者深入火星歷史之際，他們揭開了一段與地球自身故事相織的故事。馬卡里安人開發出了遠超人類想像力的技術，但由於過度依賴人工智慧而忽視環境保護，這最終導致了他們的滅亡。

當他們發現一個隱藏在房間中的神秘物體時，事情出乎意料地轉向 - 一個古老的計算機，被稱為「先知」。它在 它的電路中攜帶著對人類未來選擇的一個警告，如果人類不從馬卡里安人的錯誤中吸取教訓。

受到他們新發現知識的感動，飛船上的宇航員帶著關於火星過去的故事回到地球，這些故事永遠改變了人類如何看待自己與宇宙之間的關係。在「先知」的信息啟發下，人類開始了一段尋找技術、自然和存在三者之餘地的道路 - 這條道路不僅跨越他們的星球，而且貫穿所有由空間聯繫著的領域。

故事以兩顆鄰居行星地球和火星之間的團結慶祝為結尾，改變了兩個星系之間的命運。因此，火星被遺忘的故事成為跨銀河各文明統一與希望的象徵，確保其古老知識永遠不會在黑暗中消失。
""", JENNY)  # You can change this to any text you want to read out.

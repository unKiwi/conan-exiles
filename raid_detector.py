import secret

import discord
from config import config
import pyautogui
import threading
import pytesseract

pytesseract.pytesseract.tesseract_cmd = config["tesseract_path"]
local_config = config["raid_detector"]
loop_running = 0

def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
            
    return current[n]

# trigger function
def trigger():
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

        await client.guilds[0].channels[0].channels[0].send(file=discord.File(r'last_logs.png'))

    client.run(secret.TOKEN)

def loop_function():
    global loop_running

    while loop_running:
        im = pyautogui.screenshot(region=(local_config["logs_region"]["x"], local_config["logs_region"]["y"], local_config["logs_region"]["width"], local_config["logs_region"]["height"]))
        result = pytesseract.image_to_string(im, lang='eng+rus')

        textsTested = []
        resLevenshtein = []
        for i in range(0, len(result) - len(local_config["text"])):
            textToTest = result[i:i+len(local_config["text"])]
            textsTested.append(textToTest)
            resLevenshtein.append(levenshtein(textToTest, local_config["text"]))

        index_min = 0
        for i in range(1, len(resLevenshtein)):
            if resLevenshtein[i] < resLevenshtein[index_min]:
                index_min = i
        
        try:
            if (min(resLevenshtein) <= local_config["accuracy"]):
                # destroy message found
                print('\033[91m' + ' "' + local_config["text"] + '" was find' + '\033[0m')
                im.save('last_logs.png')
                trigger()
            else:
                print('Best match: ' + textsTested[index_min])
        except:
            a = 1

        lastMousePos = pyautogui.position()
        pyautogui.click(local_config["submit_pos"]["x"], local_config["submit_pos"]["y"]) # click submit button
        pyautogui.moveTo(lastMousePos) # come back

        pyautogui.sleep(local_config["interval"])

def toggle_raid_detector_loop():
    global loop_running

    if loop_running:
        loop_running = False
    else:
        loop_running = True
        loop_thread = threading.Thread(target=loop_function)
        loop_thread.start()

    print(f"Raid detector {loop_running}")

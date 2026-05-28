# main.py

from ui.consoleMenu import run_menu

def main():
    saved_places = {
        "Tōkyō-to": {"latitude": "35.6768601", "longitude": "139.7638947"},
        "Ōsaka-shi": {"latitude": "34.6937569", "longitude": "135.5014539"},
        "Kanazawa-shi": {"latitude": "36.561627", "longitude": "136.6568822"},
        "Chiba-shi": {"latitude": "35.6070629", "longitude": "140.1062653"},
        "Kyōto-shi": {"latitude": "35.0115754", "longitude": "135.7681441"},
        "Nara-shi": {"latitude": "34.6845445", "longitude": "135.8048359"},
        "Kōya-chō": {"latitude": "34.215788", "longitude": "135.5872944"},
        "Himeji-shi": {"latitude": "34.8153529", "longitude": "134.6854793"},
        "Hiroshima-shi": {"latitude": "34.3917241", "longitude": "132.4517589"},
        "Itsuku-shima": {"latitude": "34.271448", "longitude": "132.3088722"},
        "Magome": {"latitude": "35.5273237", "longitude": "137.5684127"},
        "Nagoya-shi": {"latitude": "35.1851045", "longitude": "136.8998438"},
        "Tsumago-juku": {"latitude": "35.5769907", "longitude": "137.595421"},
        "Hakone-machi": {"latitude": "35.2323662", "longitude": "139.1068849"},
        "Kamakura-shi": {"latitude": "35.3192808", "longitude": "139.5469627"},
        "E-no-shima": {"latitude": "35.3001052", "longitude": "139.4806371"},
        "Nikkō-Shi": {"latitude": "36.7197576", "longitude": "139.698139"},
        "Takao": {"latitude": "35.64166", "longitude": "139.2816337"}
    }
    
    run_menu(saved_places)

if __name__ == "__main__":
    main()
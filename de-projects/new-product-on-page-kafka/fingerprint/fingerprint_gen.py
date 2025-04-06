import random
import time
import base64
from urllib.parse import quote

fingerprint = {}


def generate_fingerprint():
    # Timing Metrics
    fingerprint["opts"] = '{\"endpoint\":\"https://js-data.allegro.pl/js/\",\"ajaxListenerPath\":[\"https://edge.allegro.pl\",\"https://allegro.pl\"],\"allowHtmlContentTypeOnCaptcha\":true,\"withCredentials\":true}'
    fingerprint["xhr_opts"] = ""
    base_time = random.uniform(20.0, 25.0)
    micro_variation = random.uniform(0.999999, 0.9999999)
    fingerprint["ttst"] = base_time + micro_variation - 1.0
    fingerprint["tagpu"] = round(random.uniform(5, 15), 9)

    # Boolean Flags
    fingerprint["ifov"] = False#random.choice([True, False])
    fingerprint["wbd"] = False
    fingerprint["wdif"] = False
    fingerprint["wdifrm"] = False
    fingerprint["npmtm"] = False
    fingerprint["isf"] = random.random() > 0.8
    fingerprint["phe"] = False
    fingerprint["nm"] = False
    fingerprint["jsf"] = False
    fingerprint["str_ss"] = True
    fingerprint["str_ls"] = True
    fingerprint["str_idb"] = True
    fingerprint["str_odb"] = False
    fingerprint["plgod"] = False
    fingerprint["plgne"] = True
    fingerprint["plgre"] = True
    fingerprint["plgof"] = False
    fingerprint["plggt"] = False
    fingerprint["pltod"] = False
    fingerprint["hcovdr"] = False
    fingerprint["hcovdr2"] = True
    fingerprint["plovdr"] = False
    fingerprint["plovdr2"] = True
    fingerprint["ftsovdr"] = False
    fingerprint["ftsovdr2"] = True
    fingerprint["lb"] = False
    fingerprint["lo"] = False
    fingerprint["ts_tec"] = False
    fingerprint["ts_tsa"] = False
    fingerprint["hdn"] = False
    fingerprint["awe"] = False
    fingerprint["geb"] = False
    fingerprint["dat"] = False
    fingerprint["ocpt"] = False
    fingerprint["sqt"] = False
    fingerprint["wdw"] = True
    fingerprint["ecpc"] = False
    fingerprint["lgs"] = True
    fingerprint["lgsod"] = False
    fingerprint["psn"] = True
    fingerprint["edp"] = True
    fingerprint["addt"] = True
    fingerprint["wsdc"] = True
    fingerprint["ccsr"] = True
    fingerprint["nuad"] = True
    fingerprint["bcda"] = False
    fingerprint["idn"] = True
    fingerprint["capi"] = False
    fingerprint["svde"] = False
    fingerprint["vpbq"] = True
    fingerprint["ucdv"] = False
    fingerprint["spwn"] = False
    fingerprint["emt"] = False
    fingerprint["bfr"] = True
    fingerprint["dbov"] = False
    fingerprint["ckwa"] = True
    fingerprint["prm"] = True
    fingerprint["cvs"] = True
    fingerprint["log2"] = True
    fingerprint["m_fmi"] = False
    fingerprint["mp_tr"] = True
    fingerprint["wwl"] = False

    # Integer/Float Metrics
    fingerprint["hc"] = random.randint(5, 20)  # e.g., 12
    fingerprint["br_oh"] = 1400#random.randint(1000, 1500)  # e.g., 1400
    fingerprint["br_ow"] = 2560#random.randint(2000, 3000)  # e.g., 2560
    fingerprint["br_h"] = 1279#fingerprint["br_oh"] - random.randint(50, 150)  # e.g., 1279
    fingerprint["br_w"] = 2560#fingerprint["br_ow"] - random.randint(0, 50)  # e.g., 2560
    fingerprint["nddc"] = 1
    resolutions = [(2560, 1440), (1920, 1080), (1366, 768)]
    rs_w, rs_h = random.choice(resolutions)
    fingerprint["rs_h"] = 1440#rs_h
    fingerprint["rs_w"] = 2560#rs_w
    fingerprint["rs_cd"] = 24
    fingerprint["pr"] = 1
    fingerprint["ars_h"] = fingerprint["br_oh"]  # e.g., 1400
    fingerprint["ars_w"] = fingerprint["rs_w"]  # e.g., 2560
    timezones = [(-60, "Europe/Warsaw")]
    tz_offset, tz_name = random.choice(timezones)
    fingerprint["tz"] = tz_offset
    fingerprint["tzp"] = tz_name
    common_plugins = [
        "PDF Viewer", "Chrome PDF Viewer", "Chromium PDF Viewer",
        "Microsoft Edge PDF Viewer", "WebKit built-in PDF"
    ]
    fingerprint["plg"] = random.randint(3, 5)
    fingerprint["plu"] = ",".join(random.sample(common_plugins, fingerprint["plg"]))
    fingerprint["eva"] = random.randint(20, 50)  # e.g., 33
    fingerprint["ts_mtp"] = 0
    fingerprint["dvm"] = 8
    fingerprint["jset"] = int(time.time())  # e.g., 1740433438
    fingerprint["mp_cx"] = random.randint(300, 500)  # e.g., 422
    fingerprint["mp_cy"] = random.randint(300, 500)  # e.g., 397
    fingerprint["mp_mx"] = random.randint(-5, 5)  # e.g., 1
    fingerprint["mp_my"] = random.randint(-5, 5)  # e.g., -1
    fingerprint["mp_sx"] = random.randint(2000, 3000)  # e.g., 2982
    fingerprint["mp_sy"] = random.randint(400, 600)  # e.g., 518
    fingerprint["mm_md"] = fingerprint["eva"]  # e.g., 33
    fingerprint["tbce"] = random.randint(50, 150)  # e.g., 109
    fingerprint["es_sigmdn"] = random.uniform(0.0001, 0.001)  # e.g., 0.00015197697249316345
    fingerprint["es_mumdn"] = random.uniform(5, 10)  # e.g., 8.709149295047439
    fingerprint["es_distmdn"] = random.uniform(300, 500)  # e.g., 395.102518341759
    fingerprint["es_angsmdn"] = random.uniform(1, 2)  # e.g., 1.6614562139956417
    fingerprint["es_angemdn"] = random.uniform(0, 1)  # e.g., 0.5045604387762456
    fingerprint["m_s_c"] = 0
    fingerprint["m_m_c"] = fingerprint["eva"]  # e.g., 33
    fingerprint["m_c_c"] = 0
    fingerprint["m_cm_r"] = 0
    fingerprint["m_ms_r"] = -1

    # String Values
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
    ]
    fingerprint["ua"] = random.choice(user_agents)
    fingerprint["lg"] = "pl-PL"
    fingerprint["vnd"] = "Google Inc."
    fingerprint["bid"] = "NA"
    fingerprint["mmt"] = "application/pdf,text/pdf"
    fingerprint["med"] = "defined"
    fingerprint["aco"] = "probably"
    fingerprint["acots"] = False
    fingerprint["acmp"] = "probably"
    fingerprint["acmpts"] = True
    fingerprint["acw"] = "probably"
    fingerprint["acwts"] = False
    fingerprint["acma"] = "maybe"
    fingerprint["acmats"] = False
    fingerprint["acaa"] = "probably"
    fingerprint["acaats"] = True
    fingerprint["ac3"] = ""
    fingerprint["ac3ts"] = False
    fingerprint["acf"] = "probably"
    fingerprint["acfts"] = False
    fingerprint["acmp4"] = "maybe"
    fingerprint["acmp4ts"] = False
    fingerprint["acmp3"] = "probably"
    fingerprint["acmp3ts"] = False
    fingerprint["acwm"] = "maybe"
    fingerprint["acwmts"] = False
    fingerprint["vco"] = ""
    fingerprint["vcots"] = False
    fingerprint["vch"] = "probably"
    fingerprint["vchts"] = True
    fingerprint["vcw"] = "probably"
    fingerprint["vcwts"] = True
    fingerprint["vc3"] = "maybe"
    fingerprint["vc3ts"] = False
    fingerprint["vcmp"] = ""
    fingerprint["vcmpts"] = False
    fingerprint["vcq"] = ""
    fingerprint["vcqts"] = False
    fingerprint["vc1"] = "probably"
    fingerprint["vc1ts"] = True
    fingerprint["so"] = "landscape-primary"
    fingerprint["cokys"] = base64.b64encode("loadTimesciapp".encode()).decode()
    fingerprint[
        "cfpfe"] = "ZnVuY3Rpb24odCxpKXt2YXIgZT1kb2N1bWVudC5nZXRFbGVtZW50QnlJZCh0KTtpZihlKXtpZihpJiZ0aGlzLnVzZV9nbG9iYWxzKXRyeXsidW5kZWZpbmVkIiE9dHlwZW9mIGdlbWl1c19ub3RpZnk/Z2VtaXVzX25vdGlmeShpKToidW5kZWZpbmVkIiE9dHlwZW9m"
    fingerprint[
        "stcfp"] = "b3N0YXRpYy5jb20vc2MtMTcxODQvbGliX2RiOTE4Zjk1LmpzOjI6MTEyNTUpCiAgICBhdCBIVE1MU2NyaXB0RWxlbWVudC48YW5vbnltb3VzPiAoaHR0cHM6Ly9hc3NldHMuYWxsZWdyb3N0YXRpYy5jb20vc2MtMTcxODQvbGliX2RiOTE4Zjk1LmpzOjI6MTEwMzEp"
    fingerprint["usb"] = "defined"
    #fingerprint["emd"] = "k:ai,vi,ao"
    fingerprint["glvd"] = "Google Inc. (AMD)"
    fingerprint["glrd"] = "ANGLE (AMD, AMD Radeon RX 6600 XT (0x000073FF) Direct3D11 vs_5_0 ps_5_0, D3D11)"
    #fingerprint["dcok"] = ".allegro.pl"

    return fingerprint


def encode_to_url_format(fingerprint):
    # Convert fingerprint dictionary to JSON-like string (manual formatting for exact match)
    js_data_parts = []
    for key, value in fingerprint.items():
        if isinstance(value, bool):
            encoded_value = str(value).lower()
        elif isinstance(value, (int, float)):
            encoded_value = str(value)
        else:
            encoded_value = f'"{quote(str(value))}"'  # Quote strings and URL-encode
        js_data_parts.append(f'"{key}":{encoded_value}')
    js_data = "{" + ",".join(js_data_parts) + "}"

    # Event Counters (static example from your input)
    event_counters = {
        "mousemove": 0,
        "click": 0,
        "scroll": 0,
        "touchstart": 0,
        "touchend": 0,
        "touchmove": 0,
        "keydown": 0,
        "keyup": 0
    }
    event_counters_str = "{" + ",".join(f'"{k}":{v}' for k, v in event_counters.items()) + "}"

    # Additional parameters
    additional_params = {
        "jsType": "ch",
        "cid": "0rmW7VPNGA7bEx6i8KWTWvypvgruG_vM_EHfjqtc5lADjCQkhw9inRFRHXfi6uSagkbYXfSTquPXZrAiY6phLQhnShvqWcIeB654wmplldoBmyGT_vZSBb0AkAuHGFs7",
        "ddk": "77DC0FFBAA0B77570F6B414F8E5BDB",
        #"Referer": quote("https://allegro.pl/oferta/plecak-tornister-szkolny-dla-dziewczynki-czarny-zloty-kot-kotek-klasa-1-3-14364014606"),
        "responsePage": "origin",
        "ddv": "4.29.3"
    }
    #event_counters = "[]"
    # Combine into final URL-encoded string
    encoded_str = (
        f"jsData={quote(js_data)}&"
        f"eventCounters={event_counters}&"
        f"jsType={quote(additional_params['jsType'])}&"
        f"cid={quote(additional_params['cid'])}&"
        f"ddk={quote(additional_params['ddk'])}&"
        f"responsePage={quote(additional_params['responsePage'])}&"
        f"ddv={quote(additional_params['ddv'])}"
    )
    return encoded_str


# Generate and encode
if __name__ == "__main__":
    fingerprint_data = generate_fingerprint()
    encoded_output = encode_to_url_format(fingerprint_data)
    print(encoded_output)
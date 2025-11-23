# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 05:43:19 2025
BOSIK v1.2 (The Chatbot Edition)
@author: USER
"""

import json
import os
import pickle
import glob
import random # 무작위 추천을 위해 필요

# === Global Memory ===
memory = {}
functions = {}
knowledge_base = [] 
rules = {}

# === Parser (기존 v1.11과 동일) ===
def parse_json_data(filepath):
    facts = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        items = data.get('channel', {}).get('item', [])
        for item in items:
            word_info = item.get('word_info', {})
            main_word = word_info.get('word', '').replace('-', '')
            
            # 기본 정보
            for pos_info in word_info.get('pos_info', []):
                pos = pos_info.get('pos', '')
                if pos: facts.append((main_word, "IS_A", pos))
                for ptrn in pos_info.get('comm_pattern_info', []):
                    for sense in ptrn.get('sense_info', []):
                        definition = sense.get('definition', '').replace(' ', '_')
                        if definition: facts.append((main_word, "MEANS", definition))
                        for cat in sense.get('cat_info', []):
                            cat_name = cat.get('cat', '')
                            if cat_name and cat_name != "없음": facts.append((main_word, "CATEGORY", cat_name))

            # 속담 추출
            for rel in word_info.get('relation_info', []):
                rel_word = rel.get('word', '').replace(' ', '_')
                rel_type = rel.get('type', '')
                if rel_type:
                    facts.append((rel_word, "TYPE", rel_type))
                    facts.append((rel_word, "RELATED_TO", main_word))
    except: pass
    return facts

# === [NEW] Natural Language Processor ===
def process_natural_language(user_input):
    # 아주 단순한 키워드 매칭 방식의 NLI입니다.
    # 나중에는 여기에 딥러닝 모델이나 형태소 분석기를 붙일 수 있습니다.
    
    msg = user_input.strip()
    
    # 1. 속담 추천
    if "속담" in msg and ("추천" in msg or "하나" in msg or "알려줘" in msg):
        proverbs = [s for (s, r, o) in knowledge_base if r == "TYPE" and o == "속담"]
        if proverbs:
            pick = random.choice(proverbs)
            # 언더바(_)를 다시 공백으로 바꿔서 보여줌
            print(f" >> [BOSIK] 오늘의 속담: \"{pick.replace('_', ' ')}\"")
            return True
        else:
            print(" >> [BOSIK] 아직 배운 속담이 없어요. LOAD_ALL을 해주세요.")
            return True

    # 2. 뜻 물어보기 (~가 뭐야?)
    if "뭐야" in msg or "뜻" in msg:
        # "가난이 뭐야?" -> "가난" 추출 (간단한 파싱)
        target = msg.replace("이 뭐야", "").replace("가 뭐야", "").replace(" 뜻", "").replace("?", "").strip()
        
        found = False
        for (s, r, o) in knowledge_base:
            if s == target and r == "MEANS":
                print(f" >> [BOSIK] {target}: {o.replace('_', ' ')}")
                found = True
                break
        if not found:
            print(f" >> [BOSIK] '{target}'에 대해서는 잘 모르겠어요.")
        return True

    return False # 자연어 처리 실패 시 False 반환

# === Interpreter Core ===
def execute_command(command_line):
    global knowledge_base, memory, rules
    
    # [NEW] 자연어 처리 시도
    # 명령어가 영어 키워드로 시작하지 않으면 자연어로 간주
    first_word = command_line.split()[0].upper()
    known_commands = ["LOAD_ALL", "SAVE_BRAIN", "LOAD_BRAIN", "QUERY", "EXPORT", "EXIT"]
    
    if first_word not in known_commands:
        if process_natural_language(command_line):
            return # 자연어로 처리됐으면 종료
        # 자연어 처리도 안 됐으면 에러 메시지 대신 그냥 넘어가거나 알려줌
        # print(" >> [System] 명령어를 이해하지 못했습니다.")
        # return

    tokens = command_line.strip().split()
    if not tokens: return
    keyword = tokens[0].upper()

    if keyword == "LOAD_ALL":
        # ... (기존 코드 동일) ...
        target_dir = tokens[1] if len(tokens) > 1 else "korean_dict"
        if not os.path.exists(target_dir): target_dir = os.path.join(".", target_dir)
        json_files = glob.glob(os.path.join(target_dir, "*.json"))
        print(f" >> [System] Learning from {len(json_files)} files...")
        total = 0
        cnt = 0
        for f in json_files:
            nf = parse_json_data(f)
            knowledge_base.extend(nf)
            total += len(nf)
            cnt += 1
            if cnt % 5 == 0: print(".", end="", flush=True)
        print(f"\n >> [Success] Total {total} facts.")

    elif keyword == "SAVE_BRAIN":
        # ... (기존 코드 동일) ...
        fn = tokens[1] if len(tokens) > 1 else "my_brain.kb"
        with open(fn, 'wb') as f: pickle.dump({'kb': knowledge_base, 'mem': memory, 'rules': rules}, f)
        print(f" >> Saved to {fn}")

    elif keyword == "LOAD_BRAIN":
        # ... (기존 코드 동일) ...
        fn = tokens[1] if len(tokens) > 1 else "my_brain.kb"
        try:
            with open(fn, 'rb') as f:
                d = pickle.load(f)
                knowledge_base, memory, rules = d['kb'], d['mem'], d['rules']
            print(f" >> Loaded {len(knowledge_base)} facts.")
        except: print(" >> Load failed.")

    elif keyword == "QUERY":
        # ... (기존 코드 동일) ...
        q_s, q_r, q_o = tokens[1], tokens[2], tokens[3]
        print(f" >> [Query] {q_s} {q_r} {q_o}")
        c = 0
        for (s, r, o) in knowledge_base:
            if (q_s=="?" or q_s==s) and (q_r=="?" or q_r==r) and (q_o=="?" or q_o==o):
                print(f"    {s} {r} {o}")
                c += 1
                if c>=20: break
        if c==0: print("    No result.")

    # [NEW] 속담 내보내기 기능
    elif keyword == "EXPORT":
        print(" >> [System] Exporting proverbs to 'proverbs_list.txt'...")
        with open("proverbs_list.txt", "w", encoding="utf-8") as f:
            count = 0
            for (s, r, o) in knowledge_base:
                if r == "TYPE" and o == "속담":
                    # 보기 좋게 언더바 제거하고 쓰기
                    clean_sentence = s.replace("_", " ")
                    f.write(f"{clean_sentence}\n")
                    count += 1
        print(f" >> [Success] Exported {count} proverbs.")

    elif keyword == "EXIT": return "EXIT"

def run_shell():
    print("=== BOSIK v1.2 (The Chatbot) ===")
    print("Tip: 이제 '속담 하나 추천해줘' 처럼 한국어로 말을 걸어보세요!")
    while True:
        try:
            if execute_command(input("BOSIK> ")) == "EXIT": break
        except Exception as e: print(f" >> [Crash] {e}")

if __name__ == "__main__":
    run_shell()
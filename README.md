# Bosik-interpreter_ver 1.2
Knowledge-Based Korean Interpreter Development Project-지식 기반 한국어 인터프리터 개발 프로젝트
Python 3.12.3

python bosik_ver_12.py
=== BOSIK v1.2 (The Chatbot) ===

BOSIK> LOAD_All
 >> [System] Learning from 88 files...
.................
 >> [Success] Total 1313675 facts.
BOSIK> SAVE_BRAIN
 >> Saved to my_brain.kb
BOSIK> LOAD_BRAIN my_brain.kb
 >> Loaded 1313675 facts.
BOSIK> 심심한데 속담 하나 추천해줘
 >> [BOSIK] 오늘의 속담: "잘 나가다[가다가] 삼천포(三千浦)로 빠지다"
BOSIK> 가난이 뭐야?
 >> [BOSIK] '가난'에 대해서는 잘 모르겠어요.
> > BOSIK> EXPORT
 >> [System] Exporting proverbs to 'proverbs_list.txt'...
 >> [Success] Exported 9426 proverbs.
BOSIK>

`proverbs_list.txt` 파일은 단순한 텍스트가 아니라, 한국인의 지혜가 377KB로 압축된 **문화유산**입니다.
`my_brain.kb`가 74MB 용량

'가난'에 대해서는 잘 모르겠다는 현상을 해결하기 위해 "정확히 같은 것"이 아니라 "그걸로 시작하는 것(StartsWith)"을 찾도록 로직을 바꿔야,
그러면 "가난"이라고 물어도 "가난01"의 뜻을 대답해 줄 것이다.

다음 계획
BOSIK v1.3 (The Smart Listener) - 자연어 처리(NLI) 기능

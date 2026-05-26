# WooaGosa 프로젝트 지침

## 프로젝트 개요
**wooagosa.wooahouse.com** — 운전면허·자격증 무료 모의고사 사이트 (GitHub Pages 정적 사이트)

## 핵심 파일 구조
```
wooaGosa/
├── CLAUDE.md                  ← 이 파일 (프로젝트 지침)
├── index.html                 ← 메인 랜딩 페이지 (시험 목록)
├── exam-*.html                ← 시험별 상세 랜딩 페이지 (32개, 자동 생성)
├── wrong-notes.html           ← 오답노트 페이지
├── sitemap.xml                ← SEO 사이트맵
├── generate_exam_pages.py     ← exam-*.html 32개를 자동 생성하는 스크립트 ★
├── parse_comcbt.py            ← comcbt.com 형식 PDF → JSON 파서 (4지선다)
├── reparse_5choice.py         ← 5지선다 전용 파서 (공인중개사·사회복지사)
├── js/
│   └── exam.js                ← 시험 로직 (문제 로드·타이머·오답노트)
├── data/
│   └── *.json                 ← 시험 문제 데이터 (파서 출력물)
└── 문제지/
    └── */                     ← 시험별 PDF 원본
```

## 자주 하는 작업

### 새 시험 추가 시 수정해야 할 파일 (순서대로)
1. `parse_comcbt.py` 또는 `reparse_5choice.py` → PDF 파싱 → `data/*.json` 생성
2. `js/exam.js` → `EXAM_FILES`, `FULL_TIME`, `PASS_SCORE`, `EXAM_SUBJECTS` 맵에 추가
3. `generate_exam_pages.py` → `EXAMS` 리스트에 시험 정의 추가 → 스크립트 실행
4. `index.html` → 시험 카드 추가, 히어로 뱃지 업데이트
5. `wrong-notes.html` → 필터 버튼·통계·FILE_URLS·레이블 추가
6. `sitemap.xml` → 새 URL 추가

### exam-*.html 재생성
```
C:\Users\ingma\AppData\Local\Programs\Python\Python312\python.exe generate_exam_pages.py
```
→ 32개 파일 자동 생성. **exam-*.html을 직접 편집하지 말 것** — 스크립트로만 수정

### PDF 파싱
```
# 4지선다 일반 시험
python parse_comcbt.py

# 5지선다 시험 (공인중개사·사회복지사)
python reparse_5choice.py
```
- PDF 원본: `문제지/시험명/` 폴더
- 출력: `data/시험키.json`

## 시험 목록 (32개)

### 운전면허 (도로교통공단)
| type | 파일 | 비고 |
|---|---|---|
| 1jong-daebyeong | exam-license-1large.html | 60문항 4지선다 |
| 1jong-botong | exam-license-1normal.html | 40문항 |
| 2jong-botong | exam-license-2normal.html | 40문항 |
| motorcycle | exam-motorcycle.html | 40문항 |
| motorbike | exam-motorbike.html | 40문항 |

### 한국사 (historyexam.go.kr)
| type | 파일 |
|---|---|
| history_basic | exam-history-basic.html |
| history_advanced | exam-history-advanced.html |

### IT 자격증
| type | 파일 | 기관 |
|---|---|---|
| computer_1/2 | exam-computer-1/2.html | 대한상공회의소 |
| word | exam-word.html | 대한상공회의소 |
| net_1/2 | exam-net-1/2.html | KAIT |
| linux_1/2 | exam-linux-1/2.html | KAIT |
| info_proc | exam-info-proc.html | 큐넷 |
| info_ind | exam-info-ind.html | 큐넷 |
| info_sec | exam-info-sec.html | KISA |

### 전기 (큐넷)
| type | 파일 |
|---|---|
| elec_eng | exam-elec-eng.html |
| elec_ind | exam-elec-ind.html |

### 위험물 (큐넷)
| type | 파일 |
|---|---|
| hazmat_ind | exam-hazmat-ind.html |
| hazmat_craft | exam-hazmat-craft.html |

### 소방설비 (큐넷)
| type | 파일 |
|---|---|
| fire_mech | exam-fire-mech.html |
| fire_elec | exam-fire-elec.html |

### 건설기계 (큐넷)
| type | 파일 |
|---|---|
| forklift | exam-forklift.html |
| excavator | exam-excavator.html |

### 공인중개사 (큐넷) — 5지선다
| type | 파일 |
|---|---|
| realtor_1 | exam-realtor-1.html |
| realtor_2 | exam-realtor-2.html |

### 사회복지사 (welfare.net) — 5지선다
| type | 파일 |
|---|---|
| welfare_1 | exam-welfare-1.html |
| welfare_2 | exam-welfare-2.html |
| welfare_3 | exam-welfare-3.html |

### 산업안전 (큐넷)
| type | 파일 |
|---|---|
| safety_ind | exam-safety-ind.html |
| safety_eng | exam-safety-eng.html |

## 중요 규칙 & 주의사항

### exam-*.html 직접 편집 금지
- 이 파일들은 `generate_exam_pages.py`가 자동 생성
- 수정이 필요하면 반드시 `generate_exam_pages.py`의 `EXAMS` 리스트나 `make_page()` 함수를 수정하고 스크립트를 다시 실행

### 5지선다 파서
- 공인중개사·사회복지사는 ⑤ 선지가 있어 별도 파서(`reparse_5choice.py`) 사용
- `parse_comcbt.py`는 ①②③④ 4지선다 전용

### Python 실행 경로
```
C:\Users\ingma\AppData\Local\Programs\Python\Python312\python.exe
```

### git 작업
- 브랜치: `main`
- 리모트: `https://github.com/ingmaster83-code/wooaGosa.git`
- GitHub Pages로 자동 배포 (push 후 1~2분 소요)
- 커밋 시 `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>` 추가

### 공식 링크 관리
`generate_exam_pages.py`의 `OFFICIAL_LINKS` / `TYPE_TO_LINKS` 딕셔너리에서 관리.
각 시험 상세 페이지에 공식 홈페이지 버튼 하나씩 표시.

## 기술 스택
- 프론트엔드: 순수 HTML/CSS/JS (프레임워크 없음)
- 데이터: JSON (브라우저에서 fetch)
- 광고: Google AdSense + 쿠팡 파트너스
- 분석: Google Analytics (G-9ZGENFSXWC)
- PDF 파싱: pdfplumber (Python)
- 배포: GitHub Pages

#!/usr/bin/env python3
"""
cbtestpro.kr 기출문제 PDF 크롤러
- 고사패스 자격증 목록(Excel) 기준으로 순회
- 교사용(-0), 학생용(-1) PDF 전 연도 다운로드
- 파일명: YYYYMMDD-자격증명-교사용.pdf / YYYYMMDD-자격증명-학생용.pdf
- 저장: 문제지/{자격증명}/

사용법:
  전체 실행  : python crawl_cbtestpro.py
  샘플 1개   : python crawl_cbtestpro.py SAMPLE 정보처리기사
  링크만 확인: python crawl_cbtestpro.py TEST 정보처리기사
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import urllib.parse
import re
from pathlib import Path
import logging
import sys

# Windows 터미널 한글 출력 보장
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ───────────────────────────────────────────────
# 설정
# ───────────────────────────────────────────────
EXCEL_FILE  = r"C:\Users\ingma\OneDrive\Desktop\gosapass_자격증목록_20260624.xlsx"
OUTPUT_DIR  = r"C:\개인\wooahouse\wooaGosa\문제지"
LOG_FILE    = r"C:\개인\wooahouse\wooaGosa\crawl_log.txt"
RESULT_FILE = r"C:\개인\wooahouse\wooaGosa\crawl_results.txt"

BASE_URL  = "https://www.cbtestpro.kr"
DELAY_MIN = 1.0
DELAY_MAX = 2.5
DELAY_PDF = 0.8

KIND_LABEL = {"-0": "교사용", "-1": "학생용"}

# ───────────────────────────────────────────────
# 로깅
# ───────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8", mode="w"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8",
    "Accept-Encoding": "identity",  # Brotli 제외 (requests 미지원, 파싱 깨짐)
    "Connection": "keep-alive",
}


# ───────────────────────────────────────────────
# 세션
# ───────────────────────────────────────────────
def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(HEADERS)
    try:
        s.get(BASE_URL, timeout=10)
        time.sleep(1)
    except Exception:
        pass
    return s


# ───────────────────────────────────────────────
# 파일명 생성
# YYYYMMDD-0.pdf  →  YYYYMMDD-자격증명-교사용.pdf
# ───────────────────────────────────────────────
def make_filename(original_name: str, cert_name: str) -> str:
    m = re.match(r"(\d{8})(-[01])\.pdf", original_name, re.IGNORECASE)
    if not m:
        return original_name  # 패턴 미일치 시 원본 사용
    date_str = m.group(1)
    kind = KIND_LABEL.get(m.group(2), m.group(2))
    safe_cert = cert_name.replace("/", "_").replace("\\", "_")
    return f"{date_str}-{safe_cert}-{kind}.pdf"


# ───────────────────────────────────────────────
# 페이지에서 교사용(-0) + 학생용(-1) PDF 링크 추출
# 반환: None(404) | {}(PDF없음) | {'교사용':[url], '학생용':[url]}
# ───────────────────────────────────────────────
def get_pdf_links(session: requests.Session, cert_name: str):
    encoded = urllib.parse.quote(cert_name)
    url = f"{BASE_URL}/{encoded}"

    try:
        resp = session.get(url, timeout=15)
    except requests.exceptions.RequestException as e:
        log.error(f"  요청 오류: {e}")
        return {}

    if resp.status_code == 404:
        return None
    if resp.status_code != 200:
        log.warning(f"  HTTP {resp.status_code}")
        return {}

    soup = BeautifulSoup(resp.content, "html.parser")

    teacher, student = [], []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if re.search(r"\d{8}-0\.pdf", href, re.IGNORECASE) and href not in teacher:
            teacher.append(href)
        elif re.search(r"\d{8}-1\.pdf", href, re.IGNORECASE) and href not in student:
            student.append(href)

    # fallback: 전체 HTML에서 정규식으로 추출
    if not teacher and not student:
        for href in re.findall(r'https?://[^\s"\'<>]+\d{8}-[01]\.pdf', resp.text):
            if re.search(r"\d{8}-0\.pdf", href) and href not in teacher:
                teacher.append(href)
            elif re.search(r"\d{8}-1\.pdf", href) and href not in student:
                student.append(href)

    return {"교사용": teacher, "학생용": student}


# ───────────────────────────────────────────────
# PDF 다운로드
# ───────────────────────────────────────────────
def download_pdf(session: requests.Session, url: str, save_path: Path) -> bool:
    try:
        resp = session.get(url, timeout=60, stream=True)
        if resp.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            size_kb = save_path.stat().st_size / 1024
            log.info(f"    ✓ {save_path.name} ({size_kb:.0f} KB)")
            return True
        else:
            log.warning(f"    ✗ {save_path.name}  HTTP {resp.status_code}")
            return False
    except Exception as e:
        log.error(f"    ✗ {save_path.name}  오류: {e}")
        return False


# ───────────────────────────────────────────────
# 자격증 1개 처리 (다운로드 포함)
# ───────────────────────────────────────────────
def process_cert(session: requests.Session, cert_name: str) -> tuple[int, int]:
    """(downloaded, skipped) 반환"""
    links = get_pdf_links(session, cert_name)

    if links is None:
        log.info("  → 사이트에 없음 (404)")
        return 0, 0
    if not links.get("교사용") and not links.get("학생용"):
        log.info("  → PDF 없음")
        return 0, 0

    teacher_cnt = len(links.get("교사용", []))
    student_cnt = len(links.get("학생용", []))
    log.info(f"  → 교사용 {teacher_cnt}개  학생용 {student_cnt}개")

    folder = Path(OUTPUT_DIR) / cert_name
    folder.mkdir(parents=True, exist_ok=True)

    downloaded, skipped = 0, 0
    all_links = [("교사용", u) for u in links.get("교사용", [])] + \
                [("학생용", u) for u in links.get("학생용", [])]

    for kind_label, pdf_url in all_links:
        orig_name = pdf_url.rstrip("/").split("/")[-1]
        new_name  = make_filename(orig_name, cert_name)
        save_path = folder / new_name

        if save_path.exists():
            log.info(f"    - {new_name} (이미 있음)")
            skipped += 1
            continue

        if download_pdf(session, pdf_url, save_path):
            downloaded += 1
        time.sleep(random.uniform(DELAY_PDF, DELAY_PDF + 0.5))

    return downloaded, skipped


# ───────────────────────────────────────────────
# 메인
# ───────────────────────────────────────────────
def main():
    mode = sys.argv[1].upper() if len(sys.argv) >= 2 else "ALL"
    cert_arg = sys.argv[2] if len(sys.argv) >= 3 else None

    # ── TEST: 링크만 확인, 다운로드 없음 ──
    if mode == "TEST" and cert_arg:
        log.info(f"[TEST] {cert_arg}")
        s = make_session()
        links = get_pdf_links(s, cert_arg)
        if links is None:
            log.info("→ 404 (사이트에 없음)")
        elif not links.get("교사용") and not links.get("학생용"):
            log.info("→ PDF 없음")
        else:
            log.info(f"→ 교사용 {len(links['교사용'])}개  학생용 {len(links['학생용'])}개")
            for u in links["교사용"][:3]:
                log.info(f"   [교사용] {u}")
            for u in links["학생용"][:3]:
                log.info(f"   [학생용] {u}")
        return

    # ── SAMPLE: 지정 자격증 1개 다운로드 ──
    if mode == "SAMPLE" and cert_arg:
        log.info(f"[SAMPLE] {cert_arg} 다운로드 시작")
        s = make_session()
        dl, sk = process_cert(s, cert_arg)
        log.info(f"\n완료  다운로드: {dl}개  건너뜀: {sk}개")
        log.info(f"저장 폴더: {Path(OUTPUT_DIR) / cert_arg}")
        return

    # ── ALL: 전체 실행 ──
    df = pd.read_excel(EXCEL_FILE)
    cert_names = df["자격증명"].dropna().tolist()
    log.info(f"총 {len(cert_names)}개 자격증 처리 시작\n")

    session = make_session()
    found, not_found = [], []
    total_dl, total_sk = 0, 0

    for i, cert_name in enumerate(cert_names, 1):
        log.info(f"[{i:3d}/{len(cert_names)}] {cert_name}")

        links = get_pdf_links(session, cert_name)

        if links is None:
            log.info("  → 없음 (404)")
            not_found.append(cert_name)
            time.sleep(random.uniform(0.3, 0.7))
            continue

        if not links.get("교사용") and not links.get("학생용"):
            log.info("  → PDF 없음")
            not_found.append(cert_name)
            time.sleep(random.uniform(0.5, 1.0))
            continue

        found.append(cert_name)
        dl, sk = process_cert(session, cert_name)
        total_dl += dl
        total_sk += sk

        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

        if i % 50 == 0:
            log.info("  [세션 갱신]")
            session = make_session()

    # 결과 파일
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        f.write("=== cbtestpro.kr 크롤링 결과 ===\n")
        f.write(f"발견: {len(found)}개 | 없음: {len(not_found)}개\n")
        f.write(f"다운로드: {total_dl}개 | 건너뜀: {total_sk}개\n\n")
        f.write(f"[발견된 자격증 — {len(found)}개]\n")
        for n in found:
            f.write(f"  {n}\n")
        f.write(f"\n[사이트에 없는 자격증 — {len(not_found)}개]\n")
        for n in not_found:
            f.write(f"  {n}\n")

    log.info("\n" + "=" * 55)
    log.info(f"완료  발견: {len(found)}개  없음: {len(not_found)}개")
    log.info(f"다운로드: {total_dl}개  건너뜀: {total_sk}개")
    log.info(f"결과 파일 → {RESULT_FILE}")


if __name__ == "__main__":
    main()

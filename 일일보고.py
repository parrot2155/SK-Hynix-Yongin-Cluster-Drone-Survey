import re # 정규 표현식 모듈

input_string = "IBL FAB 서 OS 315 / OBL WWT 동 TS 65 30 ES 65 150 / 지원시설 4BL 동 WS 600 / IBL 1번게이트 OB / IBL 1번게이트 WS 1100 700 / IBL 1번게이트 WS 300" # @param {type:"string"}

segments = [s.strip() for s in input_string.split('/')] # 입력 문자열을 '/'로 분리 및 공백 제거

# 구역별 서비스 저장 (중복 방지)
grouped_services = {}

# 서비스 코드와 한글명 매핑
service_mapping = {
    'TS': '통신',
    'ES': '전기',
    'OS': '오수',
    'WS': '우수',
    'SB': '소방',
    'SS': '상수',
    'GS': '가스',
    'OB': '옹벽'
}

for segment in segments: # 각 세그먼트 처리
    services_found_in_segment = []
    area_prefix = ""

    # 구역 식별
    if "OBL" in segment:
        area_prefix = "OBL"
    elif "IBL" in segment:
        area_prefix = "IBL"
    elif "서측 공동구" in segment:
        area_prefix = "서측공동구"
    elif "지원시설" in segment:
        area_prefix = "지원시설"
    elif re.search(r'154k', segment, re.IGNORECASE): # '154k' 포함 시 '154kV' 구역
        area_prefix = "154kV"

    if area_prefix: # 구역 식별 시
        for code, name in service_mapping.items(): # 서비스 코드 확인
            if re.search(r'\b' + code + r'\b', segment): # 단어 경계로 정확한 코드 일치
                services_found_in_segment.append(name)

        if services_found_in_segment: # 서비스 발견 시
            if area_prefix not in grouped_services: # 해당 구역 없으면 생성
                grouped_services[area_prefix] = set() # set으로 초기화
            for service in services_found_in_segment: # 서비스 추가
                grouped_services[area_prefix].add(service)

# 그룹화된 서비스 바탕으로 출력 문자열 생성
formatted_output = []
for area, services_set in grouped_services.items():
    sorted_services = sorted(list(services_set)) # 서비스 목록 알파벳 순 정렬
    formatted_output.append(f"{area} {' '.join(sorted_services)} 측량 및 드론촬영") # 형식에 맞춰 문자열 생성

print("일일보고 summary용") # 요약 제목 출력
print()
for line in formatted_output: # 보고서 내용 출력
    print(line)

print() # 한 줄 비움
# 서비스 한글명을 영어 약자로 변환하여 요약 문자열 생성
reverse_service_mapping = {v: k for k, v in service_mapping.items()} # 한글명-코드 역매핑 딕셔너리
short_summary_parts = []

# 최종 요약 구역 순서 정렬
for area in sorted(grouped_services.keys()): # 정렬된 구역 이름 순회
    services_set_korean = grouped_services[area]
    services_codes = [ # 한글 서비스를 영어 약자 코드로 변환
        reverse_service_mapping[name]
        for name in services_set_korean
        if name in reverse_service_mapping # 역매핑에 존재하는 경우만 변환
    ]
    sorted_codes = sorted(services_codes) # 서비스 코드 정렬
    short_summary_parts.append(f"{area} {' '.join(sorted_codes)}") # 요약 추가

final_short_summary = " / ".join(short_summary_parts) # 짧은 요약 부분들을 ' / '로 연결
print(final_short_summary) # 최종 짧은 요약 문자열 출력

# @title
segments_for_details = [s.strip() for s in input_string.split('/')] # 상세 내용을 위해 입력 문자열 분리 및 공백 제거

# 구역별 상세 내용 저장 (중복 방지)
grouped_details_by_area = {}

# 구역 식별 패턴 목록 (구체적인 패턴 먼저)
area_patterns_for_details = [
    ("OBL", r"\bOBL\b"),
    ("IBL", r"\bIBL\b"),
    ("서측공동구", r"서측 공동구"),
    ("지원시설", r"지원시설"),
    ("154kV", r"\b154k(?:v)?\b") # '154k' 또는 '154kv'
]

for segment in segments_for_details: # 각 세그먼트 순회하며 상세 내용 추출
    area_prefix_found = ""
    matched_area_str = ""
    remaining_detail_part = segment

    for name, pattern in area_patterns_for_details: # 구역 패턴 순회
        match = re.search(pattern, segment, re.IGNORECASE) # 세그먼트에서 구역 패턴 찾기
        if match: # 패턴 발견 시
            area_prefix_found = name
            matched_area_str = match.group(0)
            remaining_detail_part = segment.replace(matched_area_str, "", 1).strip() # 첫 번째 매치만 교체, 공백 제거
            break # 구역 찾았으므로 다음 세그먼트로 이동

    if area_prefix_found: # 구역 식별 시
        if area_prefix_found not in grouped_details_by_area: # 딕셔너리에 없으면
            grouped_details_by_area[area_prefix_found] = set() # 새로운 set 생성

        if remaining_detail_part: # 상세 내용 존재 시
            grouped_details_by_area[area_prefix_found].add(remaining_detail_part) # 해당 구역의 set에 상세 내용 추가

# @title
# 그룹화된 상세 내용들을 바탕으로 최종 출력 형식 생성
formatted_details_output = []
# 보고서 출력 시 구역 순서 유지 (알파벳 순 정렬)
sorted_areas_for_output = sorted(grouped_details_by_area.keys())

for area in sorted_areas_for_output: # 정렬된 구역 이름 순회
    details_set = grouped_details_by_area[area]
    sorted_details = sorted(list(details_set)) # 상세 내용 목록 알파벳 순 정렬
    formatted_details_output.append(f"{area} {', '.join(sorted_details)} 측량 및 드론촬영") # '구역명 상세내용1, 상세내용2 측량 및 드론촬영' 형식으로 문자열 생성

print("일일보고 daily work status 용") # 상세 내용 제목 출력
print()
for line in formatted_details_output: # 상세 보고서 내용 출력
    print(line)

# @title
representative_summary_parts = []
# 출력 순서를 위해 구역 이름을 정렬합니다.
sorted_areas = sorted(grouped_services.keys())

for area in sorted_areas:
    services_set = grouped_services[area]
    representative_service = ""

    if not services_set: # 서비스가 없는 구역은 건너뜁니다.
        continue

    # 사용자의 요청 예시에 따라 대표 서비스를 선택합니다.
    if area == 'IBL' and '우수' in services_set:
        representative_service = '우수'
    elif area == 'OBL' and '전기' in services_set:
        representative_service = '전기'
    else:
        # 특정 규칙이 없거나 선호하는 서비스가 없는 경우, 알파벳 순으로 첫 번째 서비스를 선택합니다.
        representative_service = sorted(list(services_set))[0]

    representative_summary_parts.append(f"{area} {representative_service}")

final_representative_summary = ", ".join(representative_summary_parts) + " 측량 및 드론촬영 / 데이터 후처리"

print("\n summary용") # 요약 제목 출력
print(final_representative_summary) # 최종 요약 문자열 출력

input_string = " IBL 1번게이트 WS BOX 3500 / IBL CUB 서 WS BOX 1500 / IBL 1번게이트 WS BOX 3500" # @param {type:"string"}

segments = [s.strip() for s in input_string.split('/')] # 입력 문자열을 '/'로 분리 및 공백 제거

# 구역별 서비스 저장 (중복 방지)
grouped_services = {}

# 서비스 코드와 한글명 매핑
service_mapping = {
    'TS': '통신',
    'ES': '전기',
    'OS': '오수',
    'WS': '우수',
    'SB': '소방',
    'SS': '상수',
    'GS': '가스',
    'OB': '옹벽'
}

for segment in segments: # 각 세그먼트 처리
    services_found_in_segment = []
    area_prefix = ""

    # 구역 식별
    if "OBL" in segment:
        area_prefix = "OBL"
    elif "IBL" in segment:
        area_prefix = "IBL"
    elif "서측 공동구" in segment:
        area_prefix = "서측공동구"
    elif "지원시설" in segment:
        area_prefix = "지원시설"
    elif re.search(r'154k', segment, re.IGNORECASE): # '154k' 포함 시 '154kV' 구역
        area_prefix = "154kV"

    if area_prefix: # 구역 식별 시
        for code, name in service_mapping.items(): # 서비스 코드 확인
            if re.search(r'\b' + code + r'\b', segment): # 단어 경계로 정확한 코드 일치
                services_found_in_segment.append(name)

        if services_found_in_segment: # 서비스 발견 시
            if area_prefix not in grouped_services: # 해당 구역 없으면 생성
                grouped_services[area_prefix] = set() # set으로 초기화
            for service in services_found_in_segment: # 서비스 추가
                grouped_services[area_prefix].add(service)

# 그룹화된 서비스 바탕으로 출력 문자열 생성
formatted_output = []
for area, services_set in grouped_services.items():
    sorted_services = sorted(list(services_set)) # 서비스 목록 알파벳 순 정렬
    formatted_output.append(f"{area} {' '.join(sorted_services)} 측량 및 드론데이터 후처리") # 형식에 맞춰 문자열 생성

print("일일보고 summary용") # 요약 제목 출력
print()
for line in formatted_output: # 보고서 내용 출력
    print(line)

print() # 한 줄 비움
# 서비스 한글명을 영어 약자로 변환하여 요약 문자열 생성
reverse_service_mapping = {v: k for k, v in service_mapping.items()} # 한글명-코드 역매핑 딕셔너리
short_summary_parts = []

# 최종 요약 구역 순서 정렬
for area in sorted(grouped_services.keys()): # 정렬된 구역 이름 순회
    services_set_korean = grouped_services[area]
    services_codes = [ # 한글 서비스를 영어 약자 코드로 변환
        reverse_service_mapping[name]
        for name in services_set_korean
        if name in reverse_service_mapping # 역매핑에 존재하는 경우만 변환
    ]
    sorted_codes = sorted(services_codes) # 서비스 코드 정렬
    short_summary_parts.append(f"{area} {' '.join(sorted_codes)}") # 요약 추가

final_short_summary = " / ".join(short_summary_parts) # 짧은 요약 부분들을 ' / '로 연결
print(final_short_summary) # 최종 짧은 요약 문자열 출력

# 그룹화된 서비스를 바탕으로 '측량 및 드론데이터 후처리'용 출력 문자열 생성
formatted_post_processing_output = []
for area, services_set in grouped_services.items():
    sorted_services = sorted(list(services_set)) # 서비스 목록 알파벳 순 정렬
    formatted_post_processing_output.append(f"{area} {', '.join(sorted_services)} 측량 및 드론데이터 후처리") # '측량 및 드론데이터 후처리'로 변경

# @title
segments_for_details = [s.strip() for s in input_string.split('/')] # 상세 내용을 위해 입력 문자열 분리 및 공백 제거

# 구역별 상세 내용 저장 (중복 방지)
grouped_details_by_area = {}

# 구역 식별 패턴 목록 (구체적인 패턴 먼저)
area_patterns_for_details = [
    ("OBL", r"\bOBL\b"),
    ("IBL", r"\bIBL\b"),
    ("서측공동구", r"서측 공동구"),
    ("지원시설", r"지원시설"),
    ("154kV", r"\b154k(?:v)?\b") # '154k' 또는 '154kv'
]

for segment in segments_for_details: # 각 세그먼트 순회하며 상세 내용 추출
    area_prefix_found = ""
    matched_area_str = ""
    remaining_detail_part = segment

    for name, pattern in area_patterns_for_details: # 구역 패턴 순회
        match = re.search(pattern, segment, re.IGNORECASE) # 세그먼트에서 구역 패턴 찾기
        if match: # 패턴 발견 시
            area_prefix_found = name
            matched_area_str = match.group(0)
            remaining_detail_part = segment.replace(matched_area_str, "", 1).strip() # 첫 번째 매치만 교체, 공백 제거
            break # 구역 찾았으므로 다음 세그먼트로 이동

    if area_prefix_found: # 구역 식별 시
        if area_prefix_found not in grouped_details_by_area: # 딕셔너리에 없으면
            grouped_details_by_area[area_prefix_found] = set() # 새로운 set 생성

        if remaining_detail_part: # 상세 내용 존재 시
            grouped_details_by_area[area_prefix_found].add(remaining_detail_part) # 해당 구역의 set에 상세 내용 추가

# @title
# 그룹화된 상세 내용들을 바탕으로 최종 출력 형식 생성
formatted_details_output = []
# 보고서 출력 시 구역 순서 유지 (알파벳 순 정렬)
sorted_areas_for_output = sorted(grouped_details_by_area.keys())

for area in sorted_areas_for_output: # 정렬된 구역 이름 순회
    details_set = grouped_details_by_area[area]
    sorted_details = sorted(list(details_set)) # 상세 내용 목록 알파벳 순 정렬
    formatted_details_output.append(f"{area} {', '.join(sorted_details)} 측량 및 드론데이터 후처리") # '구역명 상세내용1, 상세내용2 측량 및 드론촬영' 형식으로 문자열 생성

print("일일보고 daily work status 용") # 상세 내용 제목 출력
print()
for line in formatted_details_output: # 상세 보고서 내용 출력
    print(line)

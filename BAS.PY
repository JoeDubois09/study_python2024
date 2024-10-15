def calculate_batter_stats(records):
    plate_appearance = len(records)
    at_bats = sum(1 for record in records if record not in ['BB', 'HBP', 'SF'])

    hits = 0
    total_bases = 0
    for record in records:
        if record in ['H', 'D', 'T', 'HR']:
            hits += 1
            if record == 'H':
                total_bases += 1
            elif record == 'D':
                total_bases += 2
            elif record == 'T':
                total_bases += 3
            elif record == 'HR':
                total_bases += 4

    batting_average = hits / at_bats if at_bats > 0 else 0
    OBP = (hits + records.count('BB') + records.count('HBP')) / plate_appearance if plate_appearance > 0 else 0
    slugging_percentage = total_bases / at_bats if at_bats > 0 else 0
    OPS = OBP + slugging_percentage

    return plate_appearance, at_bats, hits, batting_average, OBP, total_bases, slugging_percentage, OPS

def calculate_pitcher_stats(records):
    # records: [피안타 수, 실점 수, 삼진 수, 볼넷 수, 피홈런 수, 승리 수, 패배 수, 투구 이닝 수]
    stats = [int(record) for record in records[:7]] + [float(records[7])]  # 첫 7개는 정수로, 마지막 하나는 실수로 변환

    hits_allowed, earned_runs, strikeouts, walks, home_runs, wins, losses, innings = stats

    hits_allowed_total = hits_allowed + home_runs
    pitcher_OBP = (hits_allowed_total + walks) / innings if innings > 0 else 0
    win_rate = wins / (wins + losses) if (wins + losses) > 0 else 0
    earned_run_average = (earned_runs / innings) * 9 if innings > 0 else 0
    HR_per_IP = home_runs / innings if innings > 0 else 0
    SO_per_IP = strikeouts / innings if innings > 0 else 0
    WHIP = (hits_allowed_total + walks) / innings if innings > 0 else 0

    return hits_allowed_total, pitcher_OBP, win_rate, earned_run_average, HR_per_IP, SO_per_IP, WHIP

def format_batting_average(batting_average):
    if batting_average == 0:
        return "0.000 (0할)"
    
    ba_hundred = round(batting_average * 1000)  # 소수점 3자리로 맞추기
    hund = ba_hundred // 100
    ten = (ba_hundred % 100) // 10
    unit = ba_hundred % 10

    return f"{batting_average:.3f} ({hund}할, {ten}푼, {unit}리)"

def display_player_stats(player_type, stats):
    if player_type == '1':  # 타자
        labels = [
            "타석 수",
            "타수",
            "안타 수",
            "타율",
            "출루율(OBP)",
            "총 누타수",
            "장타율(SLG)",
            "OPS"
        ]
        formatted_stats = list(stats)  # 튜플을 리스트로 변환하여 복사
        formatted_stats[3] = format_batting_average(stats[3])  # 타율은 할푼리로 포맷팅
        
        for label, stat in zip(labels, formatted_stats):
            print(f"{label}: {stat:.3f}" if isinstance(stat, float) else f"{label}: {stat}")

    elif player_type == '2':  # 투수
        labels = [
            "피안타 수",
            "투수 출루율(OBP)",
            "투수 승률",
            "방어율(ERA)",
            "이닝당 피홈런율",
            "이닝당 탈삼진 수",
            "WHIP"
        ]
        
        for label, stat in zip(labels, stats):
            print(f"{label}: {stat:.3f}" if isinstance(stat, float) else f"{label}: {stat}")

def display_record_explanation(player_type):
    explanations = {
        '1': [
            "타자 기록 입력 설명:",
            "타자 기록을 입력하세요. 다음 기호를 사용합니다:",
            "O = 아웃, H = 안타, D = 2루타, T = 3루타, HR = 홈런, BB = 볼넷, HBP = 사구, SF = 희생플라이",
            "예시: H,H,D,T,HR"
        ],
        '2': [
            "투수 기록 입력 설명:",
            "투수 기록을 입력하세요. 다음 기호를 사용합니다:",
            "H = 피안타, R = 실점, SO = 삼진, BB = 볼넷, HR = 피홈런, W = 승리, L = 패배, IP = 투구 이닝",
            "예시: 5,3,7,2,1,10,2,7.0"
        ]
    }

    for line in explanations.get(player_type, []):
        print(line)

def main():
    print("투수 또는 타자를 선택하세요.")
    print("1: 타자")
    print("2: 투수")
    player_type = input("선택: ")

    display_record_explanation(player_type)

    if player_type == '1':
        records = input("타자 기록을 입력하세요 (O, H, D, T, HR, BB, HBP, SF, 콤마로 구분): ").split(',')
        stats = calculate_batter_stats(records)
        display_player_stats('1', stats)

    elif player_type == '2':
        records = input("투수 기록을 입력하세요 (피안타, 실점, 삼진, 볼넷, 피홈런, 승리, 패배, 투구 이닝, 콤마로 구분): ").split(',')
        stats = calculate_pitcher_stats(records)
        display_player_stats('2', stats)

if __name__ == "__main__":
    main()

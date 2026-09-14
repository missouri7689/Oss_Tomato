"""암호화폐 모의투자 시뮬레이터 v0.1 — 실제 주문 없이 현재가만 조회합니다."""

import pyupbit

TICKER = "KRW-BTC"
INITIAL_CASH = 10_000_000

# TODO: 추후 팀원이 구현할 항목 — JSON/CSV 지갑 저장 및 불러오기
# TODO: 추후 팀원이 구현할 항목 — 다중 종목 지원
# TODO: 추후 팀원이 구현할 항목 — 매매 수수료 계산
# TODO: 추후 팀원이 구현할 항목 — 통신 오류 등 상세 예외 처리 및 재시도
# TODO: 추후 팀원이 구현할 항목 — 거래 내역 및 수익률 그래프 시각화


def get_price():
    """호출 시점의 비트코인 현재가를 조회합니다."""
    price = pyupbit.get_current_price(TICKER)
    if price is None or price <= 0:
        print("현재가를 조회하지 못했습니다. 잠시 후 다시 시도하세요.")
        return None
    return price


def buy_bitcoin(wallet):
    try:
        amount = float(input("매수 금액(원): "))
    except ValueError:
        print("숫자를 입력하세요.")
        return

    if not 0 < amount <= wallet["cash"]:
        print("매수 금액은 0원보다 크고 현금 잔고 이하여야 합니다.")
        return

    price = get_price()
    if price is None:
        return

    quantity = amount / price
    wallet["cash"] -= amount
    wallet["btc"] += quantity
    print(f"매수 완료: {quantity:.8f} BTC / {amount:,.2f}원")


def sell_bitcoin(wallet):
    if wallet["btc"] <= 0:
        print("보유한 비트코인이 없습니다.")
        return

    print(f"보유 수량: {wallet['btc']:.8f} BTC")
    value = input("매도 수량(BTC, 전량 매도는 '전량' 입력): ").strip()
    try:
        quantity = wallet["btc"] if value == "전량" else float(value)
    except ValueError:
        print("숫자 또는 '전량'을 입력하세요.")
        return

    if not 0 < quantity <= wallet["btc"]:
        print("매도 수량은 0보다 크고 보유 수량 이하여야 합니다.")
        return

    price = get_price()
    if price is None:
        return

    proceeds = quantity * price
    wallet["btc"] -= quantity
    wallet["cash"] += proceeds
    print(f"매도 완료: {quantity:.8f} BTC / {proceeds:,.2f}원")


def show_wallet(wallet):
    print(f"현금 잔고: {wallet['cash']:,.2f}원")
    print(f"비트코인 보유 수량: {wallet['btc']:.8f} BTC")


def main():
    # 저장 기능이 없으므로 실행할 때마다 초기 자본금으로 시작합니다.
    wallet = {"cash": INITIAL_CASH, "btc": 0.0}
    print("=== 암호화폐 모의투자 시뮬레이터 v0.1 ===")

    while True:
        print("\n[1] 현재 비트코인 시세 조회")
        print("[2] 비트코인 매수")
        print("[3] 비트코인 매도")
        print("[4] 내 지갑 조회")
        print("[5] 프로그램 종료")
        choice = input("메뉴 선택: ").strip()

        if choice == "1":
            price = get_price()
            if price is not None:
                print(f"현재 비트코인 시세: {price:,.0f}원")
        elif choice == "2":
            buy_bitcoin(wallet)
        elif choice == "3":
            sell_bitcoin(wallet)
        elif choice == "4":
            show_wallet(wallet)
        elif choice == "5":
            print("프로그램을 종료합니다. 지갑 정보는 저장되지 않습니다.")
            break
        else:
            print("1~5 중에서 선택하세요.")


if __name__ == "__main__":
    main()

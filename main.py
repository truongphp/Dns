import asyncio
import sys
import os
# Giả sử bạn để các hàm này trong cùng 1 file hoặc import từ app/
from app.resolver import resolve_uid
from app.injector import inject_gold

async def main():
    if len(sys.argv) < 2:
        print("❌ Vui lòng nhập Username!")
        return

    username = sys.argv[1]
    # Lấy token từ Secrets của GitHub
    token_config = {
        'fetch_token': os.environ.get('FETCH_TOKEN'),
        'app_transaction': os.environ.get('APP_TRANSACTION'),
        'is_sandbox': False
    }

    print(f"[*] Đang xử lý: {username}")
    uid = await resolve_uid(username)
    
    if uid:
        print(f"[+] UID: {uid}")
        # Thực hiện bơm Gold
        success, reason = await inject_gold(uid, token_config, log_callback=print)
        
        if success:
            print("\n✅ KÍCH HOẠT THÀNH CÔNG!")
            print(f"🔗 Link cài DNS của bạn: https://apple.nextdns.io/?profile=d1b656")
            print("⚠️ Hãy đảm bảo bạn đã cài DNS trước khi mở app Locket bản Mỹ.")
        else:
            print(f"❌ THẤT BẠI: {reason}")
    else:
        print("❌ Không tìm thấy UID.")

if __name__ == "__main__":
    asyncio.run(main())


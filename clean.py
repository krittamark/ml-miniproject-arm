import pandas as pd

print("กำลังโหลดข้อมูลดิบ...")
# 1. โหลดข้อมูลไฟล์ events และ items
events_df = pd.read_csv('events1.csv')
items_df = pd.read_csv('items.csv')

print("กำลังทำความสะอาดข้อมูล...")
# 2. นำชื่อสินค้า (name) จากตาราง items มาเชื่อมกับตาราง events โดยอิงจากรหัส item_id
events_df = events_df.merge(items_df[['id', 'name']], left_on='item_id', right_on='id', how='left')

# 3. คัดกรองเอาเฉพาะข้อมูลการ "สั่งซื้อสำเร็จ" (purchase) เท่านั้น
purchases = events_df[events_df['type'] == 'purchase']

# 4. จัดกลุ่มข้อมูล (Groupby) โดยใช้ ga_session_id แทนเลขบิล (Transaction)
basket = purchases.groupby(['ga_session_id', 'name'])['name'].count().unstack().fillna(0)

print("กำลังแปลงเป็น One-Hot Encoding...")
# 5. แปลงจำนวนชิ้นให้กลายเป็น 0 (ไม่ได้ซื้อ) และ 1 (ซื้อ)
df = (basket > 0).astype(int)

print(f"คลีนข้อมูลเสร็จสิ้น! ได้ตารางขนาด {df.shape[0]} บิล และมีสินค้าทั้งหมด {df.shape[1]} ชนิด")

df.to_csv('GoogleSaleData_OneHot.csv', index=False)

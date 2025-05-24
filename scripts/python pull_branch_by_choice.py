import sqlite3
import subprocess
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "branches.db"))

def main():
    # الاتصال بقاعدة البيانات
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, description, status FROM branches ORDER BY id")
    branches = cursor.fetchall()
    conn.close()

    # عرض الفروع
    print("\\n📋 قائمة الفروع:\n")
    for branch in branches:
        print(f"{branch[0]}. {branch[1]} ({branch[2]}) - {branch[3]} [status: {branch[4]}]")

    # إدخال المستخدم
    choice = input("\\n🔢 اختر رقم الفرع لسحب التحديثات (أو Enter للفرع الحالي): ").strip()

    if choice:
        try:
            selected_id = int(choice)
            selected_branch = next(b[1] for b in branches if b[0] == selected_id)
            subprocess.run(["git", "checkout", selected_branch], check=True)
            subprocess.run(["git", "pull", "origin", selected_branch], check=True)
            print(f"\\n✅ تم سحب التحديثات للفرع: {selected_branch}")
        except Exception as e:
            print(f"❌ خطأ أثناء السحب: {e}")
    else:
        result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
        current_branch = result.stdout.strip()
        if current_branch:
            subprocess.run(["git", "pull", "origin", current_branch], check=True)
            print(f"\\n✅ تم سحب التحديثات للفرع الحالي: {current_branch}")
        else:
            print("⚠️ لا يوجد فرع نشط حاليًا.")

if __name__ == "__main__":
    main()
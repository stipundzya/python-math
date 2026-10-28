---
type: acceptance-check
check: mechanical
agent: bash
verdict: PASS
severity: null
confidence: null
domain_relevance: null
diff_hash: 538cda1c739386553ac5f865ef42613b90fc951ce9c557c83a23e96350900af2
blocked_on: null
---

# Механический блок — multiplication-screens

Проект: desktop, однофайловый `Math.py`, tkinter, стандартная библиотека. Нет линтера, нет
`requirements.txt`, нет постоянной тестовой инфраструктуры — по осознанному решению спеки
(§Out of Scope). Команды выведены из проекта по приоритету 3 («ни сборки, ни тестов не
предусмотрено») и заменены равносильными проверками.

## L0 — синтаксис / запуск

```
$ /usr/bin/python3 -c "import ast; ast.parse(open('Math.py').read())"
OK
$ /usr/bin/python3 Math.py &   # жив, трейсбеков нет
```

## L1a — статический анализ

Линтера и конфигурации типов в проекте нет (отслеживаемое исключение, причина: проект сознательно
без тестовой/линт-инфраструктуры, см. спека §Out of Scope). Замена — грепы на стиль и обязательные
комментарии (см. L2-скрипт ниже, AC-14).

## L2 — изолированные тесты (равносильная замена: headless-скрипт против живых классов)

Постоянных тестов в проекте нет. L2 закрыт одноразовым headless-скриптом главной сессии
(независимым от скрипта реализующего агента — переписан с нуля, не доверие на слово), прогнанным
против **реального** `Math.py` на ветке через `import Math`. Покрывает AC-1, AC-2, AC-3, AC-4,
AC-5, AC-6, AC-7, AC-9, AC-10, AC-11, AC-12 (оба случая), AC-13 (три сценария). AC-8 закрыт
отдельным скриптом инварианта (см. `multiplication-screens-invariant-receipt.md`, независимо
переверифицирован главной сессией после правки пустых строк). AC-14 закрыт прямыми grep-проверками
ниже.

**120 проверок, 0 провалов** (три провала первой версии скрипта были ошибками самого скрипта —
прямой вызов `finish_turn()` без предшествующего `check_answer()` не взводит `pending_counts`, и
устаревшая ссылка на кнопку после `next_question()` — обе причины задокументированы и исправлены,
все три сценария переведены на реальный поток клик→пауза→проверка).

Полный текст скрипта и дословный вывод финального прогона:

```python
import re
import sys
import io

sys.path.insert(0, '/Users/stsiapanmurziankou/dev/ai/python-math2')
import tkinter as tk
import Math

failures = []
total_checks = 0


def check(name, cond, detail=""):
    global total_checks
    total_checks += 1
    status = "PASS" if cond else "FAIL"
    if not cond:
        failures.append((name, detail))
    print("[%s] %s %s" % (status, name, ("- " + str(detail)) if detail != "" else ""))


root = tk.Tk()
root.withdraw()

# ---------- AC-1, AC-2 ----------
trainer = Math.MathTrainer(root)
root.update_idletasks()

children = trainer.frame.winfo_children()
cells = set()
for c in children:
    gi = c.grid_info()
    cells.add((int(gi['row']), int(gi['column']), c.cget('text')))

for n in range(1, 10):
    btn = next((c for c in children if isinstance(c, tk.Button) and c.cget('text') == f"Умножение на {n}"), None)
    check(f"AC-1 button {n} exists", btn is not None)
    if btn is None:
        continue
    gi = btn.grid_info()
    check(f"AC-1 button {n} position", int(gi['row']) == n and int(gi['column']) == 3, str(gi))
    check(f"AC-1 button {n} font", btn.cget('font') == 'Arial 18', btn.cget('font'))
    check(f"AC-1 button {n} width/height", int(btn.cget('width')) == 20 and int(btn.cget('height')) == 2)
    check(f"AC-1 button {n} padx/pady", str(gi['padx']) == '10' and str(gi['pady']) == '5', str(gi))
    check(f"AC-1 button {n} reqsize", btn.winfo_reqwidth() == 228 and btn.winfo_reqheight() == 54,
          (btn.winfo_reqwidth(), btn.winfo_reqheight()))

check("AC-1 row0 col3 empty", (0, 3, '') not in cells and not any(r == 0 and col == 3 for r, col, _ in cells))
check("AC-1 root fits 1024x768", root.winfo_reqwidth() <= 1024 and root.winfo_reqheight() <= 768,
      (root.winfo_reqwidth(), root.winfo_reqheight()))

check("AC-2 cell count", len(cells) == 33, len(cells))
old_texts = {"Random within 10", "Random via 10", "Минус у 2х значных чисел",
             "Минус с отрицательным результатом", "Минус: 1-значное из 2-значного"}
for text in old_texts:
    check(f"AC-2 old button present: {text}", any(t == text for _, _, t in cells))

# ---------- AC-3 ----------
win1 = tk.Toplevel(root)
s1 = Math.MultiplicationScreen(win1, 3)
win1.update_idletasks()
check("AC-3 title", win1.title() == "Умножение на 3", win1.title())
geo = win1.geometry()
check("AC-3 geometry", geo.split('+')[0] == '500x700', geo)
check("AC-3 bg", win1.cget('bg') == 'lightblue', win1.cget('bg'))

win2 = tk.Toplevel(root)
s2 = Math.MultiplicationScreen(win2, 3)
s1_correct_btn = next(b for b in s1.option_buttons if b.cget('text') == str(s1.correct_answer))
s1_correct_btn.invoke()
root.after(2200, root.quit)
root.mainloop()
check("AC-3 independent counters", s1.correct_count == 1 and s2.correct_count == 0,
      (s1.correct_count, s2.correct_count))
check("AC-3 main window alive", root.winfo_exists() == 1)

# ---------- AC-4 ----------
s3_window = tk.Toplevel(root)
s3 = Math.MultiplicationScreen(s3_window, 5)
check("AC-4 back_button", s3.back_button.cget('text') == 'Back' and s3.back_button.cget('font') == 'Arial 16')
check("AC-4 question_label", s3.question_label.cget('font') == 'Arial 32' and s3.question_label.cget('bg') == 'lightblue')
check("AC-4 buttons_frame bg", s3.buttons_frame.cget('bg') == 'lightblue')
check("AC-4 option_buttons count", len(s3.option_buttons) == 6)
for i, b in enumerate(s3.option_buttons):
    gi = b.grid_info()
    check(f"AC-4 option_button {i} grid", int(gi['row']) == i // 3 and int(gi['column']) == i % 3)
    check(f"AC-4 option_button {i} style", b.cget('font') == 'Arial 24' and int(b.cget('width')) == 5 and int(b.cget('height')) == 2)
check("AC-4 result_label", s3.result_label.cget('font') == 'Arial 24' and s3.result_label.cget('bg') == 'lightblue')
check("AC-4 stats_frame bg", s3.stats_frame.cget('bg') == 'lightblue')
check("AC-4 correct_stats_label", s3.correct_stats_label.cget('fg') == 'green' and s3.correct_stats_label.cget('bg') == 'lightblue')
check("AC-4 incorrect_stats_label", s3.incorrect_stats_label.cget('fg') == 'red' and s3.incorrect_stats_label.cget('bg') == 'lightblue')
check("AC-4 reset_button", s3.reset_button.cget('text') == 'Сбросить' and s3.reset_button.cget('font') == 'Arial 16')

# ---------- AC-5, AC-7 (consistency + live click) ----------
pattern = re.compile(r'^(\d+) × (\d+) = \?$')
for a_fixed in (1, 7):
    sw = tk.Toplevel(root)
    sc = Math.MultiplicationScreen(sw, a_fixed)
    for i in range(100):
        text = sc.question_label.cget('text')
        m = pattern.match(text)
        if not m:
            check(f"AC-5 format a={a_fixed} iter={i}", False, text)
            break
        left, right = int(m.group(1)), int(m.group(2))
        if left != a_fixed or not (2 <= right <= 9):
            check(f"AC-5 range a={a_fixed} iter={i}", False, (left, right))
            break
        correct = sc.correct_answer
        texts = [b.cget('text') for b in sc.option_buttons]
        if sc.correct_answer != left * right:
            check(f"AC-7 correct_answer a={a_fixed} iter={i}", False, (correct, left * right))
            break
        matching = [b for b in sc.option_buttons if b.cget('text') == str(correct)]
        if len(matching) != 1:
            check(f"AC-7 exactly-one-correct-button a={a_fixed} iter={i}", False, (texts, correct))
            break
        if len(set(texts)) != 6 or any(t == '' for t in texts) or any(int(t) <= 0 for t in texts):
            check(f"AC-7 six-distinct-positive a={a_fixed} iter={i}", False, texts)
            break
        sc.next_question()
    else:
        check(f"AC-5/AC-7 100 iterations a={a_fixed}", True)

    final_correct_btn = next(b for b in sc.option_buttons if b.cget('text') == str(sc.correct_answer))
    final_correct_btn.invoke()
    check(f"AC-9 correct-click result a={a_fixed}", sc.result_label.cget('text') == 'Correct! Well done!' and sc.result_label.cget('fg') == 'green')
    check(f"AC-9 buttons disabled a={a_fixed}", all(b.cget('state') == 'disabled' for b in sc.option_buttons))
    check(f"AC-9 count not yet incremented a={a_fixed}", sc.correct_count == 0)

# ---------- AC-6 (fresh instance, 1000 picks) ----------
sw6 = tk.Toplevel(root)
sc6 = Math.MultiplicationScreen(sw6, 4)
picks = [sc6.pick_second_multiplier() for _ in range(1000)]
repeats = sum(1 for i in range(1, len(picks)) if picks[i] == picks[i - 1])
check("AC-6 no consecutive repeats", repeats == 0, repeats)
check("AC-6 all 8 values seen", sorted(set(picks)) == list(range(2, 10)), sorted(set(picks)))

# ---------- AC-9 full timer flow ----------
sw9 = tk.Toplevel(root)
sc9 = Math.MultiplicationScreen(sw9, 2)
q_before = sc9.question_label.cget('text')
correct_text = str(sc9.correct_answer)
btn = next(b for b in sc9.option_buttons if b.cget('text') == correct_text)
btn.invoke()
check("AC-9 immediate: disabled+green+count0", all(b.cget('state') == 'disabled' for b in sc9.option_buttons)
      and sc9.result_label.cget('text') == 'Correct! Well done!' and sc9.correct_count == 0)
root.after(2200, root.quit)
root.mainloop()
check("AC-9 after pause: count incremented, new question, enabled",
      sc9.correct_count == 1 and sc9.question_label.cget('text') != q_before
      and all(b.cget('state') == 'normal' for b in sc9.option_buttons))

# ---------- AC-10 full timer flow ----------
sw10 = tk.Toplevel(root)
sc10 = Math.MultiplicationScreen(sw10, 6)
correct10 = sc10.correct_answer
wrong_text = next(b.cget('text') for b in sc10.option_buttons if b.cget('text') != str(correct10))
wrong_btn = next(b for b in sc10.option_buttons if b.cget('text') == wrong_text)
wrong_btn.invoke()
check("AC-10 immediate: disabled+red+count0", all(b.cget('state') == 'disabled' for b in sc10.option_buttons)
      and sc10.result_label.cget('text') == f"Incorrect. The correct answer is: {correct10}"
      and sc10.result_label.cget('fg') == 'red' and sc10.incorrect_count == 0)
root.after(2200, root.quit)
root.mainloop()
check("AC-10 after pause: count incremented", sc10.incorrect_count == 1)

# ---------- AC-11 (clicks during pause ignored) ----------
sw11 = tk.Toplevel(root)
sc11 = Math.MultiplicationScreen(sw11, 8)
q11 = sc11.question_label.cget('text')
correct11_text = str(sc11.correct_answer)
first_btn = next(b for b in sc11.option_buttons if b.cget('text') == correct11_text)
first_btn.invoke()
result11 = sc11.result_label.cget('text')
for b in sc11.option_buttons:
    b.invoke()
check("AC-11 result/question unchanged during pause",
      sc11.result_label.cget('text') == result11 and sc11.question_label.cget('text') == q11)
root.after(2200, root.quit)
root.mainloop()
check("AC-11 exactly one tally after pause", sc11.correct_count + sc11.incorrect_count == 1,
      (sc11.correct_count, sc11.incorrect_count))

# ---------- AC-12 case 1: reset outside pause (real click+timer flow, 3 correct + 2 incorrect) ----------
sw12a = tk.Toplevel(root)
sc12a = Math.MultiplicationScreen(sw12a, 9)
for _ in range(3):
    b = next(bt for bt in sc12a.option_buttons if bt.cget('text') == str(sc12a.correct_answer))
    b.invoke()
    root.after(2200, root.quit)
    root.mainloop()
for _ in range(2):
    wrong = next(bt for bt in sc12a.option_buttons if bt.cget('text') != str(sc12a.correct_answer))
    wrong.invoke()
    root.after(2200, root.quit)
    root.mainloop()
check("AC-12 case1 precondition: counters non-zero before reset",
      sc12a.correct_count == 3 and sc12a.incorrect_count == 2,
      (sc12a.correct_count, sc12a.incorrect_count))
q_before_reset = sc12a.question_label.cget('text')
sc12a.reset_stats()
check("AC-12 case1: counters zero", sc12a.correct_stats_label.cget('text') == 'Correct: 0'
      and sc12a.incorrect_stats_label.cget('text') == 'Incorrect: 0')
check("AC-12 case1: question unchanged", sc12a.question_label.cget('text') == q_before_reset)

# ---------- AC-12 case 2: reset during pause ----------
sw12b = tk.Toplevel(root)
sc12b = Math.MultiplicationScreen(sw12b, 9)
q_before_pause = sc12b.question_label.cget('text')
correct12b_text = str(sc12b.correct_answer)
btn12b = next(b for b in sc12b.option_buttons if b.cget('text') == correct12b_text)
btn12b.invoke()
result_during_pause = sc12b.result_label.cget('text')
sc12b.reset_stats()
check("AC-12 case2 immediate: zero counters", sc12b.correct_count == 0 and sc12b.incorrect_count == 0)
check("AC-12 case2 immediate: result NOT erased early", sc12b.result_label.cget('text') == result_during_pause
      and sc12b.result_label.cget('text') != '')
check("AC-12 case2 immediate: question unchanged", sc12b.question_label.cget('text') == q_before_pause)
root.after(2200, root.quit)
root.mainloop()
check("AC-12 case2 after pause: still 0:0, not counted",
      sc12b.correct_count == 0 and sc12b.incorrect_count == 0)
check("AC-12 case2 after pause: new question, enabled, result cleared",
      sc12b.question_label.cget('text') != q_before_pause
      and all(b.cget('state') == 'normal' for b in sc12b.option_buttons)
      and sc12b.result_label.cget('text') == '')

# ---------- AC-13: Back / system-close during pause, stderr clean ----------
def run_pause_close(close_fn, label):
    sw = tk.Toplevel(root)
    sc = Math.MultiplicationScreen(sw, 7)
    correct_text = str(sc.correct_answer)
    b = next(bt for bt in sc.option_buttons if bt.cget('text') == correct_text)
    b.invoke()
    other_window = tk.Toplevel(root)
    captured = io.StringIO()
    old_stderr = sys.stderr
    sys.stderr = captured
    try:
        close_fn(sc, sw)
        root.after(2200, root.quit)
        root.mainloop()
    finally:
        sys.stderr = old_stderr
    check(f"AC-13 {label}: stderr clean", captured.getvalue() == '', repr(captured.getvalue()))
    check(f"AC-13 {label}: main window alive", root.winfo_exists() == 1)
    check(f"AC-13 {label}: other window alive", other_window.winfo_exists() == 1)


run_pause_close(lambda sc, sw: sc.go_back(), "go_back")
run_pause_close(lambda sc, sw: sw.destroy(), "system-close")

# ---------- AC-13: repeated open resets counters ----------
sw13 = tk.Toplevel(root)
sc13 = Math.MultiplicationScreen(sw13, 3)
b13 = next(bt for bt in sc13.option_buttons if bt.cget('text') == str(sc13.correct_answer))
b13.invoke()
root.after(2200, root.quit)
root.mainloop()
check("AC-13 precondition: counter non-zero before reopen", sc13.correct_count == 1, sc13.correct_count)
sw13.destroy()
sw13b = tk.Toplevel(root)
sc13b = Math.MultiplicationScreen(sw13b, 3)
check("AC-13 reopen starts at zero", sc13b.correct_count == 0 and sc13b.incorrect_count == 0)

root.destroy()

print()
print("=== %d checks, %d failures ===" % (total_checks, len(failures)))
if failures:
    print("FAILURES:")
    for name, detail in failures:
        print(" -", name, detail)
    sys.exit(1)
else:
    print("ALL CHECKS PASSED")
    sys.exit(0)
```

Дословный вывод финального прогона (хвост, полный лог без провалов):

```
=== 120 checks, 0 failures ===
ALL CHECKS PASSED
```

exit code: 0.

## L1a (AC-14) — grep-проверки стиля и комментариев, перепроверено после правки пустых строк

```
$ grep -F "previous_b исключён до выбора" Math.py | wc -l   # 1
$ grep -F "первый множитель в дистракторах плавает намеренно" Math.py | wc -l   # 1
$ grep -F "недостижимо при a 1..9 и b 2..9" Math.py | wc -l   # 1
$ grep -F "after_cancel защитный" Math.py | wc -l   # 1
$ grep -c "^import \|^from " Math.py   # 3 (совпадает с baseline)
$ grep -c "^ *@" Math.py   # 0
$ git diff --stat 8f2afbd -- Math.py   # 221 insertions, 0 deletions (чистая вставка)
```

Отступы `def` — 1 пробел во всех 67 определениях (включая 11 новых); межметодные разрывы в новом
классе — все 10 по 4 пустые строки, совпадает с измеренным каноном (`{4: 55, 2: 3}` на baseline,
строк с 3 — ноль).

## Гейт покрытия public API

Единственный новый публичный символ — класс `MultiplicationScreen` и его методы, плюс изменение
`MathTrainer.__init__`. Покрыт L2-скриптом выше по всем веткам поведения (AC-1…AC-13) и отдельным
скриптом инварианта (AC-7/AC-8). Непокрытых публичных символов нет.

## Вердикт

PASS. Красных находок нет, блок пропускает в слои суждения.

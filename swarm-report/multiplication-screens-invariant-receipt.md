# Квитанция инварианта — multiplication-screens

## Prereq-1 baseline

Baseline-коммит для `git diff <baseline>..HEAD -- Math.py` в AC-2 и AC-14:

```
8f2afbd1c8cd891deb679ca26e9ff7f787cc801e
```

(`git log --format=%H c3692dc..HEAD -- Math.py | tail -1`, вычислено после коммита перекладки
кнопок `8f2afbd` и коммита спеки `d57626f`, который `Math.py` не трогает.)

## V1/V2 — заполняется реализацией

(Текст одноразовых скриптов и их дословный вывод — AC-8: число нарушений, число комбинаций с
резервом, максимальная глубина, распределение, счётчик попаданий в подменённый `randrange`.)

## Контур верификации: прогон V1 и V2

Интерпретатор: `/usr/bin/python3` (3.9.6, Tk 8.5). Запуск из корня репозитория.
Оба скрипта транзиентны (§Technical Constraints, §Out of Scope): прогнаны, зафиксированы здесь
дословно и удалены из рабочего дерева, в репозиторий не коммитились.

Сводка: V1 — 272 ассерта, 0 провалов, exit 0. V2 — 432 комбинации, 0 нарушений, exit 0.

**Текст V1 ниже отражает прогон ДО пост-реализационной правки пустых строк (состояние «211
вставок»).** Его ассерт «между соседними `def` ровно 3 пустые строки» (`if n != 3`) и вывод
`check('AC-14', ...)` — для того состояния кода, которое больше не актуально. **При буквальном
повторном запуске этого текста против текущего `Math.py` (10 разрывов по 4 строки) этот конкретный
ассерт провалится** — это не регрессия кода, а известное расхождение версии скрипта с кодом.
Актуальная проверка межметодных разрывов — грепы и измерение в
`swarm-report/multiplication-screens-acceptance-mechanical.md` (AC-14, L1a) и в разделе
«Пост-реализационная правка главной сессии» выше (все 10 разрывов по 4 строки, совпадает с
каноном `{4: 55, 2: 3}` на baseline). Найдено аудитом покрытия AC (`business-analyst`,
`/acceptance` L1b), подтверждено текстом строк 787/793 ниже.

### Пост-реализационная правка главной сессии (после прогона V1/V2 агентом)

Спека дважды требовала «ровно 3 пустые строки между методами» — фактическая ошибка, не решение:
измерение на baseline `8f2afbd` даёт `{4: 55, 2: 3}` внутриклассовых разрывов между соседними
`def`, строк с 3 — ноль. Агент реализовал ровно по тексту спеки (верно для субагента — доказанный
дефект задания называют, не переигрывают по своему усмотрению), все 10 межметодных разрывов в
`MultiplicationScreen` получили 3 строки вместо канонических 4. Главная сессия исправила все 10
разрывов на 4 строки и обновила §Technical Constraints спеки (было «3», стало «4», с измерением).

Логика алгоритма правкой не затронута (только пустые строки). Независимая переверификация главной
сессией отдельным скриптом (не текстом агента) после правки:

```
checked: 432 violations: 0
reserve used: 96 max depth: 3 dist: [336, 32, 56, 8]
randrange calls == build calls: 432 432
a=3 b=3 drop=4 -> [6, 7, 9, 10, 11, 12]
a=3 b=3 drop=5 -> [6, 7, 8, 9, 11, 12]
AC-6 repeats: 0 values: [2, 3, 4, 5, 6, 7, 8, 9]
```

AC-14 перепроверена грепом на текущем файле: каждый из четырёх обязательных комментариев найден
ровно 1 раз; импортов 3 (совпадает с baseline); декораторов 0; `git diff --stat 8f2afbd -- Math.py`
— чистая вставка 221 строки (211 от реализации + 10 добавленных пустых строк), удалений 0.

### Третья правка пустых строк (найдена `ux-expert` на цикле `/acceptance` L1b)

Первая правка (выше) пропустила два разрыва вне `MultiplicationScreen` — перед новыми методами
`MathTrainer.make_multiplication_callback` и `MathTrainer.open_multiplication_screen`
(`Math.py:136, 141`), они остались по 3 строки. Исправлено на 4. Исчерпывающий повторный замер по
всему файлу: `{4: 67, 2: 3}` — 67 = 55 (baseline) + 12 новых разрывов (10 в `MultiplicationScreen`
+ 2 в `MathTrainer`); три разрыва по 2 строки предсуществуют в каноне, не тронуты. Дифф —
`git diff --stat 8f2afbd -- Math.py` → 223 вставки (211 кода + 12 пустых строк), 0 удалений.
Независимый прогон V1 главной сессии (120 проверок) после этой правки: 0 провалов, exit 0 — логика
не затронута, менялись только пустые строки.

### Прогон приложения (L0)

```
$ /usr/bin/python3 -c "import ast; ast.parse(open('Math.py').read())"  # синтаксис OK
$ /usr/bin/python3 Math.py &  # жив через 3 с, трейсбеков нет
```

### V2 — инвариант генератора (AC-6, AC-7, AC-8)

Файл `v2_generator_invariant.py` (удалён после прогона):

```python
import collections
import tkinter as tk

import Math

# Эталонные наборы AC-8 (сверяются как МНОЖЕСТВА: порядок после random.shuffle произволен).
REFERENCE = {}
for _drop in range(6):
    REFERENCE[(1, 2, _drop)] = {1, 2, 3, 4, 5, 6}
for _drop in range(4):
    REFERENCE[(3, 3, _drop)] = {6, 8, 9, 10, 11, 12}
    REFERENCE[(9, 9, _drop)] = {72, 80, 81, 82, 83, 90}
REFERENCE[(3, 3, 4)] = {6, 7, 9, 10, 11, 12}   # различающий эталон
REFERENCE[(3, 3, 5)] = {6, 7, 8, 9, 11, 12}    # различающий эталон


def survivors_after_step3(a, b, drop):
    # Независимый пересчёт ШАГА 3 — только для статистики глубины добора.
    # Нормативные ассерты идут по возвращаемому значению поставляемого метода.
    correct = a * b
    formulas = [(a - 1) * b, (a + 1) * b, a * (b - 1), a * (b + 1), a * b - 1, a * b + 1]
    kept = []
    for index in range(6):
        if index == drop:
            continue
        value = formulas[index]
        if value != correct and value != 0 and value not in kept:
            kept.append(value)
    return len(kept)


def main():
    root = tk.Tk()
    root.withdraw()
    window = tk.Toplevel(root)
    screen = Math.MultiplicationScreen(window, 1)

    forced = {'drop': 0, 'calls': 0}
    real_randrange = Math.random.randrange

    def fake_randrange(*args, **kwargs):
        forced['calls'] += 1
        return forced['drop']

    violations = []
    reference_checks = []
    depths = collections.Counter()
    checked = 0
    build_calls = 0

    Math.random.randrange = fake_randrange
    try:
        for a in range(1, 10):
            for b in range(2, 10):
                for drop in range(6):
                    forced['drop'] = drop
                    options = screen.build_answer_options(a, b)
                    build_calls += 1
                    checked += 1
                    correct = a * b
                    problems = []
                    if len(options) != 6:
                        problems.append('len != 6')
                    if len(set(options)) != 6:
                        problems.append('duplicates')
                    if any(not isinstance(v, int) for v in options):
                        problems.append('not int')
                    if any(v <= 0 for v in options):
                        problems.append('non-positive')
                    if correct not in options:
                        problems.append('correct missing')
                    if problems:
                        violations.append((a, b, drop, problems, list(options)))
                    expected = REFERENCE.get((a, b, drop))
                    if expected is not None:
                        reference_checks.append((a, b, drop, set(options) == expected,
                                                 sorted(expected), sorted(options)))
                    depths[5 - survivors_after_step3(a, b, drop)] += 1
    finally:
        Math.random.randrange = real_randrange

    # AC-6: свежий экземпляр, 1000 последовательных вызовов.
    fresh_window = tk.Toplevel(root)
    fresh = Math.MultiplicationScreen(fresh_window, 4)
    picks = [fresh.pick_second_multiplier() for _ in range(1000)]
    repeats = sum(1 for i in range(1, len(picks)) if picks[i] == picks[i - 1])
    out_of_range = [v for v in picks if not 2 <= v <= 9]

    reserve_used = checked - depths[0]
    max_depth = max(depths)
    distribution = [depths[d] for d in range(4)]

    print('=== V2: инвариант генератора вариантов ===')
    print('Math.random is random:', Math.random is __import__('random'))
    print('проверено комбинаций:', checked)
    print('нарушений:', len(violations))
    for v in violations:
        print('  ВИОЛАЦИЯ', v)
    print('комбинаций с добором из резерва:', reserve_used)
    print('максимальная глубина добора:', max_depth)
    print('распределение глубин 0/1/2/3:', ' / '.join(str(x) for x in distribution))
    print('вызовов подменённого randrange:', forced['calls'], '(вызовов build_answer_options:', build_calls, ')')
    print('--- эталонные наборы AC-8 ---')
    for a, b, drop, ok, expected, got in reference_checks:
        print('  a=%d b=%d drop=%d %s ожидалось %s получено %s'
              % (a, b, drop, 'OK ' if ok else 'FAIL', expected, got))
    print('--- AC-6: 1000 вызовов pick_second_multiplier ---')
    print('подряд одинаковых:', repeats, '| вне 2..9:', len(out_of_range),
          '| встреченные значения:', sorted(set(picks)))

    assert checked == 432, checked
    assert not violations, violations
    assert reserve_used == 96, reserve_used
    assert max_depth == 3, max_depth
    assert distribution == [336, 32, 56, 8], distribution
    assert forced['calls'] == build_calls == 432, (forced['calls'], build_calls)
    assert all(ok for _, _, _, ok, _, _ in reference_checks), reference_checks
    assert len(reference_checks) == 16, len(reference_checks)
    assert repeats == 0, repeats
    assert not out_of_range, out_of_range
    assert sorted(set(picks)) == [2, 3, 4, 5, 6, 7, 8, 9], sorted(set(picks))

    print()
    print('V2: ВСЕ АССЕРТЫ ПРОЙДЕНЫ (AC-6, AC-7, AC-8)')
    root.destroy()


main()
```

Дословный вывод `/usr/bin/python3 v2_generator_invariant.py` (exit 0):

```
=== V2: инвариант генератора вариантов ===
Math.random is random: True
проверено комбинаций: 432
нарушений: 0
комбинаций с добором из резерва: 96
максимальная глубина добора: 3
распределение глубин 0/1/2/3: 336 / 32 / 56 / 8
вызовов подменённого randrange: 432 (вызовов build_answer_options: 432 )
--- эталонные наборы AC-8 ---
  a=1 b=2 drop=0 OK  ожидалось [1, 2, 3, 4, 5, 6] получено [1, 2, 3, 4, 5, 6]
  a=1 b=2 drop=1 OK  ожидалось [1, 2, 3, 4, 5, 6] получено [1, 2, 3, 4, 5, 6]
  a=1 b=2 drop=2 OK  ожидалось [1, 2, 3, 4, 5, 6] получено [1, 2, 3, 4, 5, 6]
  a=1 b=2 drop=3 OK  ожидалось [1, 2, 3, 4, 5, 6] получено [1, 2, 3, 4, 5, 6]
  a=1 b=2 drop=4 OK  ожидалось [1, 2, 3, 4, 5, 6] получено [1, 2, 3, 4, 5, 6]
  a=1 b=2 drop=5 OK  ожидалось [1, 2, 3, 4, 5, 6] получено [1, 2, 3, 4, 5, 6]
  a=3 b=3 drop=0 OK  ожидалось [6, 8, 9, 10, 11, 12] получено [6, 8, 9, 10, 11, 12]
  a=3 b=3 drop=1 OK  ожидалось [6, 8, 9, 10, 11, 12] получено [6, 8, 9, 10, 11, 12]
  a=3 b=3 drop=2 OK  ожидалось [6, 8, 9, 10, 11, 12] получено [6, 8, 9, 10, 11, 12]
  a=3 b=3 drop=3 OK  ожидалось [6, 8, 9, 10, 11, 12] получено [6, 8, 9, 10, 11, 12]
  a=3 b=3 drop=4 OK  ожидалось [6, 7, 9, 10, 11, 12] получено [6, 7, 9, 10, 11, 12]
  a=3 b=3 drop=5 OK  ожидалось [6, 7, 8, 9, 11, 12] получено [6, 7, 8, 9, 11, 12]
  a=9 b=9 drop=0 OK  ожидалось [72, 80, 81, 82, 83, 90] получено [72, 80, 81, 82, 83, 90]
  a=9 b=9 drop=1 OK  ожидалось [72, 80, 81, 82, 83, 90] получено [72, 80, 81, 82, 83, 90]
  a=9 b=9 drop=2 OK  ожидалось [72, 80, 81, 82, 83, 90] получено [72, 80, 81, 82, 83, 90]
  a=9 b=9 drop=3 OK  ожидалось [72, 80, 81, 82, 83, 90] получено [72, 80, 81, 82, 83, 90]
--- AC-6: 1000 вызовов pick_second_multiplier ---
подряд одинаковых: 0 | вне 2..9: 0 | встреченные значения: [2, 3, 4, 5, 6, 7, 8, 9]

V2: ВСЕ АССЕРТЫ ПРОЙДЕНЫ (AC-6, AC-7, AC-8)
```

### V2 — доказательство, что различающие эталоны AC-8 имеют зубы

Ошибочное прочтение шага 4 («не более одного кандидата на шаг `k`») прогнано отдельно и
сопоставлено с поставляемым `build_answer_options` по всем 432 комбинациям:

```
wrong a=3,b=3,drop=4 -> [6, 9, 10, 11, 12, 13]   эталон AC-8: {6,7,9,10,11,12}  -> V2 провалился бы
wrong a=3,b=3,drop=5 -> [6, 8, 9, 11, 12, 13]    эталон AC-8: {6,7,8,9,11,12}  -> V2 провалился бы
комбинаций, где поставляемый код расходится с ошибочным прочтением шага 4: 58 из 432
```

Числа совпали с предсказанием спеки (58 комбинаций, оба указанных в §AC-8 ошибочных набора).

### V1 — структурные и поведенческие ассерты (AC-1…AC-5, AC-7, AC-9…AC-14)

Файл `v1_structural_check.py` (удалён после прогона):

```python
import io
import re
import subprocess
import sys
import tkinter as tk

import Math

BASELINE = '8f2afbd1c8cd891deb679ca26e9ff7f787cc801e'
QUESTION_RE = re.compile(r'^(\d+) × (\d+) = \?$')
RESULTS = []


def check(ac, name, ok, detail=''):
    RESULTS.append((ac, name, bool(ok), detail))


def spin(root, ms=2200):
    root.after(ms, root.quit)
    root.mainloop()


def parse_question(screen):
    text = screen.question_label.cget('text')
    m = QUESTION_RE.match(text)
    if m is None:
        raise AssertionError('не разобран текст вопроса: %r' % text)
    return int(m.group(1)), int(m.group(2))


def new_screen(root, a):
    window = tk.Toplevel(root)
    return Math.MultiplicationScreen(window, a)


def find_correct_button(screen):
    target = str(screen.correct_answer)
    return [b for b in screen.option_buttons if b.cget('text') == target]


def git(*args):
    return subprocess.run(('git',) + args, cwd='.', capture_output=True, text=True).stdout


def class_source(text, name):
    lines = text.split('\n')
    start = next(i for i, l in enumerate(lines) if l.startswith('class %s:' % name))
    end = next((i for i in range(start + 1, len(lines))
                if lines[i] and not lines[i].startswith((' ', '\t'))), len(lines))
    return '\n'.join(lines[start:end]).rstrip('\n'), start + 1, end


# ----------------------------------------------------------------- AC-1 / AC-2
root = tk.Tk()
trainer = Math.MathTrainer(root)
root.update_idletasks()

children = trainer.frame.winfo_children()
for n in range(1, 10):
    label = 'Умножение на %d' % n
    found = [w for w in children if w.cget('text') == label]
    check('AC-1', '%s: ровно одна кнопка' % label, len(found) == 1, 'найдено %d' % len(found))
    if len(found) != 1:
        continue
    b = found[0]
    gi = b.grid_info()
    check('AC-1', '%s: класс Button' % label, b.winfo_class() == 'Button', b.winfo_class())
    check('AC-1', '%s: row/column' % label,
          (int(gi['row']), int(gi['column'])) == (n, 3), '%s/%s' % (gi['row'], gi['column']))
    check('AC-1', '%s: font' % label, b.cget('font') == 'Arial 18', repr(b.cget('font')))
    check('AC-1', '%s: width' % label, int(b.cget('width')) == 20, repr(b.cget('width')))
    check('AC-1', '%s: height' % label, int(b.cget('height')) == 2, repr(b.cget('height')))
    check('AC-1', '%s: padx' % label, str(gi['padx']) == '10', repr(gi['padx']))
    check('AC-1', '%s: pady' % label, str(gi['pady']) == '5', repr(gi['pady']))
    check('AC-1', '%s: reqwidth 228' % label, b.winfo_reqwidth() == 228, b.winfo_reqwidth())
    check('AC-1', '%s: reqheight 54' % label, b.winfo_reqheight() == 54, b.winfo_reqheight())

print('замеры геометрии: root %dx%d, frame %dx%d, кнопка 228x54 ожидается'
      % (root.winfo_reqwidth(), root.winfo_reqheight(),
         trainer.frame.winfo_reqwidth(), trainer.frame.winfo_reqheight()))
check('AC-1', 'root reqwidth <= 1024', root.winfo_reqwidth() <= 1024, root.winfo_reqwidth())
check('AC-1', 'root reqheight <= 768', root.winfo_reqheight() <= 768, root.winfo_reqheight())

expected_grid = set()
expected_grid.add((0, 0, 'Addition (0-20)'))
expected_grid.add((0, 1, 'Random within 10'))
expected_grid.add((0, 2, 'Random via 10'))
expected_grid.add((1, 0, 'Минус у 2х значных чисел'))
expected_grid.add((2, 0, 'Минус с отрицательным результатом'))
expected_grid.add((3, 0, 'Минус: 1-значное из 2-значного'))
for i in range(1, 10):
    expected_grid.add((i, 1, 'Deduction [0-20] - %d' % i))
    expected_grid.add((i, 2, 'Deduction via 10 - %d' % i))
    expected_grid.add((i, 3, 'Умножение на %d' % i))

actual_grid = set()
for w in children:
    gi = w.grid_info()
    actual_grid.add((int(gi['row']), int(gi['column']), w.cget('text')))

check('AC-2', 'множество (row, column, text) совпадает с эталоном',
      actual_grid == expected_grid,
      'лишние %s / отсутствуют %s' % (sorted(actual_grid - expected_grid),
                                      sorted(expected_grid - actual_grid)))
check('AC-2', 'детей ровно 33', len(children) == 33, len(children))
check('AC-2', 'все дети frame — Button',
      all(w.winfo_class() == 'Button' for w in children),
      sorted({w.winfo_class() for w in children}))
check('AC-2', 'row=0, column=3 пуст',
      not any(r == 0 and c == 3 for r, c, _ in actual_grid))
check('AC-2', 'существующие 24 кнопки на прежних местах',
      {g for g in expected_grid if g[1] != 3} <= actual_grid)
numstat = git('diff', '--numstat', BASELINE, '--', 'Math.py').split()
check('AC-2', 'дифф от baseline — чистая вставка (0 удалений)',
      len(numstat) == 3 and numstat[1] == '0', numstat)

# ------------------------------------------------------------------------ AC-3
button5 = [w for w in children if w.cget('text') == 'Умножение на 5'][0]
tops_before = [w for w in root.winfo_children() if isinstance(w, tk.Toplevel)]
button5.invoke()
root.update_idletasks()
tops_after = [w for w in root.winfo_children() if isinstance(w, tk.Toplevel)]
opened = [w for w in tops_after if w not in tops_before]
check('AC-3', 'клик открыл ровно одно окно', len(opened) == 1, len(opened))
win = opened[0]
check('AC-3', 'title == "Умножение на 5"', win.title() == 'Умножение на 5', repr(win.title()))
check('AC-3', 'размер из geometry() == 500x700',
      win.geometry().split('+')[0] == '500x700', repr(win.geometry()))
check('AC-3', "bg == 'lightblue'", win.cget('bg') == 'lightblue', repr(win.cget('bg')))
check('AC-3', 'главное окно живо', root.winfo_exists() == 1)

button5.invoke()
root.update_idletasks()
same_title = [w for w in root.winfo_children()
              if isinstance(w, tk.Toplevel) and w.title() == 'Умножение на 5']
check('AC-3', 'повторный клик открыл второе независимое окно', len(same_title) == 2, len(same_title))
for w in same_title:
    w.destroy()

s_a = new_screen(root, 3)
s_b = new_screen(root, 4)
s_a.pending_counts = True
s_a.finish_turn(True)
s_a.pending_counts = True
s_a.finish_turn(False)
check('AC-3', 'счётчики первого экрана выросли',
      (s_a.correct_count, s_a.incorrect_count) == (1, 1),
      (s_a.correct_count, s_a.incorrect_count))
check('AC-3', 'счётчики второго экрана не тронуты',
      (s_b.correct_count, s_b.incorrect_count) == (0, 0),
      (s_b.correct_count, s_b.incorrect_count))
check('AC-3', 'заголовки двух экранов различны',
      (s_a.root.title(), s_b.root.title()) == ('Умножение на 3', 'Умножение на 4'),
      (s_a.root.title(), s_b.root.title()))
s_a.root.destroy()
s_b.root.destroy()

# ------------------------------------------------------------------------ AC-4
s = new_screen(root, 2)
root.update_idletasks()
order = s.root.winfo_children()
expected_order = [s.back_button, s.question_label, s.buttons_frame,
                  s.result_label, s.stats_frame, s.reset_button]
check('AC-4', 'порядок и состав виджетов экрана', order == expected_order,
      [w.winfo_class() for w in order])

check('AC-4', "back_button: text='Back'", s.back_button.cget('text') == 'Back')
check('AC-4', 'back_button: font Arial 16', s.back_button.cget('font') == 'Arial 16',
      repr(s.back_button.cget('font')))
check('AC-4', 'back_button: command задан', s.back_button.cget('command') != '')
pi = s.back_button.pack_info()
check('AC-4', 'back_button: pack(pady=10, anchor=nw, padx=10)',
      (str(pi['pady']), pi['anchor'], str(pi['padx'])) == ('10', 'nw', '10'), pi)

check('AC-4', 'question_label: класс Label', s.question_label.winfo_class() == 'Label')
check('AC-4', 'question_label: font Arial 32', s.question_label.cget('font') == 'Arial 32',
      repr(s.question_label.cget('font')))
check('AC-4', 'question_label: bg lightblue', s.question_label.cget('bg') == 'lightblue')
check('AC-4', 'question_label: pack(pady=10)',
      str(s.question_label.pack_info()['pady']) == '10')

check('AC-4', 'buttons_frame: класс Frame', s.buttons_frame.winfo_class() == 'Frame')
check('AC-4', 'buttons_frame: bg lightblue', s.buttons_frame.cget('bg') == 'lightblue')
check('AC-4', 'buttons_frame: pack(pady=20)',
      str(s.buttons_frame.pack_info()['pady']) == '20')

check('AC-4', 'option_buttons: ровно 6', len(s.option_buttons) == 6, len(s.option_buttons))
check('AC-4', 'option_buttons: дети buttons_frame',
      s.buttons_frame.winfo_children() == s.option_buttons)
for i, b in enumerate(s.option_buttons):
    gi = b.grid_info()
    check('AC-4', 'option_buttons[%d]: grid row/column' % i,
          (int(gi['row']), int(gi['column'])) == (i // 3, i % 3), gi)
    check('AC-4', 'option_buttons[%d]: font Arial 24' % i, b.cget('font') == 'Arial 24',
          repr(b.cget('font')))
    check('AC-4', 'option_buttons[%d]: width 5' % i, int(b.cget('width')) == 5)
    check('AC-4', 'option_buttons[%d]: height 2' % i, int(b.cget('height')) == 2)
    check('AC-4', 'option_buttons[%d]: padx/pady 10' % i,
          (str(gi['padx']), str(gi['pady'])) == ('10', '10'), gi)

check('AC-4', 'result_label: font Arial 24', s.result_label.cget('font') == 'Arial 24')
check('AC-4', 'result_label: bg lightblue', s.result_label.cget('bg') == 'lightblue')
check('AC-4', 'result_label: pack(pady=20)', str(s.result_label.pack_info()['pady']) == '20')

check('AC-4', 'stats_frame: класс Frame', s.stats_frame.winfo_class() == 'Frame')
check('AC-4', 'stats_frame: bg lightblue', s.stats_frame.cget('bg') == 'lightblue')
check('AC-4', 'stats_frame: pack(pady=10)', str(s.stats_frame.pack_info()['pady']) == '10')
check('AC-4', 'stats_frame: двое детей — labels статистики',
      s.stats_frame.winfo_children() == [s.correct_stats_label, s.incorrect_stats_label])

check('AC-4', "correct_stats_label: text 'Correct: 0'",
      s.correct_stats_label.cget('text') == 'Correct: 0', repr(s.correct_stats_label.cget('text')))
check('AC-4', 'correct_stats_label: font Arial 20', s.correct_stats_label.cget('font') == 'Arial 20')
check('AC-4', 'correct_stats_label: bg lightblue', s.correct_stats_label.cget('bg') == 'lightblue')
check('AC-4', 'correct_stats_label: fg green', s.correct_stats_label.cget('fg') == 'green')
pi = s.correct_stats_label.pack_info()
check('AC-4', 'correct_stats_label: pack(side=left, padx=10)',
      (pi['side'], str(pi['padx'])) == ('left', '10'), pi)

check('AC-4', "incorrect_stats_label: text 'Incorrect: 0'",
      s.incorrect_stats_label.cget('text') == 'Incorrect: 0')
check('AC-4', 'incorrect_stats_label: font Arial 20',
      s.incorrect_stats_label.cget('font') == 'Arial 20')
check('AC-4', 'incorrect_stats_label: bg lightblue',
      s.incorrect_stats_label.cget('bg') == 'lightblue')
check('AC-4', 'incorrect_stats_label: fg red', s.incorrect_stats_label.cget('fg') == 'red')
pi = s.incorrect_stats_label.pack_info()
check('AC-4', 'incorrect_stats_label: pack(side=left, padx=10)',
      (pi['side'], str(pi['padx'])) == ('left', '10'), pi)

check('AC-4', "reset_button: text 'Сбросить'", s.reset_button.cget('text') == 'Сбросить',
      repr(s.reset_button.cget('text')))
check('AC-4', 'reset_button: font Arial 16', s.reset_button.cget('font') == 'Arial 16')
check('AC-4', 'reset_button: pack(pady=5)', str(s.reset_button.pack_info()['pady']) == '5')
s.correct_count, s.incorrect_count = 7, 5
s.update_stats()
s.reset_button.invoke()
check('AC-4', 'reset_button: command == reset_stats (проверено invoke)',
      (s.correct_count, s.incorrect_count) == (0, 0)
      and s.correct_stats_label.cget('text') == 'Correct: 0',
      (s.correct_count, s.incorrect_count, s.correct_stats_label.cget('text')))

source = open('Math.py', encoding='utf-8').read()
klass, class_start, class_end = class_source(source, 'MultiplicationScreen')
for line in ('     self.question_label = tk.Label(root, text="", font=("Arial", 32), bg=\'lightblue\')',
             '         button = tk.Button(self.buttons_frame, text="", font=("Arial", 24), width=5, height=2)',
             '     self.result_label = tk.Label(root, text="", font=("Arial", 24), bg=\'lightblue\')'):
    check('AC-4', 'text="" при создании: %s' % line.strip()[:48], line in klass.split('\n'))
s.root.destroy()

# ------------------------------------------------------------------ AC-5, AC-6
s = new_screen(root, 7)
bad_format, bad_left, bad_right = [], [], []
for _ in range(1000):
    s.next_question()
    text = s.question_label.cget('text')
    m = QUESTION_RE.match(text)
    if m is None:
        bad_format.append(text)
        continue
    left, right = int(m.group(1)), int(m.group(2))
    if left != s.multiplier:
        bad_left.append(text)
    if not 2 <= right <= 9:
        bad_right.append(text)
check('AC-5', '1000 вопросов: формат "{a} × {b} = ?" (U+00D7)', not bad_format, bad_format[:3])
check('AC-5', '1000 вопросов: левый множитель всегда == multiplier', not bad_left, bad_left[:3])
check('AC-5', '1000 вопросов: правый множитель всегда в 2..9', not bad_right, bad_right[:3])
check('AC-5', 'заголовок окна == "Умножение на 7"', s.root.title() == 'Умножение на 7')
s.root.destroy()

s = new_screen(root, 1)
picks = [s.pick_second_multiplier() for _ in range(1000)]
repeats = [i for i in range(1, len(picks)) if picks[i] == picks[i - 1]]
check('AC-6', '1000 вызовов pick_second_multiplier: нет повтора подряд', not repeats, repeats[:3])
check('AC-6', 'встречаются все 8 значений', sorted(set(picks)) == list(range(2, 10)),
      sorted(set(picks)))
check('AC-6', 'структурно: нет while/цикла перевыбора в pick_second_multiplier',
      'while' not in klass.split(' def pick_second_multiplier')[1].split(' def ')[0])
check('AC-6', 'структурно: previous_b исключён до выбора (comprehension)',
      'random.choice([value for value in range(2, 10) if value != self.previous_b])' in klass)
s.root.destroy()

# ------------------------------------------------------------------------ AC-7
for a in (1, 7):
    s = new_screen(root, a)
    problems = []
    for _ in range(100):
        left, right = parse_question(s)
        expected_correct = left * right
        texts = [b.cget('text') for b in s.option_buttons]
        if left != a:
            problems.append(('левый множитель', left))
        if s.correct_answer != expected_correct:
            problems.append(('correct_answer', s.correct_answer, expected_correct))
        matching = [b for b in s.option_buttons if b.cget('text') == str(expected_correct)]
        if len(matching) != 1:
            problems.append(('кнопок с правильным ответом', len(matching), texts))
        if any(t == '' for t in texts):
            problems.append(('пустая кнопка', texts))
        if len(set(texts)) != 6:
            problems.append(('дубликаты', texts))
        values = []
        for t in texts:
            try:
                values.append(int(t))
            except ValueError:
                problems.append(('не целое', t))
        if any(v <= 0 for v in values):
            problems.append(('не положительное', texts))
        if len(matching) == 1:
            matching[0].invoke()
            if s.result_label.cget('text') != 'Correct! Well done!':
                problems.append(('result_label', s.result_label.cget('text')))
            s.cancel_pending()
            s.pending_counts = False
        s.next_question()
    check('AC-7', 'экран a=%d, 100 вопросов: 0 нарушений' % a, not problems, problems[:3])
    check('AC-7', 'экран a=%d: таймеров не осталось' % a, s.pending_after is None)
    s.root.destroy()

# ------------------------------------------------------------------------ AC-9
s = new_screen(root, 3)
left, right = parse_question(s)
question_before = s.question_label.cget('text')
btn = find_correct_button(s)
check('AC-9', 'ровно одна кнопка с правильным ответом', len(btn) == 1, len(btn))
btn[0].invoke()
check('AC-9', 'все 6 кнопок disabled сразу после ответа',
      all(b.cget('state') == 'disabled' for b in s.option_buttons),
      [b.cget('state') for b in s.option_buttons])
check('AC-9', "result_label == 'Correct! Well done!'",
      s.result_label.cget('text') == 'Correct! Well done!', repr(s.result_label.cget('text')))
check('AC-9', 'result_label fg green', s.result_label.cget('fg') == 'green')
check('AC-9', 'счётчики ещё не изменены', (s.correct_count, s.incorrect_count) == (0, 0),
      (s.correct_count, s.incorrect_count))
check('AC-9', 'labels статистики ещё 0/0',
      (s.correct_stats_label.cget('text'), s.incorrect_stats_label.cget('text'))
      == ('Correct: 0', 'Incorrect: 0'))
check('AC-9', 'pending_after поставлен', s.pending_after is not None)
spin(root)
check('AC-9', 'через 2000 мс correct_count == 1', s.correct_count == 1, s.correct_count)
check('AC-9', 'label Correct: 1', s.correct_stats_label.cget('text') == 'Correct: 1',
      s.correct_stats_label.cget('text'))
check('AC-9', 'новый вопрос', s.question_label.cget('text') != question_before,
      (question_before, s.question_label.cget('text')))
check('AC-9', 'кнопки снова normal',
      all(b.cget('state') == 'normal' for b in s.option_buttons))
check('AC-9', 'result_label очищен', s.result_label.cget('text') == '')
check('AC-9', 'pending_after сброшен в None', s.pending_after is None)
s.root.destroy()

# ----------------------------------------------------------------------- AC-10
s = new_screen(root, 4)
correct = s.correct_answer
question_before = s.question_label.cget('text')
wrong = [b for b in s.option_buttons if b.cget('text') != str(correct)]
check('AC-10', 'есть 5 неверных кнопок', len(wrong) == 5, len(wrong))
wrong[0].invoke()
check('AC-10', 'все 6 кнопок disabled сразу после ответа',
      all(b.cget('state') == 'disabled' for b in s.option_buttons))
check('AC-10', 'result_label == Incorrect. The correct answer is: N',
      s.result_label.cget('text') == 'Incorrect. The correct answer is: %d' % correct,
      repr(s.result_label.cget('text')))
check('AC-10', 'result_label fg red', s.result_label.cget('fg') == 'red')
check('AC-10', 'счётчики ещё не изменены', (s.correct_count, s.incorrect_count) == (0, 0))
spin(root)
check('AC-10', 'через 2000 мс incorrect_count == 1', s.incorrect_count == 1, s.incorrect_count)
check('AC-10', 'correct_count остался 0', s.correct_count == 0)
check('AC-10', 'label Incorrect: 1', s.incorrect_stats_label.cget('text') == 'Incorrect: 1')
check('AC-10', 'новый вопрос', s.question_label.cget('text') != question_before)
check('AC-10', 'кнопки снова normal',
      all(b.cget('state') == 'normal' for b in s.option_buttons))
s.root.destroy()

# ----------------------------------------------------------------------- AC-11
s = new_screen(root, 5)
btn = find_correct_button(s)[0]
btn.invoke()
result_after_answer = s.result_label.cget('text')
question_after_answer = s.question_label.cget('text')
for b in s.option_buttons:
    b.invoke()
btn.invoke()
check('AC-11', 'повторные клики в паузе не меняют result_label',
      s.result_label.cget('text') == result_after_answer, repr(s.result_label.cget('text')))
check('AC-11', 'повторные клики в паузе не меняют вопрос',
      s.question_label.cget('text') == question_after_answer)
check('AC-11', 'повторные клики в паузе не меняют счётчики',
      (s.correct_count, s.incorrect_count) == (0, 0))
spin(root)
check('AC-11', 'после паузы засчитан ровно один ход',
      s.correct_count + s.incorrect_count == 1, (s.correct_count, s.incorrect_count))
check('AC-11', 'засчитан именно верный ответ', s.correct_count == 1)
s.root.destroy()

# ----------------------------------------- AC-12 случай 1 (вне паузы) ---------
s = new_screen(root, 6)
for _ in range(3):
    s.pending_counts = True
    s.finish_turn(True)
for _ in range(2):
    s.pending_counts = True
    s.finish_turn(False)
check('AC-12.1', 'предусловие: счёт 3 : 2', (s.correct_count, s.incorrect_count) == (3, 2),
      (s.correct_count, s.incorrect_count))
check('AC-12.1', 'предусловие: labels 3 / 2',
      (s.correct_stats_label.cget('text'), s.incorrect_stats_label.cget('text'))
      == ('Correct: 3', 'Incorrect: 2'))
q_before = s.question_label.cget('text')
opts_before = [b.cget('text') for b in s.option_buttons]
res_before = s.result_label.cget('text')
states_before = [b.cget('state') for b in s.option_buttons]
s.reset_stats()
check('AC-12.1', 'labels немедленно 0 / 0',
      (s.correct_stats_label.cget('text'), s.incorrect_stats_label.cget('text'))
      == ('Correct: 0', 'Incorrect: 0'),
      (s.correct_stats_label.cget('text'), s.incorrect_stats_label.cget('text')))
check('AC-12.1', 'вопрос не изменился', s.question_label.cget('text') == q_before)
check('AC-12.1', 'набор вариантов не изменился',
      [b.cget('text') for b in s.option_buttons] == opts_before)
check('AC-12.1', 'текст результата не изменился', s.result_label.cget('text') == res_before)
check('AC-12.1', 'состояния кнопок не изменились',
      [b.cget('state') for b in s.option_buttons] == states_before)
check('AC-12.1', 'таймер не ставился и не отменялся', s.pending_after is None)
s.root.destroy()

# -------------------------------------- AC-12 случай 2 (в течение паузы) ------
s = new_screen(root, 8)
btn = find_correct_button(s)[0]
btn.invoke()
q_in_pause = s.question_label.cget('text')
res_in_pause = s.result_label.cget('text')
pending_id = s.pending_after
s.reset_stats()
check('AC-12.2', 'счётчики обнулены немедленно',
      (s.correct_count, s.incorrect_count) == (0, 0))
check('AC-12.2', 'labels показывают 0 : 0',
      (s.correct_stats_label.cget('text'), s.incorrect_stats_label.cget('text'))
      == ('Correct: 0', 'Incorrect: 0'))
check('AC-12.2', 'result_label НЕ стёрт досрочно', s.result_label.cget('text') == res_in_pause
      and s.result_label.cget('text') != '', repr(s.result_label.cget('text')))
check('AC-12.2', 'вопрос тот же', s.question_label.cget('text') == q_in_pause)
check('AC-12.2', 'отложенный finish_turn НЕ отменён', s.pending_after == pending_id
      and pending_id is not None)
check('AC-12.2', 'pending_counts сброшен флагом', s.pending_counts is False)
spin(root)
check('AC-12.2', 'после паузы счёт по-прежнему 0 : 0',
      (s.correct_count, s.incorrect_count) == (0, 0), (s.correct_count, s.incorrect_count))
check('AC-12.2', 'после паузы labels 0 : 0',
      (s.correct_stats_label.cget('text'), s.incorrect_stats_label.cget('text'))
      == ('Correct: 0', 'Incorrect: 0'))
check('AC-12.2', 'следующий вопрос пришёл', s.question_label.cget('text') != q_in_pause)
check('AC-12.2', 'все кнопки normal',
      all(b.cget('state') == 'normal' for b in s.option_buttons))
check('AC-12.2', "result_label == ''", s.result_label.cget('text') == '')
s.root.destroy()

# ----------------------------------------------------------------------- AC-13
survivor = new_screen(root, 9)
s = new_screen(root, 2)
btn = find_correct_button(s)[0]
btn.invoke()
s.go_back()
check('AC-13', 'go_back отменил таймер (pending_after is None)', s.pending_after is None)
buf = io.StringIO()
saved = sys.stderr
sys.stderr = buf
try:
    spin(root)
finally:
    sys.stderr = saved
check('AC-13', 'go_back в паузе: stderr пуст', buf.getvalue() == '', repr(buf.getvalue()))
check('AC-13', 'go_back в паузе: главное окно живо', root.winfo_exists() == 1)
check('AC-13', 'go_back в паузе: второй экран жив', survivor.root.winfo_exists() == 1)
check('AC-13', 'окно экрана закрыто', 'Умножение на 2' not in
      [w.title() for w in root.winfo_children() if isinstance(w, tk.Toplevel)])

s2 = new_screen(root, 3)
btn = find_correct_button(s2)[0]
btn.invoke()
pending_before_x = s2.pending_after
s2.root.destroy()
buf = io.StringIO()
saved = sys.stderr
sys.stderr = buf
try:
    spin(root)
finally:
    sys.stderr = saved
check('AC-13', 'системная ✕ в паузе: таймер был активен (after_cancel не вызывался)',
      pending_before_x is not None)
check('AC-13', 'системная ✕ в паузе: stderr пуст', buf.getvalue() == '', repr(buf.getvalue()))
check('AC-13', 'системная ✕ в паузе: главное окно живо', root.winfo_exists() == 1)
check('AC-13', 'системная ✕ в паузе: второй экран жив', survivor.root.winfo_exists() == 1)

reopened = new_screen(root, 2)
check('AC-13', 'повторное открытие: счётчики с нуля',
      (reopened.correct_count, reopened.incorrect_count) == (0, 0))
check('AC-13', 'повторное открытие: labels с нуля',
      (reopened.correct_stats_label.cget('text'),
       reopened.incorrect_stats_label.cget('text')) == ('Correct: 0', 'Incorrect: 0'))
reopened.root.destroy()
survivor.root.destroy()

# ----------------------------------------------------------------------- AC-14
COMMENTS = (
    '# previous_b исключён до выбора, поэтому перевыбора в цикле не нужно',
    '# первый множитель в дистракторах плавает намеренно: это соседние строки таблицы',
    '# недостижимо при a 1..9 и b 2..9: максимальная фактическая глубина добора 3 (прогон 432 комбинаций)',
    '# after_cancel защитный: таймер Toplevel умирает вместе с окном, но полагаться на это не стоит',
)
for c in COMMENTS:
    check('AC-14', 'комментарий найден ровно один раз: %s…' % c[:40], source.count(c) == 1,
          source.count(c))

klass_lines = klass.split('\n')
bad_def_indent, bad_stmt_indent, bad_gaps = [], [], []
depth = 0
for idx, line in enumerate(klass_lines):
    stripped = line.strip()
    continuation = depth > 0
    if stripped and not continuation:
        indent = len(line) - len(line.lstrip(' '))
        if stripped.startswith('def '):
            if indent != 1:
                bad_def_indent.append((idx, indent, stripped[:40]))
        elif not line.startswith('class '):
            if indent not in (5, 9, 13, 17):
                bad_stmt_indent.append((idx, indent, stripped[:40]))
    depth += line.count('(') + line.count('[') + line.count('{')
    depth -= line.count(')') + line.count(']') + line.count('}')
first_def = next(i for i, l in enumerate(klass_lines) if l.startswith(' def '))
for idx, line in enumerate(klass_lines):
    # первый def идёт сразу за строкой class — так во всех девяти существующих классах;
    # требование «ровно 3 пустые строки» относится к СОСЕДНИМ def.
    if line.startswith(' def ') and idx > first_def:
        j, n = idx - 1, 0
        while j >= 0 and klass_lines[j].strip() == '':
            n += 1
            j -= 1
        if n != 3:
            bad_gaps.append((idx, n, line.strip()[:40]))
check('AC-14', 'новый класс: отступ каждого def ровно 1 пробел', not bad_def_indent,
      bad_def_indent)
check('AC-14', 'новый класс: отступы statement ∈ {5, 9, 13, 17}', not bad_stmt_indent,
      bad_stmt_indent)
check('AC-14', 'новый класс: между соседними def ровно 3 пустые строки', not bad_gaps, bad_gaps)
check('AC-14', 'новый класс: нет декораторов',
      not [l for l in klass_lines if l.strip().startswith('@')])
check('AC-14', 'новый класс: нет docstring',
      not [l for l in klass_lines if l.strip().startswith(('"""', "'''"))])
check('AC-14', 'новый класс: нет type hints в сигнатурах',
      not [l for l in klass_lines if l.startswith(' def ') and ('->' in l or ':' in l[:-1].split('(')[1])],
      [l for l in klass_lines if l.startswith(' def ') and '->' in l])
check('AC-14', 'в файле 0 строк с @', not [l for l in source.split('\n') if l.strip().startswith('@')])

baseline_source = git('show', '%s:Math.py' % BASELINE)
imports_now = len([l for l in source.split('\n') if l.startswith('import ') or l.startswith('from ')])
imports_base = len([l for l in baseline_source.split('\n')
                    if l.startswith('import ') or l.startswith('from ')])
check('AC-14', 'число импортов не изменилось (%d)' % imports_now,
      imports_now == imports_base == 3, (imports_now, imports_base))

OLD_CLASSES = ('Deduction1020Screen', 'AdditionScreen', 'RandomWithin10Screen', 'RandomVia10Screen',
               'DeductionScreen', 'TwoDigitSubtractionScreen', 'NegativeResultSubtractionScreen',
               'NoBorrowSubtractionScreen')
for name in OLD_CLASSES:
    now, a1, a2 = class_source(source, name)
    base, b1, b2 = class_source(baseline_source, name)
    check('AC-14', 'класс %s не изменён ни строкой' % name, now == base,
          'now %d-%d / base %d-%d' % (a1, a2, b1, b2))
mt_now, _, _ = class_source(source, 'MathTrainer')
mt_base, _, _ = class_source(baseline_source, 'MathTrainer')
added = [l for l in mt_now.split('\n') if l not in mt_base.split('\n')]
removed = [l for l in mt_base.split('\n') if l not in mt_now.split('\n')]
check('AC-14', 'MathTrainer: из старого кода ничего не удалено', not removed, removed)
check('AC-14', 'MathTrainer: добавлены только кнопки умножения и два метода открытия',
      all(('Умножение на' in l) or ('multiplication' in l) or ('Multiplication' in l)
          or l.strip() == '' or l.strip() == 'for i in range(1, 10):'
          for l in added), added)
check('AC-14', 'новый класс один: MultiplicationScreen',
      len([l for l in source.split('\n') if l.startswith('class ')]) == 10)
check('AC-14', 'синтаксис: import Math прошёл', Math.MultiplicationScreen is not None)
check('AC-14', 'MathTrainer.make_multiplication_callback существует',
      callable(Math.MathTrainer.make_multiplication_callback))
check('AC-14', 'MathTrainer.open_multiplication_screen существует',
      callable(Math.MathTrainer.open_multiplication_screen))
check('AC-14', 'граница нового класса: %d-%d' % (class_start, class_end), True,
      'строки %d-%d' % (class_start, class_end))

root.destroy()

# ----------------------------------------------------------------------- отчёт
print('=== V1: структурные и поведенческие ассерты ===')
order_ac = []
for ac, _, _, _ in RESULTS:
    if ac not in order_ac:
        order_ac.append(ac)
failed_total = 0
for ac in order_ac:
    rows = [r for r in RESULTS if r[0] == ac]
    failed = [r for r in rows if not r[2]]
    failed_total += len(failed)
    print('%-8s %s  (%d ассертов, провалов %d)'
          % (ac, 'PASS' if not failed else 'FAIL', len(rows), len(failed)))
    for _, name, _, detail in failed:
        print('    FAIL: %s | %s' % (name, detail))
print()
print('всего ассертов:', len(RESULTS), '| провалов:', failed_total)
print('V1:', 'ВСЕ АССЕРТЫ ПРОЙДЕНЫ' if failed_total == 0 else 'ЕСТЬ ПРОВАЛЫ')
sys.exit(1 if failed_total else 0)
```

Дословный вывод `/usr/bin/python3 v1_structural_check.py` (exit 0):

```
замеры геометрии: root 992x694, frame 992x640, кнопка 228x54 ожидается
=== V1: структурные и поведенческие ассерты ===
AC-1     PASS  (92 ассертов, провалов 0)
AC-2     PASS  (6 ассертов, провалов 0)
AC-3     PASS  (9 ассертов, провалов 0)
AC-4     PASS  (68 ассертов, провалов 0)
AC-5     PASS  (4 ассертов, провалов 0)
AC-6     PASS  (4 ассертов, провалов 0)
AC-7     PASS  (4 ассертов, провалов 0)
AC-9     PASS  (13 ассертов, провалов 0)
AC-10    PASS  (10 ассертов, провалов 0)
AC-11    PASS  (5 ассертов, провалов 0)
AC-12.1  PASS  (8 ассертов, провалов 0)
AC-12.2  PASS  (11 ассертов, провалов 0)
AC-13    PASS  (11 ассертов, провалов 0)
AC-14    PASS  (27 ассертов, провалов 0)

всего ассертов: 272 | провалов: 0
V1: ВСЕ АССЕРТЫ ПРОЙДЕНЫ
```

### Замеры геометрии (AC-1)

```
root 992x694, frame 992x640, кнопка «Умножение на N» 228x54 (reqwidth/reqheight)
ожидание спеки: root ~992x694 -> совпало; порог 1024x768 выдержан по обеим осям
```

Машинный ассерт сравнивает требуемую геометрию с НОМИНАЛЬНЫМ разрешением и не учитывает
строку заголовка, menu bar и Dock — поэтому V3 (человек, 1024x768) остаётся обязательным.

### Дифф от baseline

```
$ git diff --numstat 8f2afbd -- Math.py
211	0	Math.py
```

Чистая вставка: 0 удалённых строк, девять существующих классов экранов сверены с
`git show 8f2afbd:Math.py` построчно и идентичны (ассерты AC-14 в V1).

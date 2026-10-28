---
type: acceptance-check
check: error-handling
agent: error-handling-reviewer
verdict: PASS
severity: minor
confidence: high
domain_relevance: high
diff_hash: 538cda1c739386553ac5f865ef42613b90fc951ce9c557c83a23e96350900af2
blocked_on: null
---

# Error-handling review — multiplication-screens

Дифф `main...feature/multiplication-screens` по `Math.py` (класс `MultiplicationScreen`).

## Проверено эмпирически агентом (не принято со слов спеки)

«Таймер на закрываемом Toplevel умирает вместе с ним» воспроизведено дифференциальным прогоном:
таймер на разрушаемом `Toplevel` не срабатывает и stderr пуст; контрольный таймер на выжившем
`root` срабатывает и даёт `TclError`. Отсутствие `WM_DELETE_WINDOW`-хэндлера находкой не является.
Исчерпывающий прогон `build_answer_options` по 432 комбинациям: ограничитель резерва не достигается
ни разу, максимальное `k = 4`.

## Находка (minor, не блокирует)

`Math.py:1577-1579` — ограничитель цикла добора резерва (`k > 50`) выходит молчаливым `break`.
Недостижим при доменах `a` 1..9, `b` 2..9 (доказано), поэтому не проглоченная ошибка. Но если
диапазоны когда-нибудь расширят (`b=1`, множитель 0), первым видимым симптомом станет `IndexError`
в `next_question` на кадр от причины, без `a`/`b`/`options` в трейсе.

Предложение: заменить `break` на `raise RuntimeError(f"не удалось набрать дистракторы: a={a}, b={b}, options={options}")`.

## Вне находок

Новых `except`/перехватов в диффе нет вовсе. `pending_counts` — объявленное спекой поведение
(AC-12), не fallback. `cancel_pending` не глушит `after_cancel`. Предсуществующий
`except ModuleNotFoundError` диффом не затронут.

## Вердикт

PASS. critical — 0, major — 0, minor — 1 (WARN, не блокирует).

# Порівняння алгоритмів сортування: Merge Sort, Insertion Sort, Timsort

Набори даних: `random`, `sorted`, `reverse`, `nearly_sorted`.
Розміри: [500, 2000, 6000, 12000]. Повторів: 3.
Для **Insertion Sort** великі `n` (> 6000) пропущено, щоб уникнути надто довгого очікування.

## Результати порівнянь алгоритмів сортування


### n = 500

| Dataset | Insertion Sort | Merge Sort | Timsort |
| random       | 0.002804 | 0.000476 | 0.000023 |
| sorted       | 0.000029 | 0.000336 | 0.000002 |
| reverse      | 0.005498 | 0.000353 | 0.000002 |
| nearly_sorted | 0.000049 | 0.000354 | 0.000004 |

### n = 2000

| Dataset | Insertion Sort | Merge Sort | Timsort |
| random       | 0.049956 | 0.002264 | 0.000123 |
| sorted       | 0.000124 | 0.001590 | 0.000007 |
| reverse      | 0.098502 | 0.001555 | 0.000007 |
| nearly_sorted | 0.000797 | 0.001854 | 0.000016 |

### n = 6000

| Dataset | Insertion Sort | Merge Sort | Timsort |
| random       | 0.480359 | 0.007694 | 0.000419 |
| sorted       | 0.000388 | 0.005165 | 0.000021 |
| reverse      | 0.920968 | 0.005251 | 0.000025 |
| nearly_sorted | 0.007337 | 0.006265 | 0.000047 |

### n = 12000

| Dataset | Insertion Sort | Merge Sort | Timsort |
| random       | — | 0.016671 | 0.000911 |
| sorted       | — | 0.010711 | 0.000041 |
| reverse      | — | 0.011460 | 0.000043 |
| nearly_sorted | — | 0.013466 | 0.000096 |



## Детальніше по наборах


## Набір даних: **random**

### n = 500

| Алгоритм | Середній час (с) |
| Insertion Sort | 0.002804 |
| Merge Sort | 0.000476 |
| Timsort (sorted) | 0.000023 |

**Найшвидший:** Timsort (sorted) — 0.000023 с.

### n = 2000

| Алгоритм | Середній час (с) |
| Insertion Sort | 0.049956 |
| Merge Sort | 0.002264 |
| Timsort (sorted) | 0.000123 |

**Найшвидший:** Timsort (sorted) — 0.000123 с.

### n = 6000

| Алгоритм | Середній час (с) |
| Insertion Sort | 0.480359 |
| Merge Sort | 0.007694 |
| Timsort (sorted) | 0.000419 |

**Найшвидший:** Timsort (sorted) — 0.000419 с.

### n = 12000

| Алгоритм | Середній час (с) |
| Insertion Sort | — |
| Merge Sort | 0.016671 |
| Timsort (sorted) | 0.000911 |

**Найшвидший:** Timsort (sorted) — 0.000911 с.


## Набір даних: **sorted**

### n = 500

| Алгоритм | Середній час (с) |
| Insertion Sort | 0.000029 |
| Merge Sort | 0.000336 |
| Timsort (sorted) | 0.000002 |

**Найшвидший:** Timsort (sorted) — 0.000002 с.

### n = 2000

| Алгоритм | Середній час (с) |
| Insertion Sort | 0.000124 |
| Merge Sort | 0.001590 |
| Timsort (sorted) | 0.000007 |

**Найшвидший:** Timsort (sorted) — 0.000007 с.

### n = 6000

| Алгоритм | Середній час (с) |
| Insertion Sort | 0.000388 |
| Merge Sort | 0.005165 |
| Timsort (sorted) | 0.000021 |

**Найшвидший:** Timsort (sorted) — 0.000021 с.

### n = 12000

| Алгоритм | Середній час (с) |
| Insertion Sort | — |
| Merge Sort | 0.010711 |
| Timsort (sorted) | 0.000041 |

**Найшвидший:** Timsort (sorted) — 0.000041 с.


## Набір даних: **reverse**

### n = 500

| Алгоритм | Середній час (с) |
| Insertion Sort | 0.005498 |
| Merge Sort | 0.000353 |
| Timsort (sorted) | 0.000002 |

**Найшвидший:** Timsort (sorted) — 0.000002 с.

### n = 2000

| Алгоритм | Середній час (с) |
| Insertion Sort | 0.098502 |
| Merge Sort | 0.001555 |
| Timsort (sorted) | 0.000007 |

**Найшвидший:** Timsort (sorted) — 0.000007 с.

### n = 6000

| Алгоритм | Середній час (с) |
| Insertion Sort | 0.920968 |
| Merge Sort | 0.005251 |
| Timsort (sorted) | 0.000025 |

**Найшвидший:** Timsort (sorted) — 0.000025 с.

### n = 12000

| Алгоритм | Середній час (с) |
| Insertion Sort | — |
| Merge Sort | 0.011460 |
| Timsort (sorted) | 0.000043 |

**Найшвидший:** Timsort (sorted) — 0.000043 с.


## Набір даних: **nearly_sorted**

### n = 500

| Алгоритм | Середній час (с) |
| Insertion Sort | 0.000049 |
| Merge Sort | 0.000354 |
| Timsort (sorted) | 0.000004 |

**Найшвидший:** Timsort (sorted) — 0.000004 с.

### n = 2000

| Алгоритм | Середній час (с) |
| Insertion Sort | 0.000797 |
| Merge Sort | 0.001854 |
| Timsort (sorted) | 0.000016 |

**Найшвидший:** Timsort (sorted) — 0.000016 с.

### n = 6000

| Алгоритм | Середній час (с) |
| Insertion Sort | 0.007337 |
| Merge Sort | 0.006265 |
| Timsort (sorted) | 0.000047 |

**Найшвидший:** Timsort (sorted) — 0.000047 с.

### n = 12000

| Алгоритм | Середній час (с) |
| Insertion Sort | — |
| Merge Sort | 0.013466 |
| Timsort (sorted) | 0.000096 |

**Найшвидший:** Timsort (sorted) — 0.000096 с.

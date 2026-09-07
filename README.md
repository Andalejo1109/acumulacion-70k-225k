# De 70 mil a 225 mil, luego retiro indexado al 3%

Dos fases, un mismo portafolio:

1. **Acumular** (hoy → año 5): 70 mil de partida + **23 mil al año** hasta cruzar **225 mil**.
2. **Retirar y seguir creciendo**: el año 1 se sacan **10 mil**. Cada año siguiente el retiro sube **3%** (inflación). El resto se queda invertido.

Escenarios de rentabilidad: **10%, 13% y 17%** anual. Son ilustraciones, no una promesa. 13–17% se parece más a una década buena de growth que a un promedio de planificación.

![De 70 mil a 225 mil — escenarios 10%, 13% y 17%](acumulacion_70k_225k.svg?raw=1)

## Fase 1 — llegar a 225 mil

| | |
|---|---|
| Capital inicial | 70.000 USD |
| Aporte | 23.000 USD / año (1.917 / mes) |
| Horizonte | 5 años |
| Meta | 225.000 USD |

| Escenario | Capital año 5 | ¿Llega a 225k? |
|---|---:|---|
| Solo aportes (0%) | 185.000 | No |
| ~10% | 259.478 | Sí |
| ~13% | 286.701 | Sí |
| ~17% | 327.017 | Sí |

Sin rendimiento no alcanza. Con 10% o más, sí — y sobra colchón.

## Fase 2 — 10 mil el año 1, +3% cada año

Al cruzar 225 mil dejan de ser obligatorios los 23 mil de aporte. Empieza el retiro:

| Año de retiro | Monto |
|---|---:|
| 1 | 10.000 |
| 2 | 10.300 |
| 5 | 11.255 |
| 10 | 13.048 |

En 10 años se habrían cobrado **114.639** (no 100 mil: la inflación del retiro suma ~14.6 mil extra).

Partiendo de **225 mil**, sin aportes nuevos:

| Años retirando | Capital @ 10% | Capital @ 13% | Capital @ 17% | Ya cobrado |
|---|---:|---:|---:|---:|
| 0 | 225.000 | 225.000 | 225.000 | 0 |
| 1 | 237.500 | 244.250 | 253.250 | 10.000 |
| 5 | 297.900 | 346.200 | 419.500 | 53.091 |
| 10 | 405.000 | 558.700 | 834.200 | 114.639 |

En los tres escenarios el portafolio **termina más grande** que el día 1 del retiro, después de haber pagado un sueldo que sube con inflación.

Si el año 5 cierra en 259 / 287 / 327 mil (fase 1 a 10 / 13 / 17%), el colchón es aún mayor: el 10 mil inicial es 3,9% / 3,5% / 3,1% de ese capital.

Tres matices:

1. 17% durante 15 años seguidos es un escenario **optimista**. Sirve para ver el techo, no para presupuestar el retiro.
2. El riesgo de secuencia (un 2022 el año 1 de retiro) no aparece en una línea recta. Por eso se llega a 225 mil *antes* de vivir de él.
3. El 3% del retiro es el piso de inflación del plan. Si la inflación corre al 5%, hay que revisar el monto — no el método.

## Cómo correrlo

```bash
pip install -r requirements.txt
python simular_acumulacion_225k.py
```

Genera PNG + GIF y imprime las dos tablas. Notebook: [Acumulacion_70k_225k.ipynb](Acumulacion_70k_225k.ipynb).

## Disclaimer

Proyección ilustrativa. Rentabilidades pasadas no predicen resultados futuros. No es recomendación de inversión.

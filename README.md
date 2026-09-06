# De 70 mil a 225 mil en 5 años

Proyección de **DCA mensual** para un retiro parcial de **10 mil USD al año**.

No es un backtest histórico. Es una ilustración de tres caminos a 5 años:

1. Solo aportes (0%)
2. Aportes + ~8% anual
3. Aportes + ~10% anual

![Proyección de acumulación](acumulacion_70k_225k.svg)

PNG y GIF para redes: genera `acumulacion_70k_225k.png` y `.gif` con el script o el notebook.

## Supuestos

| | |
|---|---|
| Capital inicial | 70.000 USD |
| Aporte | 23.000 USD / año (1.917 / mes) |
| Horizonte | 5 años |
| Meta | 225.000 USD |
| Retiro parcial | 10.000 USD / año (~4% de la meta) |

## Resultado

| Escenario | Capital año 5 | ¿Llega a 225k? | 4% de ese capital |
|---|---:|---|---:|
| Solo aportes | 185.000 | No | 7.400 |
| ~8% | 242.664 | Sí | 9.707 |
| ~10% | 259.478 | Sí | 10.379 |

El ahorro solo no cierra la meta. El compuesto de 8–10% sí. El mercado no sube en línea recta: 8–10% es banda de planificación, no garantía.

## Cómo correrlo

```bash
pip install -r requirements.txt
python simular_acumulacion_225k.py
```

Notebook paso a paso: [Acumulacion_70k_225k.ipynb](Acumulacion_70k_225k.ipynb) (Colab o Jupyter).

## Archivos

- `simular_acumulacion_225k.py` — script que arma PNG + GIF
- `Acumulacion_70k_225k.ipynb` — misma lógica, celda por celda
- `acumulacion_70k_225k.svg` — gráfica del README
- `acumulacion_70k_225k.png` / `.gif` — se generan al correr el script

La paleta visual reutiliza el estilo de [Retiro-portafolio](https://github.com/Andalejo1109/Retiro-portafolio).

## Disclaimer

Proyección ilustrativa. Rentabilidades pasadas no predicen resultados futuros. No es recomendación de inversión.

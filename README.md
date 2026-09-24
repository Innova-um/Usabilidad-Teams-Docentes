# Uso de Teams · Docentes

Tablero sobre el uso de Microsoft Teams por parte de los usuarios con rol **Profesor** de la Universidad del Magdalena, a partir del informe de Microsoft 365 «Actividad de usuarios de Teams».

Abre `index.html` en el navegador. No necesita servidor.

## Qué muestra

- **Profesores analizados:** total de profesores del informe, o del grupo elegido.
- **Conexión a Teams del 21 al 22 sep 2026:** cuántos profesores usaron Teams en el rango y cuántos no, con el conteo por día.
- **Detalle por profesor:** nombre completo, usuario, si usó Teams en el rango, nivel de uso, última actividad, reuniones, horas conectado, cámara, pantalla compartida, mensajes y llamadas. Se ordena por cualquier columna y se descarga en CSV.
- Filtros por conexión en el rango, nivel de uso y buscador por nombre o usuario.

## Cómo actualizarlo

1. Guarda en la raíz del repositorio (no se suben a GitHub):
   - `Usabilidad teams.csv`: informe de actividad de usuarios de Teams, con la columna `Rol`.
   - `profesores user y nombre ocmpleto.xlsx`: columnas `User` y `nombre_profesor`.
2. Si cambia el rango de fechas, edita `RANGO` al inicio de `build/build.py`. La fecha final nunca pasa de la fecha del informe.
3. Ejecuta:

   ```bash
   python build/build.py
   ```

Requisitos: Python 3 con `pandas` y `openpyxl`.

## Notas

- **Conexión en el rango:** se decide con la fecha de última actividad en Teams. El informe llega hasta su fecha de actualización (22/09/2026).
- **Reuniones, horas y mensajes** son el acumulado del periodo completo del informe (180 días), no solo del rango.
- **Nivel de uso** según reuniones en el periodo: intensivo 52 o más, frecuente 13 a 51, ocasional 1 a 12, sin reuniones (solo chat u otras acciones) y no usó Teams.
- `index.html` contiene nombres y usuarios de docentes: mantén este repositorio **privado**.

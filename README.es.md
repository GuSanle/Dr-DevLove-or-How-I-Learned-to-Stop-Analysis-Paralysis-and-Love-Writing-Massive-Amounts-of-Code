# Dr. DevLove 
### *o: Cómo aprendí a dejar de analizar y amar escribir cantidades masivas de código*

[![GitHub license](https://img.shields.io/github/license/forestsheep911/Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code)](https://github.com/forestsheep911/Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code/blob/main/LICENSE)

> "¡Caballeros, no pueden pelear aquí! ¡Esta es la Sala de Guerra!" — *Dr. Strangelove*
>
> "¡Desarrolladores, no pueden pensar demasiado aquí! ¡Esto es el IDE!" — *Dr. DevLove*

¿Estás cansado de mirar un cursor parpadeante? ¿Sufres de *Parálisis por Análisis* crónica? ¿Pasas más tiempo planeando tu código que escribiéndolo?

**Dr. DevLove** (alias `gh-stats`) es tu receta. Es una herramienta CLI que prueba que *estás* trabajando. Valida tu existencia rastreando tus contribuciones diarias de código en todo el universo GitHub, sin necesidad de clones locales porque, ¿quién tiene espacio en disco para eso?

---

[English](./README.md) | [🇨🇳 中文](./README.zh-CN.md) | [🇫🇷 Français](./README.fr.md) | [🇸🇦 العربية](./README.ar.md) | [🇮🇳 हिन्दी](./README.hi.md)

---

## 💊 La Receta (Características)

*   **Diagnóstico Remoto**: Escanea tu actividad en GitHub directamente vía API. No se requieren repositorios locales.
*   **Signos Vitales**: Hermosa salida de terminal a color con barras de progreso que giran más rápido que tu síndrome del impostor.
*   **Tratamiento Escalable**: Funciona tanto para proyectos personales como para organizaciones masivas.
*   **Viaje en el Tiempo**: Revisa tus estadísticas de `today` (hoy), `week` (semana), `month` (mes) o `year` (año).

## 📥 Ingesta (Instalación)

```bash
brew install gh
gh auth login
gh auth refresh -s read:org  # Requerido para organizaciones
```

Clona este repositorio masivo e instala con Poetry:

```bash
git clone https://github.com/forestsheep911/Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code.git
cd Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code
poetry install
```

## 📋 Dosis (Uso)

```bash
# Verifica que hiciste algo hoy
poetry run gh-stats --range today

# Demuéstrale a tu jefe que trabajaste este mes
poetry run gh-stats --range month --orgs TU_ORG
```

## 📄 Licencia

MIT. Haz lo que quieras, solo escribe código.

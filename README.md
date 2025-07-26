# Portal de Learning & Training Interno (PLTI-GD)

Este proyecto es un portal de aprendizaje y formación interno diseñado para capacitar a los empleados de una organización. Ofrece una experiencia de usuario intuitiva, moderna y escalable.

## Características

*   **Gestión de Cursos:** Creación y gestión de cursos estructurados en módulos y lecciones.
*   **Contenido Multimedia:** Soporte para lecciones en video y documentos descargables.
*   **Cuestionarios Interactivos:** Evaluaciones con temporizador y feedback instantáneo.
*   **Panel de Usuario:** Visualización del progreso, calificaciones y certificaciones.
*   **Catálogo de Cursos:** Navegación y búsqueda de cursos disponibles.
*   **Importación de Cursos:** Carga masiva de cursos desde un archivo Excel.
*   **Generación de Informes:** Reportes de desempeño y estadísticas de finalización.
*   **Diseño Responsive:** Interfaz adaptable a diferentes dispositivos.

## Manual del Sistema y Uso

### Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/mjmc4498/PLTI-GD.git
    cd PLTI-GD
    ```

2.  **Crear un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\\Scripts\\activate
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r learning_portal/backend/requirements.txt
    ```

4.  **Ejecutar la aplicación:**
    ```bash
    python learning_portal/backend/app.py
    ```

    La aplicación estará disponible en `http://127.0.0.1:5000`.

### Uso

*   **Importar Cursos:**
    1.  Vaya a `http://127.0.0.1:5000/upload_courses`.
    2.  Seleccione un archivo Excel con el formato adecuado.
    3.  Haga clic en "Upload".

*   **Navegar por los Cursos:**
    *   La página principal muestra el catálogo de cursos.
    *   Haga clic en un curso para ver sus detalles.

## Información Adicional

*   **Repositorio:** [https://github.com/mjmc4498/PLTI-GD](https://github.com/mjmc4498/PLTI-GD)
*   **Perfil de GitHub:** [https://github.com/mjmc4498](https://github.com/mjmc4498)
*   **GitHub Pages:** [https://mjmc4498.github.io/PLTI-GD](https://mjmc4498.github.io/PLTI-GD)

## Futuras Mejoras

*   Gamificación avanzada.
*   Integración con LinkedIn.
*   Motor de recomendaciones de cursos.

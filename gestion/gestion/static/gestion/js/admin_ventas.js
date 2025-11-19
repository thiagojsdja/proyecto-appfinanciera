document.addEventListener('DOMContentLoaded', function() {
    // 1. Obtener los campos del formulario
    const totalInput = document.getElementById('id_precio_total');
    const cuotasInput = document.getElementById('id_cantidad_cuotas');
    const montoInput = document.getElementById('id_monto_cuota');

    // 2. Función para formatear números (Visor de Guaraníes)
    function crearVisorDeMiles(inputId) {
        const input = document.getElementById(inputId);
        if (!input) return;

        // Crear el texto de ayuda visual
        const helpText = document.createElement('span');
        helpText.style.color = '#20c997'; // Color verde bonito
        helpText.style.marginLeft = '10px';
        helpText.style.fontWeight = 'bold';
        helpText.style.fontSize = '14px';
        
        // Insertarlo después del input
        input.parentNode.insertBefore(helpText, input.nextSibling);

        // Función que actualiza el texto
        function actualizarTexto() {
            const val = input.value.replace(/\./g, ''); // Quitar puntos si el usuario los puso
            const num = parseFloat(val);
            if (!isNaN(num)) {
                // Formato paraguayo: 8.000.000
                helpText.innerText = num.toLocaleString('es-PY') + ' Gs.';
            } else {
                helpText.innerText = '';
            }
        }

        // Escuchar cuando el usuario escribe
        input.addEventListener('keyup', actualizarTexto);
        input.addEventListener('change', actualizarTexto);
        
        // Ejecutar al inicio por si ya hay datos (modo edición)
        actualizarTexto();
    }

    // 3. Función para calcular la cuota automáticamente
    function calcularCuota() {
        if (totalInput && cuotasInput && montoInput) {
            const total = parseFloat(totalInput.value) || 0;
            const cuotas = parseInt(cuotasInput.value) || 0;

            // Solo calcular si ambos valores son válidos y positivos
            if (total > 0 && cuotas > 0) {
                // Dividir y redondear (sin decimales para guaraníes)
                const monto = Math.round(total / cuotas);
                montoInput.value = monto;
                
                // Disparar evento para que se actualice el visor del monto también
                montoInput.dispatchEvent(new Event('keyup'));
                montoInput.dispatchEvent(new Event('change'));
            }
        }
    }

    // 4. Activar las funciones
    if (totalInput) {
        crearVisorDeMiles('id_precio_total');
        totalInput.addEventListener('input', calcularCuota);
    }
    
    if (cuotasInput) {
        cuotasInput.addEventListener('input', calcularCuota);
    }
    
    if (montoInput) {
        crearVisorDeMiles('id_monto_cuota');
        // Permitimos editar manualmente también, no bloqueamos el campo
    }
});
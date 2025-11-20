document.addEventListener('DOMContentLoaded', function() {
    const $ = django.jQuery; // Usamos el jQuery interno de Django Admin
    const ventaSelect = $('#id_venta');
    const montoInput = document.getElementById('id_monto');

    // 1. FUNCIÓN: VISOR DE MILES (Para que se vea bonito)
    function crearVisorDeMiles(inputId) {
        const input = document.getElementById(inputId);
        if (!input) return;

        // Crear texto de ayuda
        const helpText = document.createElement('span');
        helpText.style.color = '#20c997';
        helpText.style.marginLeft = '10px';
        helpText.style.fontWeight = 'bold';
        helpText.style.fontSize = '14px';
        
        input.parentNode.insertBefore(helpText, input.nextSibling);

        function actualizarTexto() {
            const val = input.value.replace(/\./g, '');
            const num = parseFloat(val);
            if (!isNaN(num)) {
                helpText.innerText = num.toLocaleString('es-PY') + ' Gs.';
            } else {
                helpText.innerText = '';
            }
        }

        input.addEventListener('keyup', actualizarTexto);
        input.addEventListener('change', actualizarTexto);
        actualizarTexto(); // Ejecutar al inicio
        
        // Guardamos la referencia para llamarla desde fuera
        input.actualizarVisor = actualizarTexto;
    }

    // 2. FUNCIÓN: AUTOCOMPLETAR MONTO
    function autocompletarMonto() {
        const ventaId = ventaSelect.val();
        
        if (ventaId) {
            // Llamamos a nuestro "Puente" (API)
            $.ajax({
                url: '/api/venta/' + ventaId + '/',
                success: function(data) {
                    if (data.monto_cuota) {
                        // Rellenamos el campo (redondeado sin decimales)
                        montoInput.value = Math.round(data.monto_cuota);
                        
                        // Actualizamos el visor de miles visualmente
                        if (montoInput.actualizarVisor) {
                            montoInput.actualizarVisor();
                        }
                    }
                }
            });
        }
    }

    // 3. ACTIVAR TODO
    if (montoInput) {
        crearVisorDeMiles('id_monto');
    }

    if (ventaSelect.length > 0) {
        // Escuchar cambios en el selector de ventas
        ventaSelect.on('change', autocompletarMonto);
    }
});
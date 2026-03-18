/**
 * Gerenciamento do Dashboard de Reservas do Motel
 */

function abrirModal(quartoId) {
    const form = document.getElementById("formReserva");
    if (!form) return;

    // Define a URL de destino para a criação da reserva
    form.action = `/reservas/criar/${quartoId}/`;
    
    // Limpa o formulário e mensagens de status ao abrir
    form.reset();
    const statusDiv = document.getElementById('placa-status');
    if (statusDiv) {
        statusDiv.innerText = "";
        statusDiv.className = "small mt-1";
    }

    // Abre o modal do Bootstrap
    const modalElement = document.getElementById('modalReserva');
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}

// Aguarda o carregamento do DOM para configurar os eventos
document.addEventListener('DOMContentLoaded', function() {
    const placaInput = document.getElementById('id_placa');
    const statusDiv = document.getElementById('placa-status');
    const modeloInput = document.getElementById('id_modelo');
    const corInput = document.getElementById('id_cor');

    if (placaInput) {
        // Evento disparado quando o usuário termina de digitar a placa
        placaInput.addEventListener('blur', function() {
            const placa = this.value.trim();
            
            // Só busca se a placa tiver um tamanho mínimo (ex: ABC-1234 ou ABC1234)
            if (placa.length >= 7) {
                statusDiv.innerText = "🔍 Buscando veículo...";
                statusDiv.className = "small mt-1 text-muted";

                // Chamada AJAX para a nova rota de busca
                fetch(`/clientes/buscar-veiculo/?placa=${placa}`)
                    .then(response => {
                        if (!response.ok) throw new Error('Erro na busca');
                        return response.json();
                    })
                    .then(data => {
                        if (data.existe) {
                            // Preenche os campos automaticamente
                            if (modeloInput) modeloInput.value = data.modelo;
                            if (corInput) corInput.value = data.cor;
                            
                            statusDiv.innerText = `✅ Veículo de: ${data.nome_cliente}`;
                            statusDiv.className = "small mt-1 text-success";
                        } else {
                            statusDiv.innerText = "ℹ️ Novo veículo. Preencha os dados abaixo.";
                            statusDiv.className = "small mt-1 text-primary";
                        }
                    })
                    .catch(error => {
                        console.error('Erro:', error);
                        statusDiv.innerText = "❌ Erro ao consultar placa.";
                        statusDiv.className = "small mt-1 text-danger";
                    });
            }
        });

        // Opcional: Formata a placa para maiúsculas automaticamente
        placaInput.addEventListener('input', function() {
            this.value = this.value.toUpperCase();
        });
    }
});

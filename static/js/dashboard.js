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

// =============================================================
// ADICIONADO RECENTEMENTE — Validação de padrão de placa
// Verifica se a placa segue o padrão brasileiro (AAA9999)
// ou o padrão Mercosul (AAA9A99) e retorna o padrão detectado.
// =============================================================
function validarPlaca(placa) {  // ADICIONADO RECENTEMENTE
    // Remove hífen e espaços para normalizar (ex: "ABC-1234" → "ABC1234")
    const placaNormalizada = placa.replace(/[-\s]/g, '').toUpperCase();  // ADICIONADO RECENTEMENTE

    // Padrão Brasil antigo: 3 letras + 4 números (ex: ABC1234)
    const padraoAntigo = /^[A-Z]{3}[0-9]{4}$/;  // ADICIONADO RECENTEMENTE

    // Padrão Mercosul: 3 letras + 1 número + 1 letra + 2 números (ex: ABC1D23)
    const padraoMercosul = /^[A-Z]{3}[0-9][A-Z][0-9]{2}$/;  // ADICIONADO RECENTEMENTE

    if (padraoMercosul.test(placaNormalizada)) {  // ADICIONADO RECENTEMENTE
        return { valida: true, padrao: 'Mercosul', placa: placaNormalizada };  // ADICIONADO RECENTEMENTE
    }  // ADICIONADO RECENTEMENTE

    if (padraoAntigo.test(placaNormalizada)) {  // ADICIONADO RECENTEMENTE
        return { valida: true, padrao: 'Brasileiro', placa: placaNormalizada };  // ADICIONADO RECENTEMENTE
    }  // ADICIONADO RECENTEMENTE

    return { valida: false, padrao: null, placa: placaNormalizada };  // ADICIONADO RECENTEMENTE
}  // ADICIONADO RECENTEMENTE

// Aguarda o carregamento do DOM para configurar os eventos
document.addEventListener('DOMContentLoaded', function() {
    const placaInput = document.getElementById('id_placa');
    const statusDiv = document.getElementById('placa-status');
    const modeloInput = document.getElementById('id_modelo');
    const corInput = document.getElementById('id_cor');
    const submitBtn = document.querySelector('#formReserva button[type="submit"]');  // ADICIONADO RECENTEMENTE

    if (placaInput) {

        // ADICIONADO RECENTEMENTE — Validação em tempo real enquanto o usuário digita
        placaInput.addEventListener('input', function() {
            this.value = this.value.toUpperCase();  // Mantém maiúsculas (já existia)

            const resultado = validarPlaca(this.value);  // ADICIONADO RECENTEMENTE

            // Só exibe feedback quando a placa tem tamanho suficiente (7 chars sem hífen)
            const semHifen = this.value.replace(/[-\s]/g, '');  // ADICIONADO RECENTEMENTE
            if (semHifen.length < 7) {  // ADICIONADO RECENTEMENTE
                statusDiv.innerText = '';  // ADICIONADO RECENTEMENTE
                if (submitBtn) submitBtn.disabled = false;  // ADICIONADO RECENTEMENTE
                return;  // ADICIONADO RECENTEMENTE
            }  // ADICIONADO RECENTEMENTE

            if (resultado.valida) {  // ADICIONADO RECENTEMENTE
                // Exibe o padrão detectado (Mercosul ou Brasileiro)
                statusDiv.innerText = `✅ Placa válida — Padrão ${resultado.padrao}`;  // ADICIONADO RECENTEMENTE
                statusDiv.className = 'small mt-1 text-success';  // ADICIONADO RECENTEMENTE
                if (submitBtn) submitBtn.disabled = false;  // ADICIONADO RECENTEMENTE — libera o botão
            } else {  // ADICIONADO RECENTEMENTE
                statusDiv.innerText = '❌ Placa inválida — use o padrão Brasileiro (ABC1234) ou Mercosul (ABC1D23)';  // ADICIONADO RECENTEMENTE
                statusDiv.className = 'small mt-1 text-danger';  // ADICIONADO RECENTEMENTE
                if (submitBtn) submitBtn.disabled = true;  // ADICIONADO RECENTEMENTE — bloqueia envio
            }  // ADICIONADO RECENTEMENTE
        });  // ADICIONADO RECENTEMENTE

        // Evento disparado quando o usuário termina de digitar a placa (blur = saiu do campo)
        placaInput.addEventListener('blur', function() {
            const placa = this.value.trim();
            
            // ADICIONADO RECENTEMENTE — valida o formato antes de buscar no servidor
            const resultado = validarPlaca(placa);  // ADICIONADO RECENTEMENTE
            if (!resultado.valida) return;  // ADICIONADO RECENTEMENTE — aborta se inválida

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
                            
                            // ADICIONADO RECENTEMENTE — mantém info do padrão junto com o cliente
                            statusDiv.innerText = `✅ Veículo de: ${data.nome_cliente} — Padrão ${resultado.padrao}`;  // ADICIONADO RECENTEMENTE
                            statusDiv.className = "small mt-1 text-success";
                        } else {
                            // ADICIONADO RECENTEMENTE — exibe padrão mesmo quando veículo é novo
                            statusDiv.innerText = `ℹ️ Novo veículo. Preencha os dados abaixo. (Padrão ${resultado.padrao})`;  // ADICIONADO RECENTEMENTE
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
    }

    // ADICIONADO RECENTEMENTE — Impede envio do formulário se a placa for inválida (segurança extra)
    const formReserva = document.getElementById('formReserva');  // ADICIONADO RECENTEMENTE
    if (formReserva) {  // ADICIONADO RECENTEMENTE
        formReserva.addEventListener('submit', function(e) {  // ADICIONADO RECENTEMENTE
            const placa = document.getElementById('id_placa').value;  // ADICIONADO RECENTEMENTE
            const resultado = validarPlaca(placa);  // ADICIONADO RECENTEMENTE
            if (!resultado.valida) {  // ADICIONADO RECENTEMENTE
                e.preventDefault();  // ADICIONADO RECENTEMENTE — bloqueia o envio
                statusDiv.innerText = '❌ Corrija a placa antes de confirmar a entrada.';  // ADICIONADO RECENTEMENTE
                statusDiv.className = 'small mt-1 text-danger';  // ADICIONADO RECENTEMENTE
            }  // ADICIONADO RECENTEMENTE
        });  // ADICIONADO RECENTEMENTE
    }  // ADICIONADO RECENTEMENTE
});

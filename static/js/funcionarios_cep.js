document.addEventListener('DOMContentLoaded', function () {
    var cepInput = document.getElementById('id_cep');
    var enderecoInput = document.getElementById('id_endereco');
    var status = document.getElementById('cep-status');

    if (!cepInput || !enderecoInput) {
        return;
    }

    cepInput.addEventListener('input', function () {
        var valor = this.value.replace(/\D/g, '');

        if (valor.length > 8) {
            valor = valor.substring(0, 8);
        }

        if (valor.length > 5) {
            valor = valor.substring(0, 5) + '-' + valor.substring(5);
        }

        this.value = valor;
    });

    cepInput.addEventListener('blur', function () {
        var cep = this.value.replace(/\D/g, '');

        if (cep.length !== 8) {
            if (status) {
                status.innerText = 'Informe um CEP valido com 8 digitos.';
                status.className = 'small text-danger mt-1';
            }
            return;
        }

        if (status) {
            status.innerText = 'Buscando endereco...';
            status.className = 'small text-muted mt-1';
        }

        fetch('/funcinarios/buscar-cep/?cep=' + cep)
            .then(function (response) {
                return response.json().then(function (data) {
                    return {
                        ok: response.ok,
                        data: data
                    };
                });
            })
            .then(function (result) {
                if (!result.ok || !result.data.ok) {
                    var mensagem = 'Nao foi possivel consultar o CEP agora.';
                    if (result.data && result.data.mensagem) {
                        mensagem = result.data.mensagem;
                    }
                    if (status) {
                        status.innerText = mensagem;
                        status.className = 'small text-danger mt-1';
                    }
                    return;
                }

                enderecoInput.value = result.data.endereco || '';

                if (status) {
                    status.innerText = '';
                    status.className = '';
                }
            })
            .catch(function () {
                if (status) {
                    status.innerText = 'Nao foi possivel consultar o CEP agora.';
                    status.className = 'small text-danger mt-1';
                }
            });
    });
});

document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // MENU HAMBURGUER
    // =========================

    const sidebar = document.getElementById("sidebar");
    const toggle = document.getElementById("sidebarCollapse");
    
    // Verifica preferência salva
    const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    
    // Aplica estado inicial
    if(isCollapsed){
        sidebar.classList.add("collapsed");
    }

    if(toggle){
        toggle.addEventListener("click", function(){
            sidebar.classList.toggle("collapsed");
            // Salva preferência
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
            
            // Atualiza tooltips
            setTimeout(atualizarTooltips, 300); // Pequeno delay para animação
        });
    }

    // Função para atualizar tooltips
    function atualizarTooltips(){
        if(sidebar.classList.contains('collapsed')){
            document.querySelectorAll('#sidebar ul li a').forEach(link => {
                const span = link.querySelector('span');
                if(span && span.textContent.trim() && !link.getAttribute('title')){
                    link.setAttribute('title', span.textContent.trim());
                }
            });
        } else {
            document.querySelectorAll('#sidebar ul li a').forEach(link => {
                link.removeAttribute('title');
            });
        }
    }
    
    // Executa na carga inicial
    setTimeout(atualizarTooltips, 100);
    
    // =========================
    // MASCARAS IMASK
    // =========================

    function aplicarMascara(id, mask){
        const el = document.getElementById(id);
        if(el && typeof IMask !== 'undefined'){
            IMask(el,{mask:mask});
        }
    }

    aplicarMascara("cpf","000.000.000-00");
    aplicarMascara("telefone","(00) 00000-0000");
    aplicarMascara("cnpj","00.000.000/0000-00");

});
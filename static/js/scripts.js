document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // MENU HAMBURGUER
    // =========================

    const sidebar = document.getElementById("sidebar");
    const toggle = document.getElementById("sidebarCollapse");

    if(toggle){
        toggle.addEventListener("click", function(){
            sidebar.classList.toggle("active");
        });
    }


    // =========================
    // MASCARAS IMASK
    // =========================

    function aplicarMascara(id, mask){
        const el = document.getElementById(id);
        if(el){
            IMask(el,{mask:mask});
        }
    }

    aplicarMascara("cpf","000.000.000-00");
    aplicarMascara("telefone","(00) 00000-0000");
    aplicarMascara("cnpj","00.000.000/0000-00");

});

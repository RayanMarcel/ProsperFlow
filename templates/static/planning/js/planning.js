function update_valor_planejamento_categoria(token){
    valor = document.getElementById('valor-categoria-'+token).value

    fetch("/planning/update_value_category/"+token, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({novo_valor: valor})
    }).then(function(result){
        return result.json()
    }).then(function(data){
        if (data.status === 'Sucesso') { 
            Swal.fire({
                icon: 'success',
                title: 'Sucesso',
                text: 'Valor atualizado com sucesso!'
            }).then(function() {
                location.reload();  // Recarregue a página
            })
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Erro',
                text: 'Ocorreu um erro ao atualizar o valor.'
            })
        }
    })
}

document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.getElementById('login_btn');
    const cadastroBtn = document.getElementById('cadastro_btn');
    const adicionarBtn = document.getElementById('adicionar_carro_btn');
    const deletarBtn = document.getElementById('deletar_carro_btn');
    const lista = document.getElementById('lista');
    const pedidosContainer = document.getElementById('lista_pedidos');
    const pedidoBtn = document.getElementById('fazer_pedido_btn');
    const cancelarPedidoBtn = document.getElementById('cancelar_pedido_btn');
    const concluirPedidoBtn = document.getElementById('atualizar_pedido_btn');
    if (loginBtn) {
        loginBtn.addEventListener('click', async () => {
            const nome = document.getElementById('login_nome').value;
            const senha = document.getElementById('login_senha').value;
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nome, senha })
                });
                const data = await response.json();
                if (!data.success) { alert(data.message); return; }
                document.getElementById('login_nome').value = '';
                document.getElementById('login_senha').value = '';
                window.location.href = '/catalogo';
            } catch (err) { alert('Erro ao conectar: ' + err); }
        });
    }

    if (cadastroBtn && document.getElementById('cad_nome') && document.getElementById('cad_senha')) {
        cadastroBtn.addEventListener('click', async () => {
            const nome = document.getElementById('cad_nome').value;
            const senha = document.getElementById('cad_senha').value;
            if (!nome || !senha) { alert('Preencha todos os campos!'); return; }
            try {
                const response = await fetch('/cadastro', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nome, senha })
                });
                const data = await response.json();
                alert(data.message);
                if (data.success) { document.getElementById('cad_nome').value = ''; document.getElementById('cad_senha').value = ''; }
            } catch (err) { alert('Erro ao conectar: ' + err); }
        });
    }

    // Se estivermos na página do catálogo, buscar nomes dos carros
    if (lista) {
        fetch('/dados', { cache: 'no-store' })
            .then(r => r.json())
            .then(data => {
                data.forEach(item => {
                    const li = document.createElement('li');
                    const nomeCarro = item['nome do carro'] ;
                    li.textContent = nomeCarro;
                    lista.appendChild(li);
                });
            })
            .catch(err => console.error('Erro ao carregar dados do Mongo:', err));
    }
    if (adicionarBtn){
        adicionarBtn.addEventListener('click', async () => {
            const nome_carro = document.getElementById('input_adicionar').value.trim();
            if (!nome_carro) { alert('Digite o nome do carro!'); return; }
            try {
                const response = await fetch('/adicionar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ "nome do carro": nome_carro })
                });
                const data = await response.json();
                alert(data.message);
                if (data.success) {
                    document.getElementById('input_adicionar').value = '';
                    location.reload();
                }
            } catch(err) { alert('Erro ao conectar: ' + err); }
        });
    }
    if (deletarBtn){
        deletarBtn.addEventListener('click', async () => {
            const nome_carro = document.getElementById('input_deletar').value.trim();
            if (!nome_carro) { alert('Digite o nome do carro a deletar!'); return; }
            try {
                const response = await fetch('/deletar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ "nome do carro": nome_carro })
                });
                const data = await response.json();
                alert(data.message);
                if (data.success) {
                    document.getElementById('input_deletar').value = '';
                    location.reload();
                }
            } catch(err) { alert('Erro ao conectar: ' + err); }
        });
    }
    if (pedidosContainer){
        fetch('/pedidos', { cache: 'no-store' })
            .then(r => r.json())
            .then(data => {
                data.forEach(pedido => {
                    const li = document.createElement('li');
                    li.textContent = `${pedido.id} | Carro: ${pedido.carro} | Quantidade: ${pedido.quantidade} | Local: ${pedido.cidade} |||| Status: ${pedido.status} \n`;
                    pedidosContainer.appendChild(li);
                });
            })
            .catch(err => console.error('Erro ao carregar pedidos do Redis:', err));
    }
    if (pedidoBtn){
        pedidoBtn.addEventListener('click', async () => {
            const carro = document.getElementById('input_pedido_carro').value.trim();
            const quantidade = document.getElementById('input_pedido_quantidade').value.trim();
            const cidade = document.getElementById('input_pedido_cidade').value.trim();
            if (!carro || !quantidade || !cidade) { alert('Preencha todos os campos!'); return; }
            try {
                const response = await fetch('/fazer_pedido', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ carro, quantidade, cidade })
                });
                const data = await response.json();
                alert(data.message);
                if (data.success) {
                    document.getElementById('input_pedido_carro').value = '';
                    document.getElementById('input_pedido_quantidade').value = '';
                    document.getElementById('input_pedido_cidade').value = '';
                }
            } catch (err) { alert('Erro ao conectar: ' + err); }
        });
    }
    if (cancelarPedidoBtn){
        cancelarPedidoBtn.addEventListener('click', async () => {
            const pedidoId = document.getElementById('input_cancelar_carro').value.trim();
            if (!pedidoId) { alert('Digite o número do pedido!'); return; }
            try {
                const response = await fetch('/cancelar_pedido', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ pedido: pedidoId })
                });
                const data = await response.json();
                alert(data.message);
                if (data.success) {
                    document.getElementById('input_cancelar_carro').value = '';
                }
            } catch (err) { alert('Erro ao conectar: ' + err); }
        });
    }
    if (concluirPedidoBtn){
        concluirPedidoBtn.addEventListener('click', async () => {
            const pedidoId = document.getElementById('input_atualizar_pedido_id').value.trim();
             if (!pedidoId) { alert('Digite o número do pedido!'); return; }
            try {
                const response = await fetch('/atualizar_pedido', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ pedido: pedidoId })
                });
                const data = await response.json();
                alert(data.message);
                if (data.success) {
                    document.getElementById('input_atualizar_pedido_id').value = '';
                }
            } catch (err) { alert('Erro ao conectar: ' + err); }
        });
    }
});

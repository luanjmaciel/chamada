document.addEventListener('DOMContentLoaded', () => {
    const tabelaBody = document.querySelector('#tabela-participantes tbody');
    const statusMensagem = document.getElementById('mensagem-status');

    // Função para formatar a data e hora
    const formatarData = (dataString) => {
        if (!dataString) return 'N/A';
        const data = new Date(dataString);
        return data.toLocaleString('pt-BR');
    };

    const carregarDados = async () => {
        tabelaBody.innerHTML = '';
        statusMensagem.textContent = 'Carregando dados...';
        statusMensagem.style.color = '#007bff';

        try {
           const response = await fetch('http://127.0.0.1:5000/participantes');
            
            if (!response.ok) {
                throw new Error(`Erro na rede: ${response.status} ${response.statusText}`);
            }

            const dados = await response.json();
            
            if (Object.keys(dados).length === 0) {
                statusMensagem.textContent = 'Nenhum participante encontrado.';
                statusMensagem.style.color = '#333';
            } else {
                statusMensagem.textContent = ''; // Limpa a mensagem
                
                // Itera sobre os dados e cria as linhas da tabela
                for (const [nome, info] of Object.entries(dados)) {
                    const linha = tabelaBody.insertRow();
                    
                    const celulaNome = linha.insertCell(0);
                    const celulaParticipacoes = linha.insertCell(1);
                    const celulaPrimeira = linha.insertCell(2);
                    const celulaUltima = linha.insertCell(3);

                    celulaNome.textContent = nome;
                    celulaParticipacoes.textContent = info.participacoes;
                    celulaPrimeira.textContent = formatarData(info.primeira_participacao);
                    celulaUltima.textContent = formatarData(info.ultima_participacao);
                }
            }
        } catch (error) {
            console.error('Falha ao buscar dados:', error);
            statusMensagem.textContent = 'Erro ao carregar os dados. Verifique se a API está funcionando.';
            statusMensagem.style.color = '#dc3545';
        }
    };

    // Chama a função para carregar os dados quando a página for carregada
    carregarDados();
});
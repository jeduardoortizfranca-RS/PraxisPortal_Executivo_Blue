(function () {
  // ✅ API_BASE consistente
  const API_BASE = 
    window.API_URL || "https://praxis-portal-executivo-blue-8t5ow1ce5.vercel.app";
  window.__API_BASE__ = API_BASE;

  function getToken() {
    return localStorage.getItem("jwt") || "";
  }

  function logout() {
    localStorage.removeItem("jwt");
    window.location.href = "/frontend/index.html";
  }

  // ✅ Função utilitária para fetch com token
  async function apiFetch(url, options = {}) {
    const token = getToken();
    const config = {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
        ...options.headers
      },
      ...options
    };

    try {
      const response = await fetch(url, config);
      return response;
    } catch (error) {
      console.error("Erro de rede:", error);
      throw error;
    }
  }

  // ✅ Resumo Financeiro
  async function fetchResumo() {
    const div = document.getElementById("resumo");
    if (!div) return;

    try {
      div.textContent = "Carregando resumo...";
      const response = await apiFetch(`${API_BASE}/financeiro/resumo`);
      
      if (!response.ok) {
        const errorData = await response.json();
        div.textContent = `Erro: ${errorData.detail || "Falha ao carregar resumo"}`;
        return;
      }

      const data = await response.json();
      div.innerHTML = `
        <p><strong>Total:</strong> R$ ${data.total?.toFixed(2) || "0.00"}</p>
        <p><strong>Quantidade:</strong> ${data.qtd || 0}</p>
      `;
    } catch (error) {
      console.error("Erro no resumo:", error);
      div.textContent = "Erro de conexão";
    }
  }

  // ✅ Lista de Transações
  async function fetchTransacoes() {
    const tbody = document.getElementById("listaTransacoes");
    if (!tbody) return;

    tbody.innerHTML = "<tr><td colspan='4'>Carregando...</td></tr>";

    try {
      const response = await apiFetch(`${API_BASE}/financeiro/transacoes`);
      
      if (!response.ok) {
        const errorData = await response.json();
        tbody.innerHTML = `<tr><td colspan='4'>Erro: ${errorData.detail || "Falha ao carregar"}</td></tr>`;
        return;
      }

      const data = await response.json();
      tbody.innerHTML = "";

      if (data.length === 0) {
        tbody.innerHTML = "<tr><td colspan='4'>Nenhuma transação encontrada</td></tr>";
        return;
      }

      data.forEach(transaction => {
        const row = createTransactionRow(transaction);
        tbody.appendChild(row);
      });

    } catch (error) {
     .error("Erro nas transações:", error);
      tbody.innerHTML = "<tr><td colspan='4'>Erro de conexão</td></tr>";
    }
  }

  // ✅ Criar linha da tabela
  function createTransactionRow(transaction) {
    const row = document.createElement("tr");
    const date = new Date(transaction.created_at || Date.now()).toLocaleDateString('pt-BR');
    const value = Number(transaction.valor || 0).toFixed(2);
    const category = transaction.categoria || "Sem categoria";
    const typeClass = Number(transaction.valor || 0) >= 0 ? "positivo" : "negativo";

    row.innerHTML = `
      <td>${date}</td>
      <td class="valor ${typeClass}">R$ ${value}</td>
      <td>${category}</td>
      <td><button class="delete-btn" data-id="${transaction.id}">Excluir</button></td>
    `;

    row.querySelector(".delete-btn").addEventListener("click", () => {
      deleteTransaction(transaction.id);
    });

    return row;
  }

  // ✅ Excluir Transação
  async function deleteTransaction(id) {
    if (!confirm("Tem certeza que deseja excluir esta transação?")) {
      return;
    }

    try {
      const response = await apiFetch(`${API_BASE}/financeiro/remover/${id}`, {
        method: "DELETE"
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert(`Erro ao excluir: ${errorData.detail || "Falha na exclusão"}`);
        return;
      }

      // Atualizar lista e resumo
      await fetchTransacoes();
      await fetchResumo();
      showMessage("Transação excluída com sucesso!", "green");

    } catch (error) {
      console.error("Erro na exclusão:", error);
      alert("Erro de conexão ao excluir transação");
    }
  }

  // ✅ Nova Transação
  async function handleNewTransaction(event) {
    event.preventDefault();
    
    const descricao = document.getElementById("descricao").value.trim();
    const valor = parseFloat(document.getElementById("valor").value);
    const categoria = document.getElementById("categoria").value;

    if (!descricao || isNaN(valor)) {
      showMessage("Preencha descrição e valor válidos", "red");
      return;
    }

    try {
      const response = await apiFetch(`${API_BASE}/financeiro/nova`, {
        method: "POST",
        body: JSON.stringify({
          descricao: descricao,
          valor: valor,
          categoria: categoria || "Outros"
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        showMessage(`Erro: ${errorData.detail || "Falha ao adicionar"}`, "red");
        return;
      }

      // Limpar formulário
      document.getElementById("formNova").reset();
      showMessage("Transação adicionada com sucesso!", "green");

      // Atualizar dados
      await fetchResumo();
      await fetchTransacoes();

    } catch (error) {
      console.error("Erro ao adicionar transação:", error);
      showMessage("Erro de conexão", "red");
    }
  }

  // ✅ Mostrar mensagem global
  function showMessage(msg, color = "blue") {
    const msgDiv = document.getElementById("msgNova") || document.createElement("div");
    msgDiv.textContent = msg;
    msgDiv.style.color = color;
    msgDiv.style.margin = "10px 0";
    msgDiv.style.padding = "10px";
    msgDiv.style.borderRadius = "4px";
    
    if (!document.getElementById("msgNova")) {
      msgDiv.id = "msgNova";
      document.body.insertBefore(msgDiv, document.body.firstChild);
    }
  }

  // ✅ Configurar eventos
  document.addEventListener("DOMContentLoaded", function() {
    // Formulário de nova transação
    const formNova = document.getElementById("formNova");
    if (formNova) {
      formNova.addEventListener("submit", handleNewTransaction);
    }

    // Botão logout
    document.getElementById("btn-logout")?.addEventListener("click", logout);

    // Verificar token e carregar dados
    if (window.location.pathname.includes("financeiro.html")) {
      verifyToken().then(() => {
        fetchResumo();
        fetchTransacoes();
      });
    }
  });

  // ✅ Função verifyToken (para proteger a rota)
  async function verifyToken() {
    const token = getToken();
    if (!token) {
      redirectToLogin();
      return false;
    }

    try {
      const response = await apiFetch(`${API_BASE}/auth/verify`);
      if (!response.ok) {
        redirectToLogin();
        return false;
      }
      return true;
    } catch (error) {
      console.error("Token verification failed:", error);
      redirectToLogin();
      return false;
    }
  }

})();
